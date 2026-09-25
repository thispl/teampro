<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import ProjectCounts from "./components/ProjectCounts.vue";
import TaskCounts from "./components/TaskCounts.vue";
import PsrTable from "./components/PsrTable.vue";
import ProductionSummary from "./components/ProductionSummary.vue";
import ProductionTable from "./components/ProductionTable.vue";
import NonAllocated from "./components/NonAllocated.vue";
import DsrDpr from "./components/DsrDpr.vue";
import RetroSummary from "./components/RetroSummary.vue";
import SprintTab from "./components/SprintTab.vue";
import LiveBoard from "./components/LiveBoard.vue";
import ProjectWip from "./components/ProjectWip.vue";

const tab = ref("dashboard");
const sprintLoaded = ref(false);
const liveLoaded = ref(false);
const wipLoaded = ref(false);
const now = ref("");
const psr = ref(null);
let clockTimer = null;

function onProjectSelect(type) {
	psr.value?.setTypeFilter(type);
}

function pickTab(t) {
	tab.value = t;
	if (t === "sprint") sprintLoaded.value = true;
	if (t === "live") liveLoaded.value = true;
	if (t === "wip") wipLoaded.value = true;
}

function tick() {
	now.value = frappe.datetime
		? frappe.datetime.str_to_user(frappe.datetime.now_datetime())
		: new Date().toLocaleString();
}

onMounted(() => {
	tick();
	clockTimer = setInterval(tick, 1000);
});
onBeforeUnmount(() => clearInterval(clockTimer));
</script>

<template>
	<div class="itd">
		<header class="itd-header">
			<div class="itd-tabs">
				<button
					class="itd-tab"
					:class="{ 'itd-tab--on': tab === 'dashboard' }"
					@click="pickTab('dashboard')"
				>
					Dashboard
				</button>
				<button
					class="itd-tab"
					:class="{ 'itd-tab--on': tab === 'live' }"
					@click="pickTab('live')"
				>
					Live
				</button>
				<button
					class="itd-tab"
					:class="{ 'itd-tab--on': tab === 'sprint' }"
					@click="pickTab('sprint')"
				>
					Sprint
				</button>
				<button
					class="itd-tab"
					:class="{ 'itd-tab--on': tab === 'wip' }"
					@click="pickTab('wip')"
				>
					Project WIP
				</button>
			</div>
			<div class="itd-clock">{{ now }}</div>
		</header>

		<div v-show="tab === 'dashboard'" class="itd-page">
			<ProjectCounts @select="onProjectSelect" />
			<TaskCounts />
			<PsrTable ref="psr" />
			<ProductionSummary />
			<ProductionTable />
			<NonAllocated />
			<DsrDpr />
			<RetroSummary />
		</div>

		<div v-if="liveLoaded" v-show="tab === 'live'" class="itd-page">
			<LiveBoard />
		</div>

		<div v-if="sprintLoaded" v-show="tab === 'sprint'" class="itd-page">
			<SprintTab />
		</div>

		<div v-if="wipLoaded" v-show="tab === 'wip'" class="itd-page">
			<ProjectWip />
		</div>
	</div>
</template>
