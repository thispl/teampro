import { reactive } from "vue";

// Shared state between Production Summary (team cards) and Production Table.
export const prod = reactive({
	date: null, // YYYY-MM-DD
	openTeams: new Set(),
	openCbs: new Set(),
	allTeams: [],
	allCbs: [],
	allOpen: true,
	filters: { priority: null, sp: null, ro: null, cf: null, ts: null },
});

export function teamKey(team) {
	return `t-${String(team || "").replace(/\s+/g, "_")}`;
}

export function cbKey(team, cb) {
	return `cb-${String(team || "").replace(/\s+/g, "_")}-${String(cb || "").replace(/\s+/g, "_")}`;
}

function syncAllOpen() {
	prod.allOpen =
		prod.allTeams.length > 0 &&
		prod.allTeams.every((t) => prod.openTeams.has(t)) &&
		prod.allCbs.every((c) => prod.openCbs.has(c));
}

export function setProdData(teams, cbs) {
	prod.allTeams = teams;
	prod.allCbs = cbs;
	prod.openTeams = new Set(teams);
	prod.openCbs = new Set(cbs);
	prod.allOpen = true;
}

export function toggleProdAll(open) {
	if (open) {
		prod.openTeams = new Set(prod.allTeams);
		prod.openCbs = new Set(prod.allCbs);
	} else {
		prod.openTeams.clear();
		prod.openCbs.clear();
	}
	prod.allOpen = open;
}

export function toggleProdTeam(team) {
	if (prod.openTeams.has(team)) prod.openTeams.delete(team);
	else prod.openTeams.add(team);
	syncAllOpen();
}

export function toggleProdCb(key) {
	if (prod.openCbs.has(key)) prod.openCbs.delete(key);
	else prod.openCbs.add(key);
	syncAllOpen();
}
