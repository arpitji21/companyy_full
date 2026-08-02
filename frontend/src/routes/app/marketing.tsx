import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, money, pct } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/marketing")({
  ssr: false,
  component: MarketingPage,
});

function MarketingPage() {
  const summary = useQuery({
    queryKey: ["marketing-summary"],
    queryFn: orbit.marketingSummary,
    retry: false,
  });
  const campaigns = useQuery({
    queryKey: ["marketing-campaigns"],
    queryFn: () => orbit.campaigns(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Marketing</p>
        <h1 className="display mt-2 text-3xl">Campaigns & reach</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard
            label="Campaigns"
            value={String(summary.data.total_campaigns)}
            hint={`${summary.data.active_campaigns} active`}
          />
          <StatCard label="Impressions" value={summary.data.total_impressions.toLocaleString()} />
          <StatCard label="Clicks" value={summary.data.total_clicks.toLocaleString()} />
          <StatCard
            label="Avg. conversion"
            value={pct(summary.data.average_conversion_rate, 1)}
            accent
          />
        </div>
      )}

      <Panel title="Campaigns" subtitle={campaigns.data ? `${campaigns.data.total} total` : undefined}>
        {campaigns.error ? (
          <ErrorState error={campaigns.error} />
        ) : campaigns.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Campaign</th>
                  <th className="py-2.5 pr-4 font-medium">Channel</th>
                  <th className="py-2.5 pr-4 font-medium">Status</th>
                  <th className="py-2.5 pr-4 font-medium">Budget</th>
                  <th className="py-2.5 pr-4 font-medium">Clicks / Conv.</th>
                  <th className="py-2.5 text-right font-medium">ROI</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {campaigns.data.items.map((c) => (
                  <tr key={c.id}>
                    <td className="py-3 pr-4 font-medium">{c.name}</td>
                    <td className="text-quiet py-3 pr-4 capitalize">{c.channel}</td>
                    <td className="py-3 pr-4">
                      <StatusBadge status={c.status} />
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {c.budget !== null ? money(c.budget) : "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {c.clicks.toLocaleString()} / {c.conversions.toLocaleString()}
                    </td>
                    <td className="py-3 text-right font-mono">
                      {c.roi !== null ? pct(c.roi, 1) : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : campaigns.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No campaigns recorded." />
        )}
      </Panel>
    </div>
  );
}
