# LarkAI Orbit — Backend

FastAPI + PostgreSQL backend for the LarkAI Orbit frontend. This covers
**every department module from the brief** — Auth/Users/Roles, all 15+
department modules, Approvals/Meetings/Notifications, the CEO dashboard,
AI Agents/Chat, real-time notifications, cross-department Analytics, and
production hardening (real DB migrations, Sentry, Celery background jobs,
S3 file storage, a Redis-backed rate limiter). The two things genuinely
still open are the **Workflow engine** (Celery is wired for email/report
jobs, but no workflow-builder tasks exist yet) and **automated test
coverage**, which only covers Auth and the early department modules.

## Quick start (Docker — recommended)

```bash
cp .env.example .env        # edit SECRET_KEY at minimum
docker compose up --build
```

This starts Postgres, Redis, the API (on `http://localhost:8000`), and a
Celery worker. Then, in a second terminal, run migrations and seed data:

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.db.seed
```

The full schema (all ~30 tables) is already captured in the migration
chain under `alembic/versions/` — you don't need to autogenerate anything,
just `upgrade head`. That chain has been verified end-to-end against a
real Postgres 16 database (upgrade *and* downgrade).

API docs: `http://localhost:8000/docs`

## Quick start (local Python, no Docker)

Requires local Postgres + Redis running.

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # point DATABASE_URL / REDIS_URL at your local services
alembic upgrade head
python -m app.db.seed
uvicorn main:app --reload
```

Optional integrations (Sentry, S3, SMTP, ClamAV, LLM providers) all fail
soft when unconfigured — see `.env.example` for what each one needs and
what happens when it's left blank.

## Tests

```bash
pytest
```
Tests run against an in-memory SQLite DB (see `tests/conftest.py`), so they
work with zero external services.

**Current coverage is thin** — Auth, error tracking, and the earlier
department modules (Phase 2/3) have tests; AI Agents/Chat, Customer
Support, Procurement, Clinical, Investor, Tender, Analytics, CEO Dashboard,
Meetings, Approvals, Documents, and the WebSocket route do not yet. This is
the main piece of work left before calling the backend production-hardened.

## What's real vs. scaffolded

| Module | Status |
|---|---|
| Project structure, config, logging, exceptions | ✅ Done |
| Database schema (all ~30 tables) | ✅ Done — real baseline migration, verified against Postgres 16 |
| JWT auth: register/login/refresh/logout/forgot-reset-password/verify-email | ✅ Done |
| Users, Roles & Permissions (RBAC) | ✅ Done |
| Departments | ✅ Done |
| Health check | ✅ Done |
| Employees (CRUD) | ✅ Done |
| Projects & Tasks (CRUD, nested tasks) | ✅ Done |
| Finance (transactions, budgets, summary/cash-flow) | ✅ Done |
| HR (headcount summary, org chart) | ✅ Done; Attendance/Leave/Recruitment/Performance/Payroll/Training still need their own tables |
| Sales (customers, pipeline, forecast summary) | ✅ Done |
| Marketing (campaigns, ROI/conversion summary) | ✅ Done |
| Manufacturing (batches, yield summary) | ✅ Done |
| Quality (checks, pass-rate metrics) | ✅ Done |
| Compliance (records, compliance score) | ✅ Done |
| Regulatory (FDA/CDSCO/ISO/MDR submissions) | ✅ Done |
| Supply Chain (vendors, inventory, reorder alerts) | ✅ Done |
| Research (projects, publications) | ✅ Done |
| Patents & Grants | ✅ Done |
| Approvals (create/list/approve/reject) | ✅ Done — approval-needed emails sent via Celery |
| Meetings (create/list/upcoming) | ✅ Done |
| Notifications | ✅ Done — REST CRUD **and** real-time WebSocket push (Redis pub/sub, multi-process safe) |
| CEO Dashboard aggregation (`/api/ceo/dashboard`) | ✅ Done — see "CEO Dashboard scoring" below |
| Customer Support, Procurement, Clinical, Investor, Tender | ✅ Done |
| AI Agents / Chat | ✅ Done — multi-provider LLM factory (OpenAI, Anthropic, Gemini, Ollama), each provider optional with graceful fallback if its key is missing |
| Analytics (cross-department BI + saved reports) | ✅ Done — reports render in the background via Celery and land in S3 |
| Documents (upload, metadata, S3 storage) | ✅ Done — uploads go through virus scanning (ClamAV if configured, EICAR test-signature check otherwise) |
| Background jobs (Celery) | ✅ Done — password reset/verification emails, approval notices, async report generation, all with retry/backoff and safe no-op if the broker is down |
| Rate limiting | ✅ Done — Redis-backed sliding window, shared correctly across processes, with in-memory fallback if Redis is unreachable |
| Error tracking (Sentry) | ✅ Done — optional, no-ops if `SENTRY_DSN` is unset |
| Workflow engine | 🔲 Placeholder — Celery infrastructure exists and is used elsewhere, but no workflow-builder tasks/routes exist yet |
| Settings module | 🔲 Placeholder |
| Automated test coverage | 🔶 Partial — see "Tests" above |
| CI pipeline | 🔶 A GitHub Actions workflow (pytest + frontend lint/build) was added previously; confirm `.github/workflows/ci.yml` is present in your checkout before relying on it |

## CEO Dashboard scoring

`GET /api/ceo/dashboard` (CEO/Admin only) aggregates Finance, HR, Manufacturing,
Compliance, Quality, Projects, Approvals, Meetings, and Notifications into one
response. Two fields are **composite scores defined by a default formula**
since the brief didn't specify a calculation — both return a `*_breakdown`
dict alongside the score so you can see exactly what drove the number, and
both are easy to re-weight or replace in `app/services/ceo_service.py`:

- **`company_health_score`** (0–100, higher is better): weighted average of
  compliance score (30%), cash-flow health (30%), manufacturing yield rate
  (20%), and operational load / pending-approvals backlog (20%).
- **`risk_score`** (0–100, higher is riskier): weighted average of
  compliance risk (40%), cash-flow risk (30%), and quality fail-rate (30%).

`ai_alerts` is populated by the AI Agents system now that it's built —
see `app/agents/brain.py`.

## Project structure

```
app/
  api/v1/          routers — all department modules, auth, ws, chat, agents
  agents/           AI agent orchestration (brain.py, prompts, context)
  llm/              multi-provider LLM client (OpenAI/Anthropic/Gemini/Ollama)
  auth/            get_current_user, RBAC dependency
  core/            config, security (JWT/bcrypt), logging, exceptions, error_tracking (Sentry)
  db/              engine/session, declarative base, seed script
  models/          SQLAlchemy 2.0 models for every table
  schemas/         Pydantic v2 request/response models
  services/        business logic, one per department + cross-cutting (analytics, ceo, agent)
  repositories/    data-access layer (repository pattern)
  middlewares/      exception handling, request logging, Redis-backed rate limiting
  tasks/           Celery app + registered tasks (email, reports)
  websocket/       connection manager, Redis publisher/listener for realtime notifications
  storage/         S3-compatible object storage client
alembic/           migration environment — baseline + incremental migrations, verified against Postgres
tests/             pytest suite (auth, error tracking, phase2/phase3 department modules)
main.py            FastAPI app factory
```

## Connecting the existing React frontend

The frontend's Vite dev server should point API calls at
`http://localhost:8000/api/...`. CORS is already open for
`http://localhost:5173` and `http://localhost:3000` in `.env.example`.
The frontend now calls the real API directly (`src/lib/orbit-api.ts`) for
every module that's built — there's no mock-JSON fallback left to swap out.
Real-time notifications are wired up via `src/lib/useNotificationSocket.ts`.

## Remaining work

1. **Automated test coverage** — the main open item. Extend `tests/` to
   cover AI Agents/Chat, Customer Support, Procurement, Clinical, Investor,
   Tender, Analytics, CEO Dashboard, Meetings, Approvals, Documents, and the
   WebSocket route, plus add frontend tests.
2. **Workflow engine** — design and build the workflow-builder module
   (routes, models, Celery tasks) that the brief calls for.
3. **Settings module** — still a placeholder route.
4. Confirm the CI workflow (`.github/workflows/ci.yml`) is present and
   passing in your checkout.
