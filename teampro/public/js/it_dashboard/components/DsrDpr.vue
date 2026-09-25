<script setup>
import { ref, computed } from "vue";
import { today, sysDate, downloadUrl } from "../api";
import { Icon } from "../icons";
import FrappControl from "./FrappControl.vue";
import HtmlSection from "./HtmlSection.vue";

const date = ref(today());
const args = computed(() => ({ date: sysDate(date.value) || today() }));

function download() {
	const d = sysDate(date.value) || frappe.datetime.add_days(frappe.datetime.get_today(), -1);
	const NS = "/api/method/teampro.teampro.page.new_it_dashboard.new_it.";
	downloadUrl(`${NS}download_dsr_excel?date=${d}`);
	setTimeout(() => downloadUrl(`${NS}download_dpr_excel?date=${d}`), 1500);
}
</script>

<template>
	<HtmlSection title="DSR Summary" method="dsr_table" :args="args" max-height="520px">
		<template #actions>
			<FrappControl
				:df="{ fieldtype: 'Date', fieldname: 'dsr_date', placeholder: 'Select Date' }"
				v-model="date"
			/>
			<button class="itd-iconbtn" title="Download DSR + DPR Excel" @click="download">
				<Icon name="download" :size="15" />
			</button>
		</template>
	</HtmlSection>

	<HtmlSection title="DPR Summary" method="dpr_table" :args="args" max-height="520px" />

	<HtmlSection title="AMC Project SLA" method="get_amc_project_sla_table" max-height="520px">
		<template #actions>
			<button
				class="itd-iconbtn"
				title="Download Excel"
				@click="downloadUrl('/api/method/teampro.teampro.page.new_it_dashboard.new_it.download_amc_project_sla_excel')"
			>
				<Icon name="download" :size="15" />
			</button>
		</template>
	</HtmlSection>
</template>
