import { r as orbit } from "./orbit-api-Ceoci-7Q.mjs";
import { n as require_jsx_runtime } from "../_libs/radix-ui__react-context+react.mjs";
import { t as CompliancePanel } from "./CompliancePanel-B-UMZzKx.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/regulatory-q8CDYB-k.js
var import_jsx_runtime = require_jsx_runtime();
var SplitComponent = () => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(CompliancePanel, {
	eyebrow: "Regulatory",
	title: "Submissions & filings",
	recordLabel: "Submissions",
	summaryQueryKey: "regulatory-summary",
	recordsQueryKey: "regulatory-submissions",
	fetchSummary: orbit.regulatorySummary,
	fetchRecords: () => orbit.regulatorySubmissions(1, 25)
});
//#endregion
export { SplitComponent as component };
