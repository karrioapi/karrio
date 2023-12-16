import { CopiableLink } from "@karrio/ui/components/copiable-link";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/components/app-link";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";


export default function ApiPage(pageProps: any) {
  const { references } = useAPIMetadata();

  const Component: React.FC = () => {

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Developers</span>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/developers" shallow={false} prefetch={false}>
                <span>Overview</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/apikeys" shallow={false} prefetch={false}>
                <span>API Keys</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/webhooks" shallow={false} prefetch={false}>
                <span>Webhooks</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/events" shallow={false} prefetch={false}>
                <span>Events</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/logs" shallow={false} prefetch={false}>
                <span>Logs</span>
              </AppLink>
            </li>
          </ul>
        </div>

        {/* APIs Overview */}
        <div className="card px-0 py-3 mt-6">

          <div className="is-flex my-0 px-3">
            <div className="py-1" style={{ width: '40%' }}>API Version</div>
            <div className="py-1" style={{ width: '40%' }}><code>{references?.VERSION}</code></div>
          </div>
          <div className="is-flex my-0 px-3">
            <div className="py-1" style={{ width: '40%' }}>REST API</div>
            <div className="py-1" style={{ width: '40%' }}>
              <CopiableLink className="button is-white py-2 px-1" text={references?.HOST} />
            </div>
          </div>
          <div className="is-flex my-0 px-3">
            <div className="py-1" style={{ width: '40%' }}>GRAPHQL API</div>
            <div className="py-1" style={{ width: '40%' }}>
              <CopiableLink className="button is-white py-2 px-1" text={references?.GRAPHQL} />
            </div>
          </div>
        </div>

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`API Keys - ${references?.APP_NAME}`}</title></Head>
      <Component />
    </DashboardLayout>
  ), pageProps);
}
