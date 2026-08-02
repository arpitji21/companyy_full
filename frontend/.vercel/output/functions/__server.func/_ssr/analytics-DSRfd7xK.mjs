import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { a as StatCard, c as money, i as Panel, n as ErrorState, t as EmptyState } from "./Primitives-DCYrco_Z.mjs";
import { n as useQuery } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/analytics-DSRfd7xK.js
var import_jsx_runtime = require_jsx_runtime();
function AnalyticsPage() {
	const summary = useQuery({
		queryKey: ["analytics-summary"],
		queryFn: orbit.analyticsSummary,
		retry: false
	});
	const reports = useQuery({
		queryKey: ["analytics-reports"],
		queryFn: () => orbit.analyticsReports(1, 25),
		retry: false
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "eyebrow",
					children: "Analytics"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
					className: "display mt-2 text-3xl",
					children: "Cross-department reporting"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-quiet mt-2 text-[13px]",
					children: "Live numbers blended from Finance, Sales, Manufacturing, and Compliance — the same data each department page shows, in one view."
				})
			] }),
			summary.error && /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: summary.error }),
			summary.data && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-2 xl:grid-cols-4",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Net cash flow",
						value: money(summary.data.net_cash_flow),
						accent: true
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Open pipeline",
						value: money(summary.data.open_pipeline_value)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Mfg. yield rate",
						value: `${summary.data.manufacturing_yield_rate}%`
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Compliance score",
						value: `${summary.data.compliance_score}%`
					})
				]
			}),
			summary.data && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "grid gap-4 sm:grid-cols-2",
				children: summary.data.snapshots.map((s) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "rounded-xl border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-5 py-4",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "eyebrow",
							children: s.department
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mt-2 flex items-baseline justify-between text-[13px]",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-quiet",
								children: s.headline_metric
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "font-mono font-semibold",
								children: s.headline_value
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mt-1 flex items-baseline justify-between text-[13px]",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-quiet",
								children: s.secondary_metric
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "font-mono",
								children: s.secondary_value
							})]
						})
					]
				}, s.department))
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "Saved reports",
				subtitle: reports.data ? `${reports.data.total} total` : void 0,
				children: reports.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: reports.error }) : reports.data?.items?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "overflow-x-auto",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("table", {
						className: "w-full text-left text-[13px]",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("thead", {
							className: "text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Title"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Type"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 font-medium",
									children: "Period"
								})
							] })
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", {
							className: "divide-y divide-[color:var(--hairline)]",
							children: reports.data.items.map((r) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 pr-4 font-medium",
									children: r.title
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 capitalize",
									children: r.report_type
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("td", {
									className: "text-quiet py-3 font-mono text-[12px]",
									children: [
										r.period_start ?? "—",
										" – ",
										r.period_end ?? "—"
									]
								})
							] }, r.id))
						})]
					})
				}) : reports.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-quiet text-[13px]",
					children: "Loading…"
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No saved reports yet. Custom report building and scheduled exports aren't wired up." })
			})
		]
	});
}
//#endregion
export { AnalyticsPage as component };
