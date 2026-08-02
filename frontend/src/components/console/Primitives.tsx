import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Panel({
  title,
  subtitle,
  action,
  className,
  children,
}: {
  title?: string;
  subtitle?: string;
  action?: ReactNode;
  className?: string;
  children: ReactNode;
}) {
  return (
    <section className={cn("glass rounded-2xl p-6", className)}>
      {(title || action) && (
        <header className="mb-5 flex items-start justify-between gap-4">
          <div>
            {title && <h2 className="text-[15px] font-semibold tracking-tight">{title}</h2>}
            {subtitle && <p className="text-quiet mt-1 text-[12.5px]">{subtitle}</p>}
          </div>
          {action}
        </header>
      )}
      {children}
    </section>
  );
}

export function StatCard({
  label,
  value,
  hint,
  accent,
}: {
  label: string;
  value: ReactNode;
  hint?: string;
  accent?: boolean;
}) {
  return (
    <div className="glass rounded-2xl p-5">
      <p className="eyebrow">{label}</p>
      <p
        className={cn(
          "display mt-3 text-3xl",
          accent ? "text-[color:var(--crimson-soft)]" : "text-foreground",
        )}
      >
        {value}
      </p>
      {hint && <p className="text-quiet mt-2 text-[12px]">{hint}</p>}
    </div>
  );
}

export function Meter({ label, value }: { label: string; value: number }) {
  const pct = Math.max(0, Math.min(100, value));
  return (
    <div>
      <div className="mb-2 flex items-baseline justify-between">
        <span className="text-[12.5px] capitalize">{label.replace(/_/g, " ")}</span>
        <span className="text-quiet font-mono text-[12px]">{pct.toFixed(0)}</span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-[color:var(--surface-elevated)]">
        <div
          className="h-full rounded-full bg-primary transition-[width] duration-700"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

export function EmptyState({ message }: { message: string }) {
  return (
    <div className="text-quiet rounded-xl border border-dashed border-[color:var(--hairline)] px-5 py-10 text-center text-[13px]">
      {message}
    </div>
  );
}

export function ErrorState({ error }: { error: unknown }) {
  const message = error instanceof Error ? error.message : "Unable to reach the Orbit API.";
  return (
    <div className="rounded-xl border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-5 py-6 text-[13px]">
      <p className="font-semibold text-[color:var(--crimson-soft)]">Request failed</p>
      <p className="text-quiet mt-1">{message}</p>
    </div>
  );
}

export function money(n: number | string | undefined, currency = "USD") {
  const v = typeof n === "string" ? Number(n) : (n ?? 0);
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(Number.isFinite(v) ? v : 0);
}

export function fileSize(bytes: number | null | undefined) {
  if (bytes === null || bytes === undefined || !Number.isFinite(bytes)) return "—";
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB", "TB"];
  let value = bytes / 1024;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${value.toFixed(1)} ${units[unit]}`;
}

export function pct(n: number | string | null | undefined, digits = 0) {
  const v = typeof n === "string" ? Number(n) : n;
  if (v === null || v === undefined || !Number.isFinite(v)) return "—";
  return `${v.toFixed(digits)}%`;
}

const POSITIVE = ["approved", "completed", "won", "active", "pass", "resolved", "delivered"];
const NEGATIVE = ["rejected", "expired", "lost", "fail", "failed", "at_risk", "high", "critical", "cancelled"];
const PENDING = ["pending", "in_progress", "in progress", "draft", "planning", "review"];

export function StatusBadge({ status }: { status: string | null | undefined }) {
  const s = (status ?? "unknown").toLowerCase().replace(/-/g, "_");
  const tone = POSITIVE.some((k) => s.includes(k))
    ? "positive"
    : NEGATIVE.some((k) => s.includes(k))
      ? "negative"
      : PENDING.some((k) => s.includes(k))
        ? "pending"
        : "neutral";

  const toneClass = {
    positive: "bg-[color-mix(in_oklab,oklch(0.72_0.19_150)_18%,transparent)] text-[oklch(0.78_0.17_150)]",
    negative: "bg-[color-mix(in_oklab,var(--crimson)_18%,transparent)] text-[color:var(--crimson-soft)]",
    pending: "bg-[color-mix(in_oklab,oklch(0.8_0.15_85)_18%,transparent)] text-[oklch(0.82_0.14_85)]",
    neutral: "bg-[color:var(--surface-elevated)] text-quiet",
  }[tone];

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-1 text-[11px] font-medium capitalize",
        toneClass,
      )}
    >
      {(status ?? "unknown").replace(/_/g, " ")}
    </span>
  );
}
