// Placeholder.tsx — foundation stand-in for screens not yet implemented.
import { NAV } from "~/lib/modes";

function labelFor(route: string): string {
  for (const groups of Object.values(NAV)) {
    for (const group of groups) {
      const item = group.items.find((i) => i.route === route);
      if (item) return item.label;
    }
  }
  return route;
}

export function Placeholder({ route }: { route: string }) {
  const label = labelFor(route);
  return (
    <div className="page" data-testid={`screen-${route}`}>
      <div className="page-header">
        <h1 className="page-title">{label}</h1>
      </div>
      <div className="placeholder">
        <h2>{label}</h2>
        <p>
          This screen is part of the Karrio Studio migration and is tracked in
          Linear. It renders at <code>/{route}</code> and will be wired to the
          Karrio GraphQL/REST API via <code>@karrio/hooks</code>.
        </p>
      </div>
    </div>
  );
}
