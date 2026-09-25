<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { call, fmt, sysDate } from "../api";
import { prod, cbKey, teamKey, toggleProdTeam, toggleProdCb, toggleProdAll } from "../store";
import SectionCard from "./SectionCard.vue";
import FilterPills from "./FilterPills.vue";
import FrappControl from "./FrappControl.vue";
import SkeletonRows from "./SkeletonRows.vue";

const emit = defineEmits([]);

const loading = ref(true);
const raw = ref({ data: [], team_order: [] });

const FILTER_GROUPS = [
	{
		key: "priority",
		label: "Priority",
		options: [
			{ label: "Low", value: "Low" },
			{ label: "Medium", value: "Medium" },
			{ label: "High", value: "High" },
			{ label: "Urgent", value: "Critical" },
		],
	},
	{
		key: "sp",
		label: "S/P",
		options: [
			{ label: "Spot", value: "S" },
			{ label: "Plan", value: "P" },
		],
	},
	{ key: "ro", label: "RO", options: [{ label: "Reopen", value: "RO" }] },
	{ key: "cf", label: "CF", options: [{ label: "Carry Forward", value: "CF" }] },
];

async function load() {
	loading.value = true;
	try {
		const args = prod.date ? { from_date: prod.date, to_date: prod.date } : {};
		raw.value = (await call("get_today_task_data11", args)) || { data: [], team_order: [] };
	} finally {
		loading.value = false;
	}
}

const teams = computed(() => {
	const grouped = {};
	for (const row of raw.value.data || []) {
		if (!row[3]) continue;
		const team = row[12] || "No Team";
		const cb = row[3];
		((grouped[team] = grouped[team] || {})[cb] =
			grouped[team][cb] || []).push(row);
	}
	const order = raw.value.team_order || [];
	const names = order.filter((t) => grouped[t]);
	for (const t of Object.keys(grouped)) if (!names.includes(t)) names.push(t);
	return names.map((team) => {
		const cbs = Object.entries(grouped[team])
			.sort((a, b) => (a[1][0][25] || 0) - (b[1][0][25] || 0))
			.map(([cb, rs]) => {
				const r = rs[0];
				const aph = +r[24] || 0;
				const rt = +r[14] || 0;
				const ut = +r[13] || 0;
				return {
					cb,
					key: cbKey(team, cb),
					img: r[18],
					aph,
					rt,
					ut,
					utp: aph > 0 ? (ut / aph) * 100 : 0,
				};
			});
		const t = {
			name: team,
			key: teamKey(team),
			logo: cbs.length ? grouped[team][cbs[0].cb][0][19] : "",
			cbs,
			aph: cbs.reduce((s, c) => s + c.aph, 0),
			rt: cbs.reduce((s, c) => s + c.rt, 0),
			ut: cbs.reduce((s, c) => s + c.ut, 0),
		};
		t.utp = t.aph > 0 ? (t.ut / t.aph) * 100 : 0;
		return t;
	});
});

function onDate(v) {
	prod.date = sysDate(v);
	load();
}

function onFilters(v) {
	prod.filters = { ...v, priority: v.priority, sp: v.sp, ro: v.ro, cf: v.cf, ts: v.ts };
}

onMounted(load);
</script>

<template>
	<SectionCard title="Production Summary">
		<template #actions>
			<button class="itd-textbtn" @click="toggleProdAll(!prod.allOpen)">
				{{ prod.allOpen ? "− All" : "+ All" }}
			</button>
			<FilterPills :groups="FILTER_GROUPS" v-model="prod.filters" @change="onFilters" />
			<FrappControl
				:df="{ fieldtype: 'Date', fieldname: 'prod_date', placeholder: 'Select date' }"
				:modelValue="prod.date"
				@update:modelValue="onDate"
			/>
		</template>

		<SkeletonRows v-if="loading" :rows="2" :cols="3" />
		<div v-else-if="!teams.length" class="itd-empty">No production data</div>

		<div v-else class="itd-teamgrid">
			<div v-for="t in teams" :key="t.key" class="itd-teamcard">
				<header class="itd-teamcard-head" @click="toggleProdTeam(t.name)">
					<img v-if="t.logo" :src="t.logo" class="itd-teamcard-logo" alt="" />
					<span class="itd-teamcard-name">{{ t.name }}</span>
					<span class="itd-teamcard-metrics">
						APH <b class="c-green">{{ fmt(t.aph) }}</b> · RT
						<b class="c-blue">{{ fmt(t.rt) }}</b> · UT <b class="c-red">{{ fmt(t.ut) }}</b>
						· UT% <b>{{ t.utp.toFixed(1) }}%</b>
					</span>
				</header>
				<div class="itd-teamcard-body">
					<button
						v-for="m in t.cbs"
						:key="m.key"
						class="itd-member"
						:title="m.cb"
						@click="toggleProdCb(m.key)"
					>
						<img v-if="m.img" :src="m.img" class="itd-avatar" alt="" />
						<span v-else class="itd-avatar itd-avatar--fallback">{{ m.cb }}</span>
						<span class="itd-member-name">{{ m.cb }}</span>
						<span class="itd-member-metrics">
							<span><i class="c-green">{{ fmt(m.aph) }}</i> / <i class="c-blue">{{ fmt(m.rt) }}</i></span>
							<span
								><i class="c-red">{{ fmt(m.ut) }}</i> /
								<i>{{ m.utp.toFixed(1) }}%</i></span
							>
						</span>
					</button>
				</div>
			</div>
		</div>
	</SectionCard>
</template>
