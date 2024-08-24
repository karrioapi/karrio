"use client";
import { LabelTemplateEditModalProvider } from "@karrio/ui/modals/label-template-edit-modal";
import { SystemCarrierManagement } from "@karrio/ui/admin/system-carrier-management";
import { ConnectProviderModal } from "@karrio/ui/modals/connect-provider-modal";
import { RateSheetManagement } from "@karrio/ui/admin/rate-sheet-management";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { ConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { bundleContexts } from "@karrio/hooks/utils";

export const generateMetadata = dynamicMetadata("Carriers");

const ContextProviders = bundleContexts([
  ConfirmModal,
  ConnectProviderModal,
  LabelTemplateEditModalProvider,
]);

export default function Page(pageProps: any) {
  const Component: React.FC = () => {
    return (
      <>
        <header className="px-0 pb-5 pt-1 mb-1">
          <span className="title is-4 has-text-weight-bold">
            Carrier connections
          </span>
        </header>

        {/* System carriers */}
        <SystemCarrierManagement />

        <div className="p-4"></div>

        {/* System carriers */}
        <RateSheetManagement />

        <div className="p-4"></div>
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
