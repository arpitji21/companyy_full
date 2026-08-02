import { Reveal } from "./Reveal";
import logo from "@/assets/lark-logo.png";

export function Platform() {
  return (
    <section id="platform" className="mx-auto max-w-6xl px-6 py-28">
      <Reveal>
        <p className="eyebrow">The platform</p>
        <h2 className="display mt-5 max-w-3xl text-[clamp(2.1rem,5vw,3.6rem)]">
          Precision infrastructure for
          <br />
          <span className="text-quiet">regulated healthcare.</span>
        </h2>
      </Reveal>

      <div className="mt-14 grid gap-4 lg:grid-cols-3">
        <Reveal className="lg:col-span-2">
          <div className="glass h-full rounded-3xl p-10">
            <h3 className="text-[22px] font-semibold tracking-tight">
              A single source of operational truth
            </h3>
            <p className="mt-4 max-w-lg text-[14.5px] leading-relaxed text-quiet">
              Batch yields, budget variance, vendor risk and compliance posture stop living in
              separate spreadsheets. Orbit models them once, then exposes them everywhere — the CEO
              dashboard, the approval queue, and the agents.
            </p>
            <div className="mt-10 grid gap-6 sm:grid-cols-3">
              {[
                ["Real-time", "Aggregations computed on request, never stale"],
                ["Governed", "Role-based permissions on every endpoint"],
                ["Traceable", "Structured logs from edge to database row"],
              ].map(([t, d]) => (
                <div key={t}>
                  <div className="text-[14px] font-semibold">{t}</div>
                  <div className="mt-1.5 text-[12.5px] leading-relaxed text-quiet">{d}</div>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        <Reveal delay={120}>
          <div className="glass flex h-full flex-col justify-between rounded-3xl p-10">
            <img src={logo} alt="Lark Healthcare" className="h-12 w-12 object-contain drift" />
            <div className="mt-12">
              <h3 className="text-[18px] font-semibold leading-snug tracking-tight">
                Built for Lark Healthcare
              </h3>
              <p className="mt-3 text-[13.5px] leading-relaxed text-quiet">
                Designed around pharmaceutical operations — from CDSCO submissions to line-level
                batch quality.
              </p>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
