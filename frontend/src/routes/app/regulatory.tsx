import { createFileRoute } from "@tanstack/react-router";
import { CompliancePanel } from "@/components/console/CompliancePanel";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/regulatory")({
  ssr: false,
  component: () => (
    <CompliancePanel
      eyebrow="Regulatory"
      title="Submissions & filings"
      recordLabel="Submissions"
      summaryQueryKey="regulatory-summary"
      recordsQueryKey="regulatory-submissions"
      fetchSummary={orbit.regulatorySummary}
      fetchRecords={() => orbit.regulatorySubmissions(1, 25)}
    />
  ),
});
