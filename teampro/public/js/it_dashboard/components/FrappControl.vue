<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from "vue";

const props = defineProps({
	df: { type: Object, required: true },
	modelValue: { type: [String, null], default: "" },
});
const emit = defineEmits(["update:modelValue", "change"]);
const el = ref(null);
let ctrl = null;

onMounted(() => {
	ctrl = frappe.ui.form.make_control({
		parent: el.value,
		df: {
			...props.df,
			onchange: () => {
				const v = ctrl.get_value();
				emit("update:modelValue", v);
				emit("change", v);
			},
		},
		render_input: true,
	});
	if (props.modelValue) ctrl.set_value(props.modelValue);
});

watch(
	() => props.modelValue,
	(v) => {
		if (ctrl && ctrl.get_value() !== v) ctrl.set_value(v || "");
	}
);

function set_value(v) {
	ctrl && ctrl.set_value(v);
}
function get_value() {
	return ctrl ? ctrl.get_value() : "";
}

defineExpose({ set_value, get_value });

onBeforeUnmount(() => {
	el.value && (el.value.innerHTML = "");
});
</script>

<template>
	<div ref="el" class="itd-ctrl"></div>
</template>
