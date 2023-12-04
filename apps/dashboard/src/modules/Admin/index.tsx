import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { AdminLayout } from "@/layouts/admin-layout";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";


export default function Page(pageProps: any) {
    const { APP_NAME } = (pageProps as any).metadata || {};

    const Component: React.FC = () => {

        return (
            <>
                <header className="px-0 py-4">
                    <span className="title is-4">Platform details</span>
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
