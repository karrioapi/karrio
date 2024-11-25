"use client";
import { SurchargeManagement } from "@karrio/ui/admin/surcharge-management";
import { dynamicMetadata } from "@karrio/core/components/metadata";

export const generateMetadata = dynamicMetadata("Surcharges");

export default function Page(pageProps: any) {
  const { APP_NAME } = (pageProps as any).metadata || {};

  const Component= (): JSX.Element =>  {
    return (
      <>
        <header className="px-0 pb-5 pt-1 mb-1">
          <span className="title is-4 has-text-weight-bold">
            Surcharge & discounts
          </span>
        </header>

        {/* Surcharges */}
        <SurchargeManagement />
      </>
    );
  };

  return (
    <>
      <Component />
    </>
  );
}
