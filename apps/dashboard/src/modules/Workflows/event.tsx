import { failsafe, formatDateTimeLong, isNone, jsonify } from "@karrio/lib";
import { Tabs, TabStateProvider } from "@karrio/ui/components/tabs";
import { CopiableLink } from "@karrio/ui/components/copiable-link";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { useWorkflowEvent } from "@karrio/hooks/workflow-events";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useLoader } from "@karrio/ui/components/loader";
import { AppLink } from "@karrio/ui/components/app-link";
import { useRouter } from "next/dist/client/router";
import json from 'highlight.js/lib/languages/json';
import hljs from "highlight.js";
import Head from "next/head";
import moment from "moment";
import React from "react";

export { getServerSideProps } from "@/context/main";

hljs.registerLanguage('json', json);


export const Component: React.FC<{ eventId?: string }> = ({ eventId }) => {
  const router = useRouter();
  const { setLoading } = useLoader();
  const entity_id = eventId || router.query.id as string;
  const { query: { data: { workflow_event } = {}, ...query } } = useWorkflowEvent(entity_id);

  React.useEffect(() => {
    (window as any).moment = moment;
    setLoading(query.isFetching);
  }, [query.isFetching]);

  return (
    <>
      {workflow_event !== undefined && <>

        <div className="columns my-1">
          <div className="column is-10">
            <span className="subtitle is-size-7 has-text-weight-semibold">WORKFLOW EVENT</span>
            <br />
            <div className="title is-5">
              <span className="mr-2">{workflow_event?.event_type}</span>
              <StatusBadge status={workflow_event?.status as string} />
            </div>
          </div>
          {!isNone(eventId) && <div className="column is-2 is-flex is-justify-content-end">
            <AppLink href={`/workflows/events/${eventId}`} target="blank"
              className="button is-default has-text-info is-small mx-1">
              <span className="icon">
                <i className="fas fa-external-link-alt"></i>
              </span>
            </AppLink>
          </div>}
        </div>

        <hr className="mt-1 mb-2" style={{ height: '1px' }} />

        <div className="py-3">
          <div className="columns my-0">
            <div className="column is-3 py-1">ID</div>
            <div className="column is-8 py-1">{workflow_event?.id}</div>
          </div>
          <div className="columns my-0">
            <div className="column is-3 py-1">Workflow ID</div>
            <div className="column is-8 py-1">{workflow_event?.workflow?.id}</div>
          </div>
          <div className="columns my-0">
            <div className="column is-3 py-1">Workflow name</div>
            <div className="column is-8 py-1">{workflow_event?.workflow?.name}</div>
          </div>
          <div className="columns my-0">
            <div className="column is-3 py-1">Date</div>
            <div className="column is-8 py-1">{formatDateTimeLong(workflow_event?.created_at)}</div>
          </div>
        </div>

        <TabStateProvider tabs={["Parameters", "Timeline"]}>
          <Tabs tabContainerClass="mb-1">

            <div>

              <h2 className="title is-5 my-4">Event parameters</h2>

              {(Object.keys(workflow_event?.parameters || {}).length == 0) && <div className="notification is-default my-4 p-4 is-size-6">
                No parameters provided...
              </div>}

              {(Object.keys(workflow_event?.parameters || {}).length > 0) && <>
                <div className="py-3 is-relative">
                  <CopiableLink text="COPY"
                    value={workflow_event?.parameters || ""}
                    style={{ position: 'absolute', right: 5 }}
                    className="button is-primary is-small m-1"
                  />
                  <pre className="code p-1" style={{ minHeight: '40px' }}>
                    <code
                      dangerouslySetInnerHTML={{
                        __html: hljs.highlight(jsonify(workflow_event?.parameters) as string, { language: 'json' }).value,
                      }}
                    />
                  </pre>
                </div>
              </>}

            </div>

            <div>
              {(workflow_event?.records || []).length == 0 && <div className="notification is-default my-4 p-4 is-size-6">
                No tracing records...
              </div>}

              {(workflow_event?.records || []).length > 0 && <>

                {workflow_event!.records.map((trace) => {

                  return (<div className={"card mx-0 my-2"} key={trace.id}>
                    <div className="p-3 is-size-7 has-text-weight-semibold has-text-grey">
                      <p className="my-1">
                        <span>Record type: <strong>{trace.key}</strong></span>
                      </p>
                      {!!trace.record.url && <p className="my-1">
                        <span>URL: <strong>{trace.record.url}</strong></span>
                      </p>}
                      {!!trace.record.request_id && <p className="my-1">
                        <span>Request ID: <strong>{trace.record.request_id}</strong></span>
                      </p>}
                      {!!trace.record.action_name && <p className="my-1">
                        <span>Action: <strong>{trace.record.action_name}</strong></span>
                      </p>}
                      {trace?.timestamp && <p className="my-1">
                        <span>Request Timestamp: <strong>{moment(trace.timestamp * 1000).format('LTS')}</strong></span>
                      </p>}
                    </div>

                    <div className="p-0 is-relative">
                      <CopiableLink text="COPY"
                        value={trace.record || trace.record?.url || ""}
                        style={{ position: 'absolute', right: 4 }}
                        className="button is-primary is-small m-1"
                      />
                      <pre className="code p-1" style={{ overflow: 'auto', minHeight: '40px', maxHeight: '30vh' }}>
                        <code style={{ whiteSpace: 'pre-wrap' }}
                          dangerouslySetInnerHTML={{
                            __html: hljs.highlight(
                              parseWorkflowEventRecordData(trace.record.output || trace.record) || trace.record.url || "",
                              { language: trace.record?.format || 'json' }
                            ).value,
                          }}
                        />
                      </pre>
                    </div>

                  </div>);
                })}

              </>}
            </div>

          </Tabs>
        </TabStateProvider>

      </>}
    </>
  );
};

export default function Page(pageProps: any) {
  return AuthenticatedPage((
    <DashboardLayout>
      <Head><title>{`Workflow Event - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <Component />
    </DashboardLayout>
  ), pageProps);
}

export function parseWorkflowEventRecordData(record: any) {
  if (!record) return null;
  if (record?.format === 'xml') {
    return (record.data || record.response || record.error);
  }

  return failsafe(
    () => jsonify(record.data || record.response || record.error || record.parameters),
    (record.data || record.response || record.error)
  )
}
