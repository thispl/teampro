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
const completed = ref([]);
const working = ref([]);

async function load() {
	loading.value = true;
	try {
		const r = await call("get_rtat_exception_data", {
			team: props.team || "",
			sprint: props.sprint || "",
		});
		completed.value = r?.completed || [];
		working.value = r?.working || [];
	} finally {
		loading.value = false;
	}
}

function grand(teams) {
	return {
		rt: teams.reduce((s, t) => s + (t.total_rt || 0), 0),
		at: teams.reduce((s, t) => s + (t.total_at || 0), 0),
		n: teams.reduce((s, t) => s + (t.total_count || 0), 0),
	};
}

const grandC = computed(() => grand(completed.value));
const grandW = computed(() => grand(working.value));

watch(() => [props.team, props.sprint], load);
onMounted(load);
</script>

<template>
	<SectionCard title="RT vs AT &gt; 150%" subtitle="Exceptions">
		<SkeletonRows v-if="loading" :rows="6" :cols="4" />
		<div v-else-if="!completed.length && !working.length" class="itd-empty">
			No exceptions found
		</div>

		<div v-else class="itd-cols2">
			<div v-for="(sec, si) in [
				{ label: 'Completed Tasks', teams: completed, g: grandC },
				{ label: 'Working Tasks', teams: working, g: grandW },
			]" :key="si">
				<h4 class="itd-subhead">{{ sec.label }}</h4>
				<div v-if="!sec.teams.length" class="itd-empty">No exceptions found</div>
				<div v-else class="itd-table-wrap">
					<table class="itd-table">
						<thead>
							<tr>
								<th class="itd-left">Team / CB</th>
								<th class="itd-num">Sum of RT</th>
								<th class="itd-num">Sum of AT Period</th>
								<th class="itd-num">Count of Task</th>
							</tr>
						</thead>
						<tbody v-for="t in sec.teams" :key="t.team">
							<tr class="itd-row-group">
								<td class="itd-left"><b>{{ t.team }}</b></td>
								<td class="itd-num"><b>{{ fmt(t.total_rt) }}</b></td>
								<td class="itd-num"><b>{{ fmt(t.total_at) }}</b></td>
								<td class="itd-num"><b>{{ t.total_count }}</b></td>
							</tr>
							<tr v-for="c in t.cbs || []" :key="t.team + c.cb">
								<td class="itd-left itd-indent">{{ c.cb }}</td>
								<td class="itd-num">{{ fmt(c.sum_rt) }}</td>
								<td class="itd-num">{{ fmt(c.sum_at) }}</td>
								<td class="itd-num">{{ c.task_count }}</td>
							</tr>
						</tbody>
						<tfoot>
							<tr>
								<td class="itd-left">Grand Total</td>
								<td class="itd-num">{{ fmt(sec.g.rt) }}</td>
								<td class="itd-num">{{ fmt(sec.g.at) }}</td>
								<td class="itd-num">{{ sec.g.n }}</td>
							</tr>
						</tfoot>
					</table>
				</div>
			</div>
		</div>
	</SectionCard>
</template>
