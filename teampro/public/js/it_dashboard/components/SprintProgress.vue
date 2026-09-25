<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { call, fmt } from "../api";
import SectionCard from "./SectionCard.vue";
import SkeletonRows from "./SkeletonRows.vue";

const props = defineProps({
	team: { type: String, default: "" },
	sprint: { type: String, default: "" },
});

const loading = ref(true);
const message = ref(null);

async function load() {
	loading.value = true;
	try {
		message.value = await call("get_sprint_chart_data", {
			team: props.team || "",
			sprint: props.sprint || "",
		});
	} finally {
		loading.value = false;
	}
}

const blocks = computed(() => {
	const m = message.value;
	if (!m?.labels?.length) return [];
	const order = [];
	const map = {};
	m.labels.forEach((sc, i) => {
		const team = m.teams?.[i] || "Unassigned";
		if (!map[team]) {
			map[team] = { team, sprintId: m.sprint_ids?.[i] || "", cbs: [] };
			order.push(team);
		}
		const aph = parseFloat(m.available_hours?.[i] || 0);
		const e = parseFloat(m.expected_hours?.[i] || 0);
		const rv = parseFloat(m.sprint_avl_time?.[i] || 0);
		map[team].cbs.push({
			sc,
			aph,
			e,
			rv,
			rtPct: aph ? (rv / aph) * 100 : 0,
			lsPct: aph ? (e / aph) * 100 : 0,
			balance: aph - rv,
		});
	});
	return order.map((t) => map[t]);
});

function dotColor(c) {
	const ratio = c.aph ? c.rv / c.aph : 0;
	return ratio >= 0.9 ? "#4caf50" : ratio >= 0.5 ? "#ff9800" : "#f44336";
}

watch(() => [props.team, props.sprint], load);
onMounted(load);
</script>

<template>
	<SectionCard title="Sprint Progress">
		<SkeletonRows v-if="loading" :rows="4" :cols="4" />
		<div v-else-if="!blocks.length" class="itd-empty itd-empty--warn">
			No Sprint Data Found for Today
		</div>

		<div v-else class="itd-sprintprog">
			<div class="itd-legend">
				<span class="itd-legend-item">
					<i class="itd-legend-dot itd-legend-dot--track"></i> APH (full track)
				</span>
				<span class="itd-legend-item">
					<i class="itd-legend-dot itd-legend-dot--fill"></i> RT (filled portion)
				</span>
				<span class="itd-legend-item">
					<i class="itd-legend-dot itd-legend-dot--marker"></i> Lifespan (marker)
				</span>
			</div>

			<div v-for="b in blocks" :key="b.team" class="itd-sp-team">
				<div class="itd-sp-teamhead">
					<h4>{{ b.team }}</h4>
					<span class="itd-tag">{{ b.sprintId || "—" }}</span>
				</div>
				<div class="itd-sp-grid">
					<div v-for="c in b.cbs" :key="c.sc" class="itd-sp-card">
						<div class="itd-sp-cardhead">
							<span class="itd-sp-cb">{{ c.sc }}</span>
							<span class="itd-sp-dot" :style="{ background: dotColor(c) }"></span>
						</div>
						<div class="itd-sp-bar">
							<span class="itd-sp-aph">{{ fmt(c.aph, 1) }}<em>APH</em></span>
							<div class="itd-sp-track">
								<div
									class="itd-sp-fill"
									:style="{ width: Math.min(Math.max(c.rtPct, 0), 100) + '%' }"
								>
									<span v-if="c.rtPct >= 15" class="itd-sp-fillpct">RT {{ c.rtPct.toFixed(0) }}%</span>
								</div>
								<div
									class="itd-sp-marker"
									:style="{ left: Math.min(Math.max(c.lsPct, 0), 100) + '%' }"
								>
									<div class="itd-sp-markerline"></div>
									<div class="itd-sp-markerflag">L {{ fmt(c.e, 1) }}h</div>
								</div>
							</div>
							<span class="itd-sp-rt">{{ fmt(c.rv, 1) }}<em>RT</em></span>
						</div>
						<div class="itd-sp-stats">
							<span>RT / APH <b>{{ c.rtPct.toFixed(1) }}%</b></span>
							<span>Lifespan <b>{{ c.lsPct.toFixed(1) }}%</b></span>
							<span>Balance <b>{{ fmt(c.balance, 1) }}h</b></span>
						</div>
					</div>
				</div>
			</div>
		</div>
	</SectionCard>
</template>
