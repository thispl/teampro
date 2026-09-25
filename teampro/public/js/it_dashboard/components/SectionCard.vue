<script setup>
defineProps({
	title: String,
	subtitle: String,
	pad: { type: Boolean, default: false },
});
</script>

<template>
	<section class="itd-card">
		<header class="itd-card-head">
			<h3 class="itd-card-title">
				{{ title }}
				<span v-if="subtitle" class="itd-card-sub">{{ subtitle }}</span>
			</h3>
			<div class="itd-card-actions">
				<slot name="actions" />
			</div>
		</header>
		<div class="itd-card-body" :class="{ 'itd-card-body--pad': pad }">
			<slot />
		</div>
	</section>
</template>
