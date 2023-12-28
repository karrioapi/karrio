import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/components/app-link";
import { useWorkflows } from "@karrio/hooks/workflows";
import { Spinner } from "@karrio/ui/components";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";


export default function Page(pageProps: any) {
  const { references } = useAPIMetadata();

  const Component: React.FC = () => {
    const { query: { data: { workflows } = {}, ...query } } = useWorkflows();

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <div className="title is-4">
            <span>Workflows</span>
            <span className="tag is-warning is-size-7 has-text-weight-bold mx-2">BETA</span>
          </div>
          <div>
            <button className="button is-small">
              <span>Create Workflow</span>
            </button>
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/workflows" shallow={false} prefetch={false}>
                <span>Overview</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/workflows/events" shallow={false} prefetch={false}>
                <span>Event history</span>
              </AppLink>
            </li>
          </ul>
        </div>

        {!query.isFetched && <Spinner />}

        {(query.isFetched && (workflows?.edges || []).length > 0) && <>

          <nav className="panel is-shadowless" style={{ border: '1px solid #e5e5e5', boxShadow: '0.5px 0.5px 2.5px #efefef' }}>
            {(workflows?.edges || []).map(({ node: workflow }) => (<>

              <a key={workflow.id} className="columns m-0 panel-block">

                <div className="column is-11 is-size-7 has-text-grey p-0">
                  <div className="has-text-weight-bold is-size-6">{workflow.name}</div>
                  <div className="has-text-weight-semibold mt-2">
                    <span className="tag is-light">{`${workflow.action_nodes.length} actions`}</span>
                  </div>
                </div>

                <div className="column p-0 is-vcentered">
                  <div className="buttons has-addons is-right">
                    <button className="button is-default">
                      <span className="icon is-small">
                        <i className="fas fa-ellipsis-h"></i>
                      </span>
                    </button>
                  </div>
                </div>

              </a>

            </>))}
          </nav>

        </>}

        {(query.isFetched && (workflows?.edges || []).length == 0) && <>
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No workflow found.</p>
            </div>

          </div>
        </>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Workflows - ${references?.APP_NAME}`}</title></Head>
      <Component />
    </DashboardLayout>
  ), pageProps);
}
