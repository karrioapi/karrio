"use client";
import { AccountSettings } from "@karrio/ui/components/account-settings";
import { SettingsLayout } from "@karrio/ui/components/settings-layout";

export default function AccountPage(pageProps: any) {
  const Component = (): JSX.Element => {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-0">
          <SettingsLayout>
            <AccountSettings />
          </SettingsLayout>
        </div>
      </div>
    );
  };

  return <Component />;
}
