import { Reveal } from "./Reveal";

const pillars = [
  {
    k: "01",
    title: "Agents that read your ledger",
    body: "Department agents are grounded in live tables — not documents. Ask for the yield drop behind last quarter's margin, and the answer cites the batches.",
  },
  {
    k: "02",
    title: "Provider-agnostic reasoning",
    body: "OpenAI, Claude, Gemini or a private Ollama model, swapped behind one factory. Sensitive workloads never have to leave your perimeter.",
  },
  {
    k: "03",
    title: "Approvals with a paper trail",
    body: "Every agent recommendation becomes a routed approval — requested, reviewed, resolved, and permanently recorded.",
  },
];

export function Intelligence() {
  return (
    <section id="intelligence" className="relative overflow-hidden py-28">
      <div className="halo pointer-events-none absolute inset-x-0 top-1/4 h-[520px] opacity-60" />
      <div className="relative mx-auto max-w-6xl px-6">
        <Reveal>
          <p className="eyebrow">Intelligence layer</p>
          <h2 className="display mt-5 max-w-3xl text-[clamp(2.1rem,5vw,3.6rem)]">
            The enterprise, <span className="text-quiet">answerable.</span>
          </h2>
        </Reveal>

        <div className="mt-16 grid gap-10 md:grid-cols-3">
          {pillars.map((p, i) => (
            <Reveal key={p.k} delay={i * 110}>
              <div className="hairline-t pt-7">
                <span className="font-mono text-[12px] text-crimson">{p.k}</span>
                <h3 className="mt-5 text-[19px] font-semibold leading-snug tracking-tight">
                  {p.title}
                </h3>
                <p className="mt-3 text-[13.5px] leading-relaxed text-quiet">{p.body}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
