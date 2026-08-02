import { t as cn } from "./utils-C_uf36nf.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/Primitives-DCYrco_Z.js
var import_jsx_runtime = require_jsx_runtime();
function Panel({ title, subtitle, action, className, children }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
		className: cn("glass rounded-2xl p-6", className),
		children: [(title || action) && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
			className: "mb-5 flex items-start justify-between gap-4",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [title && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
				className: "text-[15px] font-semibold tracking-tight",
				children: title
			}), subtitle && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "text-quiet mt-1 text-[12.5px]",
				children: subtitle
			})] }), action]
		}), children]
	});
}
function StatCard({ label, value, hint, accent }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "glass rounded-2xl p-5",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: label
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: cn("display mt-3 text-3xl", accent ? "text-[color:var(--crimson-soft)]" : "text-foreground"),
				children: value
			}),
			hint && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "text-quiet mt-2 text-[12px]",
				children: hint
			})
		]
	});
}
function Meter({ label, value }) {
	const pct = Math.max(0, Math.min(100, value));
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "mb-2 flex items-baseline justify-between",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
			className: "text-[12.5px] capitalize",
			children: label.replace(/_/g, " ")
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
			className: "text-quiet font-mono text-[12px]",
			children: pct.toFixed(0)
		})]
	}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "h-1.5 overflow-hidden rounded-full bg-[color:var(--surface-elevated)]",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "h-full rounded-full bg-primary transition-[width] duration-700",
			style: { width: `${pct}%` }
		})
	})] });
}
function EmptyState({ message }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "text-quiet rounded-xl border border-dashed border-[color:var(--hairline)] px-5 py-10 text-center text-[13px]",
		children: message
	});
}
function ErrorState({ error }) {
	const message = error instanceof Error ? error.message : "Unable to reach the Orbit API.";
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "rounded-xl border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-5 py-6 text-[13px]",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
			className: "font-semibold text-[color:var(--crimson-soft)]",
			children: "Request failed"
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
			className: "text-quiet mt-1",
			children: message
		})]
	});
}
function money(n, currency = "USD") {
	const v = typeof n === "string" ? Number(n) : n ?? 0;
	return new Intl.NumberFormat("en-US", {
		style: "currency",
		currency,
		maximumFractionDigits: 0
	}).format(Number.isFinite(v) ? v : 0);
}
function fileSize(bytes) {
	if (bytes === null || bytes === void 0 || !Number.isFinite(bytes)) return "—";
	if (bytes < 1024) return `${bytes} B`;
	const units = [
		"KB",
		"MB",
		"GB",
		"TB"
	];
	let value = bytes / 1024;
	let unit = 0;
	while (value >= 1024 && unit < units.length - 1) {
		value /= 1024;
		unit += 1;
	}
	return `${value.toFixed(1)} ${units[unit]}`;
}
function pct(n, digits = 0) {
	const v = typeof n === "string" ? Number(n) : n;
	if (v === null || v === void 0 || !Number.isFinite(v)) return "—";
	return `${v.toFixed(digits)}%`;
}
var POSITIVE = [
	"approved",
	"completed",
	"won",
	"active",
	"pass",
	"resolved",
	"delivered"
];
var NEGATIVE = [
	"rejected",
	"expired",
	"lost",
	"fail",
	"failed",
	"at_risk",
	"high",
	"critical",
	"cancelled"
];
var PENDING = [
	"pending",
	"in_progress",
	"in progress",
	"draft",
	"planning",
	"review"
];
function StatusBadge({ status }) {
	const s = (status ?? "unknown").toLowerCase().replace(/-/g, "_");
	const toneClass = {
		positive: "bg-[color-mix(in_oklab,oklch(0.72_0.19_150)_18%,transparent)] text-[oklch(0.78_0.17_150)]",
		negative: "bg-[color-mix(in_oklab,var(--crimson)_18%,transparent)] text-[color:var(--crimson-soft)]",
		pending: "bg-[color-mix(in_oklab,oklch(0.8_0.15_85)_18%,transparent)] text-[oklch(0.82_0.14_85)]",
		neutral: "bg-[color:var(--surface-elevated)] text-quiet"
	}[POSITIVE.some((k) => s.includes(k)) ? "positive" : NEGATIVE.some((k) => s.includes(k)) ? "negative" : PENDING.some((k) => s.includes(k)) ? "pending" : "neutral"];
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
		className: cn("inline-flex items-center rounded-full px-2.5 py-1 text-[11px] font-medium capitalize", toneClass),
		children: (status ?? "unknown").replace(/_/g, " ")
	});
}
//#endregion
export { StatCard as a, money as c, Panel as i, pct as l, ErrorState as n, StatusBadge as o, Meter as r, fileSize as s, EmptyState as t };
