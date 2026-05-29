// SettingsScreen.tsx — Govern › Settings (E6). Workspace / Shipping / Developer.
import { useState } from "react";
import { PageHeader, SettingsGroup, SettingsRow, Toggle } from "~/components/ui/primitives";

export function SettingsScreen() {
  const [autoTrack, setAutoTrack] = useState(true);
  const [insurance, setInsurance] = useState(false);

  return (
    <div className="page" data-testid="screen-settings">
      <PageHeader title="Settings" />
      <SettingsGroup title="Workspace">
        <SettingsRow label="Workspace name" description="Shown across the app." control={<button className="btn btn-sm">acme-shipping</button>} />
        <SettingsRow label="Default address" description="Used as the ship-from when none is set." control={<button className="btn btn-sm">Acme Brooklyn HQ</button>} />
      </SettingsGroup>
      <SettingsGroup title="Shipping">
        <SettingsRow
          label="Auto-create trackers"
          description="Start tracking automatically when a label is purchased."
          control={<Toggle checked={autoTrack} onChange={setAutoTrack} label="Auto-create trackers" testid="set-autotrack" />}
        />
        <SettingsRow
          label="Add insurance by default"
          description="Include insurance on new shipments."
          control={<Toggle checked={insurance} onChange={setInsurance} label="Add insurance" testid="set-insurance" />}
        />
      </SettingsGroup>
      <SettingsGroup title="Developer">
        <SettingsRow label="API version" description="The API version used for requests." control={<button className="btn btn-sm">2026.5</button>} />
        <SettingsRow label="Webhooks" description="Manage webhook endpoints." control={<button className="btn btn-sm">Configure</button>} />
      </SettingsGroup>
    </div>
  );
}
