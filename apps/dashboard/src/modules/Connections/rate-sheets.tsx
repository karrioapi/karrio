import { LabelTemplateEditModalProvider } from "@karrio/ui/modals/label-template-edit-modal";
import { RateSheetEditModalProvider } from "@karrio/ui/modals/rate-sheet-edit-modal";
import { ConnectProviderModal } from "@karrio/ui/modals/connect-provider-modal";
import { RateSheetModalEditor } from "@karrio/ui/modals/rate-sheet-editor";
import { RateSheetList } from "@karrio/ui/forms/rate-sheet-list";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { useRateSheetMutation } from "@karrio/hooks/rate-sheet";
import { ConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { TabStateContext } from "@karrio/ui/components/tabs";
import { AppLink } from "@karrio/ui/components/app-link";
import { ModalProvider } from "@karrio/ui/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";
import { useContext } from "react";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";
const ContextProviders = bundleContexts([
  ModalProvider,
  ConfirmModal,
  ConnectProviderModal,
  LabelTemplateEditModalProvider,
  RateSheetEditModalProvider,
]);


export default function ConnectionsPage(pageProps: any) {
  const Component: React.FC = () => {
    const mutation = useRateSheetMutation();

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Carriers</span>
          <div>
            <RateSheetModalEditor
              onSubmit={_ => mutation.createRateSheet.mutateAsync(_)}
              trigger={
                <button className="button is-small">
                  <span>Add rate sheet</span>
                </button>
              }
            />
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/connections" shallow={false} prefetch={false}>
                <span>Your Accounts</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/connections/system" shallow={false} prefetch={false}>
                <span>System Accounts</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/connections/rate-sheets" shallow={false} prefetch={false}>
                <span>Rate Sheets</span>
              </AppLink>
            </li>
          </ul>
        </div>

        <RateSheetList />

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Carrier Connections - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <ContextProviders>
        <Component />
      </ContextProviders>

    </DashboardLayout>
  ), pageProps);
}
