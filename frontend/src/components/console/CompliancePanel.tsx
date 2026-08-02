import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Meter, Panel, StatCard, StatusBadge } from "@/components/console/Primitives";
import type { ComplianceRecordRead, ComplianceSummary, Page } from "@/lib/orbit-api";

export function CompliancePanel({
  eyebrow,
  title,
  recordLabel,
  summaryQueryKey,
  recordsQueryKey,
  fetchSummary,
  fetchRecords,
}: {
  eyebrow: string;
  title: string;
  recordLabel: string;
  summaryQueryKey: string;
  recordsQueryKey: string;
  fetchSummary: () => Promise<ComplianceSummary>;
  fetchRecords: () => Promise<Page<ComplianceRecordRead>>;
}) {
  const summary = useQuery({ queryKey: [summaryQueryKey], queryFn: fetchSummary, retry: false });
  const records = useQuery({ queryKey: [recordsQueryKey], queryFn: fetchRecords, retry: false });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h1 className="display mt-2 text-3xl">{title}</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="grid gap-4 sm:grid-cols-3 lg:col-span-2">
            <StatCard label="Total records" value={String(summary.data.total_records)} />
            <StatCard label="Approved" value={String(summary.data.approved)} />
            <StatCard label="Expired" value={String(summary.data.expired)} />
          </div>
          <Panel title="Compliance score">
            <p className="display text-4xl">{summary.data.compliance_score.toFixed(0)}%</p>
            <div className="mt-5">
              <Meter label="Compliance score" value={summary.data.compliance_score} />
            </div>
          </Panel>
        </div>
      )}

      <Panel title={recordLabel} subtitle={records.data ? `${records.data.total} total` : undefined}>
        {records.error ? (
          <ErrorState error={records.error} />
        ) : records.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Framework</th>
                  <th className="py-2.5 pr-4 font-medium">Status</th>
                  <th className="py-2.5 pr-4 font-medium">Submitted</th>
                  <th className="py-2.5 pr-4 font-medium">Expires</th>
                  <th className="py-2.5 font-medium">Certificate</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {records.data.items.map((r) => (
                  <tr key={r.id}>
                    <td className="py-3 pr-4 font-medium">{r.title}</td>
                    <td className="text-quiet py-3 pr-4 uppercase">{r.framework}</td>
                    <td className="py-3 pr-4">
                      <StatusBadge status={r.status} />
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {r.submission_date ?? "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{r.expiry_date ?? "—"}</td>
                    <td className="text-quiet py-3 font-mono text-[12px]">{r.certificate_number ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : records.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No records recorded." />
        )}
      </Panel>
    </div>
  );
}
