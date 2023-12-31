import { WorkflowPreviewModal } from "@/components/workflow-event-preview";
import { formatDateTimeLong, getURLSearchParams } from "@karrio/lib";
import { useWorkflowEvents } from "@karrio/hooks/workflow-events";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useLoader } from "@karrio/ui/components/loader";
import { AppLink } from "@karrio/ui/components/app-link";
import { ModalProvider } from "@karrio/ui/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";
import { Spinner } from "@karrio/ui/components";
import { useRouter } from "next/router";
import Head from "next/head";
import React from "react";
import { WorkflowEventFilter } from "@karrio/types/graphql/ee";

export { getServerSideProps } from "@/context/main";
const ContextProviders = bundleContexts([
  ModalProvider,
]);

export const WorkflowEventList: React.FC<{ defaultFilter?: WorkflowEventFilter }> = ({ defaultFilter }) => {
  const router = useRouter();
  const loader = useLoader();
  const { query: { data: { workflow_events } = {}, ...query }, filter, setFilter } = useWorkflowEvents({
    setVariablesToURL: true,
    ...(defaultFilter || {}),
  });

  const updateFilter = (extra: Partial<typeof filter> = {}) => {
    const query = {
      ...filter,
      ...getURLSearchParams(),
      ...extra
    };

    setFilter(query);
  }

  React.useEffect(() => { updateFilter(); }, [router.query]);
  React.useEffect(() => { loader.setLoading(query.isFetching); }, [query.isFetching]);
  React.useEffect(() => {
    // if (query.isFetched && !initialized && !isNoneOrEmpty(router.query.modal)) {
    //   previewEvent(router.query.modal as string);
    //   setInitialized(true);
    // }
  }, [router.query.modal, query.isFetched]);

  return (
    <>

      {/* APIs Overview */}
      {!query.isFetched && <Spinner />}

      {(query.isFetched && (workflow_events?.edges || []).length > 0) && <>
        <div className="table-container">
          <table className="workflow-events-table is-size-7 table is-fullwidth">

            <tbody className="workflow-events-table">
              <tr>
                <td className="status"><span className="ml-1">EVENT</span></td>
                <td className="event is-size-7 px-0"></td>
                <td className="date has-text-right mr-2">DATE</td>
              </tr>

              {(workflow_events?.edges || []).map(({ node: event }) => (

                <WorkflowPreviewModal
                  key={event.id}
                  eventId={event.id}
                  trigger={
                    <tr key={event.id} className="items is-clickable">
                      <td className="status is-vcentered">
                        <StatusBadge status={event.status as string} style={{ width: '100%' }} />
                      </td>
                      <td className="description">
                        <span className="text-ellipsis" title={event.event_type || ""}>
                          {`${event.event_type} trigger of ${event.workflow.name}`}
                        </span>
                      </td>
                      <td className="date has-text-right pr-0">
                        <span className="mx-2">{formatDateTimeLong(event.created_at)}</span>
                      </td>
                    </tr>
                  }
                />

              ))}
            </tbody>

          </table>
        </div>

        <footer className="px-2 py-2 is-vcentered">
          <span className="is-size-7 has-text-weight-semibold">
            {(workflow_events?.edges || []).length} results
          </span>

          <div className="buttons has-addons is-centered is-pulled-right">
            <button className="button is-small"
              onClick={() => updateFilter({ offset: (filter.offset as number - 20) })}
              disabled={filter.offset == 0}>
              Previous
            </button>
            <button className="button is-small"
              onClick={() => updateFilter({ offset: (filter.offset as number + 20) })}
              disabled={!workflow_events?.page_info.has_next_page}>
              Next
            </button>
          </div>
        </footer>
      </>}

      {(query.isFetched && (workflow_events?.edges || []).length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No Workflow events found.</p>
        </div>

      </div>}

    </>
  )
};

export default function Page(pageProps: any) {
  const { references } = useAPIMetadata();

  const Component: React.FC = () => {
    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <div className="title is-4">
            <span>Workflows</span>
            <span className="tag is-warning is-size-7 has-text-weight-bold mx-2">BETA</span>
          </div>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/workflows" shallow={false} prefetch={false}>
                <span>Overview</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/workflows/workflow_events" shallow={false} prefetch={false}>
                <span>Event history</span>
              </AppLink>
            </li>
          </ul>
        </div>

        <WorkflowEventList />

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Workflows - ${references?.APP_NAME}`}</title></Head>

      <ContextProviders>
        <Component />
      </ContextProviders>

    </DashboardLayout>
  ), pageProps);
}
