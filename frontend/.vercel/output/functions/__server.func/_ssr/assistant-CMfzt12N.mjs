import { r as __toESM } from "../_runtime.mjs";
import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { i as Panel, n as ErrorState } from "./Primitives-DCYrco_Z.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { n as useQuery } from "../_libs/tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/assistant-CMfzt12N.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
function AssistantPage() {
	const agents = useQuery({
		queryKey: ["agents"],
		queryFn: orbit.agents,
		retry: false
	});
	const [agentId, setAgentId] = (0, import_react.useState)(null);
	const [turns, setTurns] = (0, import_react.useState)([]);
	const [input, setInput] = (0, import_react.useState)("");
	const [busy, setBusy] = (0, import_react.useState)(false);
	const [error, setError] = (0, import_react.useState)(null);
	const conversationId = (0, import_react.useRef)(null);
	async function send(e) {
		e.preventDefault();
		const message = input.trim();
		if (!message || busy) return;
		setInput("");
		setError(null);
		setTurns((t) => [...t, {
			role: "user",
			content: message
		}]);
		setBusy(true);
		try {
			const res = await orbit.chat({
				message,
				conversation_id: conversationId.current,
				agent_id: agentId ?? agents.data?.[0]?.id ?? null
			});
			conversationId.current = res.conversation_id;
			setTurns((t) => [...t, {
				role: "assistant",
				content: res.message.content
			}]);
		} catch (err) {
			setError(err instanceof Error ? err.message : "The agent could not respond.");
		} finally {
			setBusy(false);
		}
	}
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-6",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "eyebrow",
				children: "Intelligence"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
				className: "display mt-2 text-3xl",
				children: "AI assistant"
			})] }),
			agents.error && /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ErrorState, { error: agents.error }),
			agents.data && agents.data.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "flex flex-wrap gap-2",
				children: agents.data.map((a) => {
					const active = (agentId ?? agents.data[0].id) === a.id;
					return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
						onClick: () => {
							setAgentId(a.id);
							conversationId.current = null;
							setTurns([]);
						},
						className: `rounded-full border px-3.5 py-1.5 text-[12px] transition-colors ${active ? "border-transparent bg-primary text-primary-foreground" : "text-quiet border-[color:var(--hairline)] hover:text-foreground"}`,
						children: [a.name, /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "ml-2 opacity-60",
							children: a.provider
						})]
					}, a.id);
				})
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Panel, {
				title: "Conversation",
				subtitle: "Routed through the Orbit agent brain",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "min-h-64 space-y-4",
					children: [
						turns.length === 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "text-quiet text-[13px]",
							children: "Ask about finance, compliance, manufacturing or people — the agent has enterprise context."
						}),
						turns.map((t, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: `max-w-[85%] rounded-2xl px-4 py-3 text-[13px] leading-relaxed ${t.role === "user" ? "ml-auto bg-primary text-primary-foreground" : "bg-[color:var(--surface-elevated)]"}`,
							children: t.content
						}, i)),
						busy && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "text-quiet text-[12.5px]",
							children: "Thinking…"
						}),
						error && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "text-[12.5px] text-[color:var(--crimson-soft)]",
							children: error
						})
					]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("form", {
					onSubmit: send,
					className: "mt-6 flex gap-2",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("input", {
						value: input,
						onChange: (e) => setInput(e.target.value),
						placeholder: "Ask Orbit…",
						className: "flex-1 rounded-full border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-4 py-2.5 text-[13px] outline-none focus:border-[color:var(--crimson)]"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
						type: "submit",
						disabled: busy,
						className: "rounded-full bg-primary px-5 py-2.5 text-[13px] font-semibold text-primary-foreground disabled:opacity-50",
						children: "Send"
					})]
				})]
			})
		]
	});
}
//#endregion
export { AssistantPage as component };
