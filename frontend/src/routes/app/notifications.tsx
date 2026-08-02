import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel } from "@/components/console/Primitives";
import { orbit, type NotificationRead } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/notifications")({
  ssr: false,
  component: NotificationsPage,
});

function NotificationsPage() {
  const qc = useQueryClient();
  const list = useQuery({
    queryKey: ["notifications"],
    queryFn: () => orbit.notifications(1, 30),
    retry: false,
  });
  const markRead = useMutation({
    mutationFn: (id: string) => orbit.markRead(id),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: ["notifications"] });
      void qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
    },
  });
  const decide = useMutation({
    mutationFn: ({ id, approve }: { id: string; approve: boolean }) =>
      orbit.decideApproval(id, approve),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: ["notifications"] });
      void qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
      void qc.invalidateQueries({ queryKey: ["approvals"] });
    },
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Inbox</p>
        <h1 className="display mt-2 text-3xl">Notifications</h1>
      </div>

      <Panel title="Recent" subtitle={list.data ? `${list.data.total} total` : undefined}>
        {list.error ? (
          <ErrorState error={list.error} />
        ) : list.data?.items?.length ? (
          <ul className="divide-y divide-[color:var(--hairline)]">
            {list.data.items.map((n) => (
              <NotificationRow
                key={n.id}
                notification={n}
                onMarkRead={() => markRead.mutate(n.id)}
                onDecide={(approve) => decide.mutate({ id: n.reference_id as string, approve })}
                markReadBusy={markRead.isPending}
                decideBusy={decide.isPending}
              />
            ))}
          </ul>
        ) : list.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="Nothing here yet." />
        )}
      </Panel>
    </div>
  );
}

function NotificationRow({
  notification: n,
  onMarkRead,
  onDecide,
  markReadBusy,
  decideBusy,
}: {
  notification: NotificationRead;
  onMarkRead: () => void;
  onDecide: (approve: boolean) => void;
  markReadBusy: boolean;
  decideBusy: boolean;
}) {
  const isActionableApproval = !n.is_read && n.reference_type === "approval" && n.reference_id;

  return (
    <li className="flex items-start justify-between gap-4 py-4">
      <div>
        <p className="flex items-center gap-2 text-[13px] font-medium">
          {!n.is_read && <span className="h-1.5 w-1.5 rounded-full bg-primary" />}
          {n.title}
        </p>
        {n.body && <p className="text-quiet mt-1 text-[12.5px]">{n.body}</p>}
        <p className="text-quiet mt-1 font-mono text-[11px] uppercase">{n.type}</p>
      </div>
      {isActionableApproval ? (
        <div className="flex shrink-0 items-center gap-2">
          <button
            onClick={() => onDecide(true)}
            disabled={decideBusy}
            className="rounded-full bg-primary px-3.5 py-1.5 text-[12px] font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            Approve
          </button>
          <button
            onClick={() => onDecide(false)}
            disabled={decideBusy}
            className="rounded-full border border-[color:var(--hairline)] px-3 py-1.5 text-[12px] transition-colors hover:bg-[color:var(--surface-elevated)] disabled:opacity-50"
          >
            Reject
          </button>
        </div>
      ) : (
        !n.is_read && (
          <button
            onClick={onMarkRead}
            disabled={markReadBusy}
            className="text-quiet shrink-0 rounded-full border border-[color:var(--hairline)] px-3 py-1 text-[11.5px] transition-colors hover:text-foreground"
          >
            Mark read
          </button>
        )
      )}
    </li>
  );
}
