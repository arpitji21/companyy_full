import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { a as StatCard, i as Panel, n as ErrorState, o as StatusBadge, t as EmptyState } from "./Primitives-DCYrco_Z.mjs";
import { n as useQuery } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/meetings-znulhB2K.js
var import_jsx_runtime = require_jsx_runtime();
function MeetingsPage() {
	const upcoming = useQuery({
		queryKey: ["meetings-upcoming"],
		queryFn: orbit.upcomingMeetings,
		retry: false
	});
	const all = useQuery({
		queryKey: ["meetings-all"],
		queryFn: () => orbit.meetings(1, 25),
		retry: false
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: "Meetings"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
				className: "display mt-2 text-3xl",
				children: "Schedule"
			})] }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
					label: "Upcoming",
					value: String(upcoming.data?.length ?? "—")
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
					label: "All meetings",
					value: String(all.data?.total ?? "—")
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "Upcoming",
				children: upcoming.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: upcoming.error }) : upcoming.data?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "divide-y divide-[color:var(--hairline)]",
					children: upcoming.data.map((m) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "flex items-center justify-between gap-4 py-3 text-[13px]",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "font-medium",
							children: m.title
						}), m.location && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "text-quiet mt-0.5 text-[12px]",
							children: m.location
						})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-quiet font-mono text-[12px]",
							children: new Date(m.starts_at).toLocaleString()
						})]
					}, m.id))
				}) : upcoming.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-quiet text-[13px]",
					children: "Loading…"
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No upcoming meetings scheduled." })
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "All meetings",
				subtitle: all.data ? `${all.data.total} total` : void 0,
				children: all.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: all.error }) : all.data?.items?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
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
									children: "Location"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 pr-4 font-medium",
									children: "Starts"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "py-2.5 font-medium",
									children: "Status"
								})
							] })
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", {
							className: "divide-y divide-[color:var(--hairline)]",
							children: all.data.items.map((m) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3 pr-4 font-medium",
									children: m.title
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4",
									children: m.location ?? "—"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "text-quiet py-3 pr-4 font-mono text-[12px]",
									children: new Date(m.starts_at).toLocaleString()
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
									className: "py-3",
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatusBadge, { status: m.status })
								})
							] }, m.id))
						})]
					})
				}) : all.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-quiet text-[13px]",
					children: "Loading…"
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No meetings recorded." })
			})
		]
	});
}
//#endregion
export { MeetingsPage as component };
