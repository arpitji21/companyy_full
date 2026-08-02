import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { i as Panel, n as ErrorState, t as EmptyState } from "./Primitives-DCYrco_Z.mjs";
import { i as useQueryClient, n as useQuery, t as useMutation } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/notifications-DluGGwcr.js
var import_jsx_runtime = require_jsx_runtime();
function NotificationsPage() {
	const qc = useQueryClient();
	const list = useQuery({
		queryKey: ["notifications"],
		queryFn: () => orbit.notifications(1, 30),
		retry: false
	});
	const markRead = useMutation({
		mutationFn: (id) => orbit.markRead(id),
		onSuccess: () => {
			qc.invalidateQueries({ queryKey: ["notifications"] });
			qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
		}
	});
	const decide = useMutation({
		mutationFn: ({ id, approve }) => orbit.decideApproval(id, approve),
		onSuccess: () => {
			qc.invalidateQueries({ queryKey: ["notifications"] });
			qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
			qc.invalidateQueries({ queryKey: ["approvals"] });
		}
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
			className: "eyebrow",
			children: "Inbox"
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
			className: "display mt-2 text-3xl",
			children: "Notifications"
		})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
			title: "Recent",
			subtitle: list.data ? `${list.data.total} total` : void 0,
			children: list.error ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: list.error }) : list.data?.items?.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
				className: "divide-y divide-[color:var(--hairline)]",
				children: list.data.items.map((n) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(NotificationRow, {
					notification: n,
					onMarkRead: () => markRead.mutate(n.id),
					onDecide: (approve) => decide.mutate({
						id: n.reference_id,
						approve
					}),
					markReadBusy: markRead.isPending,
					decideBusy: decide.isPending
				}, n.id))
			}) : list.isLoading ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "text-quiet text-[13px]",
				children: "Loading…"
			}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EmptyState, { message: "Nothing here yet." })
		})]
	});
}
function NotificationRow({ notification: n, onMarkRead, onDecide, markReadBusy, decideBusy }) {
	const isActionableApproval = !n.is_read && n.reference_type === "approval" && n.reference_id;
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
		className: "flex items-start justify-between gap-4 py-4",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
				className: "flex items-center gap-2 text-[13px] font-medium",
				children: [!n.is_read && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "h-1.5 w-1.5 rounded-full bg-primary" }), n.title]
			}),
			n.body && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "text-quiet mt-1 text-[12.5px]",
				children: n.body
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "text-quiet mt-1 font-mono text-[11px] uppercase",
				children: n.type
			})
		] }), isActionableApproval ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "flex shrink-0 items-center gap-2",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
				onClick: () => onDecide(true),
				disabled: decideBusy,
				className: "rounded-full bg-primary px-3.5 py-1.5 text-[12px] font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-50",
				children: "Approve"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
				onClick: () => onDecide(false),
				disabled: decideBusy,
				className: "rounded-full border border-[color:var(--hairline)] px-3 py-1.5 text-[12px] transition-colors hover:bg-[color:var(--surface-elevated)] disabled:opacity-50",
				children: "Reject"
			})]
		}) : !n.is_read && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
			onClick: onMarkRead,
			disabled: markReadBusy,
			className: "text-quiet shrink-0 rounded-full border border-[color:var(--hairline)] px-3 py-1 text-[11.5px] transition-colors hover:text-foreground",
			children: "Mark read"
		})]
	});
}
//#endregion
export { NotificationsPage as component };
