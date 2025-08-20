"use client";
import { OrganizationManagement } from "@karrio/ui/components/organization-management";
import { SettingsLayout } from "@karrio/ui/components/settings-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

export default function OrganizationPage(pageProps: any) {
  const Component = (): JSX.Element => {
    const { metadata } = useAPIMetadata();

    if (!metadata?.MULTI_ORGANIZATIONS) {
      return (
        <div className="min-h-screen bg-background">
          <div className="container mx-auto p-0">
            <SettingsLayout>
              <div className="text-center py-12">
                <p className="text-muted-foreground">Organization management is not available.</p>
              </div>
            </SettingsLayout>
          </div>
        </div>
      );
    }

    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-0">
          <SettingsLayout showOrganization={true}>
            <OrganizationManagement />
          </SettingsLayout>
        </div>
      </div>
    );
  };

  return <Component />;
}
