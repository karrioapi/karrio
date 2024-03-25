import { CopiableLink } from "@karrio/ui/components/copiable-link";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/components/app-link";
import { SelectField } from "@karrio/ui/components";
import { useAPIUsage } from "@karrio/hooks/usage";
import Head from "next/head";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis } from "recharts";
import moment from "moment";

export { getServerSideProps } from "@/context/main";


export default function ApiPage(pageProps: any) {
  const { references } = useAPIMetadata();

  const Component: React.FC = () => {
    const { query: { data: { usage } = {} }, setFilter, filter, USAGE_FILTERS, DAYS_LIST, currentFilter } = useAPIUsage();

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


        <div className="columns is-multiline m-0">

          {/* API usage stats */}
          <div className="column p-0">

            <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
              <span className="title is-5 mb-3">Your Integration</span>
              <div className="p-0 m-0">
                <SelectField
                  className="is-small"
                  value={JSON.stringify(filter)}
                  onChange={e => setFilter(JSON.parse(e.target.value))}
                >
                  {Object.entries(USAGE_FILTERS).map(([key, value]) => (
                    <option key={key} value={JSON.stringify(value)}>{key}</option>
                  ))}
                </SelectField>
              </div>
            </header>
            <hr className="mt-1 mb-2" style={{ height: '1px' }} />

            <div className="columns is-multiline m-0">

              <div className="column is-full" style={{ minWidth: '300px' }}>
                <div className="p-0 is-size-6">
                  <div className="icon-text has-text-grey">
                    <span className="has-text-weight-bold m-1">API requests</span>
                  </div>

                  <p className="has-text-grey-dark my-1 has-text-weight-bold is-size-5">{!!usage ? usage?.total_requests : 0}</p>

                  <div style={{ width: 'calc(100%)', height: '150px' }}>
                    {!!usage?.api_requests &&
                      <ResponsiveContainer width="100%" height={150}>
                        <LineChart data={
                          DAYS_LIST[currentFilter() || "15 days"].map((_, i) => ({
                            name: ((i === 0 || i === DAYS_LIST[currentFilter() || "15 days"].length - 1) ? _ : ''),
                            total: usage!.api_requests!.find(({ date }) => moment(date).format('MMM D') === _)?.count || 0
                          }))
                        } margin={{ top: 5, right: 15, left: 15, bottom: 5 }}>
                          <CartesianGrid horizontal={false} vertical={true} />
                          <Tooltip />
                          <Line type="monotone" dataKey="total" stroke="#79e5dd" />
                          <XAxis
                            height={10} dataKey="name" interval={0} stroke={'#ddd'}
                            tick={{ fill: '#000000' }} style={{ fontSize: '0.6rem' }}
                          />
                        </LineChart>
                      </ResponsiveContainer>}
                  </div>
                </div>
              </div>

              <div className="column is-full" style={{ minWidth: '300px' }}>
                <div className="p-0 is-size-6">
                  <div className="icon-text has-text-grey">
                    <span className="has-text-weight-bold m-1">API errors</span>
                  </div>

                  <p className="has-text-grey-dark my-1 has-text-weight-bold is-size-5">{!!usage ? usage?.total_errors : 0}</p>

                  <div style={{ width: 'calc(100%)', height: '150px' }}>
                    {!!usage?.api_errors &&
                      <ResponsiveContainer width="100%" height={150}>
                        <LineChart data={
                          DAYS_LIST[currentFilter() || "15 days"].map((_, i) => ({
                            name: ((i === 0 || i === DAYS_LIST[currentFilter() || "15 days"].length - 1) ? _ : ''),
                            total: usage!.api_errors!.find(({ date }) => moment(date).format('MMM D') === _)?.count || 0
                          }))
                        } margin={{ top: 5, right: 15, left: 15, bottom: 5 }}>
                          <CartesianGrid horizontal={false} vertical={true} />
                          <Tooltip />
                          <Line type="monotone" dataKey="total" stroke="#79e5dd" />
                          <XAxis
                            height={10} dataKey="name" interval={0} stroke={'#ddd'}
                            tick={{ fill: '#000000' }} style={{ fontSize: '0.6rem' }}
                          />
                        </LineChart>
                      </ResponsiveContainer>}
                  </div>
                </div>
              </div>

            </div>
          </div>

          <div className="column is-narrow is-full-mobile p-2"></div>

          {/* APIs Overview */}
          <div className="column p-0">

            <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
              <span className="title is-5 mb-3">API Details</span>
              <div></div>
            </header>
            <hr className="mt-1 mb-2" style={{ height: '1px' }} />

            <div className="columns m-0">
              <div className="column" style={{ minWidth: '300px' }}>

                <div className="is-size-7">
                  <div className="columns my-0">
                    <div className="column is-4 py-1" style={{ minWidth: '120px' }}>
                      <span className="is-size-6 has-text-weight-bold has-text-grey">API Version</span>
                    </div>
                    <div className="column is-6 py-1"><code>{references?.VERSION}</code></div>
                  </div>
                  <div className="columns my-0">
                    <div className="column is-4 py-1" style={{ minWidth: '120px' }}>
                      <span className="is-size-6 has-text-weight-bold has-text-grey">REST API</span>
                    </div>
                    <div className="column is-6 py-1">
                      <CopiableLink
                        className="button is-white py-2 px-1 text-ellipsis"
                        text={references?.HOST}
                        title={references?.HOST}
                      />
                    </div>
                  </div>
                  <div className="columns my-0">
                    <div className="column is-4 py-1" style={{ minWidth: '120px' }}>
                      <span className="is-size-6 has-text-weight-bold has-text-grey">GRAPHQL API</span>
                    </div>
                    <div className="column is-6 py-1">
                      <CopiableLink
                        className="button is-white py-2 px-1 text-ellipsis"
                        text={references?.GRAPHQL}
                        title={references?.GRAPHQL}
                      />
                    </div>
                  </div>
                </div>

              </div>
            </div>

          </div>

        </div>

        <div className="p-6"></div>

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
