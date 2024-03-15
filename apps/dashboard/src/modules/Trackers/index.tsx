import { TrackerModalProvider, TrackerModalContext } from "@karrio/ui/modals/track-shipment-modal";
import { TrackingPreview, TrackingPreviewContext } from "@/components/tracking-preview";
import { ConfirmModal, ConfirmModalContext } from "@karrio/ui/modals/confirm-modal";
import { formatRef, getURLSearchParams, isNone, isNoneOrEmpty } from "@karrio/lib";
import { useTrackerMutation, useTrackers } from "@karrio/hooks/tracker";
import { TrackersFilter } from "@karrio/ui/filters/trackers-filter";
import { CarrierImage } from "@karrio/ui/components/carrier-image";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useLoader } from "@karrio/ui/components/loader";
import { Spinner } from "@karrio/ui/components/spinner";
import { TrackingEvent } from "@karrio/types/rest/api";
import React, { useContext, useEffect } from "react";
import { useRouter } from "next/dist/client/router";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";


export default function TrackersPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const { modal } = router.query;
    const { setLoading } = useLoader();
    const mutation = useTrackerMutation();
    const { addTracker } = useContext(TrackerModalContext);
    const { previewTracker } = useContext(TrackingPreviewContext);
    const { confirm: confirmDeletion } = useContext(ConfirmModalContext);
    const [initialized, setInitialized] = React.useState(false);
    const context = useTrackers({ setVariablesToURL: true, preloadNextPage: true });
    const { query: { data: { trackers } = {}, ...query }, filter, setFilter } = context;

    const remove = (id: string) => async () => {
      await mutation.deleteTracker.mutateAsync({ idOrTrackingNumber: id });
    };
    const updateFilter = (extra: Partial<any> = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra,
      };

      setFilter(query);
    }

    useEffect(() => { updateFilter(); }, [router.query]);
    useEffect(() => { setLoading(query.isFetching); }, [query.isFetching]);
    useEffect(() => {
      if (query.isFetching && !initialized && !isNoneOrEmpty(modal)) {
        const tracker = (trackers?.edges || []).find(t => t.node.id === modal)?.node;
        (modal === 'new') && addTracker({ onChange: updateFilter });
        tracker && previewTracker(tracker);
        setInitialized(true);
      }
    }, [modal, query.isFetched]);

    return (
      <>
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Trackers</span>
          <div>
            <TrackersFilter context={context} />
            <button className="button is-small is-primary ml-1" onClick={() => addTracker({ onChange: updateFilter })}>
              <span>Track a Shipment</span>
            </button>
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold ${isNone(filter?.status) ? 'is-active' : ''}`}>
              <a onClick={() => !isNone(filter?.status) && updateFilter({ status: null, offset: 0 })}>all</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('in_transit') ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('in_transit') && updateFilter({ status: ['in_transit', 'on_hold', 'out_for_delivery', 'ready_for_pickup'], offset: 0 })}>in-transit</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('pending') ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('pending') && updateFilter({ status: ['pending'], offset: 0 })}>pending</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('delivery_delayed') ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('delivery_delayed') && updateFilter({ status: ['delivery_delayed', 'delivery_failed', 'on_hold'], offset: 0 })}>exception</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('delivered') ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('delivered') && updateFilter({ status: ['delivered'], offset: 0 })}>delivered</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('unknown') ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('unknown') && updateFilter({ status: ['delivery_failed', 'unknown'], offset: 0 })}>failed</a>
            </li>
          </ul>
        </div>

        {(!query.isFetched && query.isFetching) && <Spinner />}

        {(query.isFetched && (trackers?.edges || []).length > 0) && <>
          <div className="table-container pb-3">
            <table className="trackers-table table is-fullwidth">

              <tbody className="trackers-table">
                <tr>
                  <td className="service is-size-7">SHIPPING SERVICE</td>
                  <td className="status"></td>
                  <td className="last-event is-size-7">LAST EVENT</td>
                  <td className="date is-size-7"></td>
                  <td className="action"></td>
                </tr>

                {(trackers?.edges || []).map(({ node: tracker }) => (
                  <tr key={tracker.id} className="items" onClick={() => previewTracker(tracker)}>
                    <td className="service is-vcentered py-1 px-0 is-size-7 has-text-weight-bold has-text-grey">
                      <div className="icon-text">
                        <CarrierImage
                          carrier_name={tracker.meta?.carrier || tracker.carrier_name}
                          containerClassName="mt-1 ml-1 mr-2" height={28} width={28}
                          text_color={tracker.tracking_carrier?.config?.text_color}
                          background={tracker.tracking_carrier?.config?.brand_color}
                        />
                        <div className="text-ellipsis" style={{ maxWidth: '190px', lineHeight: '16px' }}>
                          <span className="has-text-info has-text-weight-bold">{tracker.tracking_number}</span>
                          <br />
                          <span className="text-ellipsis">
                            {formatRef(tracker.info?.shipment_service || tracker.shipment?.meta?.service_name || tracker.shipment?.service || `SERVICE UNKNOWN`)}
                          </span>
                        </div>
                      </div>
                    </td>
                    <td className="status is-vcentered">
                      <StatusBadge status={tracker.status as string} style={{ width: '100%' }} />
                    </td>
                    <td className="last-event is-vcentered py-1 last-event is-size-7 has-text-weight-bold has-text-grey text-ellipsis">
                      <span className="text-ellipsis"
                        title={isNoneOrEmpty(tracker?.events) ? "" : formatEventDescription((tracker?.events as TrackingEvent[])[0])}>
                        {isNoneOrEmpty(tracker?.events) ? "" : formatEventDescription((tracker?.events as TrackingEvent[])[0])}
                      </span>
                    </td>
                    <td className="date is-vcentered has-text-right">
                      <p className="is-size-7 has-text-weight-semibold has-text-grey">
                        {isNoneOrEmpty(tracker?.events) ? "" : formatEventDate((tracker?.events as TrackingEvent[])[0])}
                      </p>
                    </td>
                    <td className="action is-vcentered p-1">
                      <button className="button is-white is-pulled-right"
                        onClick={(e) => {
                          e.stopPropagation();
                          confirmDeletion({ label: "Delet Shipment Tracker", identifier: tracker.id as string, onConfirm: remove(tracker.id) })
                        }}>
                        <span className="icon is-small">
                          <i className="fas fa-trash"></i>
                        </span>
                      </button>
                    </td>
                  </tr>
                ))}

              </tbody>

            </table>

          </div>

          <div className="px-2 py-2 is-vcentered">
            <span className="is-size-7 has-text-weight-semibold">{(trackers?.edges || []).length} results</span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number - 20) })}
                disabled={filter.offset == 0}>
                Previous
              </button>
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number + 20) })}
                disabled={!trackers?.page_info.has_next_page}>
                Next
              </button>
            </div>
          </div>
        </>}

        {(query.isFetched && (trackers?.edges || []).length == 0) && <div className="card my-6">

          <div className="card-content has-text-centered">
            <p>No shipment trackers found.</p>
          </div>

        </div>}

      </>
    );
  };


  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Trackers - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <TrackerModalProvider>
        <TrackingPreview>
          <ConfirmModal>

            <Component />

          </ConfirmModal>
        </TrackingPreview>
      </TrackerModalProvider>
    </DashboardLayout>
  ), pageProps)
}

function formatEventDescription(last_event?: TrackingEvent): string {
  return last_event?.description || '';
}

function formatEventDate(last_event?: TrackingEvent): string {
  if (isNone(last_event)) return '';

  return [
    last_event?.date,
    last_event?.time
  ].filter(a => !isNone(a) && a !== "").join(" ");
}
