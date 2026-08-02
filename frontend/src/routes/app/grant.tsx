import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, money } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/grant")({
  ssr: false,
  component: GrantPage,
});

function GrantPage() {
  const summary = useQuery({ queryKey: ["grant-summary"], queryFn: orbit.grantSummary, retry: false });
  const applications = useQuery({
    queryKey: ["grant-applications"],
    queryFn: () => orbit.grantApplications(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Grant</p>
        <h1 className="display mt-2 text-3xl">Funding & grants</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Awarded" value={String(summary.data.awarded)} accent />
          <StatCard label="Under review" value={String(summary.data.under_review)} />
          <StatCard label="Awarded amount" value={money(summary.data.total_awarded_amount)} />
          <StatCard label="Disbursed" value={money(summary.data.total_disbursed_amount)} />
        </div>
      )}
      {summary.data && summary.data.upcoming_reporting_deadlines > 0 && (
        <div className="rounded-xl border border-[color:var(--hairline)] bg-[color:var(--surface-elevated)] px-5 py-4 text-[13px]">
          <span className="font-semibold">{summary.data.upcoming_reporting_deadlines}</span> grant
          {summary.data.upcoming_reporting_deadlines === 1 ? "" : "s"} with a reporting deadline in the next 30 days.
        </div>
      )}

      <Panel
        title="Applications"
        subtitle={applications.data ? `${applications.data.total} total` : undefined}
      >
        {applications.error ? (
          <ErrorState error={applications.error} />
        ) : applications.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Funding body</th>
                  <th className="py-2.5 pr-4 font-medium">Requested</th>
                  <th className="py-2.5 pr-4 font-medium">Awarded</th>
                  <th className="py-2.5 pr-4 font-medium">Reporting due</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {applications.data.items.map((a) => (
                  <tr key={a.id}>
                    <td className="py-3 pr-4 font-medium">{a.title}</td>
                    <td className="text-quiet py-3 pr-4">{a.funding_body}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {a.amount_requested !== null ? money(a.amount_requested) : "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {a.amount_awarded !== null ? money(a.amount_awarded) : "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {a.reporting_due_date ?? "—"}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={a.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : applications.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No grant applications recorded." />
        )}
      </Panel>
    </div>
  );
}
