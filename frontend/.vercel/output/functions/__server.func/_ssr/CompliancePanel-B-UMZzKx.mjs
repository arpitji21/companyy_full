import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { a as StatCard, i as Panel, n as ErrorState, o as StatusBadge, r as Meter, t as EmptyState } from "./Primitives-DCYrco_Z.mjs";
import { n as useQuery } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/CompliancePanel-B-UMZzKx.js
var import_jsx_runtime = require_jsx_runtime();
function CompliancePanel({ eyebrow, title, recordLabel, summaryQueryKey, recordsQueryKey, fetchSummary, fetchRecords }) {
	const summary = useQuery({
		queryKey: [summaryQueryKey],
		queryFn: fetchSummary,
		retry: false
	});
	const records = useQuery({
		queryKey: [recordsQueryKey],
		queryFn: fetchRecords,
		retry: false
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: eyebrow
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
				className: "display mt-2 text-3xl",
				children: title
			})] }),
			summary.error && /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: summary.error }),
			summary.data && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-6 lg:grid-cols-3",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "grid gap-4 sm:grid-cols-3 lg:col-span-2",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
							label: "Total records",
							value: String(summary.data.total_records)
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
							label: "Approved",
							value: String(summary.data.approved)
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
							label: "Expired",
							value: String(summary.data.expired)
						})
					]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Panel, {
					title: "Compliance score",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
						className: "display text-4xl",
						children: [summary.data.compliance_score.toFixed(0), "%"]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-5",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Meter, {
							label: "Compliance score",
							value: summary.data.compliance_score
						})
					})]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: recordLabel,
				subtitle: records.data ? `${records.data.total} total` : void 0,
				children: records.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: records.error }) : records.data?.items?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
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
									children: "Framework"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Status"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Submitted"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Expires"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 font-medium",
									children: "Certificate"
								})
							] })
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", {
							className: "divide-y divide-[color:var(--hairline)]",
							children: records.data.items.map((r) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 pr-4 font-medium",
									children: r.title
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 uppercase",
									children: r.framework
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 pr-4",
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatusBadge, { status: r.status })
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 font-mono text-[12px]",
									children: r.submission_date ?? "—"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 font-mono text-[12px]",
									children: r.expiry_date ?? "—"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 font-mono text-[12px]",
									children: r.certificate_number ?? "—"
								})
							] }, r.id))
						})]
					})
				}) : records.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-quiet text-[13px]",
					children: "Loading…"
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No records recorded." })
			})
		]
	});
}
//#endregion
export { CompliancePanel as t };
