import { r as __toESM } from "../_runtime.mjs";
import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { a as StatCard, c as money, i as Panel, n as ErrorState, o as StatusBadge, r as Meter, t as EmptyState } from "./Primitives-DCYrco_Z.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { i as useQueryClient, n as useQuery, t as useMutation } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/app-CC5zGhyU.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
function Overview() {
	const qc = useQueryClient();
	const dash = useQuery({
		queryKey: ["ceo-dashboard"],
		queryFn: orbit.ceoDashboard,
		retry: false
	});
	const decide = useMutation({
		mutationFn: ({ id, approve }) => orbit.decideApproval(id, approve),
		onSuccess: () => {
			qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
			qc.invalidateQueries({ queryKey: ["approvals"] });
			qc.invalidateQueries({ queryKey: ["notifications"] });
		}
	});
	if (dash.isLoading) return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
		className: "text-quiet text-[13px]",
		children: "Loading dashboard…"
	});
	if (dash.error) return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: dash.error });
	const d = dash.data;
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: "Executive"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
				className: "display mt-2 text-3xl",
				children: "Company overview"
			})] }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-2 xl:grid-cols-4",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Revenue",
						value: money(d.revenue)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Expenses",
						value: money(d.expenses)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Cash flow",
						value: money(d.cash_flow),
						accent: true
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Burn rate",
						value: money(d.burn_rate),
						hint: "avg. monthly"
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "Action center",
				subtitle: "Requests waiting on you — approve or reject right here, from any department.",
				children: d.action_items?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "divide-y divide-[color:var(--hairline)]",
					children: d.action_items.map((a) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ActionItemRow, {
						approval: a,
						onDecide: (approve) => decide.mutate({
							id: a.id,
							approve
						}),
						busy: decide.isPending
					}, a.id))
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "Nothing needs your sign-off right now." })
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-6 lg:grid-cols-3",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Panel, {
						title: "Health score",
						subtitle: "Composite operational health",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "display text-5xl",
							children: d.company_health_score?.toFixed(0)
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mt-6 space-y-4",
							children: Object.entries(d.health_score_breakdown ?? {}).map(([k, v]) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Meter, {
								label: k,
								value: Number(v)
							}, k))
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Panel, {
						title: "Risk score",
						subtitle: "Weighted exposure across domains",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "display text-5xl text-[color:var(--crimson-soft)]",
							children: d.risk_score?.toFixed(0)
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mt-6 space-y-4",
							children: Object.entries(d.risk_score_breakdown ?? {}).map(([k, v]) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Meter, {
								label: k,
								value: Number(v)
							}, k))
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "space-y-6",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
							title: "Attention",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("ul", {
								className: "space-y-3 text-[13px]",
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Row, {
										label: "Pending approvals",
										value: d.pending_approvals
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Row, {
										label: "Open tasks",
										value: d.open_tasks
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Row, {
										label: "Unread notifications",
										value: d.unread_notifications
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Row, {
										label: "Compliance score",
										value: `${Number(d.compliance_score).toFixed(0)}%`
									})
								]
							})
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
							title: "Workforce",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("ul", {
								className: "space-y-3 text-[13px]",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Row, {
									label: "Employees",
									value: d.employee_count
								}), Object.entries(d.hiring_status ?? {}).map(([k, v]) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Row, {
									label: k.replace(/_/g, " "),
									value: v
								}, k))]
							})
						})]
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "Upcoming meetings",
				children: d.upcoming_meetings?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "divide-y divide-[color:var(--hairline)]",
					children: d.upcoming_meetings.map((m) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "flex items-center justify-between py-3 text-[13px]",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: m.title }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-quiet font-mono text-[12px]",
							children: new Date(m.starts_at).toLocaleString()
						})]
					}, m.id))
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No meetings scheduled." })
			})
		]
	});
}
function ActionItemRow({ approval, onDecide, busy }) {
	const [acted, setActed] = (0, import_react.useState)(false);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
		className: "flex flex-col gap-3 py-4 sm:flex-row sm:items-center sm:justify-between",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
			className: "text-[13px] font-medium",
			children: approval.title
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "text-quiet mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-[12px]",
			children: [approval.amount !== null && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "font-mono",
				children: money(approval.amount)
			}), approval.notes && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: approval.notes })]
		})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "flex shrink-0 items-center gap-3",
			children: acted ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatusBadge, { status: approval.status }) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "flex items-center gap-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
					disabled: busy,
					onClick: () => {
						setActed(true);
						onDecide(true);
					},
					className: "rounded-full bg-primary px-3.5 py-1.5 text-[12px] font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-50",
					children: "Approve"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
					disabled: busy,
					onClick: () => {
						setActed(true);
						onDecide(false);
					},
					className: "rounded-full border border-[color:var(--hairline)] px-3.5 py-1.5 text-[12px] transition-colors hover:bg-[color:var(--surface-elevated)] disabled:opacity-50",
					children: "Reject"
				})]
			})
		})]
	});
}
function Row({ label, value }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
		className: "flex items-center justify-between",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
			className: "text-quiet capitalize",
			children: label
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
			className: "font-mono",
			children: value
		})]
	});
}
//#endregion
export { Overview as component };
