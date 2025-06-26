"use client";
import { AddressesManagement } from "@karrio/ui/components/addresses-management";
import { SettingsLayout } from "@karrio/ui/components/settings-layout";

export default function AddressesPage(pageProps: any) {
  const Component = (): JSX.Element => {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-0">
          <SettingsLayout>
            <AddressesManagement />
          </SettingsLayout>
        </div>
      </div>
    );
  };

  return <Component />;
}
