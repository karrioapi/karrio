"use client";
import { StaffManagement } from "@karrio/ui/admin/staff-management";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { ModalProvider } from "@karrio/ui/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";

export const generateMetadata = dynamicMetadata("Staff");
const ContextProviders = bundleContexts([ModalProvider]);

export default function Page(pageProps: any) {
  const Component= (): JSX.Element =>  {
    return (
      <>
        <header className="px-0 pb-5 pt-1 mb-1">
          <span className="title is-4 has-text-weight-bold">
            User and permissions
          </span>
        </header>

        {/* Staff */}
        <StaffManagement />
      </>
    );
  };

  return (
    <>
      <ContextProviders>
        <Component />
      </ContextProviders>
    </>
  );
}
