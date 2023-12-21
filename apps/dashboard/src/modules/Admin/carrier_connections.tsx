import { LabelTemplateEditModalProvider } from "@karrio/ui/modals/label-template-edit-modal";
import { SystemCarrierManagement } from "@karrio/ui/admin/system-carrier-management";
import { RateSheetEditModalProvider } from "@karrio/ui/modals/rate-sheet-edit-modal";
import { ConnectProviderModal } from "@karrio/ui/modals/connect-provider-modal";
import { RateSheetManagement } from "@karrio/ui/admin/rate-sheet-management";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { ConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { bundleContexts } from '@karrio/hooks/utils';
import { AdminLayout } from "@/layouts/admin-layout";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";

const ContextProviders = bundleContexts([
    ConfirmModal,
    ConnectProviderModal,
    LabelTemplateEditModalProvider,
    RateSheetEditModalProvider,
]);


export default function Page(pageProps: any) {
    const { APP_NAME } = (pageProps as any).metadata || {};

    const Component: React.FC = () => {

        return (
            <>
                <header className="px-0 pb-5 pt-1 mb-1">
                    <span className="title is-4 has-text-weight-bold">Carrier connections</span>
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

    return AuthenticatedPage((
        <AdminLayout showModeIndicator={true}>
            <Head><title>{`Carriers - ${APP_NAME}`}</title></Head>

            <ContextProviders>
                <Component />
            </ContextProviders>

        </AdminLayout>
    ), pageProps)
}
