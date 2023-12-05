import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { AdminLayout } from "@/layouts/admin-layout";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";


export default function Page(pageProps: any) {
    const { APP_NAME } = (pageProps as any).metadata || {};

    const Component: React.FC = () => {

        return (
            <>
                <header className="px-0 pb-0 pt-2">
                    <span className="title is-4">User accounts</span>
                </header>
            </>
        );
    };

    return AuthenticatedPage((
        <AdminLayout>
            <Head><title>{`Administration - ${APP_NAME}`}</title></Head>

            <Component />

        </AdminLayout>
    ), pageProps)
}
