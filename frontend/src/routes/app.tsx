import { createFileRoute, Link, Outlet, useNavigate, useRouterState } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { ChevronLeft, LogOut, Menu } from "lucide-react";
import { useEffect, useState } from "react";
import logo from "@/assets/lark-logo.png";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { AuthProvider, useAuth } from "@/lib/auth";
import { orbit } from "@/lib/orbit-api";
import { useNotificationSocket } from "@/lib/useNotificationSocket";

export const Route = createFileRoute("/app")({
  ssr: false,
  head: () => ({
    meta: [
      { title: "Orbit Console — LarkAI Healthcare" },
      {
        name: "description",
        content:
          "Live enterprise console for LarkAI Orbit: finance, people, notifications and AI agents from the Orbit API.",
      },
      { property: "og:title", content: "Orbit Console — LarkAI Healthcare" },
      {
        property: "og:description",
        content: "Live enterprise operations console powered by the LarkAI Orbit API.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: () => (
    <AuthProvider>
      <ConsoleShell />
    </AuthProvider>
  ),
});

const navGroups: { label: string | null; items: { to: string; label: string; exact?: boolean }[] }[] = [
  {
    label: null,
    items: [{ to: "/app", label: "Overview", exact: true }],
  },
  {
    label: "Live",
    items: [
      { to: "/app/finance", label: "Finance" },
      { to: "/app/sales", label: "Sales" },
      { to: "/app/marketing", label: "Marketing" },
      { to: "/app/manufacturing", label: "Manufacturing" },
      { to: "/app/quality", label: "Quality" },
      { to: "/app/compliance", label: "Compliance" },
      { to: "/app/regulatory", label: "Regulatory" },
      { to: "/app/supply-chain", label: "Supply Chain" },
      { to: "/app/research", label: "Research" },
      { to: "/app/patent", label: "Patent" },
      { to: "/app/grant", label: "Grant" },
      { to: "/app/docs", label: "Docs" },
      { to: "/app/projects", label: "Projects" },
      { to: "/app/meetings", label: "Meetings" },
      { to: "/app/approvals", label: "Approvals" },
      { to: "/app/people", label: "People" },
      { to: "/app/notifications", label: "Notifications" },
      { to: "/app/assistant", label: "AI Assistant" },
      { to: "/app/clinical", label: "Clinical" },
      { to: "/app/investor", label: "Investor" },
      { to: "/app/tender", label: "Tender" },
      { to: "/app/customer", label: "Customer" },
      { to: "/app/procurement", label: "Procurement" },
      { to: "/app/analytics", label: "Analytics" },
    ],
  },
];

const nav = navGroups.flatMap((g) => g.items);

function ConsoleShell() {
  const { user, status, signOut } = useAuth();
  const navigate = useNavigate();
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const [menuOpen, setMenuOpen] = useState(false);

  useNotificationSocket(status === "authenticated");
  const unread = useQuery({
    queryKey: ["notifications", "unread-count"],
    queryFn: () => orbit.unreadCount(),
    enabled: status === "authenticated",
    // The socket keeps this fresh in real time; this poll is just the
    // fallback for tabs where the WebSocket hasn't connected yet, or a
    // Redis outage has degraded push back to poll-only.
    refetchInterval: 60_000,
  });
  const unreadCount = Number((unread.data as Record<string, number> | undefined)?.unread_count ?? 0);

  useEffect(() => {
    if (status === "anonymous") void navigate({ to: "/login", replace: true });
  }, [status, navigate]);

  // Close the mobile drawer automatically whenever the route changes.
  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  if (status !== "authenticated") {
    return (
      <div className="text-quiet flex min-h-screen items-center justify-center text-[13px]">
        {status === "loading" ? "Connecting to Orbit…" : "Redirecting to sign in…"}
      </div>
    );
  }

  const current = nav.find((item) => (item.exact ? pathname === item.to : pathname.startsWith(item.to)));
  const isRoot = pathname === "/app";

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b border-[color:var(--hairline)] bg-[color-mix(in_oklab,var(--background)_82%,transparent)] backdrop-blur-xl">
        <div className="mx-auto flex h-14 max-w-7xl items-center justify-between gap-3 px-4 sm:px-6">
          <div className="flex min-w-0 items-center gap-1.5">
            <button
              onClick={() => setMenuOpen(true)}
              aria-label="Open menu"
              className="text-quiet -ml-1.5 shrink-0 rounded-full p-2 transition-colors hover:bg-[color:var(--surface-elevated)] hover:text-foreground lg:hidden"
            >
              <Menu className="h-[18px] w-[18px]" />
            </button>
            <Link to="/app" className="flex min-w-0 items-center gap-2.5">
              <img src={logo} alt="Lark Healthcare" className="h-7 w-7 shrink-0 object-contain" />
              <span className="truncate text-[13px] font-semibold tracking-tight">Orbit Console</span>
            </Link>
          </div>
          <div className="flex shrink-0 items-center gap-3 sm:gap-4">
            <span className="text-quiet hidden text-[12.5px] sm:block">{user?.full_name}</span>
            <button
              onClick={() => void signOut()}
              aria-label="Sign out"
              className="text-quiet flex items-center gap-1.5 rounded-full border border-[color:var(--hairline)] p-2 text-[12px] transition-colors hover:bg-[color:var(--surface-elevated)] hover:text-foreground sm:px-3.5 sm:py-1.5"
            >
              <LogOut className="h-[15px] w-[15px] sm:hidden" />
              <span className="hidden sm:inline">Sign out</span>
            </button>
          </div>
        </div>

        {/* Mobile-only: always-available way back to the main control page,
            since the full section list lives in the drawer, not on-screen. */}
        {!isRoot && (
          <div className="border-t border-[color:var(--hairline)] px-4 py-2 lg:hidden">
            <Link
              to="/app"
              className="text-quiet inline-flex items-center gap-1 text-[12.5px] transition-colors hover:text-foreground"
            >
              <ChevronLeft className="h-3.5 w-3.5" />
              Overview
              {current && <span className="text-foreground font-medium">&nbsp;/ {current.label}</span>}
            </Link>
          </div>
        )}
      </header>

      <Sheet open={menuOpen} onOpenChange={setMenuOpen}>
        <SheetContent side="left" className="glass flex w-[82%] max-w-xs flex-col gap-0 p-0">
          <SheetHeader className="border-b border-[color:var(--hairline)] px-5 py-4 text-left">
            <SheetTitle className="flex items-center gap-2.5 text-[13px] font-semibold tracking-tight">
              <img src={logo} alt="Lark Healthcare" className="h-6 w-6 object-contain" />
              Orbit Console
            </SheetTitle>
          </SheetHeader>

          <nav className="flex-1 space-y-5 overflow-y-auto px-3 py-4">
            {navGroups.map((group) => (
              <div key={group.label ?? "top"}>
                {group.label && (
                  <p className="text-quiet mb-1.5 px-3.5 text-[10.5px] font-semibold tracking-wider uppercase">
                    {group.label}
                  </p>
                )}
                <div className="space-y-1">
                  {group.items.map((item) => {
                    const active = item.exact ? pathname === item.to : pathname.startsWith(item.to);
                    return (
                      <SheetClose asChild key={item.to}>
                        <Link
                          to={item.to}
                          className={`block rounded-xl px-3.5 py-2.5 text-[13.5px] transition-colors ${
                            active
                              ? "bg-[color:var(--surface-elevated)] font-semibold text-foreground"
                              : "text-quiet hover:bg-[color:var(--surface-elevated)] hover:text-foreground"
                          }`}
                        >
                          <span className="flex items-center justify-between gap-2">
                            {item.label}
                            {item.to === "/app/notifications" && unreadCount > 0 && (
                              <span className="rounded-full bg-[color:var(--accent,#4f7cff)] px-1.5 py-0.5 text-[10px] font-semibold text-white">
                                {unreadCount > 99 ? "99+" : unreadCount}
                              </span>
                            )}
                          </span>
                        </Link>
                      </SheetClose>
                    );
                  })}
                </div>
              </div>
            ))}
          </nav>

          <div className="border-t border-[color:var(--hairline)] px-5 py-4">
            <p className="truncate text-[12.5px] font-medium">{user?.full_name}</p>
            <p className="text-quiet truncate text-[11.5px]">{user?.email}</p>
            <button
              onClick={() => void signOut()}
              className="mt-3 flex w-full items-center justify-center gap-1.5 rounded-full border border-[color:var(--hairline)] py-2 text-[12.5px] transition-colors hover:bg-[color:var(--surface-elevated)]"
            >
              <LogOut className="h-[14px] w-[14px]" />
              Sign out
            </button>
          </div>
        </SheetContent>
      </Sheet>

      <div className="mx-auto flex max-w-7xl gap-8 px-4 py-6 sm:px-6 sm:py-8">
        <aside className="hidden w-52 shrink-0 lg:block">
          <nav className="sticky top-24 max-h-[calc(100vh-7rem)] space-y-5 overflow-y-auto pb-6 pr-1">
            {navGroups.map((group) => (
              <div key={group.label ?? "top"}>
                {group.label && (
                  <p className="text-quiet mb-1.5 px-3.5 text-[10.5px] font-semibold tracking-wider uppercase">
                    {group.label}
                  </p>
                )}
                <div className="space-y-1">
                  {group.items.map((item) => {
                    const active = item.exact ? pathname === item.to : pathname.startsWith(item.to);
                    return (
                      <Link
                        key={item.to}
                        to={item.to}
                        className={`block rounded-xl px-3.5 py-2 text-[13px] transition-colors ${
                          active
                            ? "bg-[color:var(--surface-elevated)] font-semibold text-foreground"
                            : "text-quiet hover:text-foreground"
                        }`}
                      >
                        <span className="flex items-center justify-between gap-2">
                          {item.label}
                          {item.to === "/app/notifications" && unreadCount > 0 && (
                            <span className="rounded-full bg-[color:var(--accent,#4f7cff)] px-1.5 py-0.5 text-[10px] font-semibold text-white">
                              {unreadCount > 99 ? "99+" : unreadCount}
                            </span>
                          )}
                        </span>
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}
          </nav>
        </aside>

        <main className="min-w-0 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
