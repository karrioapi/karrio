"use client";
import { ProfileSettings } from "@karrio/ui/components/profile-settings";
import { SettingsLayout } from "@karrio/ui/components/settings-layout";

export default function ProfilePage(pageProps: any) {
  const Component = (): JSX.Element => {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-0">
          <SettingsLayout>
            <ProfileSettings />
          </SettingsLayout>
        </div>
      </div>
    );
  };

  return <Component />;
}
