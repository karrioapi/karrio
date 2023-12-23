import { StaffManagement } from "@karrio/ui/admin/staff-management";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { ModalProvider } from "@karrio/ui/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";
import { AdminLayout } from "@/layouts/admin-layout";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";

const ContextProviders = bundleContexts([
    ModalProvider,
]);


export default function Page(pageProps: any) {
    const { APP_NAME } = (pageProps as any).metadata || {};

    const Component: React.FC = () => {
        return (
            <>
                <header className="px-0 pb-5 pt-1 mb-1">
                    <span className="title is-4 has-text-weight-bold">User and permissions</span>
                </header>

                {/* Staff */}
                <StaffManagement />
            </>
        );
    };

    return AuthenticatedPage((
        <AdminLayout>
            <Head><title>{`Users - ${APP_NAME}`}</title></Head>

            <ContextProviders>
                <Component />
            </ContextProviders>

        </AdminLayout>
    ), pageProps)
}
