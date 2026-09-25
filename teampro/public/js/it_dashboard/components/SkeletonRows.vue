<script setup>
defineProps({
	rows: { type: Number, default: 6 },
	cols: { type: Number, default: 6 },
});
</script>

<template>
	<div class="itd-skel-table">
		<div class="itd-skel-head"></div>
		<div v-for="i in rows" :key="i" class="itd-skel-row">
			<div v-for="j in cols" :key="j" class="itd-skel-cell"></div>
		</div>
	</div>
</template>
