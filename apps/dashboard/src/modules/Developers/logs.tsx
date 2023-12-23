import { formatDateTimeLong, getURLSearchParams, isNone, isNoneOrEmpty } from "@karrio/lib";
import { LogPreview, LogPreviewContext } from "@/components/log-preview";
import { StatusCode } from "@karrio/ui/components/status-code-badge";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { LogsFilter } from "@karrio/ui/filters/logs-filter";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useLoader } from "@karrio/ui/components/loader";
import { Spinner } from "@karrio/ui/components/spinner";
import React, { useContext, useEffect } from "react";
import { useRouter } from "next/dist/client/router";
import { useLogs } from "@karrio/hooks/log";
import Head from "next/head";
import { AppLink } from "@karrio/ui/components/app-link";

export { getServerSideProps } from "@/context/main";


export default function LogsPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const { setLoading } = useLoader();
    const { previewLog } = useContext(LogPreviewContext);
    const [initialized, setInitialized] = React.useState(false);
    const context = useLogs();
    const { query: { data: { logs } = {}, ...query }, filter, setFilter } = context;

    const updateFilter = (extra: any = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra
      };

      setFilter(query);
    }

    useEffect(() => { updateFilter(); }, [router.query]);
    useEffect(() => { setLoading(query.isFetching); }, [query.isFetching]);
    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(router.query.modal)) {
        previewLog(router.query.modal as string);
        setInitialized(true);
      }
    }, [router.query.modal, query.isFetched]);

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Developers</span>
          <div>
            <LogsFilter context={context} />
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
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
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/developers/logs" shallow={false} prefetch={false}>
                <span>Logs</span>
              </AppLink>
            </li>
          </ul>
        </div>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold ${isNone(filter?.status) ? 'is-active' : ''}`}>
              <a onClick={() => !isNone(filter?.status) && updateFilter({ status: null, offset: 0 })}>all</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status === 'succeeded' ? 'is-active' : ''}`}>
              <a onClick={() => filter?.status !== 'succeeded' && updateFilter({ status: 'succeeded', offset: 0 })}>succeeded</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status === 'failed' ? 'is-active' : ''}`}>
              <a onClick={() => filter?.status !== 'failed' && updateFilter({ status: 'failed', offset: 0 })}>failed</a>
            </li>
          </ul>
        </div>

        {!query.isFetched && <Spinner />}


        {(query.isFetched && (logs?.edges || []).length > 0) && <>
          <div className="table-container">
            <table className="logs-table table is-fullwidth is-size-7">

              <tbody>
                <tr>
                  <td className="status is-size-7 is-vcentered"><span className="ml-2">STATUS</span></td>
                  <td className="description is-size-7 is-vcentered">DESCRIPTION</td>
                  <td className="date has-text-right is-size-7"></td>
                </tr>

                {(logs?.edges || []).map(({ node: log }) => (

                  <tr key={log.id} className="items is-clickable" onClick={() => previewLog(log.id as any)}>
                    <td className="status"><StatusCode code={log.status_code as number} /></td>
                    <td className="description text-ellipsis">{`${log.method} ${log.path}`}</td>
                    <td className="date has-text-right">
                      <span className="mr-2">{formatDateTimeLong(log.requested_at)}</span>
                    </td>
                  </tr>

                ))}
              </tbody>

            </table>
          </div>

          <footer className="px-2 py-2 is-vcentered">
            <span className="is-size-7 has-text-weight-semibold">
              {(logs?.edges || []).length} results
            </span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number - 20) })}
                disabled={filter.offset == 0}>
                Previous
              </button>
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number + 20) })}
                disabled={!logs?.page_info.has_next_page}>
                Next
              </button>
            </div>
          </footer>
        </>}


        {(query.isFetched && (logs?.edges || []).length == 0) && <div className="card my-6">

          <div className="card-content has-text-centered">
            <p>No API logs found.</p>
            <p>Use the <strong>API</strong> to send shipping requests.</p>
          </div>

        </div>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Logs - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <LogPreview>
        <Component />
      </LogPreview>
    </DashboardLayout>
  ), pageProps)
}
