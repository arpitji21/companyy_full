import { createFileRoute, useNavigate, Link } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import logo from "@/assets/lark-logo.png";
import { orbit, tokens, ORBIT_BASE_URL } from "@/lib/orbit-api";

export const Route = createFileRoute("/login")({
  ssr: false,
  head: () => ({
    meta: [
      { title: "Sign in — LarkAI Orbit Console" },
      {
        name: "description",
        content:
          "Sign in to the LarkAI Orbit console to access live finance, people, compliance and AI agent data.",
      },
      { property: "og:title", content: "Sign in — LarkAI Orbit Console" },
      {
        property: "og:description",
        content: "Secure access to the LarkAI Orbit enterprise operating system.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const pair = await orbit.login(email, password);
      tokens.set(pair.access_token, pair.refresh_token);
      await navigate({ to: "/app" });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Sign-in failed. Check the API endpoint and your credentials.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="relative flex min-h-screen items-center justify-center px-6">
      <div className="halo pointer-events-none absolute inset-0" />
      <div className="relative w-full max-w-sm">
        <Link to="/" className="mb-10 flex items-center justify-center gap-3">
          <img src={logo} alt="Lark Healthcare" className="h-9 w-9 object-contain" />
          <span className="text-[13px] font-semibold tracking-tight">
            Orbit<span className="text-quiet font-normal"> by LarkAI</span>
          </span>
        </Link>

        <div className="glass rounded-3xl p-8">
          <h1 className="display text-2xl">Sign in</h1>
          <p className="text-quiet mt-2 text-[13px]">
            Enterprise console access for LarkAI Healthcare operators.
          </p>

          <form onSubmit={onSubmit} className="mt-7 space-y-4">
            <Field
              label="Work email"
              type="email"
              value={email}
              onChange={setEmail}
              placeholder="you@larkhealthcare.ai"
            />
            <Field
              label="Password"
              type="password"
              value={password}
              onChange={setPassword}
              placeholder="••••••••"
            />

            {error && (
              <p className="rounded-lg border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-3 py-2 text-[12.5px] text-[color:var(--crimson-soft)]">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={busy}
              className="w-full rounded-full bg-primary py-2.5 text-[13px] font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              {busy ? "Signing in…" : "Continue"}
            </button>
          </form>
        </div>

        <p className="text-quiet mt-6 text-center font-mono text-[11px]">API · {ORBIT_BASE_URL}</p>
      </div>
    </main>
  );
}

function Field({
  label,
  type,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  type: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
}) {
  return (
    <label className="block">
      <span className="text-quiet mb-1.5 block text-[11.5px] font-medium">{label}</span>
      <input
        type={type}
        required
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-xl border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-3.5 py-2.5 text-[13px] outline-none transition-colors focus:border-[color:var(--crimson)]"
      />
    </label>
  );
}
