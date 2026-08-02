import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useRef, useState, type FormEvent } from "react";
import { ErrorState, Panel } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/assistant")({
  ssr: false,
  component: AssistantPage,
});

interface Turn {
  role: "user" | "assistant";
  content: string;
}

function AssistantPage() {
  const agents = useQuery({ queryKey: ["agents"], queryFn: orbit.agents, retry: false });
  const [agentId, setAgentId] = useState<string | null>(null);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const conversationId = useRef<string | null>(null);

  async function send(e: FormEvent) {
    e.preventDefault();
    const message = input.trim();
    if (!message || busy) return;
    setInput("");
    setError(null);
    setTurns((t) => [...t, { role: "user", content: message }]);
    setBusy(true);
    try {
      const res = await orbit.chat({
        message,
        conversation_id: conversationId.current,
        agent_id: agentId ?? (agents.data?.[0]?.id ?? null),
      });
      conversationId.current = res.conversation_id;
      setTurns((t) => [...t, { role: "assistant", content: res.message.content }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "The agent could not respond.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Intelligence</p>
        <h1 className="display mt-2 text-3xl">AI assistant</h1>
      </div>

      {agents.error && <ErrorState error={agents.error} />}

      {agents.data && agents.data.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {agents.data.map((a) => {
            const active = (agentId ?? agents.data[0].id) === a.id;
            return (
              <button
                key={a.id}
                onClick={() => {
                  setAgentId(a.id);
                  conversationId.current = null;
                  setTurns([]);
                }}
                className={`rounded-full border px-3.5 py-1.5 text-[12px] transition-colors ${
                  active
                    ? "border-transparent bg-primary text-primary-foreground"
                    : "text-quiet border-[color:var(--hairline)] hover:text-foreground"
                }`}
              >
                {a.name}
                <span className="ml-2 opacity-60">{a.provider}</span>
              </button>
            );
          })}
        </div>
      )}

      <Panel title="Conversation" subtitle="Routed through the Orbit agent brain">
        <div className="min-h-64 space-y-4">
          {turns.length === 0 && (
            <p className="text-quiet text-[13px]">
              Ask about finance, compliance, manufacturing or people — the agent has enterprise
              context.
            </p>
          )}
          {turns.map((t, i) => (
            <div
              key={i}
              className={`max-w-[85%] rounded-2xl px-4 py-3 text-[13px] leading-relaxed ${
                t.role === "user"
                  ? "ml-auto bg-primary text-primary-foreground"
                  : "bg-[color:var(--surface-elevated)]"
              }`}
            >
              {t.content}
            </div>
          ))}
          {busy && <p className="text-quiet text-[12.5px]">Thinking…</p>}
          {error && <p className="text-[12.5px] text-[color:var(--crimson-soft)]">{error}</p>}
        </div>

        <form onSubmit={send} className="mt-6 flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Orbit…"
            className="flex-1 rounded-full border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-4 py-2.5 text-[13px] outline-none focus:border-[color:var(--crimson)]"
          />
          <button
            type="submit"
            disabled={busy}
            className="rounded-full bg-primary px-5 py-2.5 text-[13px] font-semibold text-primary-foreground disabled:opacity-50"
          >
            Send
          </button>
        </form>
      </Panel>
    </div>
  );
}
