"use client";
import { ProductsManagement } from "@karrio/ui/components/products-management";
import { SettingsLayout } from "@karrio/ui/components/settings-layout";

export default function ProductsPage(pageProps: any) {
  const Component = (): JSX.Element => {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-0">
          <SettingsLayout>
            <ProductsManagement />
          </SettingsLayout>
        </div>
      </div>
    );
  };

  return <Component />;
}
