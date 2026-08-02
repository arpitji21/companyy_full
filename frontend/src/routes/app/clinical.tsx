import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/clinical")({
  ssr: false,
  component: ClinicalPage,
});

function ClinicalPage() {
  const summary = useQuery({ queryKey: ["clinical-summary"], queryFn: orbit.clinicalSummary, retry: false });
  const trials = useQuery({ queryKey: ["clinical-trials"], queryFn: () => orbit.clinicalTrials(1, 25), retry: false });
  const events = useQuery({ queryKey: ["clinical-events"], queryFn: () => orbit.clinicalEvents(1, 25), retry: false });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Clinical</p>
        <h1 className="display mt-2 text-3xl">Trials & protocols</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Active trials" value={String(summary.data.active_trials)} accent />
          <StatCard label="Enrollment rate" value={`${summary.data.enrollment_rate}%`} />
          <StatCard label="Open adverse events" value={String(summary.data.open_adverse_events)} />
          <StatCard label="Open protocol deviations" value={String(summary.data.open_protocol_deviations)} />
        </div>
      )}

      <Panel title="Trials" subtitle={trials.data ? `${trials.data.total} total` : undefined}>
        {trials.error ? (
          <ErrorState error={trials.error} />
        ) : trials.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Phase</th>
                  <th className="py-2.5 pr-4 font-medium">Site</th>
                  <th className="py-2.5 pr-4 font-medium">Enrollment</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {trials.data.items.map((t) => (
                  <tr key={t.id}>
                    <td className="py-3 pr-4 font-medium">{t.title}</td>
                    <td className="text-quiet py-3 pr-4">{t.phase}</td>
                    <td className="text-quiet py-3 pr-4">{t.site ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {t.actual_enrollment} / {t.target_enrollment ?? "—"}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={t.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : trials.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No clinical trials recorded." />
        )}
      </Panel>

      <Panel title="Adverse events & protocol deviations" subtitle={events.data ? `${events.data.total} total` : undefined}>
        {events.error ? (
          <ErrorState error={events.error} />
        ) : events.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Type</th>
                  <th className="py-2.5 pr-4 font-medium">Severity</th>
                  <th className="py-2.5 pr-4 font-medium">Reported</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {events.data.items.map((e) => (
                  <tr key={e.id}>
                    <td className="py-3 pr-4 font-medium capitalize">{e.event_type.replace("_", " ")}</td>
                    <td className="text-quiet py-3 pr-4 capitalize">{e.severity}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{e.reported_date}</td>
                    <td className="py-3">
                      <StatusBadge status={e.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : events.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No adverse events or protocol deviations recorded." />
        )}
      </Panel>
    </div>
  );
}
