import { Bar, BarChart, Tooltip, ResponsiveContainer, XAxis } from "recharts";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/components/app-link";
import { SelectField } from "@karrio/ui/components";
import { useAppMode } from "@karrio/hooks/app-mode";
import { useAPIUsage } from "@karrio/hooks/usage";
import { useUser } from "@karrio/hooks/user";
import { useRouter } from "next/router";
import Head from "next/head";
import moment from "moment";
import React from "react";

export { getServerSideProps } from "@/context/main";


export default function ApiPage(pageProps: any) {
  const { references } = useAPIMetadata();

  const Component: React.FC = () => {
    const router = useRouter();
    const { basePath } = useAppMode();
    const { query: { data: { user } = {} } } = useUser();
    const { query: { data: { usage } = {} }, setFilter, filter, USAGE_FILTERS, DAYS_LIST, currentFilter } = useAPIUsage();

    return (
      <>

        <header className="pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">{`Welcome${!!user?.full_name ? ', ' + user.full_name : ''}`}</span>
          <div></div>
        </header>

        {/* Usage stats */}
        <div className="m-0">
          <SelectField
            className="is-small"
            fieldClass="py-2"
            value={JSON.stringify(filter)}
            onChange={e => setFilter(JSON.parse(e.target.value))}
          >
            {Object.entries(USAGE_FILTERS).map(([key, value]) => (
              <option key={key} value={JSON.stringify(value)}>{key}</option>
            ))}
          </SelectField>

          <div className="columns is-multiline">

            <div className="column p-0">
              <div className="columns m-0">
                <div className="column" style={{ minWidth: '250px' }}>
                  <div className="card p-4 is-size-6">
                    <div className="icon-text has-text-grey">
                      <span className="tag is-light icon has-text-grey-light is-medium">
                        <i className="fas fa-truck"></i>
                      </span>
                      <span className="has-text-weight-bold m-1">Shipment</span>
                    </div>

                    <p className="has-text-grey-light my-2 has-text-weight-semibold">Total shipments</p>
                    <p className="has-text-grey-dark my-1 has-text-weight-bold is-size-5">{!!usage ? usage?.total_shipments : 0}</p>

                    <div style={{ width: 'calc(100%)', height: '150px' }}>
                      {!!usage?.shipment_count &&
                        <ResponsiveContainer width="100%" height={150}>
                          <BarChart data={
                            DAYS_LIST[currentFilter() || "15 days"].map(_ => ({
                              name: _,
                              total: usage!.shipment_count!.find(({ date }) => moment(date).format('MMM D') === _)?.count || 0
                            }))
                          }>
                            <Tooltip />
                            <Bar dataKey="total" fill="#79e5dd" />
                            <XAxis height={10} dataKey="name" interval={"preserveStartEnd"} stroke={'#ddd'} tick={{ fill: '#000000' }} style={{ fontSize: '0.6rem' }} ticks={[
                              DAYS_LIST[currentFilter() || "15 days"][0],
                              DAYS_LIST[currentFilter() || "15 days"][DAYS_LIST[currentFilter() || "15 days"].length - 1],
                            ]} />
                          </BarChart>
                        </ResponsiveContainer>}
                    </div>
                  </div>
                </div>
                <div className="column" style={{ minWidth: '250px' }}>
                  <div className="card p-4 is-size-6">
                    <div className="icon-text has-text-grey">
                      <span className="tag is-light icon has-text-grey-light is-medium">
                        <i className="fas fa-location-arrow"></i>
                      </span>
                      <span className="has-text-weight-bold m-1">Tracker</span>
                    </div>

                    <p className="has-text-grey-light my-2 has-text-weight-semibold">Total trackers</p>
                    <p className="has-text-grey-dark my-1 has-text-weight-bold is-size-5">{!!usage ? usage?.total_trackers : 0}</p>

                    <div style={{ width: 'calc(100%)', height: '150px' }}>
                      {!!usage?.tracker_count &&
                        <ResponsiveContainer width="100%" height={150}>
                          <BarChart data={
                            DAYS_LIST[currentFilter() || "15 days"].map(_ => ({
                              name: _,
                              total: usage!.tracker_count!.find(({ date }) => moment(date).format('MMM D') === _)?.count || 0
                            }))
                          }>
                            <Tooltip />
                            <Bar dataKey="total" fill="#79e5dd" />
                            <XAxis height={10} dataKey="name" interval={"preserveStartEnd"} stroke={'#ddd'} tick={{ fill: '#000000' }} style={{ fontSize: '0.6rem' }} ticks={[
                              DAYS_LIST[currentFilter() || "15 days"][0],
                              DAYS_LIST[currentFilter() || "15 days"][DAYS_LIST[currentFilter() || "15 days"].length - 1],
                            ]} />
                          </BarChart>
                        </ResponsiveContainer>}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="column p-0">
              <div className="columns m-0">
                <div className="column" style={{ minWidth: '250px' }}>
                  <div className="card p-4 is-size-6">
                    <div className="icon-text has-text-grey">
                      <span className="tag is-light icon has-text-grey-light is-medium">
                        <i className="fas fa-inbox"></i>
                      </span>
                      <span className="has-text-weight-bold m-1">Order</span>
                    </div>

                    <p className="has-text-grey-light my-2 has-text-weight-semibold">Fullfilled orders volume</p>
                    <p className="has-text-grey-dark my-1 has-text-weight-bold is-size-5">
                      <span className="icon-text">
                        <span className="icon">
                          <i className="fas fa-dollar-sign"></i>
                        </span>
                        <span>{!!usage ? usage?.order_volume : 0}</span>
                      </span>
                    </p>

                    <div style={{ width: 'calc(100%)', height: '150px' }}>
                      {!!usage?.order_volumes &&
                        <ResponsiveContainer width="100%" height={150}>
                          <BarChart data={
                            DAYS_LIST[currentFilter() || "15 days"].map(_ => ({
                              name: _,
                              value: usage!.order_volumes!.find(({ date }) => moment(date).format('MMM D') === _)?.count || 0
                            }))
                          }>
                            <Tooltip />
                            <Bar dataKey="value" fill="#79e5dd" />
                            <XAxis height={10} dataKey="name" interval={"preserveStartEnd"} stroke={'#ddd'} tick={{ fill: '#000000' }} style={{ fontSize: '0.6rem' }} ticks={[
                              DAYS_LIST[currentFilter() || "15 days"][0],
                              DAYS_LIST[currentFilter() || "15 days"][DAYS_LIST[currentFilter() || "15 days"].length - 1],
                            ]} />
                          </BarChart>
                        </ResponsiveContainer>}
                    </div>
                  </div>
                </div>
                <div className="column" style={{ minWidth: '250px' }}>
                  <div className="card p-4 is-size-6">
                    <div className="icon-text has-text-grey">
                      <span className="tag is-light icon has-text-grey-light is-medium">
                        <i className="fas fa-dollar-sign"></i>
                      </span>
                      <span className="has-text-weight-bold m-1">Spend</span>
                    </div>

                    <p className="has-text-grey-light my-2 has-text-weight-semibold">Estimated shipping spend</p>
                    <p className="has-text-grey-dark my-1 has-text-weight-bold is-size-5">
                      <span className="icon-text">
                        <span className="icon">
                          <i className="fas fa-dollar-sign"></i>
                        </span>
                        <span>{!!usage ? usage?.total_shipping_spend : 0}</span>
                      </span>
                    </p>

                    <div style={{ width: 'calc(100%)', height: '150px' }}>
                      {!!usage?.shipping_spend &&
                        <ResponsiveContainer width="100%" height={150}>
                          <BarChart data={
                            DAYS_LIST[currentFilter() || "15 days"].map(_ => ({
                              name: _,
                              value: usage!.shipping_spend!.find(({ date }) => moment(date).format('MMM D') === _)?.count || 0
                            }))
                          }>
                            <Tooltip />
                            <Bar dataKey="value" fill="#79e5dd" />
                            <XAxis height={10} dataKey="name" interval={"preserveStartEnd"} stroke={'#ddd'} tick={{ fill: '#000000' }} style={{ fontSize: '0.6rem' }} ticks={[
                              DAYS_LIST[currentFilter() || "15 days"][0],
                              DAYS_LIST[currentFilter() || "15 days"][DAYS_LIST[currentFilter() || "15 days"].length - 1],
                            ]} />
                          </BarChart>
                        </ResponsiveContainer>}
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* Next actions */}
        <div className="has-text-weight-bold mt-6 mb-4">Things to do next</div>

        {(!!usage?.unfulfilled_orders && usage.unfulfilled_orders > 0) && <div className="my-3">
          <AppLink href="/orders?status=unfulfilled,partial" className="button" style={{ width: '150px' }}>
            <span className="icon">
              <i className="fas fa-inbox"></i>
            </span>
            <span className="has-text-weight-bold has-text-grey">
              {`${usage.unfulfilled_orders} order${usage.unfulfilled_orders > 1 ? 's' : ''} to fulfill`}
            </span>
          </AppLink>
        </div>}

        <div className="columns is-multiline my-4">

          <div className="column" style={{ minWidth: '350px' }}>
            <div className="card is-clickable" onClick={() => router.push(`${basePath}/settings/addresses`)}>
              <div className="columns icon-text has-text-grey m-0 p-4">
                <span className="tag is-primary icon has-text-white is-medium mt-1">
                  <i className="fas fa-location-dot"></i>
                </span>
                <div className="column py-0 px-1" style={{ lineHeight: '16px' }}>
                  <p className="has-text-weight-bold mb-1">Add shipping location address</p>
                  <p className="has-text-grey m-0 is-size-7">Add one or multiple warehouse locations.</p>
                </div>
                <span className="p-0 icon has-text-right">
                  <i className="fas fa-arrow-right"></i>
                </span>
              </div>
            </div>
          </div>

          <div className="column" style={{ minWidth: '350px' }}>
            <div className="card is-clickable" onClick={() => router.push(`${basePath}/connections`)}>
              <div className="columns icon-text has-text-grey m-0 p-4">
                <span className="tag is-primary icon has-text-white is-medium mt-1">
                  <i className="fas fa-truck-fast"></i>
                </span>
                <div className="column py-0 px-1" style={{ lineHeight: '16px' }}>
                  <p className="has-text-weight-bold mb-1">Set up carrier accounts</p>
                  <p className="has-text-grey m-0 is-size-7">Connect your carrier accounts to start</p>
                </div>
                <span className="p-0 icon has-text-right">
                  <i className="fas fa-arrow-right"></i>
                </span>
              </div>
            </div>
          </div>

          <div className="column" style={{ minWidth: '350px' }}>
            <div className="card is-clickable" onClick={() => router.push(`/test/create_label?shipment_id=new`)}>
              <div className="columns icon-text has-text-grey m-0 p-4">
                <span className="tag is-primary icon has-text-white is-medium mt-1">
                  <i className="fas fa-file-lines"></i>
                </span>
                <div className="column py-0 px-1" style={{ lineHeight: '16px' }}>
                  <p className="has-text-weight-bold mb-1">Print a test label</p>
                  <p className="has-text-grey m-0 is-size-7">Generate a test label for a sample shipment.</p>
                </div>
                <span className="p-0 icon has-text-right">
                  <i className="fas fa-arrow-right"></i>
                </span>
              </div>
            </div>
          </div>

          <div className="column" style={{ minWidth: '350px' }}>
            <div className="card is-clickable" onClick={() => router.push(`${basePath}/trackers?modal=new`)}>
              <div className="columns icon-text has-text-grey m-0 p-4">
                <span className="tag is-primary icon has-text-white is-medium mt-1">
                  <i className="fas fa-location-arrow"></i>
                </span>
                <div className="column py-0 px-1" style={{ lineHeight: '16px' }}>
                  <p className="has-text-weight-bold mb-1">Add a tracking number</p>
                  <p className="has-text-grey m-0 is-size-7">Add one or multiple shipments to track.</p>
                </div>
                <span className="p-0 icon has-text-right">
                  <i className="fas fa-arrow-right"></i>
                </span>
              </div>
            </div>
          </div>

          <div className="column" style={{ minWidth: '350px' }}>
            <div className="card is-clickable" onClick={() => router.push(`${basePath}/developers/apikeys`)}>
              <div className="columns icon-text has-text-grey m-0 p-4">
                <span className="tag is-primary icon has-text-white is-medium mt-1">
                  <i className="fas fa-plug"></i>
                </span>
                <div className="column py-0 px-1" style={{ lineHeight: '16px' }}>
                  <p className="has-text-weight-bold mb-1">Set up an API connection</p>
                  <p className="has-text-grey m-0 is-size-7">Retrieve your API key to connect via API.</p>
                </div>
                <span className="p-0 icon has-text-right">
                  <i className="fas fa-arrow-right"></i>
                </span>
              </div>
            </div>
          </div>

          <div className="column" style={{ minWidth: '350px' }}>
            <div className="card is-clickable" onClick={() => router.push(`${basePath}/developers/logs`)}>
              <div className="columns icon-text has-text-grey m-0 p-4">
                <span className="tag is-primary icon has-text-white is-medium mt-1">
                  <i className="fas fa-list-check"></i>
                </span>
                <div className="column py-0 px-1" style={{ lineHeight: '16px' }}>
                  <p className="has-text-weight-bold mb-1">Review your API request</p>
                  <p className="has-text-grey m-0 is-size-7">Audit your API requests logs and system health.</p>
                </div>
                <span className="p-0 icon has-text-right">
                  <i className="fas fa-arrow-right"></i>
                </span>
              </div>
            </div>
          </div>

        </div>

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Home - ${references?.APP_NAME}`}</title></Head>
      <Component />
    </DashboardLayout>
  ), pageProps);
}
