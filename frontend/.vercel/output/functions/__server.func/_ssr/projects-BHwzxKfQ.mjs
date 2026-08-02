import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { a as StatCard, i as Panel, n as ErrorState, o as StatusBadge, t as EmptyState } from "./Primitives-DCYrco_Z.mjs";
import { n as useQuery } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/projects-BHwzxKfQ.js
var import_jsx_runtime = require_jsx_runtime();
function ProjectsPage() {
	const projects = useQuery({
		queryKey: ["projects"],
		queryFn: () => orbit.projects(1, 25),
		retry: false
	});
	const items = projects.data?.items ?? [];
	const totalTasks = items.reduce((n, p) => n + (p.tasks?.length ?? 0), 0);
	const openTasks = items.reduce((n, p) => n + (p.tasks?.filter((t) => t.status !== "done" && t.status !== "completed").length ?? 0), 0);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: "Projects"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
				className: "display mt-2 text-3xl",
				children: "Delivery & task status"
			})] }),
			projects.data && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-3",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Projects",
						value: String(projects.data.total)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Tasks (page)",
						value: String(totalTasks)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Open tasks (page)",
						value: String(openTasks),
						accent: openTasks > 0
					})
				]
			}),
			projects.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: projects.error }) : items.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "space-y-4",
				children: items.map((p) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Panel, {
					title: p.name,
					subtitle: p.description ?? void 0,
					action: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatusBadge, { status: p.status }),
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "text-quiet mb-4 flex flex-wrap gap-x-6 gap-y-1 text-[12px]",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: ["Start: ", p.start_date ?? "—"] }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: ["Due: ", p.due_date ?? "—"] }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: [p.tasks?.length ?? 0, " tasks"] })
						]
					}), p.tasks?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
						className: "divide-y divide-[color:var(--hairline)]",
						children: p.tasks.map((t) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
							className: "flex items-center justify-between gap-4 py-3 text-[13px]",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
								className: "font-medium",
								children: t.title
							}), t.description && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
								className: "text-quiet mt-0.5 text-[12px]",
								children: t.description
							})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "flex shrink-0 items-center gap-3",
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
										className: "text-quiet font-mono text-[11.5px] capitalize",
										children: t.priority
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
										className: "text-quiet font-mono text-[11.5px]",
										children: t.due_date ?? "—"
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatusBadge, { status: t.status })
								]
							})]
						}, t.id))
					}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No tasks under this project yet." })]
				}, p.id))
			}) : projects.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "text-quiet text-[13px]",
				children: "Loading…"
			}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No projects recorded." })
		]
	});
}
//#endregion
export { ProjectsPage as component };
