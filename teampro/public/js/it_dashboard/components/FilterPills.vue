<script setup>
// groups: [{key, label, options: [{label, value}]}]
const props = defineProps({
	groups: { type: Array, default: () => [] },
	modelValue: { type: Object, default: () => ({}) },
});
const emit = defineEmits(["update:modelValue", "change"]);

function toggle(groupKey, value) {
	const next = { ...props.modelValue };
	next[groupKey] = next[groupKey] === value ? null : value;
	emit("update:modelValue", next);
	emit("change", next);
}
</script>

<template>
	<div class="itd-pills">
		<div v-for="g in groups" :key="g.key" class="itd-pill-group">
			<span class="itd-pill-label">{{ g.label }}</span>
			<button
				v-for="o in g.options"
				:key="o.value"
				class="itd-pill"
				:class="{ 'itd-pill--on': modelValue[g.key] === o.value }"
				@click="toggle(g.key, o.value)"
			>
				{{ o.label }}
			</button>
		</div>
	</div>
</template>
