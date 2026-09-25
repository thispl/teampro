// Lightweight inline SVG icon helper (stroke icons, lucide-style).
const PATHS = {
	folder: '<path d="M4 6a2 2 0 0 1 2-2h3l2 2h7a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/>',
	globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 4 5.6 4 9s-1.5 6.4-4 9c-2.5-2.6-4-5.6-4-9s1.5-6.4 4-9z"/>',
	wrench: '<path d="M14.7 6.3a4.5 4.5 0 0 0-6 6L3 18l3 3 5.7-5.7a4.5 4.5 0 0 0 6-6L14 13l-3-3z"/>',
	search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
	building: '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 8h2M13 8h2M9 12h2M13 12h2M9 16h2M13 16h2"/>',
	list: '<path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
	"folder-open": '<path d="M4 6a2 2 0 0 1 2-2h3l2 2h7a2 2 0 0 1 2 2v2"/><path d="M4 6v12a2 2 0 0 0 2 2h13l3-9a2 2 0 0 0-2-2H6.5a2 2 0 0 0-2 1.7z"/>',
	refresh: '<path d="M21 12a9 9 0 1 1-2.64-6.36M21 3v6h-6"/>',
	"user-check": '<path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/><path d="M2 21a7 7 0 0 1 14 0M16 11l2 2 4-4"/>',
	users: '<path d="M8 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/><path d="M1 21a7 7 0 0 1 14 0"/><path d="M17 8a3 3 0 1 1 2-5.2M23 21a7 7 0 0 0-5-6.7"/>',
	download: '<path d="M12 3v12m0 0 4-4m-4 4-4-4"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>',
	calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/>',
	clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
	check: '<path d="m4 12.5 5 5L20 6.5"/>',
	eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
	"chevron-down": '<path d="m6 9 6 6 6-6"/>',
	"chevron-right": '<path d="m9 6 6 6-6 6"/>',
	"bar-chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
	layers: '<path d="m12 2 9 5-9 5-9-5z"/><path d="m3 12 9 5 9-5M3 17l9 5 9-5"/>',
	alert: '<path d="M12 3 2 21h20z"/><path d="M12 10v5m0 3h.01"/>',
	filter: '<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',
	printer: '<path d="M6 9V3h12v6"/><rect x="4" y="9" width="16" height="8" rx="1"/><path d="M6 15h12v6H6z"/>',
};

export function icon(name, size = 16) {
	return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${PATHS[name] || PATHS.folder}</svg>`;
}

export const Icon = {
	props: { name: String, size: { type: Number, default: 16 } },
	computed: {
		html() {
			return icon(this.name, this.size);
		},
	},
	template: `<span class="itd-icon" v-html="html"></span>`,
};
