import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Meter, Panel, StatCard, StatusBadge, pct } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/quality")({
  ssr: false,
  component: QualityPage,
});

function QualityPage() {
  const metrics = useQuery({ queryKey: ["quality-metrics"], queryFn: orbit.qualityMetrics, retry: false });
  const checks = useQuery({
    queryKey: ["quality-checks"],
    queryFn: () => orbit.qualityChecks(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Quality</p>
        <h1 className="display mt-2 text-3xl">Checks & pass rate</h1>
      </div>

      {metrics.error && <ErrorState error={metrics.error} />}
      {metrics.data && (
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="grid gap-4 sm:grid-cols-3 lg:col-span-2 lg:grid-cols-3">
            <StatCard label="Total checks" value={String(metrics.data.total_checks)} />
            <StatCard label="Pass" value={String(metrics.data.pass_count)} />
            <StatCard label="Fail" value={String(metrics.data.fail_count)} />
          </div>
          <Panel title="Pass rate">
            <p className="display text-4xl">{pct(metrics.data.pass_rate, 1)}</p>
            <div className="mt-5">
              <Meter label="Pass rate" value={metrics.data.pass_rate} />
            </div>
          </Panel>
        </div>
      )}

      <Panel title="Checks" subtitle={checks.data ? `${checks.data.total} total` : undefined}>
        {checks.error ? (
          <ErrorState error={checks.error} />
        ) : checks.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Check type</th>
                  <th className="py-2.5 pr-4 font-medium">Result</th>
                  <th className="py-2.5 pr-4 font-medium">Defect rate</th>
                  <th className="py-2.5 font-medium">Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {checks.data.items.map((c) => (
                  <tr key={c.id}>
                    <td className="py-3 pr-4 font-medium capitalize">{c.check_type.replace(/_/g, " ")}</td>
                    <td className="py-3 pr-4">
                      <StatusBadge status={c.result} />
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {c.defect_rate !== null ? pct(c.defect_rate, 1) : "—"}
                    </td>
                    <td className="text-quiet py-3">{c.notes ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : checks.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No quality checks recorded." />
        )}
      </Panel>
    </div>
  );
}
