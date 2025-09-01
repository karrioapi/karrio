"use client";
import {
  TrackerModalProvider,
  useTrackerModal,
} from "@karrio/ui/core/modals/track-shipment-modal";
import {
  TrackingPreview,
  useTrackingPreview,
} from "@karrio/core/components/tracking-preview";
import { ConfirmModal, useConfirmModal } from "@karrio/ui/core/modals/confirm-modal";
import {
  formatRef,
  getURLSearchParams,
  isNone,
  isNoneOrEmpty,
  preventPropagation,
} from "@karrio/lib";
import { useTrackerMutation, useTrackers } from "@karrio/hooks/tracker";
import { TrackersFilter } from "@karrio/ui/core/filters/trackers-filter";
import { FiltersCard } from "@karrio/ui/components/filters-card";
import { StickyTableWrapper } from "@karrio/ui/components/sticky-table-wrapper";
import { 
  Table, 
  TableHeader, 
  TableBody, 
  TableHead, 
  TableRow, 
  TableCell 
} from "@karrio/ui/components/ui/table";
import { Button } from "@karrio/ui/components/ui/button";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { StatusBadge } from "@karrio/ui/core/components/status-badge";
import { useLoader } from "@karrio/ui/core/components/loader";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { TrackingEvent } from "@karrio/types/rest/api";
import { useSearchParams } from "next/navigation";
import React, { useEffect } from "react";


export default function TrackersPage(pageProps: any) {
  const Component = (): JSX.Element => {
    const searchParams = useSearchParams();
    const modal = searchParams.get("modal") as string;
    const { setLoading } = useLoader();
    const mutation = useTrackerMutation();
    const { addTracker } = useTrackerModal();
    const { previewTracker } = useTrackingPreview();
    const { confirm: confirmDeletion } = useConfirmModal();
    const [initialized, setInitialized] = React.useState(false);
    const context = useTrackers({
      setVariablesToURL: true,
      preloadNextPage: true,
    });
    const {
      query: { data: { trackers } = {}, ...query },
      filter,
      setFilter,
    } = context;

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
    };
    
    // Define filter options for the cards
    const getFilterOptions = () => [
      {
        label: "All",
        value: []
      },
      {
        label: "In-Transit", 
        value: ["in_transit", "on_hold", "out_for_delivery", "ready_for_pickup"]
      },
      {
        label: "Pending",
        value: ["pending"]
      },
      {
        label: "Exception",
        value: ["delivery_delayed", "delivery_failed", "on_hold"]
      },
      {
        label: "Delivered",
        value: ["delivered"]
      },
      {
        label: "Failed",
        value: ["delivery_failed", "unknown"]
      }
    ];

    useEffect(() => {
      updateFilter();
    }, [searchParams]);
    useEffect(() => {
      setLoading(query.isFetching);
    }, [query.isFetching]);
    useEffect(() => {
      if (query.isFetching && !initialized && !isNoneOrEmpty(modal)) {
        const tracker = (trackers?.edges || []).find(
          (t) => t.node.id === modal,
        )?.node;
        modal === "new" && addTracker({ onChange: updateFilter });
        tracker && previewTracker(tracker);
        setInitialized(true);
      }
    }, [modal, query.isFetched]);

    return (
      <>
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between px-0 pb-0 pt-4 mb-2">
          <div className="mb-4 sm:mb-0">
            <h1 className="text-2xl font-semibold text-gray-900">Trackers</h1>
          </div>
          <div className="flex flex-row items-center gap-1 flex-wrap">
            <TrackersFilter context={context} />
            <button
              className="button is-small is-primary ml-1"
              onClick={() => addTracker({ onChange: updateFilter })}
            >
              <span>Track a Shipment</span>
            </button>
          </div>
        </header>

        <FiltersCard
          filters={getFilterOptions()}
          activeFilter={filter?.status || []}
          onFilterChange={(status) => updateFilter({ status: status.length > 0 ? status : null, offset: 0 })}
        />

        {!query.isFetched && query.isFetching && <Spinner />}

        {query.isFetched && (trackers?.edges || []).length > 0 && (
          <>
            <StickyTableWrapper>
              <Table className="trackers-table">
                <TableHeader>
                  <TableRow>
                    <TableHead className="service text-xs items-center">
                      SHIPPING SERVICE
                    </TableHead>
                    <TableHead className="status items-center"></TableHead>
                    <TableHead className="last-event text-xs items-center">
                      LAST EVENT
                    </TableHead>
                    <TableHead className="date text-xs items-center">DATE</TableHead>
                    <TableHead className="action sticky-right"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>

                  {(trackers?.edges || []).map(({ node: tracker }) => (
                    <TableRow
                      key={tracker.id}
                      className="items cursor-pointer transition-colors duration-150 ease-in-out hover:bg-gray-50"
                      onClick={() => previewTracker(tracker)}
                    >
                      <TableCell className="service items-center py-1 px-0 text-xs font-bold text-gray-600">
                        <div className="flex items-center">
                          <CarrierImage
                            carrier_name={
                              tracker.meta?.carrier || tracker.carrier_name
                            }
                            containerClassName="mt-1 ml-1 mr-2"
                            height={28}
                            width={28}
                            text_color={
                              tracker.tracking_carrier?.config?.text_color
                            }
                            background={
                              tracker.tracking_carrier?.config?.brand_color
                            }
                          />
                          <div
                            className="text-ellipsis"
                            style={{ maxWidth: "190px", lineHeight: "16px" }}
                          >
                            <span className="text-blue-600 font-bold">
                              {tracker.tracking_number}
                            </span>
                            <br />
                            <span className="text-ellipsis">
                              {formatRef(
                                tracker.info?.shipment_service ||
                                tracker.shipment?.meta?.service_name ||
                                tracker.shipment?.service ||
                                `SERVICE UNKNOWN`,
                              )}
                            </span>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell className="status items-center">
                        <StatusBadge
                          status={tracker.status as string}
                          style={{ width: "100%" }}
                        />
                      </TableCell>
                      <TableCell className="last-event items-center py-1 text-xs font-bold text-gray-600 text-ellipsis">
                        <span
                          className="text-ellipsis"
                          title={
                            isNoneOrEmpty(tracker?.events)
                              ? ""
                              : formatEventDescription(
                                (tracker?.events as TrackingEvent[])[0],
                              )
                          }
                        >
                          {isNoneOrEmpty(tracker?.events)
                            ? ""
                            : formatEventDescription(
                              (tracker?.events as TrackingEvent[])[0],
                            )}
                        </span>
                      </TableCell>
                      <TableCell className="date items-center text-right">
                        <p className="text-xs font-semibold text-gray-600">
                          {isNoneOrEmpty(tracker?.events)
                            ? ""
                            : formatEventDate(
                              (tracker?.events as TrackingEvent[])[0],
                            )}
                        </p>
                      </TableCell>
                      <TableCell className="action items-center p-1 sticky-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="ml-auto"
                          onClick={(e) => {
                            e.stopPropagation();
                            confirmDeletion({
                              label: "Delet Shipment Tracker",
                              identifier: tracker.id as string,
                              onConfirm: remove(tracker.id),
                            });
                          }}
                        >
                          <span className="icon is-small">
                            <i className="fas fa-trash"></i>
                          </span>
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </StickyTableWrapper>

            <div className="px-2 py-2 is-vcentered">
              <span className="is-size-7 has-text-weight-semibold">
                {(trackers?.edges || []).length} results
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
                  disabled={!trackers?.page_info.has_next_page}
                >
                  Next
                </button>
              </div>
            </div>
          </>
        )}

        {query.isFetched && (trackers?.edges || []).length == 0 && (
          <div className="card my-6">
            <div className="card-content has-text-centered">
              <p>No shipment trackers found.</p>
            </div>
          </div>
        )}
      </>
    );
  };

  return (
    <>
      <TrackerModalProvider>
        <TrackingPreview>
          <ConfirmModal>
            <Component />
          </ConfirmModal>
        </TrackingPreview>
      </TrackerModalProvider>
    </>
  );
}

function formatEventDescription(last_event?: TrackingEvent): string {
  return last_event?.description || "";
}

function formatEventDate(last_event?: TrackingEvent): string {
  if (isNone(last_event)) return "";

  return [last_event?.date, last_event?.time]
    .filter((a) => !isNone(a) && a !== "")
    .join(" ");
}
