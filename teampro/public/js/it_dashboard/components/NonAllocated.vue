<script setup>
import { ref, computed, onMounted } from "vue";
import { call, fmt, downloadRowsAsXlsx } from "../api";
import { Icon } from "../icons";
import SectionCard from "./SectionCard.vue";
import SkeletonRows from "./SkeletonRows.vue";

const loading = ref(true);
const data = ref([]);
const view = ref("overall");
const kt = ref("");
const openProjects = ref(new Set());

async function load() {
	loading.value = true;
	try {
		const r = await call("get_non_allocated_tasks_test", {
			view: view.value,
			kt_confirmed: kt.value,
		});
		data.value = r?.data || [];
		openProjects.value = new Set();
	} finally {
		loading.value = false;
	}
}

const groups = computed(() => {
	const g = {};
	for (const t of data.value) {
		const p = t.project || "No Project";
		(g[p] = g[p] || []).push(t);
	}
	return Object.keys(g)
		.sort()
		.map((project) => {
			const tasks = g[project];
			return {
				project,
				tasks,
				et: tasks.reduce((s, t) => s + (+t.expected_time || 0), 0),
				rt: tasks.reduce((s, t) => s + (+t.rt || 0), 0),
				at: tasks.reduce((s, t) => s + (+t.actual_time || 0), 0),
			};
		});
});

const grand = computed(() => ({
	et: groups.value.reduce((s, g) => s + g.et, 0),
	rt: groups.value.reduce((s, g) => s + g.rt, 0),
	at: groups.value.reduce((s, g) => s + g.at, 0),
}));

const allOpen = computed(
	() => groups.value.length > 0 && openProjects.value.size === groups.value.length
);

function toggleAll() {
	openProjects.value = allOpen.value
		? new Set()
		: new Set(groups.value.map((g) => g.project));
}

function toggle(p) {
	const s = new Set(openProjects.value);
	s.has(p) ? s.delete(p) : s.add(p);
	openProjects.value = s;
}

function setView(v) {
	view.value = v;
	load();
}

function onKt(e) {
	kt.value = e.target.value;
	load();
}

function download() {
	if (!data.value.length) return frappe.msgprint("No data available to download");
	const rows = [["Project", "CB", "Sprint", "Task", "Subject", "ET", "RT", "AT", "AGE", "CF", "Priority", "Status"]];
	for (const g of groups.value)
		for (const t of g.tasks)
			rows.push([
				g.project, t.cb || "", t.custom_sprint || "", t.name || "", t.subject || "",
				+t.expected_time || 0, +t.rt || 0, +t.actual_time || 0,
				t.custom_age || "", t.custom_production_date_count || "", t.priority || "", t.status || "",
			]);
	rows.push(["GRAND TOTAL", "", "", "", "", +grand.value.et.toFixed(2), +grand.value.rt.toFixed(2), +grand.value.at.toFixed(2), "", "", "", ""]);
	downloadRowsAsXlsx("NonAllocatedTasks.xlsx", "Non Allocated Tasks", rows);
}

onMounted(load);
</script>

<template>
	<SectionCard title="Non-Allocated Total">
		<template #actions>
			<div class="itd-seg">
				<button
					class="itd-seg-btn"
					:class="{ 'itd-seg-btn--on': view === 'overall' }"
					@click="setView('overall')"
				>
					Overall
				</button>
				<button
					class="itd-seg-btn"
					:class="{ 'itd-seg-btn--on': view === 'sprint' }"
					@click="setView('sprint')"
				>
					NA
				</button>
			</div>
			<select class="itd-select" @change="onKt" :value="kt" title="KT Confirmed">
				<option value="">KT Confirm</option>
				<option value="Yes">Yes</option>
				<option value="No">No</option>
			</select>
			<button class="itd-iconbtn" title="Download Excel" @click="download">
				<Icon name="download" :size="15" />
			</button>
		</template>

		<SkeletonRows v-if="loading" :rows="6" :cols="10" />
		<div v-else-if="!groups.length" class="itd-empty">No tasks found</div>

		<div v-else class="itd-table-wrap itd-na-scroll">
			<table class="itd-table">
				<thead>
					<tr>
						<th class="itd-left itd-th-toggle" @click="toggleAll">
							{{ allOpen ? "− All" : "+ All" }}
						</th>
						<th>Sprint</th>
						<th>Task</th>
						<th class="itd-left">Subject</th>
						<th class="itd-num" title="Estimated time (hrs)">ET</th>
						<th class="itd-num" title="Remaining time (hrs)">RT</th>
						<th class="itd-num" title="Actual time (hrs)">AT</th>
						<th class="itd-num" title="Age (days)">Age</th>
						<th class="itd-num" title="Carry-forward count">CF</th>
						<th>Priority</th>
						<th>Status</th>
					</tr>
				</thead>
				<tbody v-for="g in groups" :key="g.project">
					<tr class="itd-row-group" @click="toggle(g.project)">
						<td colspan="4" class="itd-left">
							<Icon :name="openProjects.has(g.project) ? 'chevron-down' : 'chevron-right'" :size="13" />
							{{ g.project }}
						</td>
						<td class="itd-num"><b>{{ fmt(g.et) }}</b></td>
						<td class="itd-num"><b>{{ fmt(g.rt) }}</b></td>
						<td class="itd-num"><b>{{ fmt(g.at) }}</b></td>
						<td colspan="4"></td>
					</tr>
					<template v-if="openProjects.has(g.project)">
						<tr
							v-for="t in g.tasks"
							:key="t.name"
							:class="{ 'itd-row-alert': (+t.custom_age || 0) > 3 }"
						>
							<td class="itd-muted">{{ t.cb || "" }}</td>
							<td>{{ t.custom_sprint || "" }}</td>
							<td>
								<a :href="`/app/task/${encodeURIComponent(t.name)}`" target="_blank" class="itd-link">{{ t.name }}</a>
							</td>
							<td class="itd-left">{{ t.subject || "" }}</td>
							<td class="itd-num itd-mono">{{ fmt(t.expected_time) }}</td>
							<td class="itd-num itd-mono">{{ fmt(t.rt) }}</td>
							<td class="itd-num itd-mono">{{ fmt(t.actual_time) }}</td>
							<td class="itd-num">{{ t.custom_age || "" }}</td>
							<td class="itd-num">{{ t.custom_production_date_count || "" }}</td>
							<td>
								<span v-if="t.priority" class="itd-prio" :class="'itd-prio--' + String(t.priority).toLowerCase()">{{ t.priority }}</span>
							</td>
							<td>{{ t.status || "" }}</td>
						</tr>
					</template>
				</tbody>
				<tfoot>
					<tr>
						<td colspan="4">Grand Total</td>
						<td class="itd-num">{{ fmt(grand.et) }}</td>
						<td class="itd-num">{{ fmt(grand.rt) }}</td>
						<td class="itd-num">{{ fmt(grand.at) }}</td>
						<td colspan="4"></td>
					</tr>
				</tfoot>
			</table>
		</div>
	</SectionCard>
</template>
