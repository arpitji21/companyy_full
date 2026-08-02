import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, money } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/tender")({
  ssr: false,
  component: TenderPage,
});

function TenderPage() {
  const summary = useQuery({ queryKey: ["tender-summary"], queryFn: orbit.tenderSummary, retry: false });
  const tenders = useQuery({ queryKey: ["tenders"], queryFn: () => orbit.tenders(1, 25), retry: false });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Tender</p>
        <h1 className="display mt-2 text-3xl">Tenders & bids</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Open tenders" value={String(summary.data.open_tenders)} accent />
          <StatCard label="Win rate" value={`${summary.data.win_rate}%`} />
          <StatCard label="Open bid value" value={money(summary.data.total_open_bid_value)} />
          <StatCard label="Deadlines (14d)" value={String(summary.data.upcoming_deadlines)} />
        </div>
      )}

      <Panel title="Tenders" subtitle={tenders.data ? `${tenders.data.total} total` : undefined}>
        {tenders.error ? (
          <ErrorState error={tenders.error} />
        ) : tenders.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Client</th>
                  <th className="py-2.5 pr-4 font-medium">Bid value</th>
                  <th className="py-2.5 pr-4 font-medium">Win prob.</th>
                  <th className="py-2.5 pr-4 font-medium">Deadline</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {tenders.data.items.map((t) => (
                  <tr key={t.id}>
                    <td className="py-3 pr-4 font-medium">{t.title}</td>
                    <td className="text-quiet py-3 pr-4">{t.client_name ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {t.bid_value !== null ? money(t.bid_value) : "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {t.win_probability !== null ? `${t.win_probability}%` : "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{t.submission_deadline ?? "—"}</td>
                    <td className="py-3">
                      <StatusBadge status={t.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : tenders.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No tenders recorded." />
        )}
      </Panel>
    </div>
  );
}
