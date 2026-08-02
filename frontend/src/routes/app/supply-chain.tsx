import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { cn } from "@/lib/utils";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, money, pct } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/supply-chain")({
  ssr: false,
  component: SupplyChainPage,
});

function SupplyChainPage() {
  const summary = useQuery({
    queryKey: ["supplychain-summary"],
    queryFn: orbit.supplyChainSummary,
    retry: false,
  });
  const vendors = useQuery({ queryKey: ["vendors"], queryFn: () => orbit.vendors(1, 25), retry: false });
  const inventory = useQuery({
    queryKey: ["inventory"],
    queryFn: () => orbit.inventory(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Supply chain</p>
        <h1 className="display mt-2 text-3xl">Vendors & inventory</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-3">
          <StatCard label="Vendors" value={String(summary.data.total_vendors)} />
          <StatCard label="SKUs tracked" value={String(summary.data.total_sku_count)} />
          <StatCard
            label="Below reorder level"
            value={String(summary.data.items_below_reorder_level)}
            accent={summary.data.items_below_reorder_level > 0}
          />
        </div>
      )}

      <Panel title="Vendors" subtitle={vendors.data ? `${vendors.data.total} total` : undefined}>
        {vendors.error ? (
          <ErrorState error={vendors.error} />
        ) : vendors.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Vendor</th>
                  <th className="py-2.5 pr-4 font-medium">Category</th>
                  <th className="py-2.5 pr-4 font-medium">Contact</th>
                  <th className="py-2.5 pr-4 font-medium">On-time rate</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {vendors.data.items.map((v) => (
                  <tr key={v.id}>
                    <td className="py-3 pr-4 font-medium">{v.name}</td>
                    <td className="text-quiet py-3 pr-4">{v.category ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {v.contact_email ?? v.contact_phone ?? "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {v.on_time_delivery_rate !== null ? pct(v.on_time_delivery_rate, 1) : "—"}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={v.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : vendors.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No vendors recorded." />
        )}
      </Panel>

      <Panel title="Inventory" subtitle={inventory.data ? `${inventory.data.total} SKUs` : undefined}>
        {inventory.error ? (
          <ErrorState error={inventory.error} />
        ) : inventory.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">SKU</th>
                  <th className="py-2.5 pr-4 font-medium">Name</th>
                  <th className="py-2.5 pr-4 font-medium">On hand</th>
                  <th className="py-2.5 pr-4 font-medium">Reorder level</th>
                  <th className="py-2.5 pr-4 font-medium">Unit cost</th>
                  <th className="py-2.5 font-medium">Location</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {inventory.data.items.map((i) => {
                  const low = i.quantity_on_hand <= i.reorder_level;
                  return (
                    <tr key={i.id}>
                      <td className="py-3 pr-4 font-mono text-[12px]">{i.sku}</td>
                      <td className="py-3 pr-4 font-medium">{i.name}</td>
                      <td
                        className={cn(
                          "py-3 pr-4 font-mono text-[12px]",
                          low ? "text-[color:var(--crimson-soft)] font-semibold" : "text-quiet",
                        )}
                      >
                        {i.quantity_on_hand.toLocaleString()}
                      </td>
                      <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                        {i.reorder_level.toLocaleString()}
                      </td>
                      <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                        {i.unit_cost !== null ? money(i.unit_cost) : "—"}
                      </td>
                      <td className="text-quiet py-3">{i.warehouse_location ?? "—"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : inventory.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No inventory recorded." />
        )}
      </Panel>
    </div>
  );
}
