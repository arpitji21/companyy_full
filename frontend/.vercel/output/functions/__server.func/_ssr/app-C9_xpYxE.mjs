import { r as __toESM } from "../_runtime.mjs";
import { a as tokens, i as refreshSession, n as notificationsSocketUrl, r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { t as cva } from "../_libs/class-variance-authority+clsx.mjs";
import { t as cn } from "./utils-C_uf36nf.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { i as useQueryClient, n as useQuery } from "../_libs/tanstack__react-query.mjs";
import { t as lark_logo_default } from "./lark-logo-DONZ3N_a.mjs";
import { _ as useNavigate, f as Outlet, g as Link, l as useRouterState } from "../_libs/@tanstack/react-router+[...].mjs";
import { a as DialogOverlay, i as DialogDescription, n as DialogClose, o as DialogPortal, r as DialogContent, s as DialogTitle, t as Dialog } from "../_libs/@radix-ui/react-dialog+[...].mjs";
import { i as ChevronLeft, n as Menu, r as LogOut, t as X } from "../_libs/lucide-react.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/app-C9_xpYxE.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
var Sheet = Dialog;
var SheetClose = DialogClose;
var SheetPortal = DialogPortal;
var SheetOverlay = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(DialogOverlay, {
	className: cn("fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0", className),
	...props,
	ref
}));
SheetOverlay.displayName = DialogOverlay.displayName;
var sheetVariants = cva("fixed z-50 gap-4 bg-background p-6 shadow-lg transition ease-in-out data-[state=closed]:duration-300 data-[state=open]:duration-500 data-[state=open]:animate-in data-[state=closed]:animate-out", {
	variants: { side: {
		top: "inset-x-0 top-0 border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top",
		bottom: "inset-x-0 bottom-0 border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom",
		left: "inset-y-0 left-0 h-full w-3/4 border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left sm:max-w-sm",
		right: "inset-y-0 right-0 h-full w-3/4 border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right sm:max-w-sm"
	} },
	defaultVariants: { side: "right" }
});
var SheetContent = import_react.forwardRef(({ side = "right", className, children, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SheetPortal, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SheetOverlay, {}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(DialogContent, {
	ref,
	className: cn(sheetVariants({ side }), className),
	...props,
	children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(DialogClose, {
		className: "absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background cursor-pointer transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-secondary",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(X, { className: "h-4 w-4" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
			className: "sr-only",
			children: "Close"
		})]
	}), children]
})] }));
SheetContent.displayName = DialogContent.displayName;
var SheetHeader = ({ className, ...props }) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
	className: cn("flex flex-col space-y-2 text-center sm:text-left", className),
	...props
});
SheetHeader.displayName = "SheetHeader";
var SheetFooter = ({ className, ...props }) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
	className: cn("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2", className),
	...props
});
SheetFooter.displayName = "SheetFooter";
var SheetTitle = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(DialogTitle, {
	ref,
	className: cn("text-lg font-semibold text-foreground", className),
	...props
}));
SheetTitle.displayName = DialogTitle.displayName;
var SheetDescription = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(DialogDescription, {
	ref,
	className: cn("text-sm text-muted-foreground", className),
	...props
}));
SheetDescription.displayName = DialogDescription.displayName;
var AuthContext = (0, import_react.createContext)(null);
function AuthProvider({ children }) {
	const [user, setUser] = (0, import_react.useState)(null);
	const [status, setStatus] = (0, import_react.useState)("loading");
	const load = (0, import_react.useCallback)(async () => {
		if (!tokens.access) {
			setUser(null);
			setStatus("anonymous");
			return;
		}
		try {
			const me = await orbit.me();
			setUser(me);
			setStatus("authenticated");
		} catch {
			tokens.clear();
			setUser(null);
			setStatus("anonymous");
		}
	}, []);
	(0, import_react.useEffect)(() => {
		load();
	}, [load]);
	const signIn = (0, import_react.useCallback)(async (email, password) => {
		const pair = await orbit.login(email, password);
		tokens.set(pair.access_token, pair.refresh_token);
		await load();
	}, [load]);
	const signOut = (0, import_react.useCallback)(async () => {
		const refresh = tokens.refresh;
		try {
			if (refresh) await orbit.logout(refresh);
		} catch {}
		tokens.clear();
		setUser(null);
		setStatus("anonymous");
	}, []);
	const value = (0, import_react.useMemo)(() => ({
		user,
		status,
		signIn,
		signOut,
		refreshUser: load
	}), [
		user,
		status,
		signIn,
		signOut,
		load
	]);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(AuthContext.Provider, {
		value,
		children
	});
}
function useAuth() {
	const ctx = (0, import_react.useContext)(AuthContext);
	if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
	return ctx;
}
/**
* Real-time notification push, layered on top of the existing
* REST + react-query setup rather than replacing it:
*
* - The WebSocket is treated as a low-latency *nudge*, not a guaranteed
*   delivery channel. Every (re)connect triggers a REST refetch of
*   notifications + unread-count, so a message dropped while offline (tab
*   asleep, network blip, server redeploy) is caught by that reconciliation
*   fetch instead of silently disappearing. Postgres is always the source
*   of truth; the socket just tells us "go look."
* - Reconnects with exponential backoff + jitter, capped at 30s, so a
*   backend restart or blip doesn't hammer the server with reconnect
*   attempts across every open tab at once.
* - The server proactively closes ~15s before the access token expires
*   (close code 4402). On that code specifically, we refresh the session
*   first and then reconnect with the new token, instead of just retrying
*   the same soon-to-be-rejected one.
* - A heartbeat "ping" is sent every 20s so idling proxies (Render's, most
*   corporate ones) don't silently drop the connection for inactivity.
*/
function useNotificationSocket(enabled) {
	const qc = useQueryClient();
	const reconnectAttempt = (0, import_react.useRef)(0);
	const reconnectTimer = (0, import_react.useRef)(null);
	const heartbeatTimer = (0, import_react.useRef)(null);
	const socketRef = (0, import_react.useRef)(null);
	const stoppedRef = (0, import_react.useRef)(false);
	(0, import_react.useEffect)(() => {
		if (!enabled) return;
		stoppedRef.current = false;
		const reconcile = () => {
			qc.invalidateQueries({ queryKey: ["notifications"] });
			qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
		};
		const bumpUnreadCount = (delta) => {
			qc.setQueryData(["notifications", "unread-count"], (current) => current ? {
				...current,
				unread_count: Math.max(0, (current.unread_count ?? 0) + delta)
			} : current);
		};
		const scheduleReconnect = () => {
			if (stoppedRef.current) return;
			const attempt = reconnectAttempt.current++;
			const base = Math.min(1e3 * 2 ** attempt, 3e4);
			const jitter = Math.random() * Math.min(1e3, base);
			reconnectTimer.current = setTimeout(connect, base + jitter);
		};
		const connect = async () => {
			if (stoppedRef.current) return;
			if (!tokens.access) return;
			const socket = new WebSocket(notificationsSocketUrl(tokens.access));
			socketRef.current = socket;
			socket.onopen = () => {
				reconnectAttempt.current = 0;
				reconcile();
				heartbeatTimer.current = setInterval(() => {
					if (socket.readyState === WebSocket.OPEN) socket.send("ping");
				}, 2e4);
			};
			socket.onmessage = (raw) => {
				let msg = null;
				try {
					msg = JSON.parse(raw.data);
				} catch {
					return;
				}
				if (msg?.kind === "notification.created" && msg.notification) {
					qc.setQueryData(["notifications"], (current) => current ? {
						...current,
						items: [msg.notification, ...current.items],
						total: current.total + 1
					} : current);
					bumpUnreadCount(1);
					qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
				} else if (msg?.kind === "notification.resolved") reconcile();
			};
			socket.onclose = async (event) => {
				if (heartbeatTimer.current) clearInterval(heartbeatTimer.current);
				if (stoppedRef.current) return;
				if (event.code === 4402) {
					if (await refreshSession()) {
						reconnectAttempt.current = 0;
						connect();
						return;
					}
				}
				if (event.code === 4401) return;
				scheduleReconnect();
			};
			socket.onerror = () => socket.close();
		};
		connect();
		const onFocusOrOnline = () => {
			if (socketRef.current?.readyState !== WebSocket.OPEN) {
				if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
				reconnectAttempt.current = 0;
				connect();
			}
		};
		window.addEventListener("focus", onFocusOrOnline);
		window.addEventListener("online", onFocusOrOnline);
		return () => {
			stoppedRef.current = true;
			window.removeEventListener("focus", onFocusOrOnline);
			window.removeEventListener("online", onFocusOrOnline);
			if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
			if (heartbeatTimer.current) clearInterval(heartbeatTimer.current);
			socketRef.current?.close();
			socketRef.current = null;
		};
	}, [enabled, qc]);
}
var navGroups = [{
	label: null,
	items: [{
		to: "/app",
		label: "Overview",
		exact: true
	}]
}, {
	label: "Live",
	items: [
		{
			to: "/app/finance",
			label: "Finance"
		},
		{
			to: "/app/sales",
			label: "Sales"
		},
		{
			to: "/app/marketing",
			label: "Marketing"
		},
		{
			to: "/app/manufacturing",
			label: "Manufacturing"
		},
		{
			to: "/app/quality",
			label: "Quality"
		},
		{
			to: "/app/compliance",
			label: "Compliance"
		},
		{
			to: "/app/regulatory",
			label: "Regulatory"
		},
		{
			to: "/app/supply-chain",
			label: "Supply Chain"
		},
		{
			to: "/app/research",
			label: "Research"
		},
		{
			to: "/app/patent",
			label: "Patent"
		},
		{
			to: "/app/grant",
			label: "Grant"
		},
		{
			to: "/app/docs",
			label: "Docs"
		},
		{
			to: "/app/projects",
			label: "Projects"
		},
		{
			to: "/app/meetings",
			label: "Meetings"
		},
		{
			to: "/app/approvals",
			label: "Approvals"
		},
		{
			to: "/app/people",
			label: "People"
		},
		{
			to: "/app/notifications",
			label: "Notifications"
		},
		{
			to: "/app/assistant",
			label: "AI Assistant"
		},
		{
			to: "/app/clinical",
			label: "Clinical"
		},
		{
			to: "/app/investor",
			label: "Investor"
		},
		{
			to: "/app/tender",
			label: "Tender"
		},
		{
			to: "/app/customer",
			label: "Customer"
		},
		{
			to: "/app/procurement",
			label: "Procurement"
		},
		{
			to: "/app/analytics",
			label: "Analytics"
		}
	]
}];
var nav = navGroups.flatMap((g) => g.items);
function ConsoleShell() {
	const { user, status, signOut } = useAuth();
	const navigate = useNavigate();
	const pathname = useRouterState({ select: (s) => s.location.pathname });
	const [menuOpen, setMenuOpen] = (0, import_react.useState)(false);
	useNotificationSocket(status === "authenticated");
	const unread = useQuery({
		queryKey: ["notifications", "unread-count"],
		queryFn: () => orbit.unreadCount(),
		enabled: status === "authenticated",
		refetchInterval: 6e4
	});
	const unreadCount = Number(unread.data?.unread_count ?? 0);
	(0, import_react.useEffect)(() => {
		if (status === "anonymous") navigate({
			to: "/login",
			replace: true
		});
	}, [status, navigate]);
	(0, import_react.useEffect)(() => {
		setMenuOpen(false);
	}, [pathname]);
	if (status !== "authenticated") return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "text-quiet flex min-h-screen items-center justify-center text-[13px]",
		children: status === "loading" ? "Connecting to Orbit…" : "Redirecting to sign in…"
	});
	const current = nav.find((item) => item.exact ? pathname === item.to : pathname.startsWith(item.to));
	const isRoot = pathname === "/app";
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "min-h-screen",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
				className: "sticky top-0 z-40 border-b border-[color:var(--hairline)] bg-[color-mix(in_oklab,var(--background)_82%,transparent)] backdrop-blur-xl",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mx-auto flex h-14 max-w-7xl items-center justify-between gap-3 px-4 sm:px-6",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex min-w-0 items-center gap-1.5",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
							onClick: () => setMenuOpen(true),
							"aria-label": "Open menu",
							className: "text-quiet -ml-1.5 shrink-0 rounded-full p-2 transition-colors hover:bg-[color:var(--surface-elevated)] hover:text-foreground lg:hidden",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Menu, { className: "h-[18px] w-[18px]" })
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Link, {
							to: "/app",
							className: "flex min-w-0 items-center gap-2.5",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("img", {
								src: lark_logo_default,
								alt: "Lark Healthcare",
								className: "h-7 w-7 shrink-0 object-contain"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "truncate text-[13px] font-semibold tracking-tight",
								children: "Orbit Console"
							})]
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex shrink-0 items-center gap-3 sm:gap-4",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-quiet hidden text-[12.5px] sm:block",
							children: user?.full_name
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
							onClick: () => void signOut(),
							"aria-label": "Sign out",
							className: "text-quiet flex items-center gap-1.5 rounded-full border border-[color:var(--hairline)] p-2 text-[12px] transition-colors hover:bg-[color:var(--surface-elevated)] hover:text-foreground sm:px-3.5 sm:py-1.5",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(LogOut, { className: "h-[15px] w-[15px] sm:hidden" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "hidden sm:inline",
								children: "Sign out"
							})]
						})]
					})]
				}), !isRoot && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "border-t border-[color:var(--hairline)] px-4 py-2 lg:hidden",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Link, {
						to: "/app",
						className: "text-quiet inline-flex items-center gap-1 text-[12.5px] transition-colors hover:text-foreground",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ChevronLeft, { className: "h-3.5 w-3.5" }),
							"Overview",
							current && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
								className: "text-foreground font-medium",
								children: ["\xA0/ ", current.label]
							})
						]
					})
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Sheet, {
				open: menuOpen,
				onOpenChange: setMenuOpen,
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SheetContent, {
					side: "left",
					className: "glass flex w-[82%] max-w-xs flex-col gap-0 p-0",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SheetHeader, {
							className: "border-b border-[color:var(--hairline)] px-5 py-4 text-left",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SheetTitle, {
								className: "flex items-center gap-2.5 text-[13px] font-semibold tracking-tight",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("img", {
									src: lark_logo_default,
									alt: "Lark Healthcare",
									className: "h-6 w-6 object-contain"
								}), "Orbit Console"]
							})
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("nav", {
							className: "flex-1 space-y-5 overflow-y-auto px-3 py-4",
							children: navGroups.map((group) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [group.label && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
								className: "text-quiet mb-1.5 px-3.5 text-[10.5px] font-semibold tracking-wider uppercase",
								children: group.label
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "space-y-1",
								children: group.items.map((item) => {
									const active = item.exact ? pathname === item.to : pathname.startsWith(item.to);
									return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SheetClose, {
										asChild: true,
										children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Link, {
											to: item.to,
											className: `block rounded-xl px-3.5 py-2.5 text-[13.5px] transition-colors ${active ? "bg-[color:var(--surface-elevated)] font-semibold text-foreground" : "text-quiet hover:bg-[color:var(--surface-elevated)] hover:text-foreground"}`,
											children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
												className: "flex items-center justify-between gap-2",
												children: [item.label, item.to === "/app/notifications" && unreadCount > 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
													className: "rounded-full bg-[color:var(--accent,#4f7cff)] px-1.5 py-0.5 text-[10px] font-semibold text-white",
													children: unreadCount > 99 ? "99+" : unreadCount
												})]
											})
										})
									}, item.to);
								})
							})] }, group.label ?? "top"))
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "border-t border-[color:var(--hairline)] px-5 py-4",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
									className: "truncate text-[12.5px] font-medium",
									children: user?.full_name
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
									className: "text-quiet truncate text-[11.5px]",
									children: user?.email
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
									onClick: () => void signOut(),
									className: "mt-3 flex w-full items-center justify-center gap-1.5 rounded-full border border-[color:var(--hairline)] py-2 text-[12.5px] transition-colors hover:bg-[color:var(--surface-elevated)]",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(LogOut, { className: "h-[14px] w-[14px]" }), "Sign out"]
								})
							]
						})
					]
				})
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "mx-auto flex max-w-7xl gap-8 px-4 py-6 sm:px-6 sm:py-8",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("aside", {
					className: "hidden w-52 shrink-0 lg:block",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("nav", {
						className: "sticky top-24 max-h-[calc(100vh-7rem)] space-y-5 overflow-y-auto pb-6 pr-1",
						children: navGroups.map((group) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [group.label && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "text-quiet mb-1.5 px-3.5 text-[10.5px] font-semibold tracking-wider uppercase",
							children: group.label
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "space-y-1",
							children: group.items.map((item) => {
								const active = item.exact ? pathname === item.to : pathname.startsWith(item.to);
								return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Link, {
									to: item.to,
									className: `block rounded-xl px-3.5 py-2 text-[13px] transition-colors ${active ? "bg-[color:var(--surface-elevated)] font-semibold text-foreground" : "text-quiet hover:text-foreground"}`,
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
										className: "flex items-center justify-between gap-2",
										children: [item.label, item.to === "/app/notifications" && unreadCount > 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
											className: "rounded-full bg-[color:var(--accent,#4f7cff)] px-1.5 py-0.5 text-[10px] font-semibold text-white",
											children: unreadCount > 99 ? "99+" : unreadCount
										})]
									})
								}, item.to);
							})
						})] }, group.label ?? "top"))
					})
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("main", {
					className: "min-w-0 flex-1",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Outlet, {})
				})]
			})
		]
	});
}
var SplitComponent = () => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(AuthProvider, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ConsoleShell, {}) });
//#endregion
export { SplitComponent as component };
