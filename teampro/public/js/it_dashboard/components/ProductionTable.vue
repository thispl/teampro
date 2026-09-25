<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { call, callRaw, fmt, downloadRowsAsXlsx } from "../api";
import { prod, cbKey, teamKey, setProdData, toggleProdAll, toggleProdTeam, toggleProdCb } from "../store";
import { Icon } from "../icons";
import SectionCard from "./SectionCard.vue";
import SkeletonRows from "./SkeletonRows.vue";

const loading = ref(true);
const raw = ref({ data: [], team_order: [] });
const confirmBusy = ref({});

async function load() {
	loading.value = true;
	try {
		const args = prod.date ? { from_date: prod.date, to_date: prod.date } : {};
		raw.value = (await call("get_today_task_data1", args)) || { data: [], team_order: [] };
		const t = [], c = [];
		for (const row of raw.value.data || []) {
			t.push(row[12] || "No Team");
			c.push(cbKey(row[12], row[3]));
		}
		setProdData([...new Set(t)], [...new Set(c)]);
	} finally {
		loading.value = false;
	}
}

const groups = computed(() => {
	const byTeam = {};
	for (const row of raw.value.data || []) {
		const team = row[12] || "No Team";
		const cb = row[3] || "—";
		(((byTeam[team] = byTeam[team] || {})[cb] =
			byTeam[team][cb] || []).push(row));
	}
	const order = raw.value.team_order || [];
	const names = order.filter((t) => byTeam[t]);
	for (const t of Object.keys(byTeam)) if (!names.includes(t)) names.push(t);
	return names.map((team) => {
		const cbs = Object.entries(byTeam[team])
			.sort((a, b) => (a[1][0][25] || 0) - (b[1][0][25] || 0))
			.map(([cb, tasks]) => ({ cb, key: cbKey(team, cb), tasks }));
		return { team, key: teamKey(team), logo: cbs[0]?.tasks[0][19] || "", cbs };
	});
});

function passesFilters(row) {
	const f = prod.filters;
	if (f.priority && String(row[8] || "").toLowerCase() !== f.priority.toLowerCase())
		return false;
	if (f.sp && (row[21] == 1 ? "S" : "P") !== f.sp) return false;
	if (f.ro && !(parseInt(row[22]) > 0)) return false;
	if (f.cf && !(parseInt(row[23]) > 0)) return false;
	if (f.ts) {
		const p = progress(row);
		const band = p > 100 ? "red" : p > 75 ? "orange" : p > 0 ? "blue" : "";
		if (band !== f.ts) return false;
	}
	return true;
}

function progress(row) {
	const at = +row[13] || 0;
	const rt = +row[14] || 0;
	return rt > 0 ? Math.round((at / rt) * 100) : 0;
}

function progressColor(p) {
	return p > 100 ? "var(--itd-red)" : p > 75 ? "var(--itd-amber)" : "var(--itd-teal)";
}

const STATUS_LETTER = {
	Working: "W",
	"Pending Review": "PR",
	"Client Review": "CR",
	Completed: "✓",
};

function isOpen(team, cbkey) {
	return prod.openTeams.has(team) && prod.openCbs.has(cbkey);
}

const toggleAll = () => toggleProdAll(!prod.allOpen);
const toggleTeam = (team) => toggleProdTeam(team);
const toggleCb = (team, cb) => toggleProdCb(cbKey(team, cb));

function sum(tasks, idx) {
	return tasks.reduce((s, r) => s + (+r[idx] || 0), 0);
}

function taskStatus(row) {
	return (row[10] || "").trim();
}

// ---- confirm / unconfirm ----
async function confirmTask(row) {
	const task = row[0];
	confirmBusy.value[task] = true;
	try {
		await callRaw("frappe.client.set_value", {
			doctype: "Task",
			name: task,
			fieldname: "is_confirmed",
			value: 1,
		});
		row[20] = 1;
		frappe.show_alert({ message: "Task Confirmed", indicator: "green" });
	} finally {
		confirmBusy.value[task] = false;
	}
}

async function unconfirmTask(row) {
	const task = row[0];
	confirmBusy.value[task] = true;
	try {
		const running = await call("check_running_timesheet", { task });
		if (running) {
			frappe.msgprint({
				title: "Not Allowed",
				message: "This task is already running in a timesheet.",
				indicator: "red",
			});
			return;
		}
		await callRaw("frappe.client.set_value", {
			doctype: "Task",
			name: task,
			fieldname: "is_confirmed",
			value: 0,
		});
		row[20] = 0;
		frappe.show_alert({ message: "Task Unconfirmed", indicator: "orange" });
	} finally {
		confirmBusy.value[task] = false;
	}
}

// ---- task info dialog ----
async function showTaskInfo(task) {
	const t = await callRaw("frappe.client.get", { doctype: "Task", name: task });
	if (!t) return;
	const row = (k, v) =>
		`<tr><td class="tdl">${k}</td><td class="tdv">${v ?? ""}</td></tr>`;
	const html = `
		<table class="itd-dialog-table">
			${row("Task", t.name)}${row("Project", t.project || "")}
			${row("Subject", t.subject || "")}${row("Description", t.description || "")}
			${row("ET", t.expected_time ?? "")}${row("RT", t.rt ?? "")}${row("AT", t.actual_time ?? "")}
			${row("CF", t.custom_production_date_count ?? "")}${row("RO", t.revisions ?? "")}
			${row("Created On", t.creation ? frappe.datetime.str_to_user(t.creation) : "")}
			${row("Allocated On", t.custom_allocated_on ? frappe.datetime.str_to_user(t.custom_allocated_on) : "")}
			${row("Age", t.custom_age ?? "")}
			${row("Developer Note", t.custom_developer_note || "")}
			${row("Remarks", t.custom_taskissue_action_taken || "")}
		</table>`;
	const d = new frappe.ui.Dialog({
		title: `Task Details — ${t.name}`,
		fields: [{ fieldtype: "HTML", fieldname: "d", options: html }],
	});
	d.show();
	d.$wrapper.find(".modal-dialog").css({ "max-width": "900px", width: "90%" });
}

// ---- export ----
function exportExcel() {
	if (!raw.value.data?.length) return frappe.msgprint("No data available");
	const rows = [
		["Sl No", "Sprint", "Project", "Task", "Subject", "S/P", "RO", "CF", "ET", "AT", "RT", "Priority", "Status"],
	];
	let i = 1;
	for (const t of groups.value)
		for (const c of t.cbs)
			for (const r of c.tasks) {
				if (!passesFilters(r)) continue;
				rows.push([
					i++, r[15], r[1], r[0], r[2], r[21] == 1 ? "S" : "P",
					r[22] || 0, r[23] || 0, +r[5] || 0, +r[7] || 0, +r[14] || 0,
					r[8] || "", taskStatus(r),
				]);
			}
	downloadRowsAsXlsx(`Production_Tasks_${frappe.datetime.now_date()}.xlsx`, "Production", rows);
}

watch(() => prod.date, load);
onMounted(load);
defineExpose({ reload: load, toggleTeam, toggleCb });
</script>

<template>
	<SectionCard title="Production Table" class="itd-prodtable">
		<template #actions>
			<button class="itd-textbtn" @click="toggleAll">{{ prod.allOpen ? "− All" : "+ All" }}</button>
			<button class="itd-iconbtn" title="Download Excel" @click="exportExcel">
				<Icon name="download" :size="15" />
			</button>
		</template>

		<SkeletonRows v-if="loading" :rows="10" :cols="12" />
		<div v-else-if="!raw.data?.length" class="itd-empty">No production tasks for this date</div>

		<div v-else class="itd-table-wrap">
			<table class="itd-table itd-table--fixed">
				<thead>
					<tr>
						<th style="width:44px">#</th>
						<th style="width:88px">Sprint</th>
						<th class="itd-left" style="width:170px">Project</th>
						<th style="width:120px">Task</th>
						<th class="itd-left">Subject</th>
						<th title="Spot / Plan">S/P</th>
						<th title="Reopen count">RO</th>
						<th title="Carry-forward count">CF</th>
						<th class="itd-num" title="Estimated time (hrs)">ET</th>
						<th class="itd-num" title="Actual time (hrs)">AT</th>
						<th class="itd-num" title="Remaining today (hrs)">RT</th>
						<th>Priority</th>
						<th style="width:150px">Status</th>
					</tr>
				</thead>
				<tbody v-for="t in groups" :key="t.key">
					<!-- Team header -->
					<tr class="itd-row-team">
						<td>
							<img v-if="t.logo" :src="t.logo" class="itd-teamlogo" alt="" />
						</td>
						<td colspan="7" class="itd-left">
							<div class="itd-teamrow">
								<button class="itd-mini" @click="toggleTeam(t.team)">
									{{ prod.openTeams.has(t.team) ? "−" : "+" }} All
								</button>
								<span class="itd-teamrow-name">{{ t.team }}</span>
								<button
									v-for="c in t.cbs"
									:key="c.key"
									class="itd-cbchip"
									:class="{ 'itd-cbchip--off': !prod.openCbs.has(c.key) }"
									:title="c.cb"
									@click="toggleCb(t.team, c.cb)"
								>
									<img
										v-if="c.tasks[0][18]"
										:src="c.tasks[0][18]"
										class="itd-avatar itd-avatar--sm"
										alt=""
									/>
									<span v-else class="itd-avatar itd-avatar--sm itd-avatar--fallback">{{ c.cb }}</span>
								</button>
							</div>
						</td>
						<td class="itd-num"><b>{{ fmt(t.cbs.reduce((s, c) => s + sum(c.tasks, 5), 0)) }}</b></td>
						<td class="itd-num"><b>{{ fmt(t.cbs.reduce((s, c) => s + sum(c.tasks, 7), 0)) }}</b></td>
						<td class="itd-num"><b>{{ fmt(t.cbs.reduce((s, c) => s + sum(c.tasks, 14), 0)) }}</b></td>
						<td colspan="2"></td>
					</tr>

					<template v-for="c in t.cbs" :key="c.key">
						<!-- CB header -->
						<tr v-if="prod.openTeams.has(t.team)" class="itd-row-cb" @click="toggleCb(t.team, c.cb)">
							<td class="itd-chev">
								<Icon :name="prod.openCbs.has(c.key) ? 'chevron-down' : 'chevron-right'" :size="14" />
							</td>
							<td colspan="7" class="itd-left">{{ c.tasks[0][24] || c.cb }}</td>
							<td class="itd-num"><b>{{ fmt(sum(c.tasks, 5)) }}</b></td>
							<td class="itd-num"><b>{{ fmt(sum(c.tasks, 7)) }}</b></td>
							<td class="itd-num"><b>{{ fmt(sum(c.tasks, 14)) }}</b></td>
							<td colspan="2"></td>
						</tr>

						<!-- Task rows -->
						<template v-for="(r, ri) in c.tasks" :key="r[0] + '-' + ri">
							<tr v-if="isOpen(t.team, c.key) && passesFilters(r)" class="itd-row-task">
								<td class="itd-muted">{{ ri + 1 }}</td>
								<td>{{ r[15] }}</td>
								<td class="itd-left">
									<a :href="`/app/project/${encodeURIComponent(r[1])}`" target="_blank" class="itd-link">{{ r[1] }}</a>
								</td>
								<td>
									<span class="itd-taskcell">
										<button class="itd-iconbtn itd-iconbtn--xs" title="Task details" @click="showTaskInfo(r[0])">
											<Icon name="eye" :size="13" />
										</button>
										<a :href="`/app/task/${encodeURIComponent(r[0])}`" target="_blank" class="itd-link">{{ r[0] }}</a>
									</span>
								</td>
								<td class="itd-left">{{ r[2] }}</td>
								<td>
									<span class="itd-tag" :class="r[21] == 1 ? 'itd-tag--spot' : 'itd-tag--plan'">{{ r[21] == 1 ? "S" : "P" }}</span>
								</td>
								<td>{{ r[22] || 0 }}</td>
								<td>{{ r[23] || 0 }}</td>
								<td class="itd-num itd-mono">{{ fmt(r[5]) }}</td>
								<td class="itd-num itd-mono">{{ fmt(r[7]) }}</td>
								<td class="itd-num itd-mono">{{ fmt(r[14]) }}</td>
								<td>
									<span v-if="r[8]" class="itd-prio" :class="'itd-prio--' + String(r[8]).toLowerCase()">{{ r[8] }}</span>
								</td>
								<td>
									<button
										v-if="r[20] == 0"
										class="itd-statusicon itd-statusicon--confirm"
										:disabled="confirmBusy[r[0]]"
										title="Confirm task"
										@click="confirmTask(r)"
									>
										<Icon name="check" :size="13" />
									</button>
									<div v-else-if="(+r[13] || 0) > 0" class="itd-prog" :title="`AT ${fmt(r[13])} / RT ${fmt(r[14])}`">
										<div class="itd-prog-track">
											<div
												class="itd-prog-fill"
												:style="{ width: Math.min(progress(r), 100) + '%', background: progressColor(progress(r)) }"
											></div>
										</div>
										<span class="itd-prog-label">{{ STATUS_LETTER[taskStatus(r)] || "" }} {{ progress(r) }}%</span>
									</div>
									<button
										v-else
										class="itd-statusicon itd-statusicon--unconfirm"
										:disabled="confirmBusy[r[0]]"
										title="Unconfirm task"
										@click="unconfirmTask(r)"
									>
										C
									</button>
								</td>
							</tr>
						</template>
					</template>
				</tbody>
			</table>
		</div>
	</SectionCard>
</template>
