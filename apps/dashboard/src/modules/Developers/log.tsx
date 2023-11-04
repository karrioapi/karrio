import { failsafe, formatDateTimeLong, groupBy, isNone, jsonify, notEmptyJSON } from "@/lib/helper";
import Tabs, { TabStateProvider } from "@/components/generic/tabs";
import AuthenticatedPage from "@/layouts/authenticated-page";
import DashboardLayout from "@/layouts/dashboard-layout";
import StatusCode from "@/components/status-code-badge";
import { useRouter } from "next/dist/client/router";
import json from 'highlight.js/lib/languages/json';
import { useLoader } from "@/components/loader";
import AppLink from "@/components/app-link";
import { useLog } from "@/context/log";
import hljs from "highlight.js";
import Head from "next/head";
import React from "react";
import moment from "moment";
import CopiableLink from "@/components/copiable-link";

export { getServerSideProps } from "@/lib/data-fetching";

hljs.registerLanguage('json', json);


export const LogComponent: React.FC<{ logId?: string }> = ({ logId }) => {
  const router = useRouter();
  const { setLoading } = useLoader();
  const entity_id = logId || router.query.id as string;
  const [data, setData] = React.useState<string>();
  const [response, setResponse] = React.useState<string>();
  const [query_params, setQueryParams] = React.useState<string>();
  const { query: { data: { log } = {}, ...query } } = useLog(entity_id);

  React.useEffect(() => {
    (window as any).moment = moment;
    setLoading(query.isFetching);
  }, [query.isFetching]);
  React.useEffect(() => {
    if (log !== undefined) {
      setQueryParams(failsafe(() => jsonify(log?.query_params), '{}'));
      setResponse(failsafe(() => jsonify(log?.response), '{}'));
      setData(failsafe(() => jsonify(log?.data), '{}'));
    }
  });

  return (
    <>
      {log !== undefined && <>

        <div className="columns my-1">
          <div className="column is-10">
            <span className="subtitle is-size-7 has-text-weight-semibold">LOG</span>
            <br />
            <span className="title is-5 mr-2">
              {log?.method} {log?.path} <StatusCode code={log?.status_code as number} />
            </span>
          </div>
          {!isNone(logId) && <div className="column is-2 is-flex is-justify-content-end">
            <AppLink href={`/developers/logs/${logId}`} target="blank"
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
            <div className="column is-8 py-1">{log?.id}</div>
          </div>
          <div className="columns my-0">
            <div className="column is-3 py-1">Date</div>
            <div className="column is-8 py-1">{formatDateTimeLong(log?.requested_at)}</div>
          </div>
          <div className="columns my-0">
            <div className="column is-3 py-1">Origin</div>
            <div className="column is-8 py-1">{log?.remote_addr}</div>
          </div>
          <div className="columns my-0">
            <div className="column is-3 py-1">IP Address</div>
            <div className="column is-8 py-1">{log?.host}</div>
          </div>
        </div>

        <TabStateProvider tabs={["API Response", "API Request", "Timeline"]}>
          <Tabs tabContainerClass="mb-1">

            {notEmptyJSON(response) && <div>

              <h2 className="title is-5 my-4">Response body</h2>

              <div className="py-3 is-relative">
                <CopiableLink text="COPY"
                  value={response}
                  style={{ position: 'absolute', right: 0, zIndex: 1 }}
                  className="button is-primary is-small m-1"
                />
                <pre className="code p-1">
                  <code
                    dangerouslySetInnerHTML={{
                      __html: hljs.highlight(response as string, { language: 'json' }).value,
                    }}
                  />
                </pre>
              </div>

            </div>}

            <div>
              {notEmptyJSON(query_params) && query_params !== data && <>

                <h2 className="title is-5 my-4">Request query params</h2>

                <div className="py-3">
                  <pre className="code p-1">
                    <code
                      dangerouslySetInnerHTML={{
                        __html: hljs.highlight(query_params as string, { language: 'json' }).value,
                      }}
                    />
                  </pre>
                </div>

                <hr className="mt-1 mb-2" style={{ height: '1px' }} />
              </>}

              {notEmptyJSON(data) && <>

                <h2 className="title is-5 my-4">Request {log?.method} body</h2>

                <div className="py-3 is-relative">
                  <CopiableLink text="COPY"
                    value={data}
                    style={{ position: 'absolute', right: 0, zIndex: 1 }}
                    className="button is-primary is-small m-1"
                  />
                  <pre className="code p-1">
                    <code
                      dangerouslySetInnerHTML={{
                        __html: hljs.highlight(data as string, { language: 'json' }).value,
                      }}
                    />
                  </pre>
                </div>

              </>}
            </div>

            <div>
              {(log?.records || []).length == 0 && <div className="notification is-default my-4 p-4 is-size-6">
                No tracing records...
              </div>}
              {(log?.records || []).length > 0 && <>

                {Object.values(groupBy(log!.records, (r: any) => r.record?.request_id)).map((records: any, key) => {
                  const request = records.find((r: any) => r.key === "request");
                  const response = records.find((r: any) => r.key !== "request");
                  const request_data = parseRecordData(request?.record);
                  const response_data = parseRecordData(response?.record);
                  const tabs = [...(request ? ["request"] : []), ...(response ? [response.key] : [])];

                  return (<div className="card mx-0 my-2" key={key}>
                    <div className="p-3 is-size-7 has-text-weight-semibold has-text-grey">
                      <p className="is-size-6 my-1">
                        <span>Carrier: <strong>{(request || response)?.meta?.carrier_name}</strong></span>
                      </p>
                      <p className="my-1">
                        <span>Connection: <strong>{(request || response)?.meta?.carrier_id}</strong></span>
                      </p>
                      <p className="my-1">
                        <span>URL: <strong>{(request?.record || response?.record)?.url}</strong></span>
                      </p>
                      <p className="my-1">
                        <span>Request ID: <strong>{(request?.record || response?.record)?.request_id}</strong></span>
                      </p>
                      {request?.timestamp && <p className="my-1">
                        <span>Request Timestamp: <strong>{moment(request.timestamp * 1000).format('LTS')}</strong></span>
                      </p>}
                      {response?.timestamp && <p className="my-1">
                        <span>Response Timestamp: <strong>{moment(response.timestamp * 1000).format('LTS')}</strong></span>
                      </p>}
                    </div>
                    <TabStateProvider tabs={tabs}>
                      <Tabs>

                        {request && <div className="p-0 is-relative">
                          <CopiableLink text="COPY"
                            value={request_data || request.record?.url || ""}
                            style={{ position: 'absolute', right: 0, zIndex: 1 }}
                            className="button is-primary is-small m-1"
                          />
                          <pre className="code p-1" style={{ overflow: 'auto', maxHeight: '40vh' }}>
                            <code style={{ whiteSpace: 'pre-wrap' }}
                              dangerouslySetInnerHTML={{
                                __html: hljs.highlight(
                                  request_data || request.record?.url || "",
                                  { language: request.record?.format || 'json' }
                                ).value,
                              }}
                            />
                          </pre>
                        </div>}

                        {response_data && <div className="p-0 is-relative">
                          <CopiableLink text="COPY"
                            value={response_data.replaceAll("><", ">\n<")}
                            style={{ position: 'absolute', right: 0, zIndex: 1 }}
                            className="button is-primary is-small m-1"
                          />
                          <pre className="code p-1 is-relative" style={{ overflow: 'auto', maxHeight: '40vh' }}>
                            <code style={{ whiteSpace: 'pre-wrap' }}
                              dangerouslySetInnerHTML={{
                                __html: hljs.highlight(
                                  response_data.replaceAll("><", ">\n<"),
                                  { language: response.record?.format || 'json' }
                                ).value
                              }}
                            />
                          </pre>
                        </div>}

                      </Tabs>
                    </TabStateProvider>
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

export default function LogPage(pageProps: any) {
  return AuthenticatedPage((
    <DashboardLayout>
      <Head><title>{`Log - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <LogComponent />
    </DashboardLayout>
  ), pageProps);
}

function parseRecordData(record: any) {
  if (!record) return null;
  if (record?.format === 'xml') {
    return (record.data || record.response || record.error);
  }

  return failsafe(
    () => jsonify(record.data || record.response || record.error),
    (record.data || record.response || record.error)
  )
}
