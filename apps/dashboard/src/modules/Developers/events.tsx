import EventPreview, { EventPreviewContext } from "@/components/descriptions/event-preview";
import { formatDateTimeLong, getURLSearchParams, isNoneOrEmpty } from "@/lib/helper";
import EventsFilter from "@/components/filters/events-filter";
import AuthenticatedPage from "@/layouts/authenticated-page";
import DashboardLayout from "@/layouts/dashboard-layout";
import React, { useContext, useEffect } from "react";
import { useRouter } from "next/dist/client/router";
import { useLoader } from "@/components/loader";
import { useEvents } from "@/context/event";
import Spinner from "@/components/spinner";
import Head from "next/head";

export { getServerSideProps } from "@/lib/data-fetching";

export default function EventsPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const context = useEvents();
    const { setLoading } = useLoader();
    const { previewEvent } = useContext(EventPreviewContext);
    const [initialized, setInitialized] = React.useState(false);
    const { query: { data: { events } = {}, ...query }, filter, setFilter } = context;

    const updateFilter = (extra: Partial<typeof filter> = {}) => {
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
        previewEvent(router.query.modal as string);
        setInitialized(true);
      }
    }, [router.query.modal, query.isFetched]);

    return (
      <>
        <header className="px-0 pb-3 pt-6 is-flex is-justify-content-space-between">
          <span className="title is-4">Events</span>
          <EventsFilter context={context} />
        </header>

        {!query.isFetched && <Spinner />}


        {(query.isFetched && (events?.edges || []).length > 0) && <div className="table-container">
          <table className="events-table is-size-7 table is-fullwidth">

            <tbody className="events-table">
              <tr>
                <td className="event is-size-7"><span className="ml-2">EVENT</span></td>
                <td className="id has-text-right is-size-7">ID</td>
                <td className="date has-text-right is-size-7"><span className="mr-2">DATE</span></td>
              </tr>

              {(events?.edges || []).map(({ node: event }) => (

                <tr key={event.id} className="items is-clickable" onClick={() => previewEvent(event.id)}>
                  <td className="description">{`${event.type}`}</td>
                  <td className="id has-text-right">
                    <span>{event.id}</span>
                  </td>
                  <td className="date has-text-right">
                    <span className="mx-2">{formatDateTimeLong(event.created_at)}</span>
                  </td>
                </tr>

              ))}
            </tbody>

          </table>

          <footer className="px-2 py-2 is-vcentered">
            <span className="is-size-7 has-text-weight-semibold">
              {(events?.edges || []).length} results
            </span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number - 20) })}
                disabled={filter.offset == 0}>
                Previous
              </button>
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number + 20) })}
                disabled={!events?.page_info.has_next_page}>
                Next
              </button>
            </div>
          </footer>

        </div>}


        {(query.isFetched && (events?.edges || []).length == 0) &&
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No API events found.</p>
            </div>

          </div>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Events - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <EventPreview>
        <Component />
      </EventPreview>
    </DashboardLayout>
  ), pageProps)
}
