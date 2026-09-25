<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { call, fmt, sysDate, today } from "../api";
import SectionCard from "./SectionCard.vue";
import SkeletonRows from "./SkeletonRows.vue";
import FrappControl from "./FrappControl.vue";

const loading = ref(true);
const teams = ref([]);
const generatedAt = ref("");
const fromDm = ref(false);
const dataDate = ref("");
const selDate = ref(null);
const autoRefresh = ref(true);
const openCbs = ref(new Set());
let timer = null;

async function load() {
	try {
		const r = await call("get_live_status", selDate.value ? { date: selDate.value } : {});
		teams.value = r?.teams || [];
		generatedAt.value = r?.generated_at || "";
		fromDm.value = !!r?.from_dm;
		dataDate.value = r?.date || "";
	} finally {
		loading.value = false;
	}
}

function onDate(v) {
	selDate.value = sysDate(v);
	load();
}

const subtitle = computed(() => {
	const when = dataDate.value && dataDate.value !== today() ? dataDate.value + " · " : "";
	return (fromDm.value ? "Plan vs actual · " : "No plan yet · ") + when + "As of " + fmtTime(generatedAt.value);
});

function toggleCb(team, cb) {
	const k = team + "|" + cb;
	const s = new Set(openCbs.value);
	s.has(k) ? s.delete(k) : s.add(k);
	openCbs.value = s;
}

function isOpen(team, cb) {
	return !openCbs.value.has(team + "|" + cb);
}

function pct(t) {
	const total = (t.at || 0) + (t.rt || 0);
	if (!total) return 0;
	return Math.min(100, Math.round(((t.at || 0) / total) * 100));
}

function barClass(t) {
	const p = (t.at || 0) / ((t.at || 0) + (t.rt || 0) || 1);
	if (p > 1) return "itd-fill--red";
	if (p > 0.8) return "itd-fill--amber";
	return "itd-fill--green";
}

function fmtTime(ts) {
	if (!ts) return "";
	try {
		return frappe.datetime.str_to_user(ts).split(" ").pop();
	} catch (e) {
		return ts;
	}
}

const totals = computed(() => {
	let planned = 0, worked = 0;
	for (const t of teams.value)
		for (const m of t.members) {
			planned += m.planned || 0;
			worked += m.worked || 0;
		}
	return { planned, worked };
});

onMounted(() => {
	load();
	timer = setInterval(() => {
		if (autoRefresh.value) load();
	}, 60000);
});
onBeforeUnmount(() => clearInterval(timer));
</script>

<template>
	<SectionCard
		title="Live Activity"
		:subtitle="subtitle"
	>
		<template #actions>
			<span v-if="fromDm && totals.planned" class="itd-livecov">
				{{ totals.worked }}/{{ totals.planned }} tasks worked
			</span>
			<FrappControl
				:df="{ fieldtype: 'Date', fieldname: 'live_date', placeholder: 'Select date' }"
				:modelValue="selDate"
				@update:modelValue="onDate"
			/>
			<label class="itd-check">
				<input type="checkbox" v-model="autoRefresh" />
				Auto-refresh
			</label>
			<button class="itd-textbtn" @click="load">Refresh</button>
		</template>

		<SkeletonRows v-if="loading" :rows="8" :cols="6" />
		<div v-else-if="!teams.length" class="itd-empty">No activity right now</div>

		<div v-else class="itd-table-wrap">
			<table class="itd-table">
				<thead>
					<tr>
						<th class="itd-left">Employee / Task</th>
						<th class="itd-left">Subject</th>
						<th class="itd-left">Project</th>
						<th>Status</th>
						<th>Priority</th>
						<th class="itd-num">ET</th>
						<th class="itd-num">Spent</th>
						<th class="itd-num">Left</th>
						<th class="itd-num">Today</th>
						<th class="itd-left" style="min-width: 140px">Progress</th>
					</tr>
				</thead>
				<tbody v-for="t in teams" :key="t.team">
					<tr class="itd-row-team">
						<td colspan="10" class="itd-left">
							<img v-if="t.logo" :src="t.logo" class="itd-teamlogo" alt="" />
							<b>{{ t.team }}</b>
						</td>
					</tr>
					<template v-for="m in t.members" :key="t.team + m.cb">
						<tr class="itd-row-cb" @click="toggleCb(t.team, m.cb)">
							<td colspan="10" class="itd-left">
								<span class="itd-cbhead">
									<img v-if="m.image" :src="m.image" class="itd-avatar" alt="" />
									<b>{{ m.cb }}</b>
									<span class="itd-muted">{{ m.employee }}</span>
									<span v-if="m.is_tl" class="itd-tag itd-tag--plan">TL</span>
									<span v-if="fromDm" class="itd-livecov">
										{{ m.worked }}/{{ m.planned }} worked
									</span>
									<span v-else class="itd-muted">· {{ m.tasks.length }} task{{ m.tasks.length === 1 ? "" : "s" }}</span>
									<span class="itd-muted">· {{ fmt(m.today_hours) }}h today</span>
									<span v-if="m.aph" class="itd-muted">· APH {{ fmt(m.aph) }}</span>
								</span>
							</td>
						</tr>
						<tr v-if="!m.tasks.length && !m.unplanned.length && isOpen(t.team, m.cb)" class="itd-row-task">
							<td colspan="10" class="itd-left itd-indent itd-muted">No tasks</td>
						</tr>
						<tr
							v-for="task in m.tasks"
							v-show="isOpen(t.team, m.cb)"
							:key="task.name"
							class="itd-row-task"
							:class="{ 'itd-row-idle': fromDm && !task.today && task.status === 'Working' }"
						>
							<td class="itd-left itd-indent">
								<a :href="`/app/task/${encodeURIComponent(task.name)}`" target="_blank" class="itd-link">{{ task.name }}</a>
							</td>
							<td class="itd-left">{{ task.subject }}</td>
							<td class="itd-left">{{ task.project }}</td>
							<td>
								<span class="itd-prio" :class="'itd-st--' + String(task.status || '').toLowerCase().replace(/ /g, '-')">{{ task.status }}</span>
							</td>
							<td>
								<span v-if="task.priority" class="itd-prio" :class="'itd-prio--' + String(task.priority).toLowerCase()">{{ task.priority }}</span>
							</td>
							<td class="itd-num itd-mono">{{ fmt(task.et) }}</td>
							<td class="itd-num itd-mono">{{ fmt(task.at) }}</td>
							<td class="itd-num itd-mono">{{ fmt(task.rt) }}</td>
							<td class="itd-num itd-mono">
								<span :class="{ 'itd-today-zero': fromDm && !task.today, 'itd-today-yes': task.today }">
									{{ fmt(task.today) }}
								</span>
							</td>
							<td>
								<div class="itd-prog">
									<div class="itd-prog-track">
										<div class="itd-prog-fill" :class="barClass(task)" :style="{ width: pct(task) + '%' }"></div>
									</div>
									<span class="itd-prog-label">{{ pct(task) }}%</span>
								</div>
							</td>
						</tr>
						<tr
							v-for="task in m.unplanned"
							v-show="isOpen(t.team, m.cb)"
							:key="'u-' + task.name"
							class="itd-row-task itd-row-unplanned"
						>
							<td class="itd-left itd-indent">
								<a :href="`/app/task/${encodeURIComponent(task.name)}`" target="_blank" class="itd-link">{{ task.name }}</a>
							</td>
							<td class="itd-left">{{ task.subject }}</td>
							<td class="itd-left">{{ task.project }}</td>
							<td>
								<span class="itd-prio itd-st--open">{{ task.status }}</span>
								<span class="itd-tag itd-tag--spot">Unplanned</span>
							</td>
							<td></td>
							<td class="itd-num itd-muted">–</td>
							<td class="itd-num itd-muted">–</td>
							<td class="itd-num itd-muted">–</td>
							<td class="itd-num itd-mono itd-today-yes">{{ fmt(task.today) }}</td>
							<td></td>
						</tr>
					</template>
				</tbody>
			</table>
		</div>
	</SectionCard>
</template>
