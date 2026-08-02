import { createFileRoute } from "@tanstack/react-router";
import { CompliancePanel } from "@/components/console/CompliancePanel";
import { orbit } from "@/lib/orbit-api";

export const Route = createFileRoute("/app/compliance")({
  ssr: false,
  component: () => (
    <CompliancePanel
      eyebrow="Compliance"
      title="Frameworks & audit trail"
      recordLabel="Records"
      summaryQueryKey="compliance-summary"
      recordsQueryKey="compliance-records"
      fetchSummary={orbit.complianceSummary}
      fetchRecords={() => orbit.complianceRecords(1, 25)}
    />
  ),
});
