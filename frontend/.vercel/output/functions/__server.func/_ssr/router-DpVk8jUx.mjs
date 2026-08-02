import { r as __toESM } from "../_runtime.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { t as QueryClient } from "../_libs/tanstack__query-core.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { r as QueryClientProvider } from "../_libs/tanstack__react-query.mjs";
import { c as HeadContent, d as createRouter, f as Outlet, g as Link, h as createRootRouteWithContext, m as createFileRoute, p as lazyRouteComponent, s as Scripts, v as useRouter } from "../_libs/@tanstack/react-router+[...].mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/router-DpVk8jUx.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
var styles_default = "/assets/styles-C7vSjXh-.css";
function reportLovableError(error, context = {}) {
	if (typeof window === "undefined") return;
	window.__lovableEvents?.captureException?.(error, {
		source: "react_error_boundary",
		route: window.location.pathname,
		...context
	}, {
		mechanism: "react_error_boundary",
		handled: false,
		severity: "error"
	});
	const message = error instanceof Response ? `Response ${error.status}${error.url ? ` at ${error.url}` : ""}` : error instanceof Error ? error.message : String(error);
	window.__lovableReportRuntimeError?.({
		message,
		stack: error instanceof Error ? error.stack : void 0,
		filename: window.location.pathname
	});
}
function NotFoundComponent() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "flex min-h-screen items-center justify-center bg-background px-4",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "max-w-md text-center",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
					className: "text-7xl font-bold text-foreground",
					children: "404"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "mt-4 text-xl font-semibold text-foreground",
					children: "Page not found"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "mt-2 text-sm text-muted-foreground",
					children: "The page you're looking for doesn't exist or has been moved."
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "mt-6",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Link, {
						to: "/",
						className: "inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90",
						children: "Go home"
					})
				})
			]
		})
	});
}
function ErrorComponent({ error, reset }) {
	console.error(error);
	const router = useRouter();
	(0, import_react.useEffect)(() => {
		reportLovableError(error, { boundary: "tanstack_root_error_component" });
	}, [error]);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "flex min-h-screen items-center justify-center bg-background px-4",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "max-w-md text-center",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
					className: "text-xl font-semibold tracking-tight text-foreground",
					children: "This page didn't load"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "mt-2 text-sm text-muted-foreground",
					children: "Something went wrong on our end. You can try refreshing or head back home."
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-6 flex flex-wrap justify-center gap-2",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
						onClick: () => {
							router.invalidate();
							reset();
						},
						className: "inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90",
						children: "Try again"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("a", {
						href: "/",
						className: "inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent",
						children: "Go home"
					})]
				})
			]
		})
	});
}
var Route$29 = createRootRouteWithContext()({
	head: () => ({
		meta: [
			{ charSet: "utf-8" },
			{
				name: "viewport",
				content: "width=device-width, initial-scale=1"
			},
			{ title: "LarkAI Orbit — Enterprise Intelligence Platform" },
			{
				name: "description",
				content: "Orbit unifies every department of Lark Healthcare into one AI-governed enterprise operating layer."
			},
			{
				name: "author",
				content: "Lark Healthcare"
			},
			{
				property: "og:title",
				content: "LarkAI Orbit — Enterprise Intelligence Platform"
			},
			{
				property: "og:description",
				content: "One system. Every department. AI agents grounded in your live enterprise data."
			},
			{
				property: "og:type",
				content: "website"
			},
			{
				name: "twitter:card",
				content: "summary_large_image"
			}
		],
		links: [
			{
				rel: "stylesheet",
				href: styles_default
			},
			{
				rel: "preconnect",
				href: "https://fonts.googleapis.com"
			},
			{
				rel: "preconnect",
				href: "https://fonts.gstatic.com",
				crossOrigin: "anonymous"
			},
			{
				rel: "stylesheet",
				href: "https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
			},
			{
				rel: "icon",
				href: "/favicon.ico",
				type: "image/x-icon"
			}
		]
	}),
	shellComponent: RootShell,
	component: RootComponent,
	notFoundComponent: NotFoundComponent,
	errorComponent: ErrorComponent
});
function RootShell({ children }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("html", {
		lang: "en",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("head", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(HeadContent, {}) }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("body", { children: [children, /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Scripts, {})] })]
	});
}
function RootComponent() {
	const { queryClient } = Route$29.useRouteContext();
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(QueryClientProvider, {
		client: queryClient,
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Outlet, {})
	});
}
var $$splitComponentImporter$27 = () => import("./routes-DNATJfP5.mjs");
var Route$28 = createFileRoute("/")({
	component: lazyRouteComponent($$splitComponentImporter$27, "component"),
	head: () => ({ meta: [
		{ title: "LarkAI Orbit — Enterprise Intelligence for Lark Healthcare" },
		{
			name: "description",
			content: "Orbit unifies finance, manufacturing, quality, compliance and supply chain into one AI-governed operating layer for regulated healthcare manufacturers."
		},
		{
			property: "og:title",
			content: "LarkAI Orbit — Enterprise Intelligence Platform"
		},
		{
			property: "og:description",
			content: "One system. Every department. AI agents grounded in your live enterprise data, built for regulated healthcare."
		},
		{
			property: "og:type",
			content: "website"
		},
		{
			name: "twitter:card",
			content: "summary_large_image"
		}
	] })
});
var $$splitComponentImporter$26 = () => import("./app-C9_xpYxE.mjs");
var Route$27 = createFileRoute("/app")({
	ssr: false,
	head: () => ({ meta: [
		{ title: "Orbit Console — LarkAI Healthcare" },
		{
			name: "description",
			content: "Live enterprise console for LarkAI Orbit: finance, people, notifications and AI agents from the Orbit API."
		},
		{
			property: "og:title",
			content: "Orbit Console — LarkAI Healthcare"
		},
		{
			property: "og:description",
			content: "Live enterprise operations console powered by the LarkAI Orbit API."
		},
		{
			property: "og:type",
			content: "website"
		},
		{
			name: "twitter:card",
			content: "summary_large_image"
		}
	] }),
	component: lazyRouteComponent($$splitComponentImporter$26, "component")
});
var $$splitComponentImporter$25 = () => import("./login-DF8JFhcV.mjs");
var Route$26 = createFileRoute("/login")({
	ssr: false,
	head: () => ({ meta: [
		{ title: "Sign in — LarkAI Orbit Console" },
		{
			name: "description",
			content: "Sign in to the LarkAI Orbit console to access live finance, people, compliance and AI agent data."
		},
		{
			property: "og:title",
			content: "Sign in — LarkAI Orbit Console"
		},
		{
			property: "og:description",
			content: "Secure access to the LarkAI Orbit enterprise operating system."
		},
		{
			property: "og:type",
			content: "website"
		},
		{
			name: "twitter:card",
			content: "summary_large_image"
		}
	] }),
	component: lazyRouteComponent($$splitComponentImporter$25, "component")
});
var BASE_URL = "";
var Route$25 = createFileRoute("/sitemap.xml")({ server: { handlers: { GET: async () => {
	const xml = [
		`<?xml version="1.0" encoding="UTF-8"?>`,
		`<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`,
		...[{
			path: "/",
			changefreq: "weekly",
			priority: "1.0"
		}].map((e) => [
			`  <url>`,
			`    <loc>${BASE_URL}${e.path}</loc>`,
			e.lastmod ? `    <lastmod>${e.lastmod}</lastmod>` : null,
			e.changefreq ? `    <changefreq>${e.changefreq}</changefreq>` : null,
			e.priority ? `    <priority>${e.priority}</priority>` : null,
			`  </url>`
		].filter(Boolean).join("\n")),
		`</urlset>`
	].join("\n");
	return new Response(xml, { headers: {
		"Content-Type": "application/xml",
		"Cache-Control": "public, max-age=3600"
	} });
} } } });
var $$splitComponentImporter$24 = () => import("./app-CC5zGhyU.mjs");
var Route$24 = createFileRoute("/app/")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$24, "component")
});
var $$splitComponentImporter$23 = () => import("./analytics-DSRfd7xK.mjs");
var Route$23 = createFileRoute("/app/analytics")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$23, "component")
});
var $$splitComponentImporter$22 = () => import("./approvals-DXty3Hgq.mjs");
var Route$22 = createFileRoute("/app/approvals")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$22, "component")
});
var $$splitComponentImporter$21 = () => import("./assistant-CMfzt12N.mjs");
var Route$21 = createFileRoute("/app/assistant")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$21, "component")
});
var $$splitComponentImporter$20 = () => import("./clinical-C2pgqEQq.mjs");
var Route$20 = createFileRoute("/app/clinical")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$20, "component")
});
var $$splitComponentImporter$19 = () => import("./compliance-y8qKFT2e.mjs");
var Route$19 = createFileRoute("/app/compliance")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$19, "component")
});
var $$splitComponentImporter$18 = () => import("./customer-BGwbl0j3.mjs");
var Route$18 = createFileRoute("/app/customer")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$18, "component")
});
var $$splitComponentImporter$17 = () => import("./docs-C1zde1w1.mjs");
var Route$17 = createFileRoute("/app/docs")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$17, "component")
});
var $$splitComponentImporter$16 = () => import("./finance-BF9bHbEQ.mjs");
var Route$16 = createFileRoute("/app/finance")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$16, "component")
});
var $$splitComponentImporter$15 = () => import("./grant-DUM79mau.mjs");
var Route$15 = createFileRoute("/app/grant")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$15, "component")
});
var $$splitComponentImporter$14 = () => import("./investor-Dve7nApZ.mjs");
var Route$14 = createFileRoute("/app/investor")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$14, "component")
});
var $$splitComponentImporter$13 = () => import("./manufacturing-BiEf0UoI.mjs");
var Route$13 = createFileRoute("/app/manufacturing")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$13, "component")
});
var $$splitComponentImporter$12 = () => import("./marketing-BRH3Mwy0.mjs");
var Route$12 = createFileRoute("/app/marketing")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$12, "component")
});
var $$splitComponentImporter$11 = () => import("./meetings-znulhB2K.mjs");
var Route$11 = createFileRoute("/app/meetings")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$11, "component")
});
var $$splitComponentImporter$10 = () => import("./notifications-DluGGwcr.mjs");
var Route$10 = createFileRoute("/app/notifications")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$10, "component")
});
var $$splitComponentImporter$9 = () => import("./patent-VD-sMVQM.mjs");
var Route$9 = createFileRoute("/app/patent")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$9, "component")
});
var $$splitComponentImporter$8 = () => import("./people-C0IsTGj5.mjs");
var Route$8 = createFileRoute("/app/people")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$8, "component")
});
var $$splitComponentImporter$7 = () => import("./procurement-OcMC94zc.mjs");
var Route$7 = createFileRoute("/app/procurement")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$7, "component")
});
var $$splitComponentImporter$6 = () => import("./projects-BHwzxKfQ.mjs");
var Route$6 = createFileRoute("/app/projects")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$6, "component")
});
var $$splitComponentImporter$5 = () => import("./quality-C6u757Ne.mjs");
var Route$5 = createFileRoute("/app/quality")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$5, "component")
});
var $$splitComponentImporter$4 = () => import("./regulatory-q8CDYB-k.mjs");
var Route$4 = createFileRoute("/app/regulatory")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$4, "component")
});
var $$splitComponentImporter$3 = () => import("./research-DBn2wzCa.mjs");
var Route$3 = createFileRoute("/app/research")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$3, "component")
});
var $$splitComponentImporter$2 = () => import("./sales-H_UR2W9t.mjs");
var Route$2 = createFileRoute("/app/sales")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$2, "component")
});
var $$splitComponentImporter$1 = () => import("./supply-chain-B6Uupj_g.mjs");
var Route$1 = createFileRoute("/app/supply-chain")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter$1, "component")
});
var $$splitComponentImporter = () => import("./tender-Dy0b0fl_.mjs");
var Route = createFileRoute("/app/tender")({
	ssr: false,
	component: lazyRouteComponent($$splitComponentImporter, "component")
});
var IndexRoute = Route$28.update({
	id: "/",
	path: "/",
	getParentRoute: () => Route$29
});
var AppRoute = Route$27.update({
	id: "/app",
	path: "/app",
	getParentRoute: () => Route$29
});
var LoginRoute = Route$26.update({
	id: "/login",
	path: "/login",
	getParentRoute: () => Route$29
});
var SitemapDotxmlRoute = Route$25.update({
	id: "/sitemap.xml",
	path: "/sitemap.xml",
	getParentRoute: () => Route$29
});
var AppIndexRoute = Route$24.update({
	id: "/",
	path: "/",
	getParentRoute: () => AppRoute
});
var AppRouteChildren = {
	AppAnalyticsRoute: Route$23.update({
		id: "/analytics",
		path: "/analytics",
		getParentRoute: () => AppRoute
	}),
	AppApprovalsRoute: Route$22.update({
		id: "/approvals",
		path: "/approvals",
		getParentRoute: () => AppRoute
	}),
	AppAssistantRoute: Route$21.update({
		id: "/assistant",
		path: "/assistant",
		getParentRoute: () => AppRoute
	}),
	AppClinicalRoute: Route$20.update({
		id: "/clinical",
		path: "/clinical",
		getParentRoute: () => AppRoute
	}),
	AppComplianceRoute: Route$19.update({
		id: "/compliance",
		path: "/compliance",
		getParentRoute: () => AppRoute
	}),
	AppCustomerRoute: Route$18.update({
		id: "/customer",
		path: "/customer",
		getParentRoute: () => AppRoute
	}),
	AppDocsRoute: Route$17.update({
		id: "/docs",
		path: "/docs",
		getParentRoute: () => AppRoute
	}),
	AppFinanceRoute: Route$16.update({
		id: "/finance",
		path: "/finance",
		getParentRoute: () => AppRoute
	}),
	AppGrantRoute: Route$15.update({
		id: "/grant",
		path: "/grant",
		getParentRoute: () => AppRoute
	}),
	AppInvestorRoute: Route$14.update({
		id: "/investor",
		path: "/investor",
		getParentRoute: () => AppRoute
	}),
	AppManufacturingRoute: Route$13.update({
		id: "/manufacturing",
		path: "/manufacturing",
		getParentRoute: () => AppRoute
	}),
	AppMarketingRoute: Route$12.update({
		id: "/marketing",
		path: "/marketing",
		getParentRoute: () => AppRoute
	}),
	AppMeetingsRoute: Route$11.update({
		id: "/meetings",
		path: "/meetings",
		getParentRoute: () => AppRoute
	}),
	AppNotificationsRoute: Route$10.update({
		id: "/notifications",
		path: "/notifications",
		getParentRoute: () => AppRoute
	}),
	AppPatentRoute: Route$9.update({
		id: "/patent",
		path: "/patent",
		getParentRoute: () => AppRoute
	}),
	AppPeopleRoute: Route$8.update({
		id: "/people",
		path: "/people",
		getParentRoute: () => AppRoute
	}),
	AppProcurementRoute: Route$7.update({
		id: "/procurement",
		path: "/procurement",
		getParentRoute: () => AppRoute
	}),
	AppProjectsRoute: Route$6.update({
		id: "/projects",
		path: "/projects",
		getParentRoute: () => AppRoute
	}),
	AppQualityRoute: Route$5.update({
		id: "/quality",
		path: "/quality",
		getParentRoute: () => AppRoute
	}),
	AppRegulatoryRoute: Route$4.update({
		id: "/regulatory",
		path: "/regulatory",
		getParentRoute: () => AppRoute
	}),
	AppResearchRoute: Route$3.update({
		id: "/research",
		path: "/research",
		getParentRoute: () => AppRoute
	}),
	AppSalesRoute: Route$2.update({
		id: "/sales",
		path: "/sales",
		getParentRoute: () => AppRoute
	}),
	AppSupplyChainRoute: Route$1.update({
		id: "/supply-chain",
		path: "/supply-chain",
		getParentRoute: () => AppRoute
	}),
	AppTenderRoute: Route.update({
		id: "/tender",
		path: "/tender",
		getParentRoute: () => AppRoute
	}),
	AppIndexRoute
};
var rootRouteChildren = {
	IndexRoute,
	AppRoute: AppRoute._addFileChildren(AppRouteChildren),
	LoginRoute,
	SitemapDotxmlRoute
};
var routeTree = Route$29._addFileChildren(rootRouteChildren)._addFileTypes();
var getRouter = () => {
	const queryClient = new QueryClient();
	return createRouter({
		routeTree,
		context: { queryClient },
		scrollRestoration: true,
		defaultPreloadStaleTime: 0
	});
};
//#endregion
export { getRouter };
