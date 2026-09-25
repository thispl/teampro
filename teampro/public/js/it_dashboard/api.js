const NS = "teampro.teampro.page.new_it_dashboard.new_it.";

export function call(method, args = {}) {
	return frappe.call({ method: NS + method, args }).then((r) => r.message);
}

export function callRaw(method, args = {}) {
	return frappe.call({ method, args }).then((r) => r.message);
}

export function today() {
	return frappe.datetime.get_today();
}

// Normalize a date control value (user format or ISO) to YYYY-MM-DD
export function sysDate(v) {
	if (!v) return null;
	if (/^\d{4}-\d{2}-\d{2}/.test(v)) return v.slice(0, 10);
	return frappe.datetime.user_to_str(v) || v;
}

export function fmt(n, digits = 2) {
	const v = parseFloat(n);
	if (isNaN(v)) return digits === 0 ? "0" : (0).toFixed(digits);
	return v.toFixed(digits);
}

export function fmtInt(n) {
	const v = parseFloat(n);
	return isNaN(v) ? "0" : String(Math.round(v));
}

// "12.34/5" -> { hr: 12.34, n: 5 }
export function splitPair(s) {
	const [a, b] = String(s || "0/0").split("/").map(Number);
	return { hr: isNaN(a) ? 0 : a, n: isNaN(b) ? 0 : b };
}

// Round long float literals inside server-rendered HTML (e.g. 64.5099999999 -> 64.51)
export function cleanHtml(html) {
	return String(html || "").replace(/(\d+\.\d{3,})/g, (m) => (+m).toFixed(2));
}

let xlsxPromise = null;
export function ensureXLSX() {
	if (window.XLSX) return Promise.resolve();
	if (!xlsxPromise) {
		xlsxPromise = frappe.require([
			"https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js",
		]);
	}
	return xlsxPromise;
}

export function downloadRowsAsXlsx(filename, sheetName, rows) {
	return ensureXLSX().then(() => {
		const ws = XLSX.utils.aoa_to_sheet(rows);
		const wb = XLSX.utils.book_new();
		XLSX.utils.book_append_sheet(wb, ws, sheetName);
		XLSX.writeFile(wb, filename);
	});
}

export function downloadUrl(url) {
	const a = document.createElement("a");
	a.href = url;
	a.style.display = "none";
	document.body.appendChild(a);
	a.click();
	setTimeout(() => a.parentNode && a.parentNode.removeChild(a), 5000);
}
