"use client";
import {
  TrackerModalProvider,
  useTrackerModal,
} from "@karrio/ui/components/track-shipment-dialog";
import {
  TrackingPreview,
  useTrackingPreview,
} from "@karrio/ui/components/tracking-preview-sheet";
import { DeleteConfirmationDialog } from "@karrio/ui/components/delete-confirmation-dialog";
import {
  formatRef,
  getURLSearchParams,
  isNone,
  isNoneOrEmpty,
  preventPropagation,
  snakeCase,
} from "@karrio/lib";
import { useTrackerMutation, useTrackers } from "@karrio/hooks/tracker";
import { TrackersFilter } from "@karrio/ui/components/trackers-filter";
import { FiltersCard } from "@karrio/ui/components/filters-card";
import { StickyTableWrapper } from "@karrio/ui/components/sticky-table-wrapper";
import { ListPagination } from "@karrio/ui/components/list-pagination";
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
import { ShipmentsStatusBadge } from "@karrio/ui/components/shipments-status-badge";
import { useLoader } from "@karrio/ui/core/components/loader";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { TrackingEvent } from "@karrio/types/rest/api";
import { useSearchParams } from "next/navigation";
import { Trash2 } from "lucide-react";
import React, { useEffect, useState } from "react";


export default function TrackersPage(pageProps: any) {
  const Component = (): JSX.Element => {
    const searchParams = useSearchParams();
    const modal = searchParams.get("modal") as string;
    const { setLoading } = useLoader();
    const mutation = useTrackerMutation();
    const { addTracker } = useTrackerModal();
    const { previewTracker } = useTrackingPreview();
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [trackerToDelete, setTrackerToDelete] = useState<string | null>(null);
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
            <Button
              size="sm"
              className="mx-1 w-auto"
              onClick={() => addTracker({ onChange: updateFilter })}
            >
              Track a Shipment
            </Button>
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
                              snakeCase(tracker.meta?.carrier || tracker.carrier_name)
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
                        <div style={{ paddingLeft: '7px', paddingRight: '7px' }}>
                          <ShipmentsStatusBadge
                            status={tracker.status as string}
                            className="w-full justify-center text-center"
                          />
                        </div>
                      </TableCell>
                      <TableCell className="last-event items-center py-1 text-xs font-bold text-gray-600 md:text-ellipsis">
                        <span
                          className="md:text-ellipsis break-words"
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
                            setTrackerToDelete(tracker.id);
                            setDeleteDialogOpen(true);
                          }}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </StickyTableWrapper>

            {/* Sticky Footer */}
            <div className="sticky bottom-0 left-0 right-0 z-10 bg-white border-t border-gray-200 pb-16 md:pb-0">
              <ListPagination
                currentOffset={filter.offset as number || 0}
                pageSize={20}
                totalCount={trackers?.page_info?.count || 0}
                hasNextPage={trackers?.page_info?.has_next_page || false}
                onPageChange={(offset) => updateFilter({ offset })}
                className="px-2 py-3"
              />
            </div>
          </>
        )}

        {query.isFetched && (trackers?.edges || []).length == 0 && (
          <div className="bg-white rounded-lg shadow-sm border my-6">
            <div className="p-6 text-center">
              <p>No shipment trackers found.</p>
            </div>
          </div>
        )}

        <DeleteConfirmationDialog
          open={deleteDialogOpen}
          onOpenChange={setDeleteDialogOpen}
          title="Delete Tracker"
          description="Are you sure you want to delete this tracker? This action cannot be undone."
          onConfirm={async () => {
            if (trackerToDelete) {
              await remove(trackerToDelete)();
              setDeleteDialogOpen(false);
              setTrackerToDelete(null);
            }
          }}
        />
      </>
    );
  };

  return (
    <>
      <TrackerModalProvider>
        <TrackingPreview>
          <Component />
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
