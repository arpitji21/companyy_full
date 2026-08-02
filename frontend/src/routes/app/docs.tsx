import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { EmptyState, ErrorState, Panel, StatCard, fileSize } from "@/components/console/Primitives";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/docs")({
  ssr: false,
  component: DocsPage,
});

function DocsPage() {
  const summary = useQuery({ queryKey: ["docs-summary"], queryFn: orbit.documentsSummary, retry: false });
  const documents = useQuery({
    queryKey: ["docs-documents"],
    queryFn: () => orbit.documents(1, 25),
    retry: false,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">Docs</p>
        <h1 className="display mt-2 text-3xl">Document management</h1>
      </div>

      {summary.error && <ErrorState error={summary.error} />}
      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          <StatCard label="Total documents" value={String(summary.data.total_documents)} accent />
          <StatCard label="Total storage" value={fileSize(summary.data.total_size_bytes)} />
          <StatCard label="Folders" value={String(Object.keys(summary.data.by_folder).length)} />
        </div>
      )}

      {summary.data && Object.keys(summary.data.by_folder).length > 0 && (
        <Panel title="By folder">
          <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {Object.entries(summary.data.by_folder).map(([folder, count]) => (
              <li
                key={folder}
                className="flex items-center justify-between rounded-xl bg-[color:var(--surface-elevated)] px-4 py-3 text-[13px]"
              >
                <span>{folder}</span>
                <span className="font-mono">{count}</span>
              </li>
            ))}
          </ul>
        </Panel>
      )}

      <Panel title="Documents" subtitle={documents.data ? `${documents.data.total} total` : undefined}>
        {documents.error ? (
          <ErrorState error={documents.error} />
        ) : documents.data?.items?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="text-quiet border-b border-[color:var(--hairline)] text-[11.5px] uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 pr-4 font-medium">Name</th>
                  <th className="py-2.5 pr-4 font-medium">Folder</th>
                  <th className="py-2.5 pr-4 font-medium">Type</th>
                  <th className="py-2.5 pr-4 font-medium">Size</th>
                  <th className="py-2.5 font-medium">Version</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[color:var(--hairline)]">
                {documents.data.items.map((d) => (
                  <tr key={d.id}>
                    <td className="py-3 pr-4 font-medium">{d.name}</td>
                    <td className="text-quiet py-3 pr-4">{d.folder ?? "Uncategorized"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{d.mime_type ?? "—"}</td>
                    <td className="text-quiet py-3 pr-4 font-mono text-[12px]">{fileSize(d.size_bytes)}</td>
                    <td className="text-quiet py-3 font-mono text-[12px]">v{d.version}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : documents.isLoading ? (
          <p className="text-quiet text-[13px]">Loading…</p>
        ) : (
          <EmptyState message="No documents recorded." />
        )}
      </Panel>
    </div>
  );
}
