import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, money } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/finance")({
  ssr: false,
  component: FinancePage,
});

function FinancePage() {
  const summary = useQuery({ queryKey: ["finance-summary"], queryFn: orbit.financeSummary, retry: false });
  const tx = useQuery({
    queryKey: ["finance-transactions"],
    queryFn: () => orbit.transactions(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Finance</p>
        <h1 className="display mt-2 text-3xl">Cash, budgets & ledger</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <>
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <StatCard label="Total revenue" value={money(summary.data.total_revenue)} />
            <StatCard label="Total expenses" value={money(summary.data.total_expenses)} />
            <StatCard label="Net cash flow" value={money(summary.data.net_cash_flow)} accent />
            <StatCard label="Burn rate" value={money(summary.data.burn_rate)} />
          </div>

          <Panel title="Spend by category">
            {Object.keys(summary.data.by_category ?? {}).length ? (
              <ul className="grid gap-3 sm:grid-cols-2">
                {Object.entries(summary.data.by_category).map(([k, v]) => (
                  <li
                    key={k}
                    className="flex items-center justify-between rounded-xl bg-[color:var(--surface-elevated)] px-4 py-3 text-[13px]"
                  >
                    <span className="capitalize">{k.replace(/_/g, " ")}</span>
                    <span className="font-mono">{money(v)}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <EmptyState message="No categorised spend yet." />
            )}
          </Panel>
        </>
      )}

      <Panel title="Recent transactions" subtitle={tx.data ? `${tx.data.total} total records` : undefined}>
        {tx.error ? (
          <ErrorState error={tx.error} />
        ) : tx.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Date</th>
                  <th className="py-2.5 pr-4 font-medium">Type</th>
                  <th className="py-2.5 pr-4 font-medium">Description</th>
                  <th className="py-2.5 pr-4 font-medium">Status</th>
                  <th className="py-2.5 text-right font-medium">Amount</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {tx.data.items.map((t) => (
                  <tr key={t.id}>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{t.transaction_date}</td>
                    <td className="py-3 pr-4 capitalize">{t.type}</td>
                    <td className="py-3 pr-4">{t.description ?? t.category ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 capitalize">{t.status}</td>
                    <td className="py-3 text-right font-mono">{money(t.amount, t.currency)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : tx.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No transactions recorded." />
        )}
      </Panel>
    </div>
  );
}
