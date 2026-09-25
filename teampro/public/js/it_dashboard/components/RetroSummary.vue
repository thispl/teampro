<script setup>
import { ref, onMounted } from "vue";
import { call, cleanHtml } from "../api";
import SectionCard from "./SectionCard.vue";
import FrappControl from "./FrappControl.vue";
import SkeletonRows from "./SkeletonRows.vue";

const loading = ref(true);
const html = ref("");
const sections = ref([]);
const sprint = ref("");
const team = ref("Summary");
const mode = ref("hrs");
const devTeams = ref([]);
const sprintCtrl = ref(null);

async function load() {
	loading.value = true;
	html.value = "";
	sections.value = [];
	try {
		if (team.value === "Summary") {
			html.value = cleanHtml(await call("summary_total_hrs_cols", { name: sprint.value }));
		} else {
			const d = await call("get_retro_summary_html", {
				name: sprint.value,
				dev_team: team.value === "ALL" ? "" : team.value,
			});
			sections.value = (d || []).map((s) => ({ ...s, html: cleanHtml(s.html) }));
		}
	} finally {
		loading.value = false;
	}
}

function pickTeam(t) {
	team.value = t;
	load();
}

function onSprint(v) {
	sprint.value = v;
	load();
}

onMounted(async () => {
	const def = await call("update_sprint_filter");
	if (def && sprintCtrl.value) sprintCtrl.value.set_value(def);
	devTeams.value = (await frappe.db.get_list("Dev Team", {
		filters: { name: ["!=", "Others"] },
		fields: ["name"],
		order_by: "name",
	})) || [];
	await load();
});
</script>

<template>
	<SectionCard title="Sprint Retrospective" class="itd-retro">
		<template #actions>
			<FrappControl
				ref="sprintCtrl"
				:df="{ fieldtype: 'Link', fieldname: 'retro_sprint', options: 'Task Sprint', placeholder: 'Sprint' }"
				@change="onSprint"
			/>
			<div class="itd-pills itd-pills--scroll">
				<button
					v-for="t in ['Summary', 'ALL', ...devTeams.map((d) => d.name)]"
					:key="t"
					class="itd-pill"
					:class="{ 'itd-pill--on': team === t }"
					@click="pickTeam(t)"
				>
					{{ t }}
				</button>
			</div>
			<div class="itd-seg">
				<button
					class="itd-seg-btn"
					:class="{ 'itd-seg-btn--on': mode === 'hrs' }"
					@click="mode = 'hrs'"
				>
					Hrs
				</button>
				<button
					class="itd-seg-btn"
					:class="{ 'itd-seg-btn--on': mode === 'count' }"
					@click="mode = 'count'"
				>
					Count
				</button>
			</div>
		</template>

		<SkeletonRows v-if="loading" :rows="8" :cols="10" />

		<template v-else>
			<div
				v-if="html"
				class="itd-html itd-retro-html"
				:class="mode === 'hrs' ? 'itd-html--hrs' : 'itd-html--count'"
				v-html="html"
			></div>
			<template v-else-if="sections.length">
				<div
					v-for="s in sections"
					:key="s.team"
					class="itd-retro-team"
				>
					<h4 class="itd-retro-teamname">{{ s.team }}</h4>
					<div
						class="itd-html itd-retro-html"
						:class="mode === 'hrs' ? 'itd-html--hrs' : 'itd-html--count'"
						v-html="s.html"
					></div>
				</div>
			</template>
			<div v-else class="itd-empty">
				No data found{{ team !== 'Summary' ? ` for ${team}` : "" }} in this sprint
			</div>
		</template>
	</SectionCard>
</template>
