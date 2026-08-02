//#region node_modules/.nitro/vite/services/ssr/assets/orbit-api-Ceoci-7Q.js
/**
* Orbit API client — talks to the LarkAI Orbit FastAPI backend.
* Base URL comes from VITE_ORBIT_API_URL (defaults to local dev backend).
*/
var ORBIT_BASE_URL = "http://localhost:8000";
/** Builds the /ws/notifications URL for the current access token, reusing
* ORBIT_BASE_URL so dev/staging/prod all point at the right backend without
* separate config. http(s) -> ws(s) since browsers require the ws/wss
* scheme for WebSocket connections even when the API itself is https. */
function notificationsSocketUrl(accessToken) {
	return `${ORBIT_BASE_URL.replace(/^http/, "ws")}/api/ws/notifications?token=${encodeURIComponent(accessToken)}`;
}
var ACCESS_KEY = "orbit.access_token";
var REFRESH_KEY = "orbit.refresh_token";
var tokens = {
	get access() {
		if (typeof window === "undefined") return null;
		return window.localStorage.getItem(ACCESS_KEY);
	},
	get refresh() {
		if (typeof window === "undefined") return null;
		return window.localStorage.getItem(REFRESH_KEY);
	},
	set(access, refresh) {
		window.localStorage.setItem(ACCESS_KEY, access);
		window.localStorage.setItem(REFRESH_KEY, refresh);
	},
	clear() {
		window.localStorage.removeItem(ACCESS_KEY);
		window.localStorage.removeItem(REFRESH_KEY);
	}
};
var ApiError = class extends Error {
	status;
	constructor(status, message) {
		super(message);
		this.status = status;
	}
};
async function parseError(res) {
	let detail = res.statusText;
	try {
		const body = await res.json();
		if (typeof body?.detail === "string") detail = body.detail;
		else if (Array.isArray(body?.detail)) detail = body.detail[0]?.msg ?? detail;
		else if (typeof body?.message === "string") detail = body.message;
	} catch {}
	return new ApiError(res.status, detail);
}
async function refreshSession() {
	const refresh_token = tokens.refresh;
	if (!refresh_token) return false;
	const res = await fetch(`${ORBIT_BASE_URL}/api/auth/refresh`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ refresh_token })
	});
	if (!res.ok) return false;
	const data = await res.json();
	tokens.set(data.access_token, data.refresh_token);
	return true;
}
async function api(path, options = {}) {
	const { method = "GET", body, auth = true, retry = true } = options;
	const headers = { "Content-Type": "application/json" };
	if (auth && tokens.access) headers.Authorization = `Bearer ${tokens.access}`;
	const res = await fetch(`${ORBIT_BASE_URL}/api${path}`, {
		method,
		headers,
		body: body === void 0 ? void 0 : JSON.stringify(body)
	});
	if (res.status === 401 && auth && retry) {
		if (await refreshSession()) return api(path, {
			...options,
			retry: false
		});
		tokens.clear();
		throw new ApiError(401, "Session expired. Please sign in again.");
	}
	if (!res.ok) throw await parseError(res);
	if (res.status === 204) return void 0;
	return await res.json();
}
var orbit = {
	login: (email, password) => api("/auth/login", {
		method: "POST",
		body: {
			email,
			password
		},
		auth: false
	}),
	register: (payload) => api("/auth/register", {
		method: "POST",
		body: payload,
		auth: false
	}),
	me: () => api("/auth/me"),
	logout: (refresh_token) => api("/auth/logout", {
		method: "POST",
		body: { refresh_token }
	}),
	ceoDashboard: () => api("/ceo/dashboard"),
	financeSummary: () => api("/finance/summary"),
	transactions: (page = 1, page_size = 20) => api(`/finance/transactions?page=${page}&page_size=${page_size}`),
	employees: (page = 1, page_size = 20) => api(`/employees?page=${page}&page_size=${page_size}`),
	headcount: () => api("/hr/headcount"),
	notifications: (page = 1, page_size = 20) => api(`/notifications?page=${page}&page_size=${page_size}`),
	unreadCount: () => api("/notifications/unread-count"),
	markRead: (id) => api(`/notifications/${id}/read`, { method: "POST" }),
	agents: () => api("/agents"),
	chat: (payload) => api("/chat", {
		method: "POST",
		body: payload
	}),
	salesSummary: () => api("/sales/summary"),
	customers: (page = 1, page_size = 20) => api(`/sales/customers?page=${page}&page_size=${page_size}`),
	deals: (page = 1, page_size = 20) => api(`/sales/deals?page=${page}&page_size=${page_size}`),
	marketingSummary: () => api("/marketing/summary"),
	campaigns: (page = 1, page_size = 20) => api(`/marketing/campaigns?page=${page}&page_size=${page_size}`),
	manufacturingSummary: () => api("/manufacturing/summary"),
	batches: (page = 1, page_size = 20) => api(`/manufacturing/batches?page=${page}&page_size=${page_size}`),
	qualityMetrics: () => api("/quality/metrics"),
	qualityChecks: (page = 1, page_size = 20) => api(`/quality/checks?page=${page}&page_size=${page_size}`),
	complianceSummary: () => api("/compliance/summary"),
	complianceRecords: (page = 1, page_size = 20) => api(`/compliance/records?page=${page}&page_size=${page_size}`),
	regulatorySummary: () => api("/regulatory/summary"),
	regulatorySubmissions: (page = 1, page_size = 20) => api(`/regulatory/submissions?page=${page}&page_size=${page_size}`),
	supplyChainSummary: () => api("/supply-chain/summary"),
	vendors: (page = 1, page_size = 20) => api(`/supply-chain/vendors?page=${page}&page_size=${page_size}`),
	inventory: (page = 1, page_size = 20) => api(`/supply-chain/inventory?page=${page}&page_size=${page_size}`),
	researchSummary: () => api("/research/summary"),
	researchProjects: (page = 1, page_size = 20) => api(`/research/projects?page=${page}&page_size=${page_size}`),
	researchPublications: (page = 1, page_size = 20) => api(`/research/publications?page=${page}&page_size=${page_size}`),
	patentSummary: () => api("/patent/summary"),
	patentFilings: (page = 1, page_size = 20) => api(`/patent/filings?page=${page}&page_size=${page_size}`),
	grantSummary: () => api("/grant/summary"),
	grantApplications: (page = 1, page_size = 20) => api(`/grant/applications?page=${page}&page_size=${page_size}`),
	documentsSummary: () => api("/documents/summary"),
	documents: (page = 1, page_size = 20) => api(`/documents?page=${page}&page_size=${page_size}`),
	projects: (page = 1, page_size = 20) => api(`/projects?page=${page}&page_size=${page_size}`),
	meetings: (page = 1, page_size = 20) => api(`/meetings?page=${page}&page_size=${page_size}`),
	upcomingMeetings: () => api("/meetings/upcoming"),
	approvals: (page = 1, page_size = 20) => api(`/approvals?page=${page}&page_size=${page_size}`),
	decideApproval: (id, approve, notes) => api(`/approvals/${id}/decision`, {
		method: "POST",
		body: {
			approve,
			notes
		}
	}),
	customerSummary: () => api("/customer/summary"),
	supportTickets: (page = 1, page_size = 20) => api(`/customer/tickets?page=${page}&page_size=${page_size}`),
	procurementSummary: () => api("/procurement/summary"),
	purchaseOrders: (page = 1, page_size = 20) => api(`/procurement/orders?page=${page}&page_size=${page_size}`),
	clinicalSummary: () => api("/clinical/summary"),
	clinicalTrials: (page = 1, page_size = 20) => api(`/clinical/trials?page=${page}&page_size=${page_size}`),
	clinicalEvents: (page = 1, page_size = 20) => api(`/clinical/events?page=${page}&page_size=${page_size}`),
	investorSummary: () => api("/investor/summary"),
	fundingRounds: (page = 1, page_size = 20) => api(`/investor/rounds?page=${page}&page_size=${page_size}`),
	investorUpdates: (page = 1, page_size = 20) => api(`/investor/updates?page=${page}&page_size=${page_size}`),
	tenderSummary: () => api("/tender/summary"),
	tenders: (page = 1, page_size = 20) => api(`/tender/tenders?page=${page}&page_size=${page_size}`),
	analyticsSummary: () => api("/analytics/summary"),
	analyticsReports: (page = 1, page_size = 20) => api(`/analytics/reports?page=${page}&page_size=${page_size}`)
};
//#endregion
export { tokens as a, refreshSession as i, notificationsSocketUrl as n, orbit as r, ORBIT_BASE_URL as t };
