// SecurityScreen.tsx — Govern › Security (E4). Config surface.
import { useState } from "react";
import { PageHeader, SettingsGroup, SettingsRow, Toggle } from "~/components/ui/primitives";

export function SecurityScreen() {
  const [twoFA, setTwoFA] = useState(true);
  const [sso, setSso] = useState(false);
  const [enforce, setEnforce] = useState(false);

  return (
    <div className="page" data-testid="screen-security">
      <PageHeader title="Security" />
      <SettingsGroup title="Authentication">
        <SettingsRow
          label="Two-factor authentication"
          description="Require a second factor for all members."
          control={<Toggle checked={twoFA} onChange={setTwoFA} label="Two-factor authentication" testid="sec-2fa" />}
        />
        <SettingsRow
          label="Single sign-on (SSO)"
          description="Allow members to sign in with your identity provider."
          control={<Toggle checked={sso} onChange={setSso} label="SSO" testid="sec-sso" />}
        />
        <SettingsRow
          label="Enforce SSO"
          description="Disable password sign-in once SSO is configured."
          control={<Toggle checked={enforce} onChange={setEnforce} label="Enforce SSO" testid="sec-enforce" />}
        />
      </SettingsGroup>
      <SettingsGroup title="Sessions">
        <SettingsRow label="Active sessions" description="Review and revoke active sessions." control={<button className="btn btn-sm">Manage</button>} />
        <SettingsRow label="Session lifetime" description="How long sessions stay valid." control={<button className="btn btn-sm">7 days</button>} />
      </SettingsGroup>
    </div>
  );
}
