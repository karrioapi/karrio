import ConnectProviderModal, { ConnectProviderModalContext } from "@/components/connect-provider-modal";
import Tabs, { TabStateContext, TabStateProvider } from "@/components/generic/tabs";
import LabelTemplateEditModalProvider from "@/components/label-template-edit-modal";
import { useSystemConnections } from "@/context/system-connection";
import { useCarrierConnections } from "@/context/user-connection";
import SystemConnectionList from "@/components/system-carrier-list";
import UserConnectionList from "@/components/user-carrier-list";
import AuthenticatedPage from "@/layouts/authenticated-page";
import DashboardLayout from "@/layouts/dashboard-layout";
import ConfirmModal from "@/components/confirm-modal";
import { useRouter } from "next/dist/client/router";
import { Loading } from "@/components/loader";
import { useContext, useEffect } from "react";
import Head from "next/head";
import RateSheetEditModalProvider from "@/components/rate-sheet-edit-modal";

export { getServerSideProps } from "@/lib/data-fetching";


export default function ConnectionsPage(pageProps: any) {
  const tabs = ['Your Accounts', 'System Accounts'];

  const Component: React.FC = () => {
    const router = useRouter();
    const { modal } = router.query;
    const { setLoading } = useContext(Loading);
    const { selectTab } = useContext(TabStateContext);
    const { editConnection } = useContext(ConnectProviderModalContext);
    const { query: carrierQuery } = useCarrierConnections();
    const { query: systemQuery } = useSystemConnections();

    useEffect(() => { setLoading(carrierQuery.isFetching || systemQuery.isFetching); });
    useEffect(() => {
      if (modal === 'new') {
        editConnection({ onConfirm: async () => { selectTab(tabs[0]); } });
      }
    }, [modal]);

    return (
      <>
        <header className="px-0 py-6">
          <span className="title is-4">Carriers</span>
          <button className="button is-primary is-small is-pulled-right" onClick={() => editConnection()}>
            <span>Register a carrier</span>
          </button>
        </header>

        <div className="table-container">

          <Tabs tabClass="is-capitalized has-text-weight-semibold" style={{ position: 'relative' }}>

            <UserConnectionList />

            <SystemConnectionList />

          </Tabs>

        </div>

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Carrier Connections - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <ConfirmModal>
        <ConnectProviderModal>
          <LabelTemplateEditModalProvider>
            <RateSheetEditModalProvider>

              <TabStateProvider tabs={tabs} setSelectedToURL={true}>
                <Component />
              </TabStateProvider>

            </RateSheetEditModalProvider>
          </LabelTemplateEditModalProvider>
        </ConnectProviderModal>
      </ConfirmModal>
    </DashboardLayout>
  ), pageProps);
}
