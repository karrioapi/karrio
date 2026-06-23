// PluginsScreen.tsx — Build › Plugins (D2). The OSS Karrio API exposes no plugin
// registry, so this renders an honest "not available" state. (Carrier
// connectors are managed under Ship › Connections.)
import { Icon } from "~/components/ui/icons";
import { PageHeader } from "~/components/ui/primitives";
import { NotAvailableNotice } from "~/components/ui/NotAvailable";
import { usePlugins } from "~/lib/karrio/hooks";

export function PluginsScreen() {
  usePlugins(); // exercises the data layer; resolves empty on OSS
  return (
    <div className="page" data-testid="screen-plugins">
      <PageHeader title="Plugins" actions={<button className="btn"><Icon.External size={14} /> Plugin docs</button>} />
      <NotAvailableNotice
        feature="The plugin registry"
        detail="A browsable plugin registry isn’t exposed by the open-source Karrio API. Carrier connectors are configured under Ship › Connections."
      />
    </div>
  );
}
