import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { a as StatCard, c as money, i as Panel, l as pct, n as ErrorState, o as StatusBadge, t as EmptyState } from "./Primitives-DCYrco_Z.mjs";
import { n as useQuery } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/research-DBn2wzCa.js
var import_jsx_runtime = require_jsx_runtime();
function ResearchPage() {
	const summary = useQuery({
		queryKey: ["research-summary"],
		queryFn: orbit.researchSummary,
		retry: false
	});
	const projects = useQuery({
		queryKey: ["research-projects"],
		queryFn: () => orbit.researchProjects(1, 25),
		retry: false
	});
	const publications = useQuery({
		queryKey: ["research-publications"],
		queryFn: () => orbit.researchPublications(1, 25),
		retry: false
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: "Research"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
				className: "display mt-2 text-3xl",
				children: "R&D pipeline"
			})] }),
			summary.error && /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: summary.error }),
			summary.data && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-2 xl:grid-cols-4",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Active projects",
						value: String(summary.data.active_projects),
						accent: true
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Completed projects",
						value: String(summary.data.completed_projects)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Publications",
						value: String(summary.data.total_publications)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Citations",
						value: String(summary.data.total_citations)
					})
				]
			}),
			summary.data && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-3",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Total budget",
						value: money(summary.data.total_budget)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Total spend",
						value: money(summary.data.total_spend)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Budget utilization",
						value: pct(summary.data.budget_utilization, 1)
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "Research projects",
				subtitle: projects.data ? `${projects.data.total} total` : void 0,
				children: projects.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: projects.error }) : projects.data?.items?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "overflow-x-auto",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("table", {
						className: "w-full text-left text-[13px]",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("thead", {
							className: "text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Project"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Field"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Budget"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Spend"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 font-medium",
									children: "Status"
								})
							] })
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", {
							className: "divide-y divide-[color:var(--hairline)]",
							children: projects.data.items.map((p) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 pr-4 font-medium",
									children: p.title
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4",
									children: p.field ?? "—"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 font-mono text-[12px]",
									children: p.budget !== null ? money(p.budget) : "—"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 font-mono text-[12px]",
									children: money(p.spend)
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3",
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatusBadge, { status: p.status })
								})
							] }, p.id))
						})]
					})
				}) : projects.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-quiet text-[13px]",
					children: "Loading…"
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No research projects recorded." })
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "Publications",
				subtitle: publications.data ? `${publications.data.total} total` : void 0,
				children: publications.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: publications.error }) : publications.data?.items?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
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
									children: "Journal"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Published"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 text-right font-medium",
									children: "Citations"
								})
							] })
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", {
							className: "divide-y divide-[color:var(--hairline)]",
							children: publications.data.items.map((pub) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 pr-4 font-medium",
									children: pub.title
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4",
									children: pub.journal ?? "—"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 font-mono text-[12px]",
									children: pub.publication_date ?? "—"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 text-right font-mono",
									children: pub.citation_count
								})
							] }, pub.id))
						})]
					})
				}) : publications.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-quiet text-[13px]",
					children: "Loading…"
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No publications recorded." })
			})
		]
	});
}
//#endregion
export { ResearchPage as component };
