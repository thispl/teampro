<script setup>
import { ref } from "vue";
import FrappControl from "./FrappControl.vue";
import SprintProgress from "./SprintProgress.vue";
import SprintOverall from "./SprintOverall.vue";
import RtAt from "./RtAt.vue";
import NtPriority from "./NtPriority.vue";

const team = ref("");
const sprint = ref("");
</script>

<template>
	<div class="itd-sprinttab">
		<div class="itd-toolbar">
			<FrappControl
				:df="{ fieldtype: 'Link', fieldname: 'sprint_team', options: 'Dev Team', placeholder: 'Select Team' }"
				v-model="team"
			/>
			<FrappControl
				:df="{ fieldtype: 'Link', fieldname: 'sprint_sprint', options: 'Task Sprint', placeholder: 'Select Sprint' }"
				v-model="sprint"
			/>
		</div>

		<SprintProgress :team="team" :sprint="sprint" />
		<SprintOverall :team="team" :sprint="sprint" />
		<RtAt :team="team" :sprint="sprint" />
		<div class="itd-cols2">
			<NtPriority :team="team" :sprint="sprint" title="NT High / Urgent — Any Sprint" :any-sprint="true" />
			<NtPriority :team="team" :sprint="sprint" title="NT High / Urgent — Current Sprint" :any-sprint="false" />
		</div>
	</div>
</template>
