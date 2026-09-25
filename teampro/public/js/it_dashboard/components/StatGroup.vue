<script setup>
import { Icon } from "../icons";

defineProps({
	title: String,
	cards: { type: Array, default: () => [] },
	active: { type: String, default: null },
	loading: Boolean,
});
const emit = defineEmits(["select"]);
</script>

<template>
	<div class="itd-statgroup">
		<div class="itd-statgroup-title">{{ title }}</div>
		<div class="itd-stat-cards">
			<template v-if="loading">
				<div v-for="i in 5" :key="i" class="itd-stat itd-skel-card"></div>
			</template>
			<button
				v-else
				v-for="c in cards"
				:key="c.key"
				class="itd-stat"
				:class="{ 'itd-stat--active': active === c.key, 'itd-stat--clickable': true }"
				:style="{ '--stat-color': c.color }"
				@click="emit('select', c.key)"
			>
				<span class="itd-stat-icon"><Icon :name="c.icon" :size="17" /></span>
				<span class="itd-stat-label">{{ c.title }}</span>
				<span class="itd-stat-value">{{ c.value }}</span>
				<span v-if="c.hours !== undefined" class="itd-stat-hours">{{ c.hours }} hr</span>
				<span v-else class="itd-stat-sub">{{ c.subtitle }}</span>
			</button>
		</div>
	</div>
</template>
