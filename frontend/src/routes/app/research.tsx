import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge, money, pct } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/research")({
  ssr: false,
  component: ResearchPage,
});

function ResearchPage() {
  const summary = useQuery({ queryKey: ["research-summary"], queryFn: orbit.researchSummary, retry: false });
  const projects = useQuery({
    queryKey: ["research-projects"],
    queryFn: () => orbit.researchProjects(1, 25),
    retry: false,
  });
  const publications = useQuery({
    queryKey: ["research-publications"],
    queryFn: () => orbit.researchPublications(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Research</p>
        <h1 className="display mt-2 text-3xl">R&D pipeline</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Active projects" value={String(summary.data.active_projects)} accent />
          <StatCard label="Completed projects" value={String(summary.data.completed_projects)} />
          <StatCard label="Publications" value={String(summary.data.total_publications)} />
          <StatCard label="Citations" value={String(summary.data.total_citations)} />
        </div>
      )}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-3">
          <StatCard label="Total budget" value={money(summary.data.total_budget)} />
          <StatCard label="Total spend" value={money(summary.data.total_spend)} />
          <StatCard label="Budget utilization" value={pct(summary.data.budget_utilization, 1)} />
        </div>
      )}

      <Panel title="Research projects" subtitle={projects.data ? `${projects.data.total} total` : undefined}>
        {projects.error ? (
          <ErrorState error={projects.error} />
        ) : projects.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Project</th>
                  <th className="py-2.5 pr-4 font-medium">Field</th>
                  <th className="py-2.5 pr-4 font-medium">Budget</th>
                  <th className="py-2.5 pr-4 font-medium">Spend</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {projects.data.items.map((p) => (
                  <tr key={p.id}>
                    <td className="py-3 pr-4 font-medium">{p.title}</td>
                    <td className="text-quiet py-3 pr-4">{p.field ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {p.budget !== null ? money(p.budget) : "—"}
                    </td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{money(p.spend)}</td>
                    <td className="py-3">
                      <StatusBadge status={p.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : projects.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No research projects recorded." />
        )}
      </Panel>

      <Panel
        title="Publications"
        subtitle={publications.data ? `${publications.data.total} total` : undefined}
      >
        {publications.error ? (
          <ErrorState error={publications.error} />
        ) : publications.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Journal</th>
                  <th className="py-2.5 pr-4 font-medium">Published</th>
                  <th className="py-2.5 text-right font-medium">Citations</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {publications.data.items.map((pub) => (
                  <tr key={pub.id}>
                    <td className="py-3 pr-4 font-medium">{pub.title}</td>
                    <td className="text-quiet py-3 pr-4">{pub.journal ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {pub.publication_date ?? "—"}
                    </td>
                    <td className="py-3 text-right font-mono">{pub.citation_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : publications.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No publications recorded." />
        )}
      </Panel>
    </div>
  );
}
