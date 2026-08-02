import heroImg from "@/assets/hero-orbit.jpg";
import logo from "@/assets/lark-logo.png";

export function Hero() {
  return (
    <section id="top" className="relative overflow-hidden pt-36 pb-10">
      <div className="halo pointer-events-none absolute inset-x-0 top-0 h-[720px]" />

      <div className="relative mx-auto max-w-6xl px-6 text-center">
        <div className="reveal inline-flex items-center gap-2.5 rounded-full border border-border px-3.5 py-1.5">
          <img src={logo} alt="" aria-hidden className="h-4 w-4 object-contain" />
          <span className="text-[11.5px] tracking-wide text-quiet">
            Lark Healthcare · Enterprise Intelligence Platform
          </span>
        </div>

        <h1
          className="display reveal mx-auto mt-8 max-w-4xl text-[clamp(2.9rem,8vw,6.2rem)]"
          style={{ animationDelay: "80ms" }}
        >
          One system.
          <br />
          <span className="text-quiet">Every department.</span>
        </h1>

        <p
          className="reveal mx-auto mt-7 max-w-xl text-[17px] leading-relaxed text-quiet"
          style={{ animationDelay: "160ms" }}
        >
          Orbit unifies finance, manufacturing, quality, compliance and supply chain into a single
          operating layer — governed by AI agents that read your live enterprise data.
        </p>

        <div
          className="reveal mt-10 flex flex-wrap items-center justify-center gap-3"
          style={{ animationDelay: "240ms" }}
        >
          <a
            href="#request"
            className="rounded-full bg-primary px-6 py-3 text-[13.5px] font-semibold text-primary-foreground transition-transform duration-300 hover:scale-[1.03]"
            style={{ boxShadow: "var(--shadow-crimson)" }}
          >
            Request access
          </a>
          <a
            href="#platform"
            className="rounded-full border border-border px-6 py-3 text-[13.5px] font-medium transition-colors hover:bg-accent"
          >
            See the platform
          </a>
        </div>
      </div>

      <div className="relative mx-auto mt-16 max-w-5xl px-6">
        <div
          className="reveal overflow-hidden rounded-3xl border border-border"
          style={{ animationDelay: "320ms", boxShadow: "var(--shadow-lift)" }}
        >
          <img
            src={heroImg}
            alt="Orbit enterprise dashboard rendered in dark glass with crimson data highlights"
            width={1600}
            height={1008}
            className="w-full"
          />
        </div>
      </div>
    </section>
  );
}
