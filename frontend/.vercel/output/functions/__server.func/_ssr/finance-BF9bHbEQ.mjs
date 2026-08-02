import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { a as StatCard, c as money, i as Panel, n as ErrorState, t as EmptyState } from "./Primitives-DCYrco_Z.mjs";
import { n as useQuery } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/finance-BF9bHbEQ.js
var import_jsx_runtime = require_jsx_runtime();
function FinancePage() {
	const summary = useQuery({
		queryKey: ["finance-summary"],
		queryFn: orbit.financeSummary,
		retry: false
	});
	const tx = useQuery({
		queryKey: ["finance-transactions"],
		queryFn: () => orbit.transactions(1, 25),
		retry: false
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: "Finance"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
				className: "display mt-2 text-3xl",
				children: "Cash, budgets & ledger"
			})] }),
			summary.error && /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: summary.error }),
			summary.data && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-2 xl:grid-cols-4",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Total revenue",
						value: money(summary.data.total_revenue)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Total expenses",
						value: money(summary.data.total_expenses)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Net cash flow",
						value: money(summary.data.net_cash_flow),
						accent: true
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Burn rate",
						value: money(summary.data.burn_rate)
					})
				]
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "Spend by category",
				children: Object.keys(summary.data.by_category ?? {}).length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "grid gap-3 sm:grid-cols-2",
					children: Object.entries(summary.data.by_category).map(([k, v]) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "flex items-center justify-between rounded-xl bg-[color:var(--surface-elevated)] px-4 py-3 text-[13px]",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "capitalize",
							children: k.replace(/_/g, " ")
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "font-mono",
							children: money(v)
						})]
					}, k))
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No categorised spend yet." })
			})] }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "Recent transactions",
				subtitle: tx.data ? `${tx.data.total} total records` : void 0,
				children: tx.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: tx.error }) : tx.data?.items?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "overflow-x-auto",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("table", {
						className: "w-full text-left text-[13px]",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("thead", {
							className: "text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Date"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Type"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Description"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Status"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 text-right font-medium",
									children: "Amount"
								})
							] })
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", {
							className: "divide-y divide-[color:var(--hairline)]",
							children: tx.data.items.map((t) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 font-mono text-[12px]",
									children: t.transaction_date
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 pr-4 capitalize",
									children: t.type
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 pr-4",
									children: t.description ?? t.category ?? "—"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 capitalize",
									children: t.status
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 text-right font-mono",
									children: money(t.amount, t.currency)
								})
							] }, t.id))
						})]
					})
				}) : tx.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-quiet text-[13px]",
					children: "Loading…"
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No transactions recorded." })
			})
		]
	});
}
//#endregion
export { FinancePage as component };
