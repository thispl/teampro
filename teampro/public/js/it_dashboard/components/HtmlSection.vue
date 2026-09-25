<script setup>
import { ref, watch, onMounted } from "vue";
import { call, cleanHtml } from "../api";
import SectionCard from "./SectionCard.vue";
import SkeletonRows from "./SkeletonRows.vue";

const props = defineProps({
	title: String,
	method: { type: String, required: true },
	args: { type: Object, default: () => ({}) },
	// reloadKey: change to force refetch
	reloadKey: { type: [String, Number], default: 0 },
	maxHeight: { type: String, default: "640px" },
});
const emit = defineEmits(["loaded"]);
const html = ref("");
const loading = ref(true);

async function load() {
	loading.value = true;
	try {
		html.value = cleanHtml(await call(props.method, props.args));
	} finally {
		loading.value = false;
	}
	emit("loaded");
}

watch(() => [props.args, props.reloadKey], load, { deep: true });
onMounted(load);
</script>

<template>
	<SectionCard :title="title">
		<template #actions><slot name="actions" /></template>
		<SkeletonRows v-if="loading" :rows="8" :cols="8" />
		<div v-else-if="!html" class="itd-empty">No data found</div>
		<div
			v-else
			class="itd-html"
			:style="{ '--itd-html-maxh': maxHeight }"
			v-html="html"
		></div>
	</SectionCard>
</template>
