import { createFileRoute } from "@tanstack/react-router";

import { SiteNav } from "@/components/site/SiteNav";
import { Hero } from "@/components/site/Hero";
import { Stats } from "@/components/site/Stats";
import { Platform } from "@/components/site/Platform";
import { Modules } from "@/components/site/Modules";
import { Intelligence } from "@/components/site/Intelligence";
import { Architecture } from "@/components/site/Architecture";
import { CallToAction, SiteFooter } from "@/components/site/CallToAction";

export const Route = createFileRoute("/")({
  component: Index,
  head: () => ({
    meta: [
      { title: "LarkAI Orbit — Enterprise Intelligence for Lark Healthcare" },
      {
        name: "description",
        content:
          "Orbit unifies finance, manufacturing, quality, compliance and supply chain into one AI-governed operating layer for regulated healthcare manufacturers.",
      },
      { property: "og:title", content: "LarkAI Orbit — Enterprise Intelligence Platform" },
      {
        property: "og:description",
        content:
          "One system. Every department. AI agents grounded in your live enterprise data, built for regulated healthcare.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
});

function Index() {
  return (
    <div className="min-h-screen bg-background">
      <SiteNav />
      <main>
        <Hero />
        <Stats />
        <Platform />
        <Modules />
        <Intelligence />
        <Architecture />
        <CallToAction />
      </main>
      <SiteFooter />
    </div>
  );
}
