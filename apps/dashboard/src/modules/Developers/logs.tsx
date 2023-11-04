import { formatDateTimeLong, getURLSearchParams, isNone, isNoneOrEmpty } from "@/lib/helper";
import LogPreview, { LogPreviewContext } from "@/components/descriptions/log-preview";
import AuthenticatedPage from "@/layouts/authenticated-page";
import LogsFilter from "@/components/filters/logs-filter";
import DashboardLayout from "@/layouts/dashboard-layout";
import StatusCode from "@/components/status-code-badge";
import React, { useContext, useEffect } from "react";
import { useRouter } from "next/dist/client/router";
import { useLoader } from "@/components/loader";
import Spinner from "@/components/spinner";
import { useLogs } from "@/context/log";
import Head from "next/head";

export { getServerSideProps } from "@/lib/data-fetching";


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
        <header className="px-0 pb-3 pt-6 is-flex is-justify-content-space-between">
          <span className="title is-4">Logs</span>
          <LogsFilter context={context} />
        </header>

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


        {(query.isFetched && (logs?.edges || []).length > 0) && <div className="table-container">
          <table className="logs-table table is-fullwidth is-size-7">

            <tbody className="logs-table">
              <tr>
                <td className="status is-size-7"><span className="ml-2">STATUS</span></td>
                <td className="description is-size-7">DESCRIPTION</td>
                <td className="date has-text-right is-size-7"><span className="mr-2">DATE</span></td>
              </tr>

              {(logs?.edges || []).map(({ node: log }) => (

                <tr key={log.id} className="items is-clickable" onClick={() => previewLog(log.id as any)}>
                  <td className="status"><StatusCode code={log.status_code as number} /></td>
                  <td className="description">{`${log.method} ${log.path}`}</td>
                  <td className="date has-text-right">
                    <span className="mr-2">{formatDateTimeLong(log.requested_at)}</span>
                  </td>
                </tr>

              ))}
            </tbody>

          </table>

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

        </div>}


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
