"use client";
import { ParcelsManagement } from "@karrio/ui/components/parcels-management";
import { SettingsLayout } from "@karrio/ui/components/settings-layout";

export default function ParcelsPage(pageProps: any) {
  const Component = (): JSX.Element => {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-0">
          <SettingsLayout>
            <ParcelsManagement />
          </SettingsLayout>
        </div>
      </div>
    );
  };

  return <Component />;
}
