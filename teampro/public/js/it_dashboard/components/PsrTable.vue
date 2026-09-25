<script setup>
import { ref, computed, onMounted } from "vue";
import { call, splitPair, fmt, downloadRowsAsXlsx } from "../api";
import { Icon } from "../icons";
import SectionCard from "./SectionCard.vue";
import SkeletonRows from "./SkeletonRows.vue";

const rows = ref([]);
const view = ref("overall");
const typeFilter = ref(null);
const loading = ref(true);

onMounted(async () => {
	try {
		rows.value = (await call("get_tasks_project_pivot")) || [];
	} finally {
		loading.value = false;
	}
});

const filtered = computed(() =>
	typeFilter.value ? rows.value.filter((r) => r.project_type === typeFilter.value) : rows.value
);

const COLS = ["open", "working", "pr", "cr"];

const totals = computed(() => {
	const t = {};
	for (const c of COLS) {
		const key = view.value === "current" && c !== "open" ? `${c}_td` : c;
		t[c] = filtered.value.reduce(
			(acc, r) => {
				const p = splitPair(r[key]);
				acc.hr += p.hr;
				acc.n += p.n;
				return acc;
			},
			{ hr: 0, n: 0 }
		);
	}
	return t;
});

function cellVal(row, col) {
	const key = view.value === "current" && col !== "open" ? `${col}_td` : col;
	const p = splitPair(row[key]);
	return `${p.hr.toFixed(2)}/${p.n}`;
}

function setTypeFilter(t) {
	typeFilter.value = t;
}
defineExpose({ setTypeFilter });

function download() {
	const header = ["S.No", "Project", "Type", "Open", "Working", "PR", "CR"];
	const data = filtered.value.map((r, i) => [
		i + 1,
		r.project,
		r.project_type,
		cellVal(r, "open"),
		cellVal(r, "working"),
		cellVal(r, "pr"),
		cellVal(r, "cr"),
	]);
	downloadRowsAsXlsx(`PSR_${view.value}_${frappe.datetime.now_date()}.xlsx`, "PSR", [
		header,
		...data,
	]);
}
</script>

<template>
	<SectionCard title="Project Status Report" subtitle="PSR" class="itd-psr">
		<template #actions>
			<div class="itd-seg">
				<button
					class="itd-seg-btn"
					:class="{ 'itd-seg-btn--on': view === 'overall' }"
					@click="view = 'overall'"
				>
					Overall
				</button>
				<button
					class="itd-seg-btn"
					:class="{ 'itd-seg-btn--on': view === 'current' }"
					@click="view = 'current'"
				>
					Current
				</button>
			</div>
			<button class="itd-iconbtn" title="Download Excel" @click="download">
				<Icon name="download" :size="15" />
			</button>
		</template>

		<SkeletonRows v-if="loading" :rows="8" :cols="7" />
		<div v-else-if="!filtered.length" class="itd-empty">No projects found</div>
		<div v-else class="itd-table-wrap itd-psr-scroll">
			<table class="itd-table">
				<thead>
					<tr>
						<th class="itd-num">S.No</th>
						<th class="itd-left">Project Name</th>
						<th class="itd-left">Type</th>
						<th class="itd-num" title="Open tasks (hours / count)">Open</th>
						<th class="itd-num" title="Working (hours / count)">W</th>
						<th class="itd-num" title="Pending review (hours / count)">PR</th>
						<th class="itd-num" title="Client review (hours / count)">CR</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="row in filtered" :key="row.project">
						<td class="itd-num itd-muted">{{ row.s_no }}</td>
						<td class="itd-left">
							<a
								:href="`/app/project/${encodeURIComponent(row.project)}`"
								target="_blank"
								class="itd-link"
								>{{ row.project }}</a
							>
						</td>
						<td class="itd-left">
							<span class="itd-tag">{{ row.project_type }}</span>
						</td>
						<td class="itd-num itd-mono">{{ cellVal(row, "open") }}</td>
						<td class="itd-num itd-mono">{{ cellVal(row, "working") }}</td>
						<td class="itd-num itd-mono">{{ cellVal(row, "pr") }}</td>
						<td class="itd-num itd-mono">{{ cellVal(row, "cr") }}</td>
					</tr>
				</tbody>
				<tfoot>
					<tr>
						<td colspan="3">Total</td>
						<td class="itd-num">{{ fmt(totals.open.hr) }}/{{ totals.open.n }}</td>
						<td class="itd-num">{{ fmt(totals.working.hr) }}/{{ totals.working.n }}</td>
						<td class="itd-num">{{ fmt(totals.pr.hr) }}/{{ totals.pr.n }}</td>
						<td class="itd-num">{{ fmt(totals.cr.hr) }}/{{ totals.cr.n }}</td>
					</tr>
				</tfoot>
			</table>
		</div>
	</SectionCard>
</template>
