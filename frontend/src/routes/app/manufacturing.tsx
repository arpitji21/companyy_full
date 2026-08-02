import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, pct } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/manufacturing")({
  ssr: false,
  component: ManufacturingPage,
});

function ManufacturingPage() {
  const summary = useQuery({
    queryKey: ["manufacturing-summary"],
    queryFn: orbit.manufacturingSummary,
    retry: false,
  });
  const batches = useQuery({
    queryKey: ["manufacturing-batches"],
    queryFn: () => orbit.batches(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Manufacturing</p>
        <h1 className="display mt-2 text-3xl">Batches & yield</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Total batches" value={String(summary.data.total_batches)} />
          <StatCard label="In progress" value={String(summary.data.in_progress)} />
          <StatCard label="Completed" value={String(summary.data.completed)} />
          <StatCard label="Avg. yield" value={pct(summary.data.average_yield_rate, 1)} accent />
        </div>
      )}

      <Panel title="Batches" subtitle={batches.data ? `${batches.data.total} total` : undefined}>
        {batches.error ? (
          <ErrorState error={batches.error} />
        ) : batches.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Batch</th>
                  <th className="py-2.5 pr-4 font-medium">Product</th>
                  <th className="py-2.5 pr-4 font-medium">Line</th>
                  <th className="py-2.5 pr-4 font-medium">Qty produced</th>
                  <th className="py-2.5 pr-4 font-medium">Yield</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {batches.data.items.map((b) => (
                  <tr key={b.id}>
                    <td className="py-3 pr-4 font-mono text-[12px]">{b.batch_number}</td>
                    <td className="py-3 pr-4 font-medium">{b.product_name}</td>
                    <td className="text-quiet py-3 pr-4">{b.line ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {b.quantity_produced.toLocaleString()}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {b.yield_rate !== null ? pct(b.yield_rate, 1) : "—"}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={b.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : batches.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No batches recorded." />
        )}
      </Panel>
    </div>
  );
}
