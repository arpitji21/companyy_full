import { Reveal } from "./Reveal";

const stats = [
  { value: "22", label: "Live API modules" },
  { value: "30+", label: "Governed data tables" },
  { value: "4", label: "LLM providers wired" },
  { value: "<120ms", label: "Median API response" },
];

export function Stats() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-24">
      <div className="grid grid-cols-2 gap-px overflow-hidden rounded-3xl border border-border bg-border md:grid-cols-4">
        {stats.map((s, i) => (
          <Reveal key={s.label} delay={i * 80}>
            <div className="h-full bg-background px-7 py-10">
              <div className="display text-[clamp(2rem,4vw,2.9rem)]">{s.value}</div>
              <div className="mt-2 text-[12.5px] text-quiet">{s.label}</div>
            </div>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
