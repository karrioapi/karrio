"use client";
import {
  formatDateTimeLong,
  getURLSearchParams,
  isNone,
  isNoneOrEmpty,
} from "@karrio/lib";
import {
  LogPreview,
  LogPreviewContext,
} from "@karrio/core/components/log-preview";
import { StatusCode } from "@karrio/ui/core/components/status-code-badge";
import { LogsFilter } from "@karrio/ui/core/filters/logs-filter";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Spinner } from "@karrio/ui/core/components/spinner";
import React, { useContext, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { useLogs } from "@karrio/hooks/log";


export default function LogsPage() {
  const Component = (): JSX.Element => {
    const searchParams = useSearchParams();
    const modal = searchParams.get("modal");
    const { setLoading } = useLoader();
    const { previewLog } = useContext(LogPreviewContext);
    const [initialized, setInitialized] = React.useState(false);
    const context = useLogs();
    const {
      query: { data: { logs } = {}, ...query },
      filter,
      setFilter,
    } = context;

    const updateFilter = (extra: any = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra,
      };

      setFilter(query);
    };

    useEffect(() => {
      updateFilter();
    }, [modal]);
    useEffect(() => {
      setLoading(query.isFetching);
    }, [query.isFetching]);
    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(modal)) {
        previewLog(modal as string);
        setInitialized(true);
      }
    }, [modal, query.isFetched]);

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
              <AppLink
                href="/developers/apikeys"
                shallow={false}
                prefetch={false}
              >
                <span>API Keys</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/developers/webhooks"
                shallow={false}
                prefetch={false}
              >
                <span>Webhooks</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/developers/events"
                shallow={false}
                prefetch={false}
              >
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
            <li
              className={`is-capitalized has-text-weight-semibold ${isNone(filter?.status) ? "is-active" : ""}`}
            >
              <a
                onClick={() =>
                  !isNone(filter?.status) &&
                  updateFilter({ status: null, offset: 0 })
                }
              >
                all
              </a>
            </li>
            <li
              className={`is-capitalized has-text-weight-semibold ${filter?.status === "succeeded" ? "is-active" : ""}`}
            >
              <a
                onClick={() =>
                  filter?.status !== "succeeded" &&
                  updateFilter({ status: "succeeded", offset: 0 })
                }
              >
                succeeded
              </a>
            </li>
            <li
              className={`is-capitalized has-text-weight-semibold ${filter?.status === "failed" ? "is-active" : ""}`}
            >
              <a
                onClick={() =>
                  filter?.status !== "failed" &&
                  updateFilter({ status: "failed", offset: 0 })
                }
              >
                failed
              </a>
            </li>
          </ul>
        </div>

        {!query.isFetched && <Spinner />}

        {query.isFetched && (logs?.edges || []).length > 0 && (
          <>
            <div className="table-container">
              <table className="logs-table table is-fullwidth is-size-7">
                <tbody>
                  <tr>
                    <td className="status is-size-7 is-vcentered">
                      <span className="ml-2">STATUS</span>
                    </td>
                    <td className="description is-size-7 is-vcentered">
                      DESCRIPTION
                    </td>
                    <td className="date has-text-right is-size-7"></td>
                  </tr>

                  {(logs?.edges || []).map(({ node: log }) => (
                    <tr
                      key={log.id}
                      className="items is-clickable"
                      onClick={() => previewLog(log.id as any)}
                    >
                      <td className="status">
                        <StatusCode code={log.status_code as number} />
                      </td>
                      <td className="description text-ellipsis">{`${log.method} ${log.path}`}</td>
                      <td className="date has-text-right">
                        <span className="mr-2">
                          {formatDateTimeLong(log.requested_at)}
                        </span>
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
                <button
                  className="button is-small"
                  onClick={() =>
                    updateFilter({ offset: (filter.offset as number) - 20 })
                  }
                  disabled={filter.offset == 0}
                >
                  Previous
                </button>
                <button
                  className="button is-small"
                  onClick={() =>
                    updateFilter({ offset: (filter.offset as number) + 20 })
                  }
                  disabled={!logs?.page_info.has_next_page}
                >
                  Next
                </button>
              </div>
            </footer>
          </>
        )}

        {query.isFetched && (logs?.edges || []).length == 0 && (
          <div className="card my-6">
            <div className="card-content has-text-centered">
              <p>No API logs found.</p>
              <p>
                Use the <strong>API</strong> to send shipping requests.
              </p>
            </div>
          </div>
        )}
      </>
    );
  };

  return (
    <>
      <LogPreview>
        <Component />
      </LogPreview>
    </>
  );
}
