import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import {
  EmptyState,
  ErrorState,
  Panel,
  StatCard,
  StatusBadge,
  money,
  pct,
} from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/sales")({
  ssr: false,
  component: SalesPage,
});

function SalesPage() {
  const summary = useQuery({ queryKey: ["sales-summary"], queryFn: orbit.salesSummary, retry: false });
  const deals = useQuery({ queryKey: ["sales-deals"], queryFn: () => orbit.deals(1, 25), retry: false });
  const customers = useQuery({
    queryKey: ["sales-customers"],
    queryFn: () => orbit.customers(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Sales</p>
        <h1 className="display mt-2 text-3xl">Pipeline & customers</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <>
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <StatCard label="Pipeline value" value={money(summary.data.total_pipeline_value)} accent />
            <StatCard label="Weighted forecast" value={money(summary.data.weighted_forecast)} />
            <StatCard label="Open deals" value={String(summary.data.open_deals)} />
            <StatCard
              label="Won / lost"
              value={`${summary.data.won_deals} / ${summary.data.lost_deals}`}
            />
          </div>

          <Panel title="Pipeline by stage">
            {Object.keys(summary.data.by_stage ?? {}).length ? (
              <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {Object.entries(summary.data.by_stage).map(([k, v]) => (
                  <li
                    key={k}
                    className="flex items-center justify-between rounded-xl bg-[color:var(--surface-elevated)] px-4 py-3 text-[13px]"
                  >
                    <span className="capitalize">{k.replace(/_/g, " ")}</span>
                    <span className="font-mono">{v}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <EmptyState message="No pipeline stages yet." />
            )}
          </Panel>
        </>
      )}

      <Panel title="Deals" subtitle={deals.data ? `${deals.data.total} total` : undefined}>
        {deals.error ? (
          <ErrorState error={deals.error} />
        ) : deals.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Deal</th>
                  <th className="py-2.5 pr-4 font-medium">Stage</th>
                  <th className="py-2.5 pr-4 font-medium">Probability</th>
                  <th className="py-2.5 pr-4 font-medium">Close date</th>
                  <th className="py-2.5 text-right font-medium">Amount</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {deals.data.items.map((d) => (
                  <tr key={d.id}>
                    <td className="py-3 pr-4 font-medium">{d.deal_name}</td>
                    <td className="py-3 pr-4">
                      <StatusBadge status={d.stage} />
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{pct(d.probability)}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {d.expected_close_date ?? "—"}
                    </td>
                    <td className="py-3 text-right font-mono">{money(d.amount)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : deals.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No deals recorded." />
        )}
      </Panel>

      <Panel title="Customers" subtitle={customers.data ? `${customers.data.total} total` : undefined}>
        {customers.error ? (
          <ErrorState error={customers.error} />
        ) : customers.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Name</th>
                  <th className="py-2.5 pr-4 font-medium">Company</th>
                  <th className="py-2.5 pr-4 font-medium">Email</th>
                  <th className="py-2.5 pr-4 font-medium">CSAT</th>
                  <th className="py-2.5 font-medium">Churn risk</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {customers.data.items.map((c) => (
                  <tr key={c.id}>
                    <td className="py-3 pr-4 font-medium">{c.name}</td>
                    <td className="text-quiet py-3 pr-4">{c.company ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{c.email ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {c.csat_score?.toFixed(1) ?? "—"}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={c.churn_risk} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : customers.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No customers recorded." />
        )}
      </Panel>
    </div>
  );
}
