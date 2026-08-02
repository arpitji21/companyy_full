import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { EmptyState, ErrorState, Meter, Panel, StatCard, StatusBadge, money } from "@/components/console/Primitives";
import { orbit, type ApprovalRead } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/")({
  ssr: false,
  component: Overview,
});

function Overview() {
  const qc = useQueryClient();
  const dash = useQuery({ queryKey: ["ceo-dashboard"], queryFn: orbit.ceoDashboard, retry: false });

  const decide = useMutation({
    mutationFn: ({ id, approve }: { id: string; approve: boolean }) =>
      orbit.decideApproval(id, approve),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
      void qc.invalidateQueries({ queryKey: ["approvals"] });
      void qc.invalidateQueries({ queryKey: ["notifications"] });
    },
  });

  if (dash.isLoading) return <p className="text-quiet text-[13px]">Loading dashboard…</p>;
  if (dash.error) return <ErrorState error={dash.error} />;
  const d = dash.data!;

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Executive</p>
        <h1 className="display mt-2 text-3xl">Company overview</h1>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Revenue" value={money(d.revenue)} />
        <StatCard label="Expenses" value={money(d.expenses)} />
        <StatCard label="Cash flow" value={money(d.cash_flow)} accent />
        <StatCard label="Burn rate" value={money(d.burn_rate)} hint="avg. monthly" />
      </div>

      <Panel
        title="Action center"
        subtitle="Requests waiting on you — approve or reject right here, from any department."
      >
        {d.action_items?.length ? (
          <ul className="divide-y divide-[color:var(--hairline)]">
            {d.action_items.map((a) => (
              <ActionItemRow
                key={a.id}
                approval={a}
                onDecide={(approve) => decide.mutate({ id: a.id, approve })}
                busy={decide.isPending}
              />
            ))}
          </ul>
        ) : (
          <EmptyState message="Nothing needs your sign-off right now." />
        )}
      </Panel>

      <div className="grid gap-6 lg:grid-cols-3">
        <Panel title="Health score" subtitle="Composite operational health">
          <p className="display text-5xl">{d.company_health_score?.toFixed(0)}</p>
          <div className="mt-6 space-y-4">
            {Object.entries(d.health_score_breakdown ?? {}).map(([k, v]) => (
              <Meter key={k} label={k} value={Number(v)} />
            ))}
          </div>
        </Panel>

        <Panel title="Risk score" subtitle="Weighted exposure across domains">
          <p className="display text-5xl text-[color:var(--crimson-soft)]">
            {d.risk_score?.toFixed(0)}
          </p>
          <div className="mt-6 space-y-4">
            {Object.entries(d.risk_score_breakdown ?? {}).map(([k, v]) => (
              <Meter key={k} label={k} value={Number(v)} />
            ))}
          </div>
        </Panel>

        <div className="space-y-6">
          <Panel title="Attention">
            <ul className="space-y-3 text-[13px]">
              <Row label="Pending approvals" value={d.pending_approvals} />
              <Row label="Open tasks" value={d.open_tasks} />
              <Row label="Unread notifications" value={d.unread_notifications} />
              <Row label="Compliance score" value={`${Number(d.compliance_score).toFixed(0)}%`} />
            </ul>
          </Panel>
          <Panel title="Workforce">
            <ul className="space-y-3 text-[13px]">
              <Row label="Employees" value={d.employee_count} />
              {Object.entries(d.hiring_status ?? {}).map(([k, v]) => (
                <Row key={k} label={k.replace(/_/g, " ")} value={v} />
              ))}
            </ul>
          </Panel>
        </div>
      </div>

      <Panel title="Upcoming meetings">
        {d.upcoming_meetings?.length ? (
          <ul className="divide-y divide-[color:var(--hairline)]">
            {d.upcoming_meetings.map((m) => (
              <li key={m.id} className="flex items-center justify-between py-3 text-[13px]">
                <span>{m.title}</span>
                <span className="text-quiet font-mono text-[12px]">
                  {new Date(m.starts_at).toLocaleString()}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <EmptyState message="No meetings scheduled." />
        )}
      </Panel>
    </div>
  );
}

function ActionItemRow({
  approval,
  onDecide,
  busy,
}: {
  approval: ApprovalRead;
  onDecide: (approve: boolean) => void;
  busy: boolean;
}) {
  const [acted, setActed] = useState(false);

  return (
    <li className="flex flex-col gap-3 py-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-[13px] font-medium">{approval.title}</p>
        <div className="text-quiet mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-[12px]">
          {approval.amount !== null && <span className="font-mono">{money(approval.amount)}</span>}
          {approval.notes && <span>{approval.notes}</span>}
        </div>
      </div>
      <div className="flex shrink-0 items-center gap-3">
        {acted ? (
          <StatusBadge status={approval.status} />
        ) : (
          <div className="flex items-center gap-2">
            <button
              disabled={busy}
              onClick={() => {
                setActed(true);
                onDecide(true);
              }}
              className="rounded-full bg-primary px-3.5 py-1.5 text-[12px] font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              Approve
            </button>
            <button
              disabled={busy}
              onClick={() => {
                setActed(true);
                onDecide(false);
              }}
              className="rounded-full border border-[color:var(--hairline)] px-3.5 py-1.5 text-[12px] transition-colors hover:bg-[color:var(--surface-elevated)] disabled:opacity-50"
            >
              Reject
            </button>
          </div>
        )}
      </div>
    </li>
  );
}

function Row({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <li className="flex items-center justify-between">
      <span className="text-quiet capitalize">{label}</span>
      <span className="font-mono">{value}</span>
    </li>
  );
}
