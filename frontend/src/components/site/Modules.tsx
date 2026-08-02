import { Reveal } from "./Reveal";

const modules = [
  {
    title: "Finance",
    body: "Transactions, budgets, cash-flow and margin summaries reconciled in real time.",
  },
  {
    title: "Manufacturing",
    body: "Batch records and yield analytics across every production line.",
  },
  {
    title: "Quality",
    body: "Checks, pass-rate metrics and deviation trails ready for audit.",
  },
  {
    title: "Compliance & Regulatory",
    body: "FDA, CDSCO, ISO and MDR submissions scored on one compliance index.",
  },
  {
    title: "Supply Chain",
    body: "Vendors, inventory positions and automatic reorder alerts.",
  },
  {
    title: "Sales & Marketing",
    body: "Pipeline forecasting alongside campaign ROI and conversion.",
  },
  {
    title: "People",
    body: "Employees, headcount summaries and a living org chart.",
  },
  {
    title: "Projects",
    body: "Nested tasks, ownership and delivery status across programs.",
  },
  {
    title: "Executive",
    body: "A single CEO dashboard aggregating every department signal.",
  },
];

export function Modules() {
  return (
    <section id="modules" className="mx-auto max-w-6xl px-6 py-28">
      <Reveal>
        <p className="eyebrow">Coverage</p>
        <h2 className="display mt-5 max-w-2xl text-[clamp(2.1rem,5vw,3.6rem)]">
          Built for the whole
          <br />
          <span className="text-quiet">operating surface.</span>
        </h2>
      </Reveal>

      <div className="mt-14 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {modules.map((m, i) => (
          <Reveal key={m.title} delay={(i % 3) * 90}>
            <article
              className="group h-full rounded-2xl border border-border bg-surface p-7 transition-all duration-500 hover:-translate-y-1"
              style={{ transitionTimingFunction: "var(--ease-apple)" }}
            >
              <div className="h-1 w-8 rounded-full bg-crimson opacity-70 transition-all duration-500 group-hover:w-14 group-hover:opacity-100" />
              <h3 className="mt-6 text-[17px] font-semibold tracking-tight">{m.title}</h3>
              <p className="mt-2.5 text-[13.5px] leading-relaxed text-quiet">{m.body}</p>
            </article>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
