<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { call, fmt, downloadRowsAsXlsx } from "../api";
import SectionCard from "./SectionCard.vue";
import FrappControl from "./FrappControl.vue";
import SkeletonRows from "./SkeletonRows.vue";

const loading = ref(true);
const rows = ref([]);
const types = ref([]);
const project = ref("");
const ptype = ref("");
const pmEl = ref(null);
let pmAssetReady = false;

const projectDf = {
	fieldtype: "Link",
	options: "Project",
	placeholder: "All Projects",
	filters: { service: "IT-SW" },
};

async function load() {
	loading.value = true;
	try {
		const r =
			(await call("get_project_wip", {
				project: project.value || null,
				project_type: ptype.value || null,
			})) || {};
		rows.value = r.rows || [];
		types.value = r.types || [];
	} finally {
		loading.value = false;
	}
}

// Mount the full Project Monitoring dashboard (same as the Project form tab)
// for the selected project, reusing teampro.project_monitoring with a stub frm.
async function renderMonitor(name) {
	if (!name) return;
	if (!pmAssetReady) {
		await frappe.require(["/assets/teampro/js/project_monitoring.js?v=20260925-1"]);
		pmAssetReady = true;
	}
	await nextTick();
	const mon = window.teampro && teampro.project_monitoring;
	if (!mon || !pmEl.value) return;
	mon.load_css();
	const frm = {
		doc: { name, service: "IT-SW" },
		_pm_tab: { wrapper: $(pmEl.value) },
	};
	mon.load(frm, true);
}

function onProjectChange(v) {
	if (!v) return;
	renderMonitor(v);
}

function pickProject(name) {
	project.value = name;
	renderMonitor(name);
}

function clearProject() {
	project.value = "";
	load();
}

const fdate = (v) => (v ? frappe.datetime.str_to_user(v) : "-");

const STATUS_CLS = {
	Open: "itd-b-gray",
	Working: "itd-b-blue",
	"In Progress": "itd-b-blue",
	Completed: "itd-b-green",
	Hold: "itd-b-amber",
	Cancelled: "itd-b-gray",
	Overdue: "itd-b-red",
};

const totalRow = computed(() => {
	const t = {
		open: 0, working: 0, review: 0, hold: 0, completed: 0,
		overdue: 0, et: 0, at: 0, meetings: 0, meetings_done: 0,
		so_value: 0, billed: 0, total: 0,
	};
	for (const r of rows.value) {
		for (const k of Object.keys(t)) t[k] += r[k] || 0;
	}
	return t;
});

function exportXlsx() {
	const head = [
		"Project", "Type", "Customer", "Status", "SPOC",
		"Open", "Working", "Review", "Hold", "Completed", "Overdue",
		"ET (Hrs)", "AT (Hrs)", "Meetings Done", "Meetings Total",
		"SLA From", "SLA To", "Expected End", "SO Value", "Billed",
	];
	const data = rows.value.map((r) => [
		r.project_name, r.project_type || "", r.customer || "", r.status || "",
		r.spoc || "", r.open, r.working, r.review, r.hold, r.completed,
		r.overdue, r.et, r.at, r.meetings_done, r.meetings,
		r.sla_from || "", r.sla_to || "", r.expected_end_date || "",
		r.so_value, r.billed,
	]);
	downloadRowsAsXlsx("project-wip.xlsx", "Project WIP", [head, ...data]);
}

onMounted(load);
</script>

<template>
	<SectionCard title="PROJECT WIP" subtitle="IT-SW projects — task & meeting rollup">
		<template #actions>
			<div class="itd-wip-filters">
				<div style="width: 210px">
					<FrappControl :df="projectDf" v-model="project" @change="onProjectChange" />
				</div>
				<select
					v-model="ptype"
					class="form-control input-xs"
					style="width: 140px"
					@change="load"
				>
					<option value="">All Types</option>
					<option v-for="t in types" :key="t" :value="t">{{ t }}</option>
				</select>
				<button class="itd-iconbtn" title="Export to Excel" @click="exportXlsx">⭳</button>
			</div>
		</template>

		<!-- Full Project Monitoring view for the selected project -->
		<div v-if="project" class="itd-wip-monitor">
			<div class="itd-wip-monitor-head">
				<b>{{ project }}</b>
				<button class="itd-textbtn" @click="clearProject">✕ Close monitoring</button>
			</div>
			<div ref="pmEl"></div>
		</div>

		<SkeletonRows v-if="loading" :rows="8" :cols="12" />
		<div v-else class="itd-table-wrap">
			<table class="itd-table itd-table--wide">
				<thead>
					<tr>
						<th>#</th>
						<th class="itd-left">Project</th>
						<th>Type</th>
						<th class="itd-left">Customer</th>
						<th>Status</th>
						<th>Open</th>
						<th>Working</th>
						<th>Review</th>
						<th>Hold</th>
						<th>Comp.</th>
						<th>Overdue</th>
						<th>ET (Hrs)</th>
						<th>AT (Hrs)</th>
						<th>Mtgs</th>
						<th>End / SLA</th>
						<th>SO Value</th>
						<th>Billed</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(r, i) in rows" :key="r.name">
						<td>{{ i + 1 }}</td>
						<td class="itd-left">
							<a href="javascript:void(0)" @click="pickProject(r.name)">{{ r.project_name }}</a>
						</td>
						<td>{{ r.project_type || "-" }}</td>
						<td class="itd-left">{{ r.customer || "-" }}</td>
						<td>
							<span class="itd-badge" :class="STATUS_CLS[r.status] || 'itd-b-gray'">
								{{ r.status || "-" }}
							</span>
						</td>
						<td class="itd-num">{{ r.open }}</td>
						<td class="itd-num">{{ r.working }}</td>
						<td class="itd-num">{{ r.review }}</td>
						<td class="itd-num">{{ r.hold }}</td>
						<td class="itd-num">{{ r.completed }}</td>
						<td class="itd-num" :style="r.overdue ? 'color:#c53030;font-weight:700' : ''">
							{{ r.overdue }}
						</td>
						<td class="itd-num">{{ fmt(r.et) }}</td>
						<td class="itd-num">{{ fmt(r.at) }}</td>
						<td class="itd-num">{{ r.meetings_done }}/{{ r.meetings }}</td>
						<td class="itd-num">{{ fdate(r.sla_to || r.expected_end_date) }}</td>
						<td class="itd-num">{{ fmt(r.so_value) }}</td>
						<td class="itd-num">{{ fmt(r.billed) }}</td>
					</tr>
					<tr v-if="!rows.length">
						<td colspan="17" style="text-align:center;color:#888">No projects match the filters.</td>
					</tr>
				</tbody>
				<tfoot v-if="rows.length">
					<tr>
						<td></td>
						<td class="itd-left">TOTAL ({{ rows.length }})</td>
						<td colspan="3"></td>
						<td>{{ totalRow.open }}</td>
						<td>{{ totalRow.working }}</td>
						<td>{{ totalRow.review }}</td>
						<td>{{ totalRow.hold }}</td>
						<td>{{ totalRow.completed }}</td>
						<td>{{ totalRow.overdue }}</td>
						<td>{{ fmt(totalRow.et) }}</td>
						<td>{{ fmt(totalRow.at) }}</td>
						<td>{{ totalRow.meetings_done }}/{{ totalRow.meetings }}</td>
						<td></td>
						<td>{{ fmt(totalRow.so_value) }}</td>
						<td>{{ fmt(totalRow.billed) }}</td>
					</tr>
				</tfoot>
			</table>
		</div>
	</SectionCard>
</template>
