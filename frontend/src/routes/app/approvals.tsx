import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, money } from "@/components/console/Primitives";
import { orbit, type ApprovalRead } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/approvals")({
  ssr: false,
  component: ApprovalsPage,
});

function ApprovalsPage() {
  const qc = useQueryClient();
  const approvals = useQuery({
    queryKey: ["approvals"],
    queryFn: () => orbit.approvals(1, 50),
    retry: false,
  });

  const decide = useMutation({
    mutationFn: ({ id, approve }: { id: string; approve: boolean }) =>
      orbit.decideApproval(id, approve),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["approvals"] }),
  });

  const items = approvals.data?.items ?? [];
  const pending = items.filter((a) => a.status === "pending");

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Approvals</p>
        <h1 className="display mt-2 text-3xl">Requests & sign-off</h1>
      </div>

      {approvals.data && (
        <div className="grid gap-4 sm:grid-cols-3">
          <StatCard label="Total" value={String(approvals.data.total)} />
          <StatCard label="Pending" value={String(pending.length)} accent={pending.length > 0} />
          <StatCard
            label="Requested value"
            value={money(items.reduce((n, a) => n + Number(a.amount ?? 0), 0))}
          />
        </div>
      )}

      <Panel title="Requests" subtitle={approvals.data ? `${approvals.data.total} total` : undefined}>
        {approvals.error ? (
          <ErrorState error={approvals.error} />
        ) : items.length ? (
          <ul className="divide-y divide-[color:var(--hairline)]">
            {items.map((a) => (
              <ApprovalRow
                key={a.id}
                approval={a}
                onDecide={(approve) => decide.mutate({ id: a.id, approve })}
                busy={decide.isPending}
              />
            ))}
          </ul>
        ) : approvals.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No approval requests." />
        )}
      </Panel>
    </div>
  );
}

function ApprovalRow({
  approval,
  onDecide,
  busy,
}: {
  approval: ApprovalRead;
  onDecide: (approve: boolean) => void;
  busy: boolean;
}) {
  const [acted, setActed] = useState(false);
  const pending = approval.status === "pending";

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
        <StatusBadge status={approval.status} />
        {pending && (
          <div className="flex items-center gap-2">
            <button
              disabled={busy || acted}
              onClick={() => {
                setActed(true);
                onDecide(true);
              }}
              className="rounded-full bg-primary px-3.5 py-1.5 text-[12px] font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              Approve
            </button>
            <button
              disabled={busy || acted}
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
