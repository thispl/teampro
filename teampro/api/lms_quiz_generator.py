# -*- coding: utf-8 -*-
"""
Rule-based LMS quiz generator for the teampro app.

Generates an ``LMS Quiz`` (with ``LMS Question`` records) for a
``Course Lesson`` purely from local content — the lesson body, EditorJS
``content`` blocks, headings, and the YouTube video reference — without
calling any paid LLM API.

Generated questions are drafts meant for instructor review. Three kinds
are produced:

* Cloze MCQs   — a sentence from the lesson with a key term blanked out
* True/False   — verbatim statements (True) or statements with a swapped
                 key term (False)
* User Input   — short-answer recall of a blanked key term

Whitelisted endpoints
---------------------
* ``generate_quiz_for_lesson``   — one lesson
* ``generate_quizzes_for_course``— every lesson in a course outline

Permission is restricted to Moderator / Course Creator / System Manager.
"""

import json
import random
import re
from collections import Counter

import frappe
from frappe import _
from frappe.utils import cint, escape_html, strip_html_tags


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ALLOWED_ROLES = ["Moderator", "Course Creator", "System Manager"]

MIN_SENTENCE_LEN = 40
MAX_SENTENCE_LEN = 300
MAX_TERMS = 15

STOPWORDS = set(
	"""
	a an the and or but if then else when while for to of in on at by with
	from as is are was were be been being it its this that these those there
	here you your we our they their he she his her i me my us them can could
	will would shall should may might must do does did done have has had not
	no yes so such than too very just also into over under again once each
	all any both few more most other some only own same out up down about
	what which who whom how why where after before between during without
	within through above below off further get got make made use used using
	like see let lets let's go going take takes new one two three way ways
	thing things say says said know knows known want wants need needs vs via
	""".split()
)

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|[\r\n]+|(?:^|\s)[•\-\*]\s+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'-]*")
CAPITALIZED_PHRASE_RE = re.compile(
	r"\b(?:[A-Z][\w'-]*(?:\s+[A-Z][\w'-]*)+|[A-Z][\w'-]*[A-Z0-9][\w'-]*|[A-Z]{2,}\d*)\b"
)


# ---------------------------------------------------------------------------
# Public whitelisted API
# ---------------------------------------------------------------------------

@frappe.whitelist()
def generate_quiz_for_lesson(lesson, num_questions=5, marks=1, passing_percentage=70, dry_run=0):
	"""Generate a quiz for a single Course Lesson.

	:param lesson: Course Lesson name
	:param num_questions: target number of questions (best effort)
	:param marks: marks per question
	:param passing_percentage: quiz passing percentage
	:param dry_run: if truthy, return the generated questions without saving
	"""
	_check_permission()
	lesson_doc = frappe.get_doc("Course Lesson", lesson)

	questions = build_questions(lesson_doc, cint(num_questions))
	if not questions:
		frappe.throw(
			_("Not enough lesson content to generate questions for {0}.").format(lesson_doc.title)
		)

	if cint(dry_run):
		return {
			"lesson": lesson_doc.name,
			"title": lesson_doc.title,
			"dry_run": True,
			"questions": [_question_preview(q) for q in questions],
		}

	quiz_name = _create_quiz(lesson_doc, questions, cint(marks), cint(passing_percentage))
	_attach_quiz_to_lesson(lesson_doc, quiz_name)
	frappe.db.commit()

	return {
		"lesson": lesson_doc.name,
		"quiz": quiz_name,
		"question_count": len(questions),
		"questions": [_question_preview(q) for q in questions],
	}


@frappe.whitelist()
def generate_quizzes_for_course(
	course, num_questions=5, marks=1, passing_percentage=70, skip_existing=1
):
	"""Generate a quiz for every lesson in a course's outline.

	Lessons that already contain a quiz block (or have ``quiz_id`` set) are
	skipped when ``skip_existing`` is truthy.
	"""
	_check_permission()

	if not frappe.db.exists("LMS Course", course):
		frappe.throw(_("Course {0} not found.").format(course))

	from lms.lms.utils import get_lessons

	lessons = get_lessons(course)
	summary = {"course": course, "generated": [], "skipped": [], "failed": []}

	for row in lessons:
		lesson_name = row.name if hasattr(row, "name") else row.get("name")
		try:
			lesson_doc = frappe.get_doc("Course Lesson", lesson_name)
			if cint(skip_existing) and _lesson_has_quiz(lesson_doc):
				summary["skipped"].append(lesson_name)
				continue

			questions = build_questions(lesson_doc, cint(num_questions))
			if not questions:
				summary["failed"].append({"lesson": lesson_name, "reason": "insufficient content"})
				continue

			quiz_name = _create_quiz(lesson_doc, questions, cint(marks), cint(passing_percentage))
			_attach_quiz_to_lesson(lesson_doc, quiz_name)
			frappe.db.commit()
			summary["generated"].append({"lesson": lesson_name, "quiz": quiz_name})
		except Exception as exc:
			frappe.db.rollback()
			frappe.log_error(
				title="LMS quiz generation failed: {0}".format(lesson_name),
				message=frappe.get_traceback(),
			)
			summary["failed"].append({"lesson": lesson_name, "reason": str(exc)})

	return summary


# ---------------------------------------------------------------------------
# Question generation
# ---------------------------------------------------------------------------

def build_questions(lesson_doc, num_questions):
	"""Return a list of question spec dicts for a lesson doc (unsaved)."""
	sentences, headings = _extract_material(lesson_doc)
	terms = _extract_terms(sentences, headings, lesson_doc.title)
	if not sentences or not terms:
		return []

	cloze, cloze_false, recall = _sentence_pools(sentences, terms)

	candidates = []
	for sentence, term in cloze:
		candidates.append(_make_cloze_question(sentence, term, terms))
	for sentence, term, replacement in cloze_false:
		candidates.append(_make_true_false_question(sentence, term, replacement))
	for sentence, term in recall:
		candidates.append(_make_recall_question(sentence, term))

	if lesson_doc.youtube:
		video_q = _make_video_question(lesson_doc, terms, headings)
		if video_q:
			candidates.insert(0, video_q)

	random.shuffle(candidates)

	questions, seen = [], set()
	for spec in candidates:
		key = spec["question"].strip().lower()
		if key in seen:
			continue
		seen.add(key)
		questions.append(spec)
		if len(questions) >= num_questions:
			break
	return questions


def _extract_material(lesson_doc):
	"""Pull (sentences, headings) out of lesson content + body markdown."""
	sentences, headings = [], []

	if lesson_doc.content:
		try:
			blocks = json.loads(lesson_doc.content).get("blocks") or []
		except (ValueError, TypeError):
			blocks = []
		for block in blocks:
			btype, data = block.get("type"), block.get("data") or {}
			if btype == "header":
				headings.append(_clean(data.get("text")))
			elif btype == "list":
				for item in data.get("items") or []:
					text = item.get("content") if isinstance(item, dict) else item
					sentences.extend(_split_sentences(text))
			elif btype == "table":
				for row in data.get("content") or []:
					for cell in row:
						sentences.extend(_split_sentences(cell))
			elif btype in ("paragraph", "quote", "code", "warning", "callout"):
				sentences.extend(_split_sentences(data.get("text") or data.get("message")))

	if lesson_doc.body:
		for line in lesson_doc.body.splitlines():
			line = line.strip()
			if not line or "{{" in line or line.startswith("!["):
				continue
			if line.startswith("#"):
				headings.append(_clean(line.lstrip("#")))
			else:
				line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
				sentences.extend(_split_sentences(line))

	sentences = [s for s in dict.fromkeys(sentences) if MIN_SENTENCE_LEN <= len(s) <= MAX_SENTENCE_LEN]
	headings = [h for h in dict.fromkeys(headings) if h and len(h.split()) <= 8]
	return sentences, headings


def _split_sentences(text):
	if not text:
		return []
	return [_clean(s) for s in SENTENCE_SPLIT_RE.split(str(text)) if s]


def _clean(text):
	if not text:
		return ""
	text = strip_html_tags(str(text))
	text = re.sub(r"\s+", " ", text)
	return text.strip(" -*•\t")


def _extract_terms(sentences, headings, title):
	"""Score key terms: headings > capitalized phrases > frequent words."""
	freq = Counter()
	for s in sentences:
		for w in WORD_RE.findall(s):
			lw = w.lower()
			if len(lw) > 3 and lw not in STOPWORDS:
				freq[lw] += 1

	cap_phrases = Counter()
	for s in sentences:
		for m in CAPITALIZED_PHRASE_RE.finditer(s):
			phrase = re.sub(r"^(?:The|A|An)\s+", "", m.group(0))
			if phrase.lower() not in STOPWORDS and len(phrase) > 1:
				cap_phrases[phrase] += 1

	terms, seen = [], set()

	def _add(term):
		key = term.lower()
		if key and key not in seen and key not in STOPWORDS:
			seen.add(key)
			terms.append(term)

	for h in headings:
		_add(h)
	for phrase, _ in cap_phrases.most_common(10):
		_add(phrase)
	for word, _count in freq.most_common(10):
		_add(word)
	if title:
		_add(title)

	return terms[:MAX_TERMS]


def _find_term_in_sentence(sentence, term):
	pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
	return pattern.search(sentence)


def _blank_out(sentence, term):
	match = _find_term_in_sentence(sentence, term)
	if not match:
		return None
	return sentence[: match.start()] + "_____" + sentence[match.end() :]


def _sentence_pools(sentences, terms):
	"""Group sentences by role: cloze MCQ, True/False, recall."""
	cloze, cloze_false, recall = [], [], []
	used = set()
	for i, sentence in enumerate(sentences):
		for term in terms:
			if not _find_term_in_sentence(sentence, term):
				continue
			replacement = (_pick_distractor(term, terms) or [None])[0]
			if i % 3 == 2:
				recall.append((sentence, term))
			elif i % 3 == 1 and replacement:
				cloze_false.append((sentence, term, replacement))
			else:
				cloze.append((sentence, term))
			used.add(i)
			break
	# Unmatched long sentences still make valid True statements.
	for i, sentence in enumerate(sentences):
		if i not in used:
			cloze_false.append((sentence, None, None))
	return cloze, cloze_false, recall


def _pick_distractor(term, terms, count=1, exclude=None):
	"""Pick distractors that look like the answer so the MCQ stays plausible."""
	is_proper = term[:1].isupper() or " " in term
	same_form = [
		t
		for t in terms
		if t.lower() != term.lower() and t != (exclude or "") and (t[:1].isupper() or " " in t) == is_proper
	]
	other = [
		t
		for t in terms
		if t.lower() != term.lower() and t != (exclude or "") and t not in same_form
	]
	random.shuffle(same_form)
	random.shuffle(other)
	return (same_form + other)[:count]


# ---------------------------------------------------------------------------
# Question builders — each returns a spec dict or None
# ---------------------------------------------------------------------------

def _make_cloze_question(sentence, term, terms):
	blanked = _blank_out(sentence, term)
	distractors = _pick_distractor(term, terms, count=3)
	if not blanked or len(distractors) < 1:
		return None
	options = distractors + [term]
	random.shuffle(options)
	return {
		"type": "Choices",
		"question": "Complete the following: {0}".format(escape_html(blanked)),
		"options": [escape_html(o) for o in options],
		"correct": options.index(term),
		"explanation": escape_html(sentence),
	}


def _make_true_false_question(sentence, term, replacement):
	if term and replacement:
		statement = _find_term_in_sentence(sentence, term)
		statement = sentence[: statement.start()] + replacement + sentence[statement.end() :]
		correct_idx = 1
	else:
		statement = sentence
		correct_idx = 0
	return {
		"type": "Choices",
		"question": "True or False: {0}".format(escape_html(statement)),
		"options": ["True", "False"],
		"correct": correct_idx,
		"explanation": escape_html(sentence),
	}


def _make_recall_question(sentence, term):
	blanked = _blank_out(sentence, term)
	if not blanked:
		return None
	possibilities = list(dict.fromkeys([term, term.lower(), term.upper()]))
	return {
		"type": "User Input",
		"question": "Fill in the blank: {0}".format(escape_html(blanked)),
		"possibilities": [escape_html(p) for p in possibilities],
		"explanation": escape_html(sentence),
	}


def _make_video_question(lesson_doc, terms, headings):
	"""Build one MCQ anchored on the lesson's YouTube reference."""
	correct = lesson_doc.title
	distractors = _pick_distractor(correct, terms, count=3)
	if len(distractors) < 1:
		return None
	options = distractors + [correct]
	random.shuffle(options)
	return {
		"type": "Choices",
		"question": "This lesson's video ({0}) primarily covers which topic?".format(
			escape_html(lesson_doc.youtube)
		),
		"options": [escape_html(o) for o in options],
		"correct": options.index(correct),
		"explanation": "Refer to the video embedded in this lesson.",
	}


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _create_quiz(lesson_doc, questions, marks, passing_percentage):
	rows = []
	for spec in questions:
		if spec is None:
			continue
		rows.append({"question": _create_question(spec).name, "marks": marks})
	if not rows:
		frappe.throw(_("No valid questions were generated."))

	quiz = frappe.get_doc(
		{
			"doctype": "LMS Quiz",
			"title": "{0} - Quiz".format(lesson_doc.title),
			"lesson": lesson_doc.name,
			"course": lesson_doc.course,
			"passing_percentage": passing_percentage,
			"show_answers": 1,
			"show_submission_history": 1,
			"shuffle_questions": 1,
			"questions": rows,
		}
	)
	quiz.insert()
	return quiz.name


def _create_question(spec):
	doc = frappe.get_doc(
		{
			"doctype": "LMS Question",
			"question": spec["question"],
			"type": spec["type"],
		}
	)
	if spec["type"] == "Choices":
		for i, option in enumerate(spec["options"][:4]):
			doc.set("option_{0}".format(i + 1), option)
			doc.set("is_correct_{0}".format(i + 1), 1 if i == spec["correct"] else 0)
		doc.set("explanation_{0}".format(spec["correct"] + 1), spec.get("explanation"))
	elif spec["type"] == "User Input":
		for i, possibility in enumerate(spec.get("possibilities", [])[:4]):
			doc.set("possibility_{0}".format(i + 1), possibility)
	doc.insert()
	return doc


def _attach_quiz_to_lesson(lesson_doc, quiz_name):
	try:
		content = json.loads(lesson_doc.content) if lesson_doc.content else {}
	except (ValueError, TypeError):
		content = {}
	blocks = content.get("blocks") or []
	already = any(
		b.get("type") == "quiz" and (b.get("data") or {}).get("quiz") == quiz_name for b in blocks
	)
	if already:
		return
	blocks.append({"type": "quiz", "data": {"quiz": quiz_name}})
	content["blocks"] = blocks
	lesson_doc.content = json.dumps(content)
	lesson_doc.save()


def _lesson_has_quiz(lesson_doc):
	if lesson_doc.quiz_id:
		return True
	try:
		blocks = json.loads(lesson_doc.content).get("blocks") if lesson_doc.content else []
	except (ValueError, TypeError):
		blocks = []
	return any(b.get("type") == "quiz" for b in blocks or []) or bool(
		re.search(r"\{\{\s*Quiz", lesson_doc.body or "")
	)


# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------

def _question_preview(spec):
	if spec["type"] == "Choices":
		return {
			"type": "Choices",
			"question": strip_html_tags(spec["question"]),
			"options": spec["options"],
			"correct_answer": spec["options"][spec["correct"]],
		}
	return {
		"type": "User Input",
		"question": strip_html_tags(spec["question"]),
		"possible_answers": spec.get("possibilities", []),
	}


def _check_permission():
	frappe.only_for(ALLOWED_ROLES)
