import { createApp } from "vue";
import ItDashboard from "./ItDashboard.vue";

let app = null;

frappe.it_dashboard = {
	mount(wrapper) {
		this.unmount();
		const el = document.createElement("div");
		el.className = "itd-host";
		wrapper.appendChild(el);
		app = createApp(ItDashboard);
		SetVueGlobals(app);
		app.mount(el);
	},
	unmount() {
		if (app) {
			app.unmount();
			app = null;
		}
	},
};
