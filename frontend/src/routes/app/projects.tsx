import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/projects")({
  ssr: false,
  component: ProjectsPage,
});

function ProjectsPage() {
  const projects = useQuery({
    queryKey: ["projects"],
    queryFn: () => orbit.projects(1, 25),
    retry: false,
  });

  const items = projects.data?.items ?? [];
  const totalTasks = items.reduce((n, p) => n + (p.tasks?.length ?? 0), 0);
  const openTasks = items.reduce(
    (n, p) => n + (p.tasks?.filter((t) => t.status !== "done" && t.status !== "completed").length ?? 0),
    0,
  );

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Projects</p>
        <h1 className="display mt-2 text-3xl">Delivery & task status</h1>
      </div>

      {projects.data && (
        <div className="grid gap-4 sm:grid-cols-3">
          <StatCard label="Projects" value={String(projects.data.total)} />
          <StatCard label="Tasks (page)" value={String(totalTasks)} />
          <StatCard label="Open tasks (page)" value={String(openTasks)} accent={openTasks > 0} />
        </div>
      )}

      {projects.error ? (
        <ErrorState error={projects.error} />
      ) : items.length ? (
        <div className="space-y-4">
          {items.map((p) => (
            <Panel
              key={p.id}
              title={p.name}
              subtitle={p.description ?? undefined}
              action={<StatusBadge status={p.status} />}
            >
              <div className="text-quiet mb-4 flex flex-wrap gap-x-6 gap-y-1 text-[12px]">
                <span>Start: {p.start_date ?? "—"}</span>
                <span>Due: {p.due_date ?? "—"}</span>
                <span>{p.tasks?.length ?? 0} tasks</span>
              </div>
              {p.tasks?.length ? (
                <ul className="divide-y divide-[color:var(--hairline)]">
                  {p.tasks.map((t) => (
                    <li key={t.id} className="flex items-center justify-between gap-4 py-3 text-[13px]">
                      <div>
                        <p className="font-medium">{t.title}</p>
                        {t.description && <p className="text-quiet mt-0.5 text-[12px]">{t.description}</p>}
                      </div>
                      <div className="flex shrink-0 items-center gap-3">
                        <span className="text-quiet font-mono text-[11.5px] capitalize">{t.priority}</span>
                        <span className="text-quiet font-mono text-[11.5px]">{t.due_date ?? "—"}</span>
                        <StatusBadge status={t.status} />
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <EmptyState message="No tasks under this project yet." />
              )}
            </Panel>
          ))}
        </div>
      ) : projects.isLoading ? (
        <p className="text-quiet text-[13px]">Loading…</p>
      ) : (
        <EmptyState message="No projects recorded." />
      )}
    </div>
  );
}
