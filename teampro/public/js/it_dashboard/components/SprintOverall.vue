<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { call, fmt } from "../api";
import { Icon } from "../icons";
import SectionCard from "./SectionCard.vue";
import SkeletonRows from "./SkeletonRows.vue";

const props = defineProps({
	team: { type: String, default: "" },
	sprint: { type: String, default: "" },
});

const loading = ref(true);
const teams = ref([]);
const open = ref(new Set());

async function load() {
	loading.value = true;
	try {
		const r = await call("get_sprint_teamwise_summary", {
			team: props.team || "",
			sprint: props.sprint || "",
		});
		teams.value = r?.teams || [];
		open.value = new Set();
	} finally {
		loading.value = false;
	}
}

const COLS = [
	"aph", "planned_rt", "comp_rt", "work_rt", "nt_rt",
	"spot_rt", "spot_comp_rt", "spot_work_rt", "spot_nt_rt",
	"total_rt", "at", "completed_rt", "completed_at",
	"working_rt", "working_at", "total_nt_hours",
	"biometric_hrs", "nc_rt", "reopen_rt", "de_rt",
];

const grand = computed(() => {
	const g = Object.fromEntries(COLS.map((c) => [c, 0]));
	for (const t of teams.value) {
		const tot = t.totals || {};
		for (const c of COLS) g[c] += +tot[c] || 0;
	}
	return g;
});

const prod = (r) => (r.aph ? (r.completed_rt / r.aph) * 100 : 0);
const eff = (r) => (r.completed_rt ? (r.completed_at / r.completed_rt) * 100 : 0);

function toggle(i) {
	const s = new Set(open.value);
	s.has(i) ? s.delete(i) : s.add(i);
	open.value = s;
}

watch(() => [props.team, props.sprint], load);
onMounted(load);
</script>

<template>
	<SectionCard title="Overall Team Summary" subtitle="Sprint">
		<SkeletonRows v-if="loading" :rows="6" :cols="12" />
		<div v-else-if="!teams.length" class="itd-empty itd-empty--warn">
			No Sprint Data Found for Today
		</div>

		<div v-else class="itd-table-wrap">
			<table class="itd-table itd-table--wide">
				<thead>
					<tr>
						<th rowspan="2" style="width:30px"></th>
						<th rowspan="2">S.No</th>
						<th rowspan="2" class="itd-left">Team</th>
						<th rowspan="2">Sprint ID</th>
						<th rowspan="2" class="itd-num" title="Available productive hours">APH</th>
						<th colspan="4" class="itd-thgrp itd-thgrp--a">PLAN</th>
						<th colspan="4" class="itd-thgrp itd-thgrp--b">SPOT</th>
						<th colspan="9" class="itd-thgrp itd-thgrp--c">TOTAL</th>
						<th rowspan="2" class="itd-num">Biometric Hrs</th>
						<th rowspan="2" class="itd-num">NC RT</th>
						<th rowspan="2" class="itd-num">Reopen RT</th>
						<th rowspan="2" class="itd-num">DE RT</th>
					</tr>
					<tr>
						<th class="itd-num">Planned RT</th><th class="itd-num">Comp RT</th><th class="itd-num">Work RT</th><th class="itd-num">NT RT</th>
						<th class="itd-num">Spot RT</th><th class="itd-num">Spot Comp RT</th><th class="itd-num">Spot Work RT</th><th class="itd-num">Spot NT RT</th>
						<th class="itd-num">Total RT</th><th class="itd-num">AT</th><th class="itd-num">Completed RT</th><th class="itd-num">Completed AT</th><th class="itd-num">Working RT</th><th class="itd-num">Working AT</th><th class="itd-num">Total NT RT</th><th class="itd-num">Productivity %</th><th class="itd-num">Efficiency %</th>
					</tr>
				</thead>
				<tbody v-for="(t, i) in teams" :key="t.team">
					<tr class="itd-row-group" @click="toggle(i)">
						<td class="itd-chev">
							<Icon :name="open.has(i) ? 'chevron-down' : 'chevron-right'" :size="13" />
						</td>
						<td>{{ i + 1 }}</td>
						<td class="itd-left"><b>{{ t.team }}</b></td>
						<td>{{ t.sprint_id || "—" }}</td>
						<td class="itd-num">{{ fmt(t.totals?.aph) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.planned_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.comp_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.work_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.nt_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.spot_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.spot_comp_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.spot_work_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.spot_nt_rt) }}</td>
						<td class="itd-num"><b>{{ fmt(t.totals?.total_rt) }}</b></td>
						<td class="itd-num">{{ fmt(t.totals?.at) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.completed_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.completed_at) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.working_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.working_at) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.total_nt_hours) }}</td>
						<td class="itd-num">{{ fmt(prod(t.totals || {})) }}%</td>
						<td class="itd-num">{{ fmt(eff(t.totals || {})) }}%</td>
						<td class="itd-num">{{ fmt(t.totals?.biometric_hrs) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.nc_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.reopen_rt) }}</td>
						<td class="itd-num">{{ fmt(t.totals?.de_rt) }}</td>
					</tr>
					<tr
						v-for="c in t.cbs || []"
						v-show="open.has(i)"
						:key="t.team + c.cb"
						class="itd-row-detail"
					>
						<td></td><td></td>
						<td class="itd-left itd-indent">{{ c.cb }}</td>
						<td></td>
						<td class="itd-num">{{ fmt(c.aph) }}</td>
						<td class="itd-num">{{ fmt(c.planned_rt) }}</td>
						<td class="itd-num">{{ fmt(c.comp_rt) }}</td>
						<td class="itd-num">{{ fmt(c.work_rt) }}</td>
						<td class="itd-num">{{ fmt(c.nt_rt) }}</td>
						<td class="itd-num">{{ fmt(c.spot_rt) }}</td>
						<td class="itd-num">{{ fmt(c.spot_comp_rt) }}</td>
						<td class="itd-num">{{ fmt(c.spot_work_rt) }}</td>
						<td class="itd-num">{{ fmt(c.spot_nt_rt) }}</td>
						<td class="itd-num">{{ fmt(c.total_rt) }}</td>
						<td class="itd-num">{{ fmt(c.at) }}</td>
						<td class="itd-num">{{ fmt(c.completed_rt) }}</td>
						<td class="itd-num">{{ fmt(c.completed_at) }}</td>
						<td class="itd-num">{{ fmt(c.working_rt) }}</td>
						<td class="itd-num">{{ fmt(c.working_at) }}</td>
						<td class="itd-num">{{ fmt(c.total_nt_hours) }}</td>
						<td class="itd-num">{{ fmt(prod(c)) }}%</td>
						<td class="itd-num">{{ fmt(eff(c)) }}%</td>
						<td class="itd-num">{{ fmt(c.biometric_hrs) }}</td>
						<td class="itd-num">{{ fmt(c.nc_rt) }}</td>
						<td class="itd-num">{{ fmt(c.reopen_rt) }}</td>
						<td class="itd-num">{{ fmt(c.de_rt) }}</td>
					</tr>
				</tbody>
				<tfoot>
					<tr>
						<td colspan="4">GRAND TOTAL</td>
						<td class="itd-num">{{ fmt(grand.aph) }}</td>
						<td class="itd-num">{{ fmt(grand.planned_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.comp_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.work_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.nt_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.spot_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.spot_comp_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.spot_work_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.spot_nt_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.total_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.at) }}</td>
						<td class="itd-num">{{ fmt(grand.completed_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.completed_at) }}</td>
						<td class="itd-num">{{ fmt(grand.working_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.working_at) }}</td>
						<td class="itd-num">{{ fmt(grand.total_nt_hours) }}</td>
						<td class="itd-num">{{ fmt(prod(grand)) }}%</td>
						<td class="itd-num">{{ fmt(eff(grand)) }}%</td>
						<td class="itd-num">{{ fmt(grand.biometric_hrs) }}</td>
						<td class="itd-num">{{ fmt(grand.nc_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.reopen_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.de_rt) }}</td>
					</tr>
				</tfoot>
			</table>
		</div>
	</SectionCard>
</template>
