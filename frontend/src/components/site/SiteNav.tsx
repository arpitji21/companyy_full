import { useEffect, useState } from "react";
import logo from "@/assets/lark-logo.png";

const links = [
  { label: "Platform", href: "#platform" },
  { label: "Modules", href: "#modules" },
  { label: "Intelligence", href: "#intelligence" },
  { label: "Architecture", href: "#architecture" },
];

export function SiteNav() {
  const [solid, setSolid] = useState(false);

  useEffect(() => {
    const onScroll = () => setSolid(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className="fixed inset-x-0 top-0 z-50 transition-all duration-500"
      style={{
        backgroundColor: solid
          ? "color-mix(in oklab, var(--background) 72%, transparent)"
          : "transparent",
        backdropFilter: solid ? "blur(22px) saturate(180%)" : "none",
        borderBottom: solid ? "1px solid var(--hairline)" : "1px solid transparent",
      }}
    >
      <nav className="mx-auto flex h-14 max-w-6xl items-center justify-between px-6">
        <a href="#top" className="flex items-center gap-2.5">
          <img src={logo} alt="Lark Healthcare" className="h-7 w-7 object-contain" />
          <span className="text-[13px] font-semibold tracking-tight">
            Orbit
            <span className="text-quiet font-normal"> by LarkAI</span>
          </span>
        </a>

        <div className="hidden items-center gap-9 md:flex">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-quiet text-[12.5px] transition-colors hover:text-foreground"
            >
              {l.label}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-4">
        <a href="/login" className="text-quiet text-[12.5px] transition-colors hover:text-foreground">Sign in</a>
        <a
          href="#request"
          className="rounded-full bg-primary px-4 py-1.5 text-[12.5px] font-semibold text-primary-foreground transition-transform duration-300 hover:scale-[1.04]"
        >
          Request access
        </a>
        </div>
      </nav>
    </header>
  );
}
