import { Reveal } from "./Reveal";

const rows = [
  { layer: "Edge", detail: "Rate limiting, structured request logging, unified exception envelope" },
  { layer: "API", detail: "FastAPI v1 router — 22 department routers under a single versioned prefix" },
  { layer: "Domain", detail: "Service layer per department, isolated from transport concerns" },
  { layer: "Data", detail: "Repository pattern over PostgreSQL, migrated with Alembic" },
  { layer: "Async", detail: "Celery workers on Redis for scheduled and long-running work" },
  { layer: "Identity", detail: "JWT auth with refresh rotation and role-based permissions" },
];

export function Architecture() {
  return (
    <section id="architecture" className="mx-auto max-w-6xl px-6 py-28">
      <div className="grid gap-16 lg:grid-cols-[0.85fr_1.15fr]">
        <Reveal>
          <div className="lg:sticky lg:top-28">
            <p className="eyebrow">Architecture</p>
            <h2 className="display mt-5 text-[clamp(2.1rem,5vw,3.4rem)]">
              Layered.
              <br />
              <span className="text-quiet">Auditable.</span>
            </h2>
            <p className="mt-6 max-w-sm text-[14px] leading-relaxed text-quiet">
              Orbit is engineered the way regulated manufacturers are inspected — every request
              traceable from the edge down to the row it changed.
            </p>
          </div>
        </Reveal>

        <div>
          {rows.map((r, i) => (
            <Reveal key={r.layer} delay={i * 70}>
              <div className="hairline-t group flex flex-col gap-1.5 py-6 transition-colors duration-500 sm:flex-row sm:items-baseline sm:gap-10">
                <span className="w-24 shrink-0 font-mono text-[12px] uppercase tracking-widest text-crimson">
                  {r.layer}
                </span>
                <span className="text-[15px] leading-relaxed text-quiet transition-colors duration-500 group-hover:text-foreground">
                  {r.detail}
                </span>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
