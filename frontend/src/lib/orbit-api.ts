/**
 * Orbit API client — talks to the LarkAI Orbit FastAPI backend.
 * Base URL comes from VITE_ORBIT_API_URL (defaults to local dev backend).
 */

export const ORBIT_BASE_URL =
  (import.meta.env.VITE_ORBIT_API_URL as string | undefined)?.replace(/\/$/, "") ??
  "http://localhost:8000";

/** Builds the /ws/notifications URL for the current access token, reusing
 * ORBIT_BASE_URL so dev/staging/prod all point at the right backend without
 * separate config. http(s) -> ws(s) since browsers require the ws/wss
 * scheme for WebSocket connections even when the API itself is https. */
export function notificationsSocketUrl(accessToken: string): string {
  const wsBase = ORBIT_BASE_URL.replace(/^http/, "ws");
  return `${wsBase}/api/ws/notifications?token=${encodeURIComponent(accessToken)}`;
}

const ACCESS_KEY = "orbit.access_token";
const REFRESH_KEY = "orbit.refresh_token";

export const tokens = {
  get access() {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem(ACCESS_KEY);
  },
  get refresh() {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem(REFRESH_KEY);
  },
  set(access: string, refresh: string) {
    window.localStorage.setItem(ACCESS_KEY, access);
    window.localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear() {
    window.localStorage.removeItem(ACCESS_KEY);
    window.localStorage.removeItem(REFRESH_KEY);
  },
};

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function parseError(res: Response) {
  let detail = res.statusText;
  try {
    const body = await res.json();
    if (typeof body?.detail === "string") detail = body.detail;
    else if (Array.isArray(body?.detail)) detail = body.detail[0]?.msg ?? detail;
    else if (typeof body?.message === "string") detail = body.message;
  } catch {
    /* non-JSON error body */
  }
  return new ApiError(res.status, detail);
}

export async function refreshSession(): Promise<boolean> {
  const refresh_token = tokens.refresh;
  if (!refresh_token) return false;
  const res = await fetch(`${ORBIT_BASE_URL}/api/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token }),
  });
  if (!res.ok) return false;
  const data = (await res.json()) as TokenPair;
  tokens.set(data.access_token, data.refresh_token);
  return true;
}

export async function api<T>(
  path: string,
  options: { method?: string; body?: unknown; auth?: boolean; retry?: boolean } = {},
): Promise<T> {
  const { method = "GET", body, auth = true, retry = true } = options;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (auth && tokens.access) headers.Authorization = `Bearer ${tokens.access}`;

  const res = await fetch(`${ORBIT_BASE_URL}/api${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (res.status === 401 && auth && retry) {
    if (await refreshSession()) {
      return api<T>(path, { ...options, retry: false });
    }
    tokens.clear();
    throw new ApiError(401, "Session expired. Please sign in again.");
  }

  if (!res.ok) throw await parseError(res);
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

/* ---------------------------------- types --------------------------------- */

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserRead {
  id: string;
  email: string;
  full_name: string;
  role_id: string | null;
  department_id: string | null;
  is_active: boolean;
  is_email_verified: boolean;
  avatar_url: string | null;
  last_login_at: string | null;
  created_at: string;
}

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface MeetingRead {
  id: string;
  title: string;
  description: string | null;
  department_id: string | null;
  organizer_id: string | null;
  starts_at: string;
  ends_at: string | null;
  location: string | null;
  status: string;
}

export interface CEODashboard {
  revenue: number;
  expenses: number;
  cash_flow: number;
  burn_rate: number;
  employee_count: number;
  hiring_status: Record<string, number>;
  open_tasks: number;
  manufacturing_status: Record<string, unknown>;
  compliance_score: number;
  pending_approvals: number;
  action_items: ApprovalRead[];
  upcoming_meetings: MeetingRead[];
  unread_notifications: number;
  company_health_score: number;
  risk_score: number;
  health_score_breakdown: Record<string, number>;
  risk_score_breakdown: Record<string, number>;
  ai_alerts: string[];
}

export interface FinanceSummary {
  total_revenue: number;
  total_expenses: number;
  net_cash_flow: number;
  burn_rate: number;
  by_category: Record<string, number>;
}

export interface TransactionRead {
  id: string;
  type: string;
  department_id: string | null;
  category: string | null;
  description: string | null;
  amount: number;
  currency: string;
  transaction_date: string;
  status: string;
}

export interface EmployeeRead {
  id: string;
  user_id: string | null;
  department_id: string | null;
  full_name: string;
  job_title: string | null;
  email: string;
  phone: string | null;
  status: string;
  employment_type: string;
  hire_date: string | null;
  manager_id: string | null;
}

export interface NotificationRead {
  id: string;
  user_id: string;
  type: string;
  title: string;
  body: string | null;
  link: string | null;
  is_read: boolean;
  reference_type: string | null;
  reference_id: string | null;
}

export interface AIAgentRead {
  id: string;
  name: string;
  department_id: string | null;
  provider: string;
  model_name: string;
  system_prompt: string | null;
  is_active: boolean;
}

export interface AgentMessageRead {
  id: string;
  conversation_id?: string;
  role: string;
  content: string;
  created_at?: string;
  [key: string]: unknown;
}

export interface ChatResponse {
  conversation_id: string;
  message: AgentMessageRead;
}

/* ----- Sales ----- */
export interface SalesSummary {
  total_pipeline_value: number;
  weighted_forecast: number;
  open_deals: number;
  won_deals: number;
  lost_deals: number;
  by_stage: Record<string, number>;
}
export interface CustomerRead {
  id: string;
  name: string;
  company: string | null;
  email: string | null;
  csat_score: number | null;
  churn_risk: string;
  owner_id: string | null;
}
export interface DealRead {
  id: string;
  customer_id: string | null;
  owner_id: string | null;
  deal_name: string;
  stage: string;
  amount: number;
  probability: number;
  expected_close_date: string | null;
}

/* ----- Marketing ----- */
export interface MarketingSummary {
  total_campaigns: number;
  active_campaigns: number;
  total_impressions: number;
  total_clicks: number;
  total_conversions: number;
  average_conversion_rate: number;
}
export interface CampaignRead {
  id: string;
  name: string;
  channel: string;
  status: string;
  start_date: string | null;
  end_date: string | null;
  budget: number | null;
  impressions: number;
  clicks: number;
  conversions: number;
  roi: number | null;
}

/* ----- Manufacturing ----- */
export interface ManufacturingSummary {
  total_batches: number;
  in_progress: number;
  completed: number;
  average_yield_rate: number;
  total_units_produced: number;
}
export interface BatchRead {
  id: string;
  batch_number: string;
  product_name: string;
  line: string | null;
  quantity_produced: number;
  yield_rate: number | null;
  status: string;
  started_at: string | null;
  completed_at: string | null;
}

/* ----- Quality ----- */
export interface QualityMetrics {
  total_checks: number;
  pass_count: number;
  fail_count: number;
  pending_count: number;
  pass_rate: number;
}
export interface QualityCheckRead {
  id: string;
  batch_id: string | null;
  check_type: string;
  result: string;
  defect_rate: number | null;
  inspector_id: string | null;
  notes: string | null;
}

/* ----- Compliance & Regulatory ----- */
export interface ComplianceSummary {
  total_records: number;
  approved: number;
  expired: number;
  in_progress: number;
  compliance_score: number;
}
export interface ComplianceRecordRead {
  id: string;
  framework: string;
  title: string;
  status: string;
  submission_date: string | null;
  expiry_date: string | null;
  certificate_number: string | null;
  notes: string | null;
}

/* ----- Supply Chain ----- */
export interface SupplyChainSummary {
  total_vendors: number;
  total_sku_count: number;
  items_below_reorder_level: number;
}
export interface VendorRead {
  id: string;
  name: string;
  category: string | null;
  contact_email: string | null;
  contact_phone: string | null;
  on_time_delivery_rate: number | null;
  status: string;
}
export interface InventoryItemRead {
  id: string;
  sku: string;
  name: string;
  category: string | null;
  quantity_on_hand: number;
  reorder_level: number;
  unit_cost: number | null;
  warehouse_location: string | null;
  vendor_id: string | null;
}

/* ----- Research ----- */
export interface ResearchSummary {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  total_publications: number;
  total_citations: number;
  total_budget: number;
  total_spend: number;
  budget_utilization: number;
}
export interface PublicationRead {
  id: string;
  research_project_id: string | null;
  title: string;
  authors: string | null;
  journal: string | null;
  publication_date: string | null;
  doi: string | null;
  citation_count: number;
}
export interface ResearchProjectRead {
  id: string;
  title: string;
  description: string | null;
  field: string | null;
  status: string;
  lead_employee_id: string | null;
  department_id: string | null;
  start_date: string | null;
  end_date: string | null;
  budget: number | null;
  spend: number;
  publications: PublicationRead[];
}

/* ----- Patent ----- */
export interface PatentSummary {
  total_filings: number;
  granted: number;
  pending: number;
  rejected: number;
  upcoming_renewals: number;
  total_portfolio_value: number;
}
export interface PatentFilingRead {
  id: string;
  research_project_id: string | null;
  title: string;
  jurisdiction: string;
  status: string;
  application_number: string | null;
  filing_date: string | null;
  grant_date: string | null;
  renewal_date: string | null;
  estimated_value: number | null;
  notes: string | null;
}

/* ----- Grant ----- */
export interface GrantSummary {
  total_applications: number;
  awarded: number;
  under_review: number;
  rejected: number;
  total_awarded_amount: number;
  total_disbursed_amount: number;
  upcoming_reporting_deadlines: number;
}
export interface GrantApplicationRead {
  id: string;
  research_project_id: string | null;
  title: string;
  funding_body: string;
  status: string;
  amount_requested: number | null;
  amount_awarded: number | null;
  amount_disbursed: number;
  submission_date: string | null;
  decision_date: string | null;
  reporting_due_date: string | null;
  notes: string | null;
}

/* ----- Customer ----- */
export interface CustomerSummary {
  total_tickets: number;
  open_tickets: number;
  escalated_tickets: number;
  resolved_tickets: number;
  breached_sla: number;
  average_csat: number | null;
  at_risk_customers: number;
}
export interface SupportTicketRead {
  id: string;
  customer_id: string | null;
  account_owner_id: string | null;
  subject: string;
  description: string | null;
  status: string;
  priority: string;
  sla_due_at: string | null;
  resolved_at: string | null;
  escalated_at: string | null;
  csat_score: number | null;
}

/* ----- Procurement ----- */
export interface ProcurementSummary {
  total_orders: number;
  pending_approval: number;
  ordered: number;
  delivered: number;
  total_spend: number;
  by_category: Record<string, number>;
  upcoming_contract_renewals: number;
}
export interface PurchaseOrderRead {
  id: string;
  vendor_id: string | null;
  requested_by_id: string | null;
  title: string;
  category: string | null;
  status: string;
  amount: number | null;
  requested_date: string | null;
  approved_date: string | null;
  delivery_date: string | null;
  contract_end_date: string | null;
  notes: string | null;
}

/* ----- Clinical ----- */
export interface ClinicalSummary {
  total_trials: number;
  active_trials: number;
  completed_trials: number;
  total_target_enrollment: number;
  total_actual_enrollment: number;
  enrollment_rate: number;
  open_adverse_events: number;
  open_protocol_deviations: number;
}
export interface ClinicalTrialRead {
  id: string;
  lead_employee_id: string | null;
  title: string;
  phase: string;
  status: string;
  site: string | null;
  target_enrollment: number | null;
  actual_enrollment: number;
  start_date: string | null;
  end_date: string | null;
}
export interface ClinicalEventRead {
  id: string;
  trial_id: string | null;
  event_type: string;
  severity: string;
  status: string;
  reported_date: string;
  description: string | null;
}

/* ----- Investor ----- */
export interface InvestorSummary {
  total_raised: number;
  latest_post_money_valuation: number | null;
  open_rounds: number;
  closed_rounds: number;
  next_report_due_date: string | null;
  updates_last_90_days: number;
}
export interface FundingRoundRead {
  id: string;
  round_name: string;
  status: string;
  amount_raised: number | null;
  pre_money_valuation: number | null;
  post_money_valuation: number | null;
  lead_investor: string | null;
  close_date: string | null;
  notes: string | null;
}
export interface InvestorUpdateRead {
  id: string;
  title: string;
  update_type: string;
  sent_date: string | null;
  next_report_due_date: string | null;
  summary: string | null;
}

/* ----- Tender ----- */
export interface TenderSummary {
  total_tenders: number;
  open_tenders: number;
  won: number;
  lost: number;
  win_rate: number;
  total_open_bid_value: number;
  upcoming_deadlines: number;
}
export interface TenderRead {
  id: string;
  title: string;
  client_name: string | null;
  client_segment: string | null;
  status: string;
  bid_value: number | null;
  win_probability: number | null;
  submission_deadline: string | null;
  outcome_date: string | null;
  notes: string | null;
}

/* ----- Analytics ----- */
export interface DepartmentSnapshot {
  department: string;
  headline_metric: string;
  headline_value: string;
  secondary_metric: string;
  secondary_value: string;
}
export interface AnalyticsSummary {
  total_revenue: number;
  total_expenses: number;
  net_cash_flow: number;
  open_pipeline_value: number;
  manufacturing_yield_rate: number;
  compliance_score: number;
  total_reports: number;
  snapshots: DepartmentSnapshot[];
}
export interface ReportRead {
  id: string;
  title: string;
  department_id: string | null;
  report_type: string;
  period_start: string | null;
  period_end: string | null;
  generated_by: string | null;
  s3_key: string | null;
}

/* ----- Docs ----- */
export interface DocumentSummary {
  total_documents: number;
  total_size_bytes: number;
  by_folder: Record<string, number>;
}
export interface DocumentRead {
  id: string;
  name: string;
  folder: string | null;
  department_id: string | null;
  uploaded_by: string | null;
  s3_key: string;
  mime_type: string | null;
  size_bytes: number | null;
  version: number;
  ai_summary: string | null;
}

/* ----- Projects ----- */
export interface TaskRead {
  id: string;
  project_id: string | null;
  assignee_id: string | null;
  title: string;
  description: string | null;
  status: string;
  priority: string;
  due_date: string | null;
}
export interface ProjectRead {
  id: string;
  name: string;
  description: string | null;
  department_id: string | null;
  owner_id: string | null;
  status: string;
  start_date: string | null;
  due_date: string | null;
  tasks: TaskRead[];
}

/* ----- Approvals ----- */
export interface ApprovalRead {
  id: string;
  title: string;
  requested_by: string | null;
  department_id: string | null;
  amount: number | null;
  status: string;
  approver_id: string | null;
  notes: string | null;
}

/* -------------------------------- endpoints ------------------------------- */

export const orbit = {
  login: (email: string, password: string) =>
    api<TokenPair>("/auth/login", { method: "POST", body: { email, password }, auth: false }),
  register: (payload: { email: string; password: string; full_name: string }) =>
    api<UserRead>("/auth/register", { method: "POST", body: payload, auth: false }),
  me: () => api<UserRead>("/auth/me"),
  logout: (refresh_token: string) =>
    api<{ message: string }>("/auth/logout", { method: "POST", body: { refresh_token } }),

  ceoDashboard: () => api<CEODashboard>("/ceo/dashboard"),

  financeSummary: () => api<FinanceSummary>("/finance/summary"),
  transactions: (page = 1, page_size = 20) =>
    api<Page<TransactionRead>>(`/finance/transactions?page=${page}&page_size=${page_size}`),

  employees: (page = 1, page_size = 20) =>
    api<Page<EmployeeRead>>(`/employees?page=${page}&page_size=${page_size}`),
  headcount: () => api<Record<string, unknown>>("/hr/headcount"),

  notifications: (page = 1, page_size = 20) =>
    api<Page<NotificationRead>>(`/notifications?page=${page}&page_size=${page_size}`),
  unreadCount: () => api<{ unread: number } | Record<string, number>>("/notifications/unread-count"),
  markRead: (id: string) => api<NotificationRead>(`/notifications/${id}/read`, { method: "POST" }),

  agents: () => api<AIAgentRead[]>("/agents"),
  chat: (payload: { message: string; conversation_id?: string | null; agent_id?: string | null }) =>
    api<ChatResponse>("/chat", { method: "POST", body: payload }),

  salesSummary: () => api<SalesSummary>("/sales/summary"),
  customers: (page = 1, page_size = 20) =>
    api<Page<CustomerRead>>(`/sales/customers?page=${page}&page_size=${page_size}`),
  deals: (page = 1, page_size = 20) =>
    api<Page<DealRead>>(`/sales/deals?page=${page}&page_size=${page_size}`),

  marketingSummary: () => api<MarketingSummary>("/marketing/summary"),
  campaigns: (page = 1, page_size = 20) =>
    api<Page<CampaignRead>>(`/marketing/campaigns?page=${page}&page_size=${page_size}`),

  manufacturingSummary: () => api<ManufacturingSummary>("/manufacturing/summary"),
  batches: (page = 1, page_size = 20) =>
    api<Page<BatchRead>>(`/manufacturing/batches?page=${page}&page_size=${page_size}`),

  qualityMetrics: () => api<QualityMetrics>("/quality/metrics"),
  qualityChecks: (page = 1, page_size = 20) =>
    api<Page<QualityCheckRead>>(`/quality/checks?page=${page}&page_size=${page_size}`),

  complianceSummary: () => api<ComplianceSummary>("/compliance/summary"),
  complianceRecords: (page = 1, page_size = 20) =>
    api<Page<ComplianceRecordRead>>(`/compliance/records?page=${page}&page_size=${page_size}`),

  regulatorySummary: () => api<ComplianceSummary>("/regulatory/summary"),
  regulatorySubmissions: (page = 1, page_size = 20) =>
    api<Page<ComplianceRecordRead>>(`/regulatory/submissions?page=${page}&page_size=${page_size}`),

  supplyChainSummary: () => api<SupplyChainSummary>("/supply-chain/summary"),
  vendors: (page = 1, page_size = 20) =>
    api<Page<VendorRead>>(`/supply-chain/vendors?page=${page}&page_size=${page_size}`),
  inventory: (page = 1, page_size = 20) =>
    api<Page<InventoryItemRead>>(`/supply-chain/inventory?page=${page}&page_size=${page_size}`),

  researchSummary: () => api<ResearchSummary>("/research/summary"),
  researchProjects: (page = 1, page_size = 20) =>
    api<Page<ResearchProjectRead>>(`/research/projects?page=${page}&page_size=${page_size}`),
  researchPublications: (page = 1, page_size = 20) =>
    api<Page<PublicationRead>>(`/research/publications?page=${page}&page_size=${page_size}`),

  patentSummary: () => api<PatentSummary>("/patent/summary"),
  patentFilings: (page = 1, page_size = 20) =>
    api<Page<PatentFilingRead>>(`/patent/filings?page=${page}&page_size=${page_size}`),

  grantSummary: () => api<GrantSummary>("/grant/summary"),
  grantApplications: (page = 1, page_size = 20) =>
    api<Page<GrantApplicationRead>>(`/grant/applications?page=${page}&page_size=${page_size}`),

  documentsSummary: () => api<DocumentSummary>("/documents/summary"),
  documents: (page = 1, page_size = 20) =>
    api<Page<DocumentRead>>(`/documents?page=${page}&page_size=${page_size}`),

  projects: (page = 1, page_size = 20) =>
    api<Page<ProjectRead>>(`/projects?page=${page}&page_size=${page_size}`),

  meetings: (page = 1, page_size = 20) =>
    api<Page<MeetingRead>>(`/meetings?page=${page}&page_size=${page_size}`),
  upcomingMeetings: () => api<MeetingRead[]>("/meetings/upcoming"),

  approvals: (page = 1, page_size = 20) =>
    api<Page<ApprovalRead>>(`/approvals?page=${page}&page_size=${page_size}`),
  decideApproval: (id: string, approve: boolean, notes?: string) =>
    api<ApprovalRead>(`/approvals/${id}/decision`, { method: "POST", body: { approve, notes } }),

  customerSummary: () => api<CustomerSummary>("/customer/summary"),
  supportTickets: (page = 1, page_size = 20) =>
    api<Page<SupportTicketRead>>(`/customer/tickets?page=${page}&page_size=${page_size}`),

  procurementSummary: () => api<ProcurementSummary>("/procurement/summary"),
  purchaseOrders: (page = 1, page_size = 20) =>
    api<Page<PurchaseOrderRead>>(`/procurement/orders?page=${page}&page_size=${page_size}`),

  clinicalSummary: () => api<ClinicalSummary>("/clinical/summary"),
  clinicalTrials: (page = 1, page_size = 20) =>
    api<Page<ClinicalTrialRead>>(`/clinical/trials?page=${page}&page_size=${page_size}`),
  clinicalEvents: (page = 1, page_size = 20) =>
    api<Page<ClinicalEventRead>>(`/clinical/events?page=${page}&page_size=${page_size}`),

  investorSummary: () => api<InvestorSummary>("/investor/summary"),
  fundingRounds: (page = 1, page_size = 20) =>
    api<Page<FundingRoundRead>>(`/investor/rounds?page=${page}&page_size=${page_size}`),
  investorUpdates: (page = 1, page_size = 20) =>
    api<Page<InvestorUpdateRead>>(`/investor/updates?page=${page}&page_size=${page_size}`),

  tenderSummary: () => api<TenderSummary>("/tender/summary"),
  tenders: (page = 1, page_size = 20) =>
    api<Page<TenderRead>>(`/tender/tenders?page=${page}&page_size=${page_size}`),

  analyticsSummary: () => api<AnalyticsSummary>("/analytics/summary"),
  analyticsReports: (page = 1, page_size = 20) =>
    api<Page<ReportRead>>(`/analytics/reports?page=${page}&page_size=${page_size}`),
};
