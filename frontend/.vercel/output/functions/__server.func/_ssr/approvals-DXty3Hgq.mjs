import { r as __toESM } from "../_runtime.mjs";
import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { a as StatCard, c as money, i as Panel, n as ErrorState, o as StatusBadge, t as EmptyState } from "./Primitives-DCYrco_Z.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { i as useQueryClient, n as useQuery, t as useMutation } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/approvals-DXty3Hgq.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
function ApprovalsPage() {
	const qc = useQueryClient();
	const approvals = useQuery({
		queryKey: ["approvals"],
		queryFn: () => orbit.approvals(1, 50),
		retry: false
	});
	const decide = useMutation({
		mutationFn: ({ id, approve }) => orbit.decideApproval(id, approve),
		onSuccess: () => qc.invalidateQueries({ queryKey: ["approvals"] })
	});
	const items = approvals.data?.items ?? [];
	const pending = items.filter((a) => a.status === "pending");
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: "Approvals"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
				className: "display mt-2 text-3xl",
				children: "Requests & sign-off"
			})] }),
			approvals.data && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-3",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Total",
						value: String(approvals.data.total)
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Pending",
						value: String(pending.length),
						accent: pending.length > 0
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatCard, {
						label: "Requested value",
						value: money(items.reduce((n, a) => n + Number(a.amount ?? 0), 0))
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
				title: "Requests",
				subtitle: approvals.data ? `${approvals.data.total} total` : void 0,
				children: approvals.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: approvals.error }) : items.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "divide-y divide-[color:var(--hairline)]",
					children: items.map((a) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ApprovalRow, {
						approval: a,
						onDecide: (approve) => decide.mutate({
							id: a.id,
							approve
						}),
						busy: decide.isPending
					}, a.id))
				}) : approvals.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-quiet text-[13px]",
					children: "Loading…"
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "No approval requests." })
			})
		]
	});
}
function ApprovalRow({ approval, onDecide, busy }) {
	const [acted, setActed] = (0, import_react.useState)(false);
	const pending = approval.status === "pending";
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
		})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "flex shrink-0 items-center gap-3",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(StatusBadge, { status: approval.status }), pending && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "flex items-center gap-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
					disabled: busy || acted,
					onClick: () => {
						setActed(true);
						onDecide(true);
					},
					className: "rounded-full bg-primary px-3.5 py-1.5 text-[12px] font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-50",
					children: "Approve"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
					disabled: busy || acted,
					onClick: () => {
						setActed(true);
						onDecide(false);
					},
					className: "rounded-full border border-[color:var(--hairline)] px-3.5 py-1.5 text-[12px] transition-colors hover:bg-[color:var(--surface-elevated)] disabled:opacity-50",
					children: "Reject"
				})]
			})]
		})]
	});
}
//#endregion
export { ApprovalsPage as component };
