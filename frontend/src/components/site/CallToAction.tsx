import { Reveal } from "./Reveal";
import logo from "@/assets/lark-logo.png";

export function CallToAction() {
  return (
    <section id="request" className="relative overflow-hidden py-32">
      <div className="halo pointer-events-none absolute inset-x-0 bottom-0 h-[560px] rotate-180" />
      <div className="relative mx-auto max-w-3xl px-6 text-center">
        <Reveal>
          <h2 className="display text-[clamp(2.4rem,6vw,4.4rem)]">
            Bring your enterprise
            <br />
            <span className="text-quiet">into orbit.</span>
          </h2>
          <p className="mx-auto mt-6 max-w-md text-[15px] leading-relaxed text-quiet">
            Private deployments for regulated manufacturers. Talk to the LarkAI team about a
            rollout.
          </p>
          <form
            className="mx-auto mt-10 flex max-w-md flex-col gap-3 sm:flex-row"
            onSubmit={(e) => e.preventDefault()}
          >
            <label htmlFor="work-email" className="sr-only">
              Work email
            </label>
            <input
              id="work-email"
              type="email"
              required
              placeholder="you@company.com"
              className="h-12 flex-1 rounded-full border border-input bg-surface px-5 text-[14px] outline-none transition-colors placeholder:text-muted-foreground focus:border-ring"
            />
            <button
              type="submit"
              className="h-12 rounded-full bg-primary px-7 text-[13.5px] font-semibold text-primary-foreground transition-transform duration-300 hover:scale-[1.03]"
              style={{ boxShadow: "var(--shadow-crimson)" }}
            >
              Request access
            </button>
          </form>
        </Reveal>
      </div>
    </section>
  );
}

export function SiteFooter() {
  return (
    <footer className="hairline-t">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 py-10 sm:flex-row">
        <div className="flex items-center gap-2.5">
          <img src={logo} alt="Lark Healthcare" className="h-6 w-6 object-contain" />
          <span className="text-[12.5px] text-quiet">
            LarkAI Orbit — Lark Healthcare · © {new Date().getFullYear()}
          </span>
        </div>
        <span className="text-[12.5px] text-quiet">Chennai · India</span>
      </div>
    </footer>
  );
}
