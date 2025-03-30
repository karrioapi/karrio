"use client";
import {
  formatDateTimeLong,
  getURLSearchParams,
  isNoneOrEmpty,
} from "@karrio/lib";
import {
  EventPreview,
  EventPreviewContext,
} from "@karrio/core/components/event-preview";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { EventsFilter } from "@karrio/ui/core/filters/events-filter";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { useLoader } from "@karrio/ui/core/components/loader";
import { Spinner } from "@karrio/ui/core/components/spinner";
import React, { useContext, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { useEvents } from "@karrio/hooks/event";

export const generateMetadata = dynamicMetadata("Events");

export default function EventsPage() {
  const Component = (): JSX.Element => {
    const context = useEvents();
    const searchParams = useSearchParams();
    const { setLoading } = useLoader();
    const { previewEvent } = useContext(EventPreviewContext);
    const [initialized, setInitialized] = React.useState(false);
    const {
      query: { data: { events } = {}, ...query },
      filter,
      setFilter,
    } = context;

    const updateFilter = (extra: Partial<typeof filter> = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra,
      };

      setFilter(query);
    };

    useEffect(() => {
      updateFilter();
    }, [searchParams]);
    useEffect(() => {
      setLoading(query.isFetching);
    }, [query.isFetching]);
    useEffect(() => {
      if (
        query.isFetched &&
        !initialized &&
        !isNoneOrEmpty(searchParams.get("modal"))
      ) {
        previewEvent(searchParams.get("modal") as string);
        setInitialized(true);
      }
    }, [searchParams.get("modal"), query.isFetched]);

    return (
      <>
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Developers</span>
          <div>
            <EventsFilter context={context} />
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
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink
                href="/developers/events"
                shallow={false}
                prefetch={false}
              >
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

        {!query.isFetched && <Spinner />}

        {query.isFetched && (events?.edges || []).length > 0 && (
          <>
            <div className="table-container">
              <table className="events-table is-size-7 table is-fullwidth">
                <tbody className="events-table">
                  <tr>
                    <td className="event is-size-7 px-0">
                      <span className="ml-2">EVENT</span>
                    </td>
                    <td className="date has-text-right"></td>
                  </tr>

                  {(events?.edges || []).map(({ node: event }) => (
                    <tr
                      key={event.id}
                      className="items is-clickable"
                      onClick={() => previewEvent(event.id)}
                    >
                      <td className="description">
                        <span
                          className="text-ellipsis"
                          title={event.type || ""}
                        >{`${event.type}`}</span>
                      </td>
                      <td className="date has-text-right">
                        <span className="mx-2">
                          {formatDateTimeLong(event.created_at)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <footer className="px-2 py-2 is-vcentered">
              <span className="is-size-7 has-text-weight-semibold">
                {(events?.edges || []).length} results
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
                  disabled={!events?.page_info.has_next_page}
                >
                  Next
                </button>
              </div>
            </footer>
          </>
        )}

        {query.isFetched && (events?.edges || []).length == 0 && (
          <div className="card my-6">
            <div className="card-content has-text-centered">
              <p>No API events found.</p>
            </div>
          </div>
        )}
      </>
    );
  };

  return (
    <>
      <EventPreview>
        <Component />
      </EventPreview>
    </>
  );
}
