import { r as __toESM } from "../_runtime.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { t as lark_logo_default } from "./lark-logo-DONZ3N_a.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/routes-DNATJfP5.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
var links = [
	{
		label: "Platform",
		href: "#platform"
	},
	{
		label: "Modules",
		href: "#modules"
	},
	{
		label: "Intelligence",
		href: "#intelligence"
	},
	{
		label: "Architecture",
		href: "#architecture"
	}
];
function SiteNav() {
	const [solid, setSolid] = (0, import_react.useState)(false);
	(0, import_react.useEffect)(() => {
		const onScroll = () => setSolid(window.scrollY > 24);
		onScroll();
		window.addEventListener("scroll", onScroll, { passive: true });
		return () => window.removeEventListener("scroll", onScroll);
	}, []);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("header", {
		className: "fixed inset-x-0 top-0 z-50 transition-all duration-500",
		style: {
			backgroundColor: solid ? "color-mix(in oklab, var(--background) 72%, transparent)" : "transparent",
			backdropFilter: solid ? "blur(22px) saturate(180%)" : "none",
			borderBottom: solid ? "1px solid var(--hairline)" : "1px solid transparent"
		},
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("nav", {
			className: "mx-auto flex h-14 max-w-6xl items-center justify-between px-6",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("a", {
					href: "#top",
					className: "flex items-center gap-2.5",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("img", {
						src: lark_logo_default,
						alt: "Lark Healthcare",
						className: "h-7 w-7 object-contain"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
						className: "text-[13px] font-semibold tracking-tight",
						children: ["Orbit", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-quiet font-normal",
							children: " by LarkAI"
						})]
					})]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "hidden items-center gap-9 md:flex",
					children: links.map((l) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("a", {
						href: l.href,
						className: "text-quiet text-[12.5px] transition-colors hover:text-foreground",
						children: l.label
					}, l.href))
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "flex items-center gap-4",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("a", {
						href: "/login",
						className: "text-quiet text-[12.5px] transition-colors hover:text-foreground",
						children: "Sign in"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("a", {
						href: "#request",
						className: "rounded-full bg-primary px-4 py-1.5 text-[12.5px] font-semibold text-primary-foreground transition-transform duration-300 hover:scale-[1.04]",
						children: "Request access"
					})]
				})
			]
		})
	});
}
var hero_orbit_default = "/assets/hero-orbit-BYWokdGg.jpg";
function Hero() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
		id: "top",
		className: "relative overflow-hidden pt-36 pb-10",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { className: "halo pointer-events-none absolute inset-x-0 top-0 h-[720px]" }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "relative mx-auto max-w-6xl px-6 text-center",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "reveal inline-flex items-center gap-2.5 rounded-full border border-border px-3.5 py-1.5",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("img", {
							src: lark_logo_default,
							alt: "",
							"aria-hidden": true,
							className: "h-4 w-4 object-contain"
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-[11.5px] tracking-wide text-quiet",
							children: "Lark Healthcare · Enterprise Intelligence Platform"
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h1", {
						className: "display reveal mx-auto mt-8 max-w-4xl text-[clamp(2.9rem,8vw,6.2rem)]",
						style: { animationDelay: "80ms" },
						children: [
							"One system.",
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("br", {}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-quiet",
								children: "Every department."
							})
						]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "reveal mx-auto mt-7 max-w-xl text-[17px] leading-relaxed text-quiet",
						style: { animationDelay: "160ms" },
						children: "Orbit unifies finance, manufacturing, quality, compliance and supply chain into a single operating layer — governed by AI agents that read your live enterprise data."
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "reveal mt-10 flex flex-wrap items-center justify-center gap-3",
						style: { animationDelay: "240ms" },
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("a", {
							href: "#request",
							className: "rounded-full bg-primary px-6 py-3 text-[13.5px] font-semibold text-primary-foreground transition-transform duration-300 hover:scale-[1.03]",
							style: { boxShadow: "var(--shadow-crimson)" },
							children: "Request access"
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("a", {
							href: "#platform",
							className: "rounded-full border border-border px-6 py-3 text-[13.5px] font-medium transition-colors hover:bg-accent",
							children: "See the platform"
						})]
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "relative mx-auto mt-16 max-w-5xl px-6",
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "reveal overflow-hidden rounded-3xl border border-border",
					style: {
						animationDelay: "320ms",
						boxShadow: "var(--shadow-lift)"
					},
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("img", {
						src: hero_orbit_default,
						alt: "Orbit enterprise dashboard rendered in dark glass with crimson data highlights",
						width: 1600,
						height: 1008,
						className: "w-full"
					})
				})
			})
		]
	});
}
function Reveal({ children, delay = 0, className = "" }) {
	const ref = (0, import_react.useRef)(null);
	const [shown, setShown] = (0, import_react.useState)(false);
	(0, import_react.useEffect)(() => {
		const el = ref.current;
		if (!el) return;
		const io = new IntersectionObserver(([entry]) => {
			if (entry.isIntersecting) {
				setShown(true);
				io.disconnect();
			}
		}, { threshold: .12 });
		io.observe(el);
		return () => io.disconnect();
	}, []);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		ref,
		className,
		style: {
			opacity: shown ? 1 : 0,
			transform: shown ? "none" : "translateY(28px)",
			transition: `opacity .9s var(--ease-apple) ${delay}ms, transform .9s var(--ease-apple) ${delay}ms`
		},
		children
	});
}
var stats = [
	{
		value: "22",
		label: "Live API modules"
	},
	{
		value: "30+",
		label: "Governed data tables"
	},
	{
		value: "4",
		label: "LLM providers wired"
	},
	{
		value: "<120ms",
		label: "Median API response"
	}
];
function Stats() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("section", {
		className: "mx-auto max-w-6xl px-6 py-24",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "grid grid-cols-2 gap-px overflow-hidden rounded-3xl border border-border bg-border md:grid-cols-4",
			children: stats.map((s, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Reveal, {
				delay: i * 80,
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "h-full bg-background px-7 py-10",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "display text-[clamp(2rem,4vw,2.9rem)]",
						children: s.value
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-2 text-[12.5px] text-quiet",
						children: s.label
					})]
				})
			}, s.label))
		})
	});
}
function Platform() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
		id: "platform",
		className: "mx-auto max-w-6xl px-6 py-28",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Reveal, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
			className: "eyebrow",
			children: "The platform"
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h2", {
			className: "display mt-5 max-w-3xl text-[clamp(2.1rem,5vw,3.6rem)]",
			children: [
				"Precision infrastructure for",
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("br", {}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "text-quiet",
					children: "regulated healthcare."
				})
			]
		})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "mt-14 grid gap-4 lg:grid-cols-3",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Reveal, {
				className: "lg:col-span-2",
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "glass h-full rounded-3xl p-10",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h3", {
							className: "text-[22px] font-semibold tracking-tight",
							children: "A single source of operational truth"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-4 max-w-lg text-[14.5px] leading-relaxed text-quiet",
							children: "Batch yields, budget variance, vendor risk and compliance posture stop living in separate spreadsheets. Orbit models them once, then exposes them everywhere — the CEO dashboard, the approval queue, and the agents."
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mt-10 grid gap-6 sm:grid-cols-3",
							children: [
								["Real-time", "Aggregations computed on request, never stale"],
								["Governed", "Role-based permissions on every endpoint"],
								["Traceable", "Structured logs from edge to database row"]
							].map(([t, d]) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "text-[14px] font-semibold",
								children: t
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mt-1.5 text-[12.5px] leading-relaxed text-quiet",
								children: d
							})] }, t))
						})
					]
				})
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Reveal, {
				delay: 120,
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "glass flex h-full flex-col justify-between rounded-3xl p-10",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("img", {
						src: lark_logo_default,
						alt: "Lark Healthcare",
						className: "h-12 w-12 object-contain drift"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mt-12",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h3", {
							className: "text-[18px] font-semibold leading-snug tracking-tight",
							children: "Built for Lark Healthcare"
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-3 text-[13.5px] leading-relaxed text-quiet",
							children: "Designed around pharmaceutical operations — from CDSCO submissions to line-level batch quality."
						})]
					})]
				})
			})]
		})]
	});
}
var modules = [
	{
		title: "Finance",
		body: "Transactions, budgets, cash-flow and margin summaries reconciled in real time."
	},
	{
		title: "Manufacturing",
		body: "Batch records and yield analytics across every production line."
	},
	{
		title: "Quality",
		body: "Checks, pass-rate metrics and deviation trails ready for audit."
	},
	{
		title: "Compliance & Regulatory",
		body: "FDA, CDSCO, ISO and MDR submissions scored on one compliance index."
	},
	{
		title: "Supply Chain",
		body: "Vendors, inventory positions and automatic reorder alerts."
	},
	{
		title: "Sales & Marketing",
		body: "Pipeline forecasting alongside campaign ROI and conversion."
	},
	{
		title: "People",
		body: "Employees, headcount summaries and a living org chart."
	},
	{
		title: "Projects",
		body: "Nested tasks, ownership and delivery status across programs."
	},
	{
		title: "Executive",
		body: "A single CEO dashboard aggregating every department signal."
	}
];
function Modules() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
		id: "modules",
		className: "mx-auto max-w-6xl px-6 py-28",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Reveal, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
			className: "eyebrow",
			children: "Coverage"
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h2", {
			className: "display mt-5 max-w-2xl text-[clamp(2.1rem,5vw,3.6rem)]",
			children: [
				"Built for the whole",
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("br", {}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "text-quiet",
					children: "operating surface."
				})
			]
		})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "mt-14 grid gap-4 sm:grid-cols-2 lg:grid-cols-3",
			children: modules.map((m, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Reveal, {
				delay: i % 3 * 90,
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("article", {
					className: "group h-full rounded-2xl border border-border bg-surface p-7 transition-all duration-500 hover:-translate-y-1",
					style: { transitionTimingFunction: "var(--ease-apple)" },
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { className: "h-1 w-8 rounded-full bg-crimson opacity-70 transition-all duration-500 group-hover:w-14 group-hover:opacity-100" }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h3", {
							className: "mt-6 text-[17px] font-semibold tracking-tight",
							children: m.title
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-2.5 text-[13.5px] leading-relaxed text-quiet",
							children: m.body
						})
					]
				})
			}, m.title))
		})]
	});
}
var pillars = [
	{
		k: "01",
		title: "Agents that read your ledger",
		body: "Department agents are grounded in live tables — not documents. Ask for the yield drop behind last quarter's margin, and the answer cites the batches."
	},
	{
		k: "02",
		title: "Provider-agnostic reasoning",
		body: "OpenAI, Claude, Gemini or a private Ollama model, swapped behind one factory. Sensitive workloads never have to leave your perimeter."
	},
	{
		k: "03",
		title: "Approvals with a paper trail",
		body: "Every agent recommendation becomes a routed approval — requested, reviewed, resolved, and permanently recorded."
	}
];
function Intelligence() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
		id: "intelligence",
		className: "relative overflow-hidden py-28",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { className: "halo pointer-events-none absolute inset-x-0 top-1/4 h-[520px] opacity-60" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "relative mx-auto max-w-6xl px-6",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Reveal, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: "Intelligence layer"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h2", {
				className: "display mt-5 max-w-3xl text-[clamp(2.1rem,5vw,3.6rem)]",
				children: ["The enterprise, ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "text-quiet",
					children: "answerable."
				})]
			})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "mt-16 grid gap-10 md:grid-cols-3",
				children: pillars.map((p, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Reveal, {
					delay: i * 110,
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "hairline-t pt-7",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "font-mono text-[12px] text-crimson",
								children: p.k
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h3", {
								className: "mt-5 text-[19px] font-semibold leading-snug tracking-tight",
								children: p.title
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
								className: "mt-3 text-[13.5px] leading-relaxed text-quiet",
								children: p.body
							})
						]
					})
				}, p.k))
			})]
		})]
	});
}
var rows = [
	{
		layer: "Edge",
		detail: "Rate limiting, structured request logging, unified exception envelope"
	},
	{
		layer: "API",
		detail: "FastAPI v1 router — 22 department routers under a single versioned prefix"
	},
	{
		layer: "Domain",
		detail: "Service layer per department, isolated from transport concerns"
	},
	{
		layer: "Data",
		detail: "Repository pattern over PostgreSQL, migrated with Alembic"
	},
	{
		layer: "Async",
		detail: "Celery workers on Redis for scheduled and long-running work"
	},
	{
		layer: "Identity",
		detail: "JWT auth with refresh rotation and role-based permissions"
	}
];
function Architecture() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("section", {
		id: "architecture",
		className: "mx-auto max-w-6xl px-6 py-28",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "grid gap-16 lg:grid-cols-[0.85fr_1.15fr]",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Reveal, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "lg:sticky lg:top-28",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "eyebrow",
						children: "Architecture"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h2", {
						className: "display mt-5 text-[clamp(2.1rem,5vw,3.4rem)]",
						children: [
							"Layered.",
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("br", {}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-quiet",
								children: "Auditable."
							})
						]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-6 max-w-sm text-[14px] leading-relaxed text-quiet",
						children: "Orbit is engineered the way regulated manufacturers are inspected — every request traceable from the edge down to the row it changed."
					})
				]
			}) }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { children: rows.map((r, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Reveal, {
				delay: i * 70,
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "hairline-t group flex flex-col gap-1.5 py-6 transition-colors duration-500 sm:flex-row sm:items-baseline sm:gap-10",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
						className: "w-24 shrink-0 font-mono text-[12px] uppercase tracking-widest text-crimson",
						children: r.layer
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
						className: "text-[15px] leading-relaxed text-quiet transition-colors duration-500 group-hover:text-foreground",
						children: r.detail
					})]
				})
			}, r.layer)) })]
		})
	});
}
function CallToAction() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
		id: "request",
		className: "relative overflow-hidden py-32",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { className: "halo pointer-events-none absolute inset-x-0 bottom-0 h-[560px] rotate-180" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "relative mx-auto max-w-3xl px-6 text-center",
			children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Reveal, { children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h2", {
					className: "display text-[clamp(2.4rem,6vw,4.4rem)]",
					children: [
						"Bring your enterprise",
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("br", {}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-quiet",
							children: "into orbit."
						})
					]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "mx-auto mt-6 max-w-md text-[15px] leading-relaxed text-quiet",
					children: "Private deployments for regulated manufacturers. Talk to the LarkAI team about a rollout."
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("form", {
					className: "mx-auto mt-10 flex max-w-md flex-col gap-3 sm:flex-row",
					onSubmit: (e) => e.preventDefault(),
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("label", {
							htmlFor: "work-email",
							className: "sr-only",
							children: "Work email"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("input", {
							id: "work-email",
							type: "email",
							required: true,
							placeholder: "you@company.com",
							className: "h-12 flex-1 rounded-full border border-input bg-surface px-5 text-[14px] outline-none transition-colors placeholder:text-muted-foreground focus:border-ring"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
							type: "submit",
							className: "h-12 rounded-full bg-primary px-7 text-[13.5px] font-semibold text-primary-foreground transition-transform duration-300 hover:scale-[1.03]",
							style: { boxShadow: "var(--shadow-crimson)" },
							children: "Request access"
						})
					]
				})
			] })
		})]
	});
}
function SiteFooter() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("footer", {
		className: "hairline-t",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 py-10 sm:flex-row",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "flex items-center gap-2.5",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("img", {
					src: lark_logo_default,
					alt: "Lark Healthcare",
					className: "h-6 w-6 object-contain"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
					className: "text-[12.5px] text-quiet",
					children: ["LarkAI Orbit — Lark Healthcare · © ", (/* @__PURE__ */ new Date()).getFullYear()]
				})]
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "text-[12.5px] text-quiet",
				children: "Chennai · India"
			})]
		})
	});
}
function Index() {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "min-h-screen bg-background",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SiteNav, {}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("main", { children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Hero, {}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Stats, {}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Platform, {}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Modules, {}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Intelligence, {}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Architecture, {}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CallToAction, {})
			] }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SiteFooter, {})
		]
	});
}
//#endregion
export { Index as component };
