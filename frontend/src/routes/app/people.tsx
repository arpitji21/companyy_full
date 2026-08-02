import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/people")({
  ssr: false,
  component: PeoplePage,
});

function PeoplePage() {
  const headcount = useQuery({ queryKey: ["hr-headcount"], queryFn: orbit.headcount, retry: false });
  const employees = useQuery({
    queryKey: ["employees"],
    queryFn: () => orbit.employees(1, 25),
    retry: false,
  });

  const byStatus = (headcount.data?.by_status ?? {}) as Record<string, number>;

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">People</p>
        <h1 className="display mt-2 text-3xl">Workforce</h1>
      </div>

      {headcount.error && <ErrorState error={headcount.error} />}
      {headcount.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Total" value={String(headcount.data.total ?? employees.data?.total ?? "—")} />
          {Object.entries(byStatus)
            .slice(0, 3)
            .map(([k, v]) => (
              <StatCard key={k} label={k.replace(/_/g, " ")} value={String(v)} />
            ))}
        </div>
      )}

      <Panel title="Directory" subtitle={employees.data ? `${employees.data.total} employees` : undefined}>
        {employees.error ? (
          <ErrorState error={employees.error} />
        ) : employees.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Name</th>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Email</th>
                  <th className="py-2.5 pr-4 font-medium">Type</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {employees.data.items.map((e) => (
                  <tr key={e.id}>
                    <td className="py-3 pr-4 font-medium">{e.full_name}</td>
                    <td className="text-quiet py-3 pr-4">{e.job_title ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{e.email}</td>
                    <td className="py-3 pr-4 capitalize">{e.employment_type?.replace(/_/g, " ")}</td>
                    <td className="py-3 capitalize">{e.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : employees.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No employees found." />
        )}
      </Panel>
    </div>
  );
}
