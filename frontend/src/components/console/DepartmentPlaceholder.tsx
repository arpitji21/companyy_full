import { Panel } from "@/components/console/Primitives";

export function DepartmentPlaceholder({
  eyebrow,
  title,
  description,
  plannedFeatures,
}: {
  eyebrow: string;
  title: string;
  description: string;
  plannedFeatures: string[];
}) {
  return (
    <div className="space-y-6">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h1 className="display mt-2 text-3xl">{title}</h1>
      </div>

      <Panel>
        <div className="flex flex-col items-start gap-6 sm:flex-row sm:items-center sm:justify-between">
          <div className="max-w-lg">
            <span className="inline-flex items-center rounded-full bg-[color:var(--surface-elevated)] px-3 py-1 text-[11px] font-medium text-quiet">
              Backend not built yet
            </span>
            <p className="mt-4 text-[14px] leading-relaxed text-quiet">{description}</p>
          </div>
        </div>

        <div className="hairline-t mt-8 pt-6">
          <p className="text-[12.5px] font-semibold tracking-tight">Planned once the API lands</p>
          <ul className="mt-3 grid gap-2.5 sm:grid-cols-2">
            {plannedFeatures.map((f) => (
              <li key={f} className="flex items-start gap-2.5 text-[13px] text-quiet">
                <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-crimson" />
                {f}
              </li>
            ))}
          </ul>
        </div>
      </Panel>
    </div>
  );
}
