import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, money } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/patent")({
  ssr: false,
  component: PatentPage,
});

function PatentPage() {
  const summary = useQuery({ queryKey: ["patent-summary"], queryFn: orbit.patentSummary, retry: false });
  const filings = useQuery({
    queryKey: ["patent-filings"],
    queryFn: () => orbit.patentFilings(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Patent</p>
        <h1 className="display mt-2 text-3xl">IP portfolio</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Granted" value={String(summary.data.granted)} accent />
          <StatCard label="Pending" value={String(summary.data.pending)} />
          <StatCard label="Upcoming renewals" value={String(summary.data.upcoming_renewals)} />
          <StatCard label="Portfolio value" value={money(summary.data.total_portfolio_value)} />
        </div>
      )}

      <Panel title="Filings" subtitle={filings.data ? `${filings.data.total} total` : undefined}>
        {filings.error ? (
          <ErrorState error={filings.error} />
        ) : filings.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Jurisdiction</th>
                  <th className="py-2.5 pr-4 font-medium">Filed</th>
                  <th className="py-2.5 pr-4 font-medium">Renewal due</th>
                  <th className="py-2.5 pr-4 font-medium">Value</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {filings.data.items.map((f) => (
                  <tr key={f.id}>
                    <td className="py-3 pr-4 font-medium">{f.title}</td>
                    <td className="text-quiet py-3 pr-4 uppercase">{f.jurisdiction}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{f.filing_date ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{f.renewal_date ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {f.estimated_value !== null ? money(f.estimated_value) : "—"}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={f.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : filings.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No patent filings recorded." />
        )}
      </Panel>
    </div>
  );
}
