import { r as __toESM } from "../_runtime.mjs";
import { a as tokens, r as orbit, t as ORBIT_BASE_URL } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { t as lark_logo_default } from "./lark-logo-DONZ3N_a.mjs";
import { _ as useNavigate, g as Link } from "../_libs/@tanstack/react-router+[...].mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/login-DF8JFhcV.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
function LoginPage() {
	const navigate = useNavigate();
	const [email, setEmail] = (0, import_react.useState)("");
	const [password, setPassword] = (0, import_react.useState)("");
	const [error, setError] = (0, import_react.useState)(null);
	const [busy, setBusy] = (0, import_react.useState)(false);
	async function onSubmit(e) {
		e.preventDefault();
		setBusy(true);
		setError(null);
		try {
			const pair = await orbit.login(email, password);
			tokens.set(pair.access_token, pair.refresh_token);
			await navigate({ to: "/app" });
		} catch (err) {
			setError(err instanceof Error ? err.message : "Sign-in failed. Check the API endpoint and your credentials.");
		} finally {
			setBusy(false);
		}
	}
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("main", {
		className: "relative flex min-h-screen items-center justify-center px-6",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", { className: "halo pointer-events-none absolute inset-0" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "relative w-full max-w-sm",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Link, {
					to: "/",
					className: "mb-10 flex items-center justify-center gap-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("img", {
						src: lark_logo_default,
						alt: "Lark Healthcare",
						className: "h-9 w-9 object-contain"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
						className: "text-[13px] font-semibold tracking-tight",
						children: ["Orbit", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-quiet font-normal",
							children: " by LarkAI"
						})]
					})]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "glass rounded-3xl p-8",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
							className: "display text-2xl",
							children: "Sign in"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "text-quiet mt-2 text-[13px]",
							children: "Enterprise console access for LarkAI Healthcare operators."
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("form", {
							onSubmit,
							className: "mt-7 space-y-4",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Field, {
									label: "Work email",
									type: "email",
									value: email,
									onChange: setEmail,
									placeholder: "you@larkhealthcare.ai"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Field, {
									label: "Password",
									type: "password",
									value: password,
									onChange: setPassword,
									placeholder: "••••••••"
								}),
								error && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
									className: "rounded-lg border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-3 py-2 text-[12.5px] text-[color:var(--crimson-soft)]",
									children: error
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
									type: "submit",
									disabled: busy,
									className: "w-full rounded-full bg-primary py-2.5 text-[13px] font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-50",
									children: busy ? "Signing in…" : "Continue"
								})
							]
						})
					]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
					className: "text-quiet mt-6 text-center font-mono text-[11px]",
					children: ["API · ", ORBIT_BASE_URL]
				})
			]
		})]
	});
}
function Field({ label, type, value, onChange, placeholder }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", {
		className: "block",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
			className: "text-quiet mb-1.5 block text-[11.5px] font-medium",
			children: label
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("input", {
			type,
			required: true,
			value,
			placeholder,
			onChange: (e) => onChange(e.target.value),
			className: "w-full rounded-xl border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-3.5 py-2.5 text-[13px] outline-none transition-colors focus:border-[color:var(--crimson)]"
		})]
	});
}
//#endregion
export { LoginPage as component };
