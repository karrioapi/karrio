"use client";
import { OrganizationManagement } from "@karrio/ui/components/organization-management";
import { SettingsLayout } from "@karrio/ui/components/settings-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

export default function OrganizationPage(pageProps: any) {
  const Component = (): JSX.Element => {
    const { metadata } = useAPIMetadata();

    if (!metadata?.MULTI_ORGANIZATIONS) {
      return (
        <SettingsLayout>
          <div className="text-center py-12">
            <p className="text-muted-foreground">Organization management is not available.</p>
          </div>
        </SettingsLayout>
      );
    }

    return (
      <SettingsLayout showOrganization={true}>
        <OrganizationManagement />
      </SettingsLayout>
    );
  };

  return <Component />;
}
