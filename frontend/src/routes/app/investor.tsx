import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, money } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/investor")({
  ssr: false,
  component: InvestorPage,
});

function InvestorPage() {
  const summary = useQuery({ queryKey: ["investor-summary"], queryFn: orbit.investorSummary, retry: false });
  const rounds = useQuery({ queryKey: ["funding-rounds"], queryFn: () => orbit.fundingRounds(1, 25), retry: false });
  const updates = useQuery({ queryKey: ["investor-updates"], queryFn: () => orbit.investorUpdates(1, 25), retry: false });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Investor</p>
        <h1 className="display mt-2 text-3xl">Investor relations</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Total raised" value={money(summary.data.total_raised)} accent />
          <StatCard
            label="Latest valuation"
            value={summary.data.latest_post_money_valuation !== null ? money(summary.data.latest_post_money_valuation) : "—"}
          />
          <StatCard label="Open rounds" value={String(summary.data.open_rounds)} />
          <StatCard label="Next report due" value={summary.data.next_report_due_date ?? "—"} />
        </div>
      )}

      <Panel title="Funding rounds" subtitle={rounds.data ? `${rounds.data.total} total` : undefined}>
        {rounds.error ? (
          <ErrorState error={rounds.error} />
        ) : rounds.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Round</th>
                  <th className="py-2.5 pr-4 font-medium">Lead investor</th>
                  <th className="py-2.5 pr-4 font-medium">Raised</th>
                  <th className="py-2.5 pr-4 font-medium">Post-money</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {rounds.data.items.map((r) => (
                  <tr key={r.id}>
                    <td className="py-3 pr-4 font-medium">{r.round_name}</td>
                    <td className="text-quiet py-3 pr-4">{r.lead_investor ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {r.amount_raised !== null ? money(r.amount_raised) : "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {r.post_money_valuation !== null ? money(r.post_money_valuation) : "—"}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={r.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : rounds.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No funding rounds recorded." />
        )}
      </Panel>

      <Panel title="Updates & board minutes" subtitle={updates.data ? `${updates.data.total} total` : undefined}>
        {updates.error ? (
          <ErrorState error={updates.error} />
        ) : updates.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Type</th>
                  <th className="py-2.5 pr-4 font-medium">Sent</th>
                  <th className="py-2.5 font-medium">Next report due</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {updates.data.items.map((u) => (
                  <tr key={u.id}>
                    <td className="py-3 pr-4 font-medium">{u.title}</td>
                    <td className="text-quiet py-3 pr-4 capitalize">{u.update_type.replace("_", " ")}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{u.sent_date ?? "—"}</td>
                    <td className="text-quiet py-3 font-mono text-[12px]">{u.next_report_due_date ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : updates.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No investor updates recorded." />
        )}
      </Panel>
    </div>
  );
}
