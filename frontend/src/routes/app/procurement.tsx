import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, money } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/procurement")({
  ssr: false,
  component: ProcurementPage,
});

function ProcurementPage() {
  const summary = useQuery({ queryKey: ["procurement-summary"], queryFn: orbit.procurementSummary, retry: false });
  const orders = useQuery({
    queryKey: ["purchase-orders"],
    queryFn: () => orbit.purchaseOrders(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Procurement</p>
        <h1 className="display mt-2 text-3xl">Purchasing & sourcing</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Pending approval" value={String(summary.data.pending_approval)} accent />
          <StatCard label="Ordered" value={String(summary.data.ordered)} />
          <StatCard label="Delivered" value={String(summary.data.delivered)} />
          <StatCard label="Total spend" value={money(summary.data.total_spend)} />
        </div>
      )}
      {summary.data && summary.data.upcoming_contract_renewals > 0 && (
        <div className="rounded-xl border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-5 py-4 text-[13px]">
          <span className="font-semibold">{summary.data.upcoming_contract_renewals}</span> contract
          {summary.data.upcoming_contract_renewals === 1 ? "" : "s"} renewing in the next 30 days.
        </div>
      )}

      <Panel title="Purchase orders" subtitle={orders.data ? `${orders.data.total} total` : undefined}>
        {orders.error ? (
          <ErrorState error={orders.error} />
        ) : orders.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Category</th>
                  <th className="py-2.5 pr-4 font-medium">Amount</th>
                  <th className="py-2.5 pr-4 font-medium">Contract end</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {orders.data.items.map((o) => (
                  <tr key={o.id}>
                    <td className="py-3 pr-4 font-medium">{o.title}</td>
                    <td className="text-quiet py-3 pr-4">{o.category ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {o.amount !== null ? money(o.amount) : "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{o.contract_end_date ?? "—"}</td>
                    <td className="py-3">
                      <StatusBadge status={o.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : orders.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No purchase orders recorded." />
        )}
      </Panel>
    </div>
  );
}
