<script setup>
import { ref, onMounted } from "vue";
import { call, fmt } from "../api";
import StatGroup from "./StatGroup.vue";

const loading = ref(true);
const cards = ref([]);

const META = {
	total: { title: "Total", color: "#0096A6", icon: "list", subtitle: "Total tasks" },
	open: { title: "Open", color: "#2F8F46", icon: "folder-open", subtitle: "Not yet started" },
	working: { title: "Working", color: "#C29100", icon: "clock", subtitle: "In progress now" },
	pr: { title: "Internal Review", color: "#540D6E", icon: "user-check", subtitle: "Awaiting internal review" },
	cr: { title: "Client Review", color: "#006D77", icon: "users", subtitle: "Awaiting client review" },
};

async function showTasks(key) {
	const rows = (await call("get_tasks_project_wise", { type: key })) || [];
	const esc = frappe.utils.escape_html;
	const trs = rows
		.map(
			(p) => `<tr>
				<td>${esc(p.project || "No Project")}</td>
				<td>${p.task_count}</td>
				<td>${fmt(p.total_hours)}</td>
				<td style="text-align:left">${esc(p.spoc || "No Spoc")}</td>
			</tr>`
		)
		.join("");
	const html = `<div style="max-height:400px;overflow-y:auto;">
		<table class="itd-dialog-table">
			<thead><tr><th>Project</th><th>Tasks</th><th>Hours</th><th>SPOC</th></tr></thead>
			<tbody>${trs || '<tr><td colspan="4" style="text-align:center">No tasks</td></tr>'}</tbody>
		</table></div>`;
	new frappe.ui.Dialog({
		title: META[key]?.title || key,
		fields: [{ fieldname: "html_table", fieldtype: "HTML", options: html }],
	}).show();
}

onMounted(async () => {
	try {
		const tc = (await call("get_task_summary")) || {};
		cards.value = Object.keys(META).map((key) => ({
			key,
			title: META[key].title,
			value: tc[key] || 0,
			hours: fmt(tc[`${key}_total_hours`] || 0),
			color: META[key].color,
			icon: META[key].icon,
			subtitle: META[key].subtitle,
		}));
	} finally {
		loading.value = false;
	}
});
</script>

<template>
	<StatGroup title="Task Count" :cards="cards" :loading="loading" @select="showTasks" />
</template>
