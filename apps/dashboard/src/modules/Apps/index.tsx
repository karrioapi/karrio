import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppMenu } from "@karrio/ui/components/app-menu";
import { AppLink } from "@karrio/ui/components/app-link";
import { ModalProvider } from "@karrio/ui/modals/modal";
import { useInstallations } from "@karrio/hooks/apps";
import { bundleContexts } from "@karrio/hooks/utils";
import { Spinner } from "@karrio/ui/components";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";
const ContextProviders = bundleContexts([
  ModalProvider,
]);


export default function Page(pageProps: any) {
  const { references } = useAPIMetadata();

  const Component: React.FC = () => {
    const { query: { data: { installations } = {}, ...query } } = useInstallations();

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <div className="title is-4">
            <span>Apps</span>
            <span className="tag is-warning is-size-7 has-text-weight-bold mx-2">BETA</span>
          </div>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/apps" shallow={false} prefetch={false}>
                <span>Installed</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/apps/development" shallow={false} prefetch={false}>
                <span>Development</span>
              </AppLink>
            </li>
          </ul>
        </div>

        {query.isLoading && <Spinner />}

        {(query.isLoading === false && (installations?.edges || []).length > 0) && <>

          <nav key={Date()} className="panel is-shadowless" style={{ border: '1px solid #e5e5e5', boxShadow: '0.5px 0.5px 2.5px #efefef' }}>
            {(installations?.edges || []).map(({ node: installation }) => (

              <label key={installation.id} className="columns is-mobile m-0 panel-block">

                <AppLink href={`/installations/${installation.id}`} className="column is-11 is-size-7 has-text-grey p-0">
                  <div className="has-text-weight-bold is-size-6 text-ellipsis">{installation.app.display_name}</div>
                  <div className="has-text-weight-semibold mt-2">
                    <span className="tag is-light">{installation.app.developer_name}</span>
                  </div>
                </AppLink>

                <div className="column p-0 is-vcentered">
                  <div className="buttons has-addons is-right">
                    <AppMenu app={installation.app} />
                  </div>
                </div>

              </label>

            ))}
          </nav>

        </>}

        {(query.isLoading === false && (installations?.edges || []).length == 0) && <>
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No apps installed.</p>
            </div>

          </div>
        </>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Apps - ${references?.APP_NAME}`}</title></Head>

      <ContextProviders>
        <Component />
      </ContextProviders>

    </DashboardLayout>
  ), pageProps);
}
