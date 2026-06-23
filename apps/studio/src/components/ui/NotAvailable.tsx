// NotAvailable.tsx — honest empty state for Studio features that have no source
// in the open-source Karrio API (app marketplace, plugin registry, MCP server
// proxy, multi-tenant accounts). Never fabricate data/status for these.
import { Icon } from "~/components/ui/icons";

export function NotAvailableNotice({
  feature,
  detail,
}: {
  feature: string;
  detail?: string;
}) {
  return (
    <div
      className="card"
      data-testid="not-available"
      style={{ padding: "20px 22px", display: "flex", gap: 14, alignItems: "flex-start" }}
    >
      <span style={{ color: "var(--fg-muted)", marginTop: 1 }}>
        <Icon.Shield size={18} />
      </span>
      <div>
        <div style={{ fontWeight: 600, marginBottom: 4 }}>
          {feature} isn’t available in this Karrio deployment
        </div>
        <div className="muted" style={{ fontSize: 13, lineHeight: 1.5 }}>
          {detail ??
            "This feature has no endpoint in the open-source Karrio API. It’s available in Karrio Enterprise/Platform, or once the backend exposes it."}
        </div>
      </div>
    </div>
  );
}
