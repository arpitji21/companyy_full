import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, StatusBadge } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/meetings")({
  ssr: false,
  component: MeetingsPage,
});

function MeetingsPage() {
  const upcoming = useQuery({
    queryKey: ["meetings-upcoming"],
    queryFn: orbit.upcomingMeetings,
    retry: false,
  });
  const all = useQuery({ queryKey: ["meetings-all"], queryFn: () => orbit.meetings(1, 25), retry: false });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Meetings</p>
        <h1 className="display mt-2 text-3xl">Schedule</h1>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <StatCard label="Upcoming" value={String(upcoming.data?.length ?? "—")} />
        <StatCard label="All meetings" value={String(all.data?.total ?? "—")} />
      </div>

      <Panel title="Upcoming">
        {upcoming.error ? (
          <ErrorState error={upcoming.error} />
        ) : upcoming.data?.length ? (
          <ul className="divide-y divide-[color:var(--hairline)]">
            {upcoming.data.map((m) => (
              <li key={m.id} className="flex items-center justify-between gap-4 py-3 text-[13px]">
                <div>
                  <p className="font-medium">{m.title}</p>
                  {m.location && <p className="text-quiet mt-0.5 text-[12px]">{m.location}</p>}
                </div>
                <span className="text-quiet font-mono text-[12px]">
                  {new Date(m.starts_at).toLocaleString()}
                </span>
              </li>
            ))}
          </ul>
        ) : upcoming.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No upcoming meetings scheduled." />
        )}
      </Panel>

      <Panel title="All meetings" subtitle={all.data ? `${all.data.total} total` : undefined}>
        {all.error ? (
          <ErrorState error={all.error} />
        ) : all.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Title</th>
                  <th className="py-2.5 pr-4 font-medium">Location</th>
                  <th className="py-2.5 pr-4 font-medium">Starts</th>
                  <th className="py-2.5 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {all.data.items.map((m) => (
                  <tr key={m.id}>
                    <td className="py-3 pr-4 font-medium">{m.title}</td>
                    <td className="text-quiet py-3 pr-4">{m.location ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">
                      {new Date(m.starts_at).toLocaleString()}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={m.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : all.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No meetings recorded." />
        )}
      </Panel>
    </div>
  );
}
