import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/customer")({
  ssr: false,
  component: CustomerPage,
});

function CustomerPage() {
  const summary = useQuery({ queryKey: ["customer-summary"], queryFn: orbit.customerSummary, retry: false });
  const tickets = useQuery({
    queryKey: ["support-tickets"],
    queryFn: () => orbit.supportTickets(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Customer</p>
        <h1 className="display mt-2 text-3xl">Customer support & success</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Open tickets" value={String(summary.data.open_tickets)} accent />
          <StatCard label="Escalated" value={String(summary.data.escalated_tickets)} />
          <StatCard label="SLA breached" value={String(summary.data.breached_sla)} />
          <StatCard label="At-risk accounts" value={String(summary.data.at_risk_customers)} />
        </div>
      )}
      {summary.data?.average_csat != null && (
        <div className="rounded-xl border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-5 py-4 text-[13px]">
          Average CSAT across resolved tickets: <span className="font-semibold">{summary.data.average_csat.toFixed(2)} / 5</span>
        </div>
      )}

      <Panel title="Support tickets" subtitle={tickets.data ? `${tickets.data.total} total` : undefined}>
        {tickets.error ? (
          <ErrorState error={tickets.error} />
        ) : tickets.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Subject</th>
                  <th className="py-2.5 pr-4 font-medium">Priority</th>
                  <th className="py-2.5 pr-4 font-medium">SLA due</th>
                  <th className="py-2.5 pr-4 font-medium">CSAT</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {tickets.data.items.map((t) => (
                  <tr key={t.id}>
                    <td className="py-3 pr-4 font-medium">{t.subject}</td>
                    <td className="text-quiet py-3 pr-4 capitalize">{t.priority}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {t.sla_due_at ? new Date(t.sla_due_at).toLocaleString() : "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {t.csat_score !== null ? `${t.csat_score} / 5` : "—"}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={t.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : tickets.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No support tickets recorded." />
        )}
      </Panel>
    </div>
  );
}
