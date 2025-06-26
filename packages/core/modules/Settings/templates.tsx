"use client";
import { TemplatesManagement } from "@karrio/ui/components/templates-management";
import { SettingsLayout } from "@karrio/ui/components/settings-layout";

export default function TemplatesPage(pageProps: any) {
  const Component = (): JSX.Element => {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-0">
          <SettingsLayout
            title="Document Templates"
          >
            <TemplatesManagement />
          </SettingsLayout>
        </div>
      </div>
    );
  };

  return <Component />;
}
