<script setup>
import { ref, onMounted } from "vue";
import { call } from "../api";
import StatGroup from "./StatGroup.vue";

const emit = defineEmits(["select"]);
const loading = ref(true);
const cards = ref([]);
const active = ref("Total");

const PALETTE = [
	"#0096A6", "#2F8F46", "#C29100", "#540D6E", "#006D77",
	"#4169e1", "#8B0000", "#f9844a", "#bc5090", "#003f5c",
];
const ICONS = {
	Total: "bar-chart",
	External: "globe",
	AMC: "wrench",
	Enquiry: "search",
	Internal: "building",
};

function select(key) {
	active.value = key;
	emit("select", key === "Total" ? null : key);
}

onMounted(async () => {
	try {
		const m = (await call("get_project_counts")) || {};
		const list = [
			{ key: "Total", title: "Total", value: m.total || 0, color: PALETTE[0], icon: "bar-chart", subtitle: "All Projects" },
		];
		(m.projects || []).forEach((p, i) => {
			if (p.project_type === "Products") return;
			list.push({
				key: p.project_type,
				title: p.project_type,
				value: p.count,
				color: PALETTE[(i + 1) % PALETTE.length],
				icon: ICONS[p.project_type] || "folder",
				subtitle: `${p.project_type} type projects`,
			});
		});
		cards.value = list;
	} finally {
		loading.value = false;
	}
});
</script>

<template>
	<StatGroup title="Project Count" :cards="cards" :active="active" :loading="loading" @select="select" />
</template>
