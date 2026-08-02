import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, money } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/analytics")({
  ssr: false,
  component: AnalyticsPage,
});

function AnalyticsPage() {
  const summary = useQuery({ queryKey: ["analytics-summary"], queryFn: orbit.analyticsSummary, retry: false });
  const reports = useQuery({ queryKey: ["analytics-reports"], queryFn: () => orbit.analyticsReports(1, 25), retry: false });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Analytics</p>
        <h1 className="display mt-2 text-3xl">Cross-department reporting</h1>
        <p className="text-quiet mt-2 text-[13px]">
          Live numbers blended from Finance, Sales, Manufacturing, and Compliance — the same data each
          department page shows, in one view.
        </p>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Net cash flow" value={money(summary.data.net_cash_flow)} accent />
          <StatCard label="Open pipeline" value={money(summary.data.open_pipeline_value)} />
          <StatCard label="Mfg. yield rate" value={`${summary.data.manufacturing_yield_rate}%`} />
          <StatCard label="Compliance score" value={`${summary.data.compliance_score}%`} />
        </div>
      )}

      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2">
          {summary.data.snapshots.map((s) => (
            <div
              key={s.department}
              className="rounded-xl border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-5 py-4"
            >
              <p className="eyebrow">{s.department}</p>
              <div className="mt-2 flex items-baseline justify-between text-[13px]">
                <span className="text-quiet">{s.headline_metric}</span>
                <span className="font-mono font-semibold">{s.headline_value}</span>
              </div>
              <div className="mt-1 flex items-baseline justify-between text-[13px]">
                <span className="text-quiet">{s.secondary_metric}</span>
                <span className="font-mono">{s.secondary_value}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      <Panel title="Saved reports" subtitle={reports.data ? `${reports.data.total} total` : undefined}>
        {reports.error ? (
          <ErrorState error={reports.error} />
        ) : reports.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Type</th>
                  <th className="py-2.5 font-medium">Period</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {reports.data.items.map((r) => (
                  <tr key={r.id}>
                    <td className="py-3 pr-4 font-medium">{r.title}</td>
                    <td className="text-quiet py-3 pr-4 capitalize">{r.report_type}</td>
                    <td className="text-quiet py-3 font-mono text-[12px]">
                      {r.period_start ?? "—"} – {r.period_end ?? "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : reports.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No saved reports yet. Custom report building and scheduled exports aren't wired up." />
        )}
      </Panel>
    </div>
  );
}
