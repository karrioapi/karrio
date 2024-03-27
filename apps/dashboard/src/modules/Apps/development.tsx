import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppMenu } from "@karrio/ui/components/app-menu";
import { AppLink } from "@karrio/ui/components/app-link";
import { ModalProvider } from "@karrio/ui/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";
import { usePrivateApps } from "@karrio/hooks/apps";
import { Spinner } from "@karrio/ui/components";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";
const ContextProviders = bundleContexts([
  ModalProvider,
]);


export default function Page(pageProps: any) {
  const { references } = useAPIMetadata();

  const Component: React.FC = () => {
    const { query: { data: { private_apps } = {}, ...query } } = usePrivateApps();

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <div className="title is-4">
            <span>Apps</span>
            <span className="tag is-warning is-size-7 has-text-weight-bold mx-2">BETA</span>
          </div>
          <div>
            <AppLink href={`/apps/new`} className="button is-small is-primary">
              <span>Create app</span>
            </AppLink>
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/apps" shallow={false} prefetch={false}>
                <span>Installed</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/apps/development" shallow={false} prefetch={false}>
                <span>Development</span>
              </AppLink>
            </li>
          </ul>
        </div>

        {query.isLoading && <Spinner />}

        {(query.isLoading === false && (private_apps?.edges || []).length > 0) && <>

          <nav key={Date()} className="panel is-shadowless" style={{ border: '1px solid #e5e5e5', boxShadow: '0.5px 0.5px 2.5px #efefef' }}>
            {(private_apps?.edges || []).map(({ node: app }) => (

              <label key={app.id} className="columns is-mobile m-0 panel-block">

                <AppLink href={`/apps/${app.id}`} className="column is-11 is-size-7 has-text-grey p-0">
                  <div className="has-text-weight-bold is-size-6 text-ellipsis">{app.display_name}</div>
                  <div className="has-text-weight-semibold mt-2">
                    <span className="tag is-light">{app.developer_name}</span>
                  </div>
                </AppLink>

                <div className="column p-0 is-vcentered">
                  <div className="buttons has-addons is-right">
                    <AppMenu app={app} />
                  </div>
                </div>

              </label>

            ))}
          </nav>

        </>}

        {(query.isLoading === false && (private_apps?.edges || []).length == 0) && <>
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No app found.</p>
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
