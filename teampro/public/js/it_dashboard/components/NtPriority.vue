<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { call, fmt } from "../api";
import SectionCard from "./SectionCard.vue";
import SkeletonRows from "./SkeletonRows.vue";

const props = defineProps({
	team: { type: String, default: "" },
	sprint: { type: String, default: "" },
	anySprint: { type: Boolean, default: false },
	title: { type: String, default: "NT High / Urgent" },
});

const loading = ref(true);
const teams = ref([]);

async function load() {
	loading.value = true;
	try {
		const r = await call("get_nt_priority_tasks", {
			team: props.team || "",
			sprint: props.sprint || "",
			any_sprint: props.anySprint ? 1 : 0,
		});
		teams.value = r?.teams || [];
	} finally {
		loading.value = false;
	}
}

const grand = computed(() => ({
	high_rt: teams.value.reduce((s, t) => s + (t.high_rt || 0), 0),
	urgent_rt: teams.value.reduce((s, t) => s + (t.urgent_rt || 0), 0),
	high_count: teams.value.reduce((s, t) => s + (t.high_count || 0), 0),
	urgent_count: teams.value.reduce((s, t) => s + (t.urgent_count || 0), 0),
}));

watch(() => [props.team, props.sprint], load);
onMounted(load);
</script>

<template>
	<SectionCard :title="title" subtitle="NT High / Urgent">
		<SkeletonRows v-if="loading" :rows="6" :cols="5" />
		<div v-else-if="!teams.length" class="itd-empty">
			No NT tasks with High/Urgent priority found
		</div>

		<div v-else class="itd-table-wrap">
			<table class="itd-table">
				<thead>
					<tr>
						<th rowspan="2" class="itd-left">Team / CB</th>
						<th colspan="2" class="itd-thgrp itd-thgrp--a">Sum of RT</th>
						<th colspan="2" class="itd-thgrp itd-thgrp--c">Count of Task</th>
					</tr>
					<tr>
						<th class="itd-num">High</th>
						<th class="itd-num">Urgent</th>
						<th class="itd-num">High</th>
						<th class="itd-num">Urgent</th>
					</tr>
				</thead>
				<tbody v-for="t in teams" :key="t.team">
					<tr class="itd-row-group">
						<td class="itd-left"><b>{{ t.team }}</b></td>
						<td class="itd-num"><b>{{ fmt(t.high_rt) }}</b></td>
						<td class="itd-num"><b>{{ fmt(t.urgent_rt) }}</b></td>
						<td class="itd-num"><b>{{ t.high_count }}</b></td>
						<td class="itd-num"><b>{{ t.urgent_count }}</b></td>
					</tr>
					<tr v-for="c in t.cbs || []" :key="t.team + c.cb">
						<td class="itd-left itd-indent">{{ c.cb }}</td>
						<td class="itd-num">{{ fmt(c.high_rt) }}</td>
						<td class="itd-num">{{ fmt(c.urgent_rt) }}</td>
						<td class="itd-num">{{ c.high_count }}</td>
						<td class="itd-num">{{ c.urgent_count }}</td>
					</tr>
				</tbody>
				<tfoot>
					<tr>
						<td class="itd-left">Grand Total</td>
						<td class="itd-num">{{ fmt(grand.high_rt) }}</td>
						<td class="itd-num">{{ fmt(grand.urgent_rt) }}</td>
						<td class="itd-num">{{ grand.high_count }}</td>
						<td class="itd-num">{{ grand.urgent_count }}</td>
					</tr>
				</tfoot>
			</table>
		</div>
	</SectionCard>
</template>
