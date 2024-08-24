import {
  ConnectProviderModal,
  ConnectProviderModalContext,
} from "@karrio/ui/modals/connect-provider-modal";
import {
  useCarrierConnectionMutation,
  useCarrierConnections,
} from "@karrio/hooks/user-connection";
import { LabelTemplateEditModalProvider } from "@karrio/ui/modals/label-template-edit-modal";
import { UserConnectionList } from "@karrio/ui/forms/user-carrier-list";
import { useSystemConnections } from "@karrio/hooks/system-connection";
import { AuthenticatedPage } from "@karrio/core/layouts/authenticated-page";
import { ConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { DashboardLayout } from "@karrio/core/layouts/dashboard-layout";
import { AppLink } from "@karrio/ui/components/app-link";
import { ModalProvider } from "@karrio/ui/modals/modal";
import { Loading } from "@karrio/ui/components/loader";
import { bundleContexts } from "@karrio/hooks/utils";
import { useRouter } from "next/dist/client/router";
import { useContext, useEffect } from "react";
import Head from "next/head";

export { getServerSideProps } from "@karrio/core/context/main";
const ContextProviders = bundleContexts([
  ModalProvider,
  ConfirmModal,
  ConnectProviderModal,
  LabelTemplateEditModalProvider,
]);

export default function ConnectionsPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const { modal } = router.query;
    const { setLoading } = useContext(Loading);
    const mutation = useCarrierConnectionMutation();
    const { query: systemQuery } = useSystemConnections();
    const { query: carrierQuery } = useCarrierConnections();
    const { editConnection } = useContext(ConnectProviderModalContext);

    useEffect(() => {
      setLoading(carrierQuery.isFetching || systemQuery.isFetching);
    });
    useEffect(() => {
      if (modal === "new") {
        editConnection({
          create: mutation.createCarrierConnection.mutateAsync,
        });
      }
    }, [modal]);

    return (
      <>
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Carriers</span>
          <div>
            <button
              className="button is-primary is-small is-pulled-right"
              onClick={() =>
                editConnection({
                  create: mutation.createCarrierConnection.mutateAsync,
                })
              }
            >
              <span>Register a carrier</span>
            </button>
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/connections" shallow={false} prefetch={false}>
                <span>Your Accounts</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/connections/system"
                shallow={false}
                prefetch={false}
              >
                <span>System Accounts</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/connections/rate-sheets"
                shallow={false}
                prefetch={false}
              >
                <span>Rate Sheets</span>
              </AppLink>
            </li>
          </ul>
        </div>

        <UserConnectionList />
      </>
    );
  };

  return AuthenticatedPage(
    <DashboardLayout showModeIndicator={true}>
      <Head>
        <title>{`Carrier Connections - ${(pageProps as any).metadata?.APP_NAME}`}</title>
      </Head>

      <ContextProviders>
        <Component />
      </ContextProviders>
    </DashboardLayout>,
    pageProps,
  );
}
