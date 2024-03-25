import { SurchargeManagement } from "@karrio/ui/admin/surcharge-management";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { AdminLayout } from "@/layouts/admin-layout";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";


export default function Page(pageProps: any) {
    const { APP_NAME } = (pageProps as any).metadata || {};

    const Component: React.FC = () => {

        return (
            <>
                <header className="px-0 pb-5 pt-1 mb-1">
                    <span className="title is-4 has-text-weight-bold">Surcharge & discounts</span>
                </header>

                {/* Surcharges */}
                <SurchargeManagement />
            </>
        );
    };

    return AuthenticatedPage((
        <AdminLayout>
            <Head><title>{`Surcharges - ${APP_NAME}`}</title></Head>

            <Component />

        </AdminLayout>
    ), pageProps)
}
