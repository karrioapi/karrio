// AppsScreen.tsx — Build › Apps (D1). The OSS Karrio API exposes no app
// marketplace (oauth_apps/app_installations are Enterprise), so this renders an
// honest "not available" state rather than fabricated tiles.
import { Icon } from "~/components/ui/icons";
import { PageHeader } from "~/components/ui/primitives";
import { NotAvailableNotice } from "~/components/ui/NotAvailable";
import { useApps } from "~/lib/karrio/hooks";

export function AppsScreen() {
  useApps(); // exercises the data layer; resolves empty on OSS
  return (
    <div className="page" data-testid="screen-apps">
      <PageHeader title="Apps" actions={<button className="btn"><Icon.External size={14} /> Browse marketplace</button>} />
      <NotAvailableNotice
        feature="The app marketplace"
        detail="Connect commerce platforms and integrations in Karrio Enterprise. The open-source Karrio API doesn’t expose an app marketplace."
      />
    </div>
  );
}
