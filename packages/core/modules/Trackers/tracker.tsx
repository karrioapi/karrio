"use client";
import { EnhancedMetadataEditor } from "@karrio/ui/components/enhanced-metadata-editor";
import { ShipmentsStatusBadge } from "@karrio/ui/components/shipments-status-badge";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { CopiableLink } from "@karrio/ui/components/copiable-link";
import { useMetadataMutation } from "@karrio/hooks/metadata";
import { useTracker } from "@karrio/hooks/tracker";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Spinner } from "@karrio/ui/components/spinner";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { Button } from "@karrio/ui/components/ui/button";
import { formatDateTime, formatDayDate, formatRef, isNone, isNoneOrEmpty } from "@karrio/lib";
import { NotificationType, MetadataObjectTypeEnum, TrackingEventType } from "@karrio/types";
import { useEvents } from "@karrio/hooks/event";
import { useLogs } from "@karrio/hooks/log";
import {
  CheckCircle,
  Truck,
  MapPin,
  Package,
  Calendar,
  Clock,
  ExternalLink,
} from "lucide-react";
import React from "react";

type DayEvents = { [k: string]: TrackingEventType[] };

export const TrackerComponent = ({
  trackerId,
  isPreview,
  isSheet,
}: {
  trackerId: string;
  isPreview?: boolean;
  isSheet?: boolean;
}): JSX.Element => {
  const notifier = useNotifier();
  const { setLoading } = useLoader();
  const entity_id = trackerId;
  const { query: logs } = useLogs({ entity_id });
  const { query: events } = useEvents({ entity_id });
  const {
    query: { data: { tracker } = {}, ...query },
  } = useTracker(entity_id);
  const { updateMetadata } = useMetadataMutation([
    "trackers",
    entity_id,
  ]);

  const computeEvents = (evts: TrackingEventType[]): DayEvents => {
    return (evts || []).reduce(
      (days: any, event: TrackingEventType) => {
        const daydate = formatDayDate(event.date as string);
        return { ...days, [daydate]: [...(days[daydate] || []), event] };
      },
      {} as DayEvents,
    );
  };

  const getEventIcon = (description?: string) => {
    const desc = description?.toLowerCase() || "";
    if (desc.includes("delivered") || desc.includes("parcel locker")) {
      return <CheckCircle className="h-3 w-3 text-green-600" />;
    }
    if (desc.includes("out for delivery")) {
      return <Truck className="h-3 w-3 text-orange-600" />;
    }
    if (desc.includes("arrived") || desc.includes("post office")) {
      return <MapPin className="h-3 w-3 text-blue-600" />;
    }
    if (desc.includes("transit") || desc.includes("departed")) {
      return <Package className="h-3 w-3 text-gray-600" />;
    }
    if (desc.includes("created") || desc.includes("awaiting")) {
      return <Calendar className="h-3 w-3 text-purple-600" />;
    }
    return <Clock className="h-3 w-3 text-gray-500" />;
  };

  const handleMetadataChange = async (newMetadata: any) => {
    try {
      const currentMetadata = tracker?.metadata || {};

      const added_values = { ...newMetadata };
      const discarded_keys = Object.keys(currentMetadata).filter(
        key => !(key in newMetadata)
      );

      await updateMetadata.mutateAsync({
        id: entity_id,
        object_type: MetadataObjectTypeEnum.tracker,
        discarded_keys,
        added_values,
      });

      notifier.notify({
        type: NotificationType.success,
        message: "Metadata updated successfully",
      });
    } catch (error) {
      notifier.notify({
        type: NotificationType.error,
        message: "Failed to update metadata",
      });
    }
  };

  React.useEffect(() => {
    setLoading(query.isFetching);
  }, [query.isFetching]);

  return (
    <>
      {!query.isFetched && query.isFetching && <Spinner />}

      {tracker && (
        <div className="space-y-4">
          {/* Header Section */}
          <div className="flex justify-between items-start gap-4">
            <div className="space-y-2 flex-1">
              <AppLink
                href="/trackers"
                className="text-sm font-semibold text-blue-600 tracking-wide hover:text-blue-800 transition-colors duration-150 flex items-center gap-1"
              >
                Trackers <i className="fas fa-chevron-right text-xs"></i>
              </AppLink>
              <div className="flex items-center gap-2">
                <span className="text-3xl font-bold">
                  {tracker.tracking_number}
                </span>
                <ShipmentsStatusBadge status={tracker.status as string} />
              </div>

              {/* Mobile actions */}
              <div className="flex justify-start items-center gap-1 md:hidden">
                {isPreview && isSheet && (
                  <Button
                    variant="ghost"
                    size="sm"
                    asChild
                    className="h-8"
                  >
                    <AppLink
                      href={`/trackers/${trackerId}`}
                      target="_blank"
                    >
                      <i className="fas fa-external-link-alt text-xs"></i>
                    </AppLink>
                  </Button>
                )}
              </div>
            </div>

            {/* Desktop actions */}
            <div className={`${isSheet ? 'hidden md:flex' : 'hidden md:flex'} items-center gap-1`}>
              {isPreview && (
                <Button
                  variant="ghost"
                  size="sm"
                  asChild
                  className="h-8"
                >
                  <AppLink
                    href={`/trackers/${trackerId}`}
                    target="_blank"
                  >
                    <i className="fas fa-external-link-alt text-xs"></i>
                  </AppLink>
                </Button>
              )}
            </div>
          </div>

          {/* Main Content with Sidebar Layout */}
          <div className={`flex flex-col ${isSheet ? '' : 'lg:grid lg:grid-cols-4'} gap-6`}>
            {/* Right Sidebar - Details Section */}
            <div className={isSheet ? '' : 'lg:order-2 lg:col-span-1 lg:col-start-4'}>
              <h3 className={`text-xl font-semibold my-4 ${isSheet ? '' : 'lg:mb-4 lg:mt-0'}`}>
                Details
              </h3>
              <div className={isSheet ? 'grid grid-cols-1 md:grid-cols-2 gap-4' : 'space-y-3'}>
                <div className="space-y-3">
                  <div>
                    <div className="text-xs mb-1 font-bold">Tracker ID</div>
                    <CopiableLink text={tracker.id as string} title="Copy ID" variant="outline" />
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Carrier</div>
                    <div className="flex items-center">
                      <CarrierImage
                        carrier_name={
                          (tracker.meta as any)?.carrier || tracker.carrier_name || ""
                        }
                        containerClassName="mt-1 ml-1 mr-2"
                        height={28}
                        width={28}
                        text_color={(tracker.tracking_carrier as any)?.config?.text_color}
                        background={(tracker.tracking_carrier as any)?.config?.brand_color}
                      />
                      <div className="text-ellipsis text-xs" style={{ maxWidth: "190px", lineHeight: "16px" }}>
                        <span className="text-blue-600 font-bold">
                          {tracker.carrier_name ? formatRef(tracker.carrier_name) : "-"}
                        </span>
                        <br />
                        <span className="text-ellipsis">
                          {tracker.carrier_id || "-"}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Status</div>
                    <ShipmentsStatusBadge status={tracker.status as string} />
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Test Mode</div>
                    <div className="text-sm font-medium">
                      {tracker.test_mode ? "Yes" : "No"}
                    </div>
                  </div>
                </div>
                <div className="space-y-3">
                  <div>
                    <div className="text-xs mb-1 font-bold">Tracking Number</div>
                    <div className="text-sm font-medium text-blue-600">
                      {tracker.tracking_number}
                    </div>
                  </div>
                  {!isNone(tracker.estimated_delivery) && (
                    <div>
                      <div className="text-xs mb-1 font-bold">Estimated Delivery</div>
                      <div className="text-sm font-medium">
                        {formatDayDate(tracker.estimated_delivery as string)}
                      </div>
                    </div>
                  )}
                  {!isNone(tracker.info?.signed_by) && (
                    <div>
                      <div className="text-xs mb-1 font-bold">Signed By</div>
                      <div className="text-sm font-medium">
                        {tracker.info?.signed_by}
                      </div>
                    </div>
                  )}
                  <div>
                    <div className="text-xs mb-1 font-bold">Created At</div>
                    <div className="text-sm font-medium">
                      {formatDateTime(tracker.created_at)}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Last update</div>
                    <div className="text-sm">{formatDateTime(tracker.updated_at)}</div>
                  </div>
                </div>
              </div>

              {/* Metadata Section - Part of sidebar on desktop only */}
              <div className={isSheet ? "hidden" : "hidden lg:block mt-6"}>
                <h4 className="text-xl font-semibold mb-3">Metadata</h4>
                <EnhancedMetadataEditor
                  value={tracker.metadata || {}}
                  onChange={handleMetadataChange}
                  placeholder="No metadata configured"
                  emptyStateMessage="Add key-value pairs to configure metadata"
                  allowEdit={true}
                  showTypeInference={true}
                  maxHeight="300px"
                />
              </div>
            </div>

            {/* Left Column - Main Content */}
            <div className={`space-y-6 order-1 mr-5 ${isSheet ? '' : 'lg:col-span-3 lg:col-start-1 lg:order-1'}`}>

              {/* Tracking Events Timeline */}
              {!isNoneOrEmpty(tracker.events) && (
                <>
                  <h2 className="text-xl font-semibold my-4">Tracking Events</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6">
                    <div className="max-h-96 overflow-y-auto">
                      {Object.entries(computeEvents(tracker.events as TrackingEventType[])).map(
                        ([day, dayEvents], dayIndex) => (
                          <div key={dayIndex} className="border-b border-gray-100 last:border-b-0">
                            <div className="bg-blue-50 px-4 py-3 border-b border-blue-100">
                              <div className="flex items-center gap-2">
                                <Calendar className="h-3 w-3 text-blue-600" />
                                <div>
                                  <h3 className="text-sm font-medium text-gray-900 capitalize">{day}</h3>
                                  <p className="text-xs text-gray-500">{dayEvents.length} events</p>
                                </div>
                              </div>
                            </div>

                            <div className="relative">
                              {dayEvents.map((event, eventIndex) => (
                                <div key={eventIndex} className="relative">
                                  {eventIndex < dayEvents.length - 1 && (
                                    <div className="absolute left-6 top-10 bottom-0 w-px bg-gray-200" />
                                  )}
                                  <div className="flex gap-3 p-3 hover:bg-gray-50 transition-colors">
                                    <div className="flex-shrink-0 relative z-10 mt-0.5">
                                      <div className="w-5 h-5 bg-white border border-gray-300 rounded-full flex items-center justify-center">
                                        {getEventIcon(event.description || undefined)}
                                      </div>
                                    </div>
                                    <div className="flex-1 min-w-0">
                                      <div className="flex items-start justify-between gap-2 mb-1">
                                        <div className="flex-1">
                                          <span className="text-xs font-mono bg-blue-50 text-blue-700 border border-blue-200 px-1.5 py-0.5 rounded mb-2 inline-block">
                                            {event.time}
                                          </span>
                                          {event.location && (
                                            <div className="flex items-center gap-1 mb-2">
                                              <MapPin className="h-2.5 w-2.5 text-gray-400" />
                                              <span className="text-sm font-medium text-gray-600">
                                                {event.location}
                                              </span>
                                            </div>
                                          )}
                                          <p className="text-sm text-gray-800 leading-relaxed">
                                            {event.description}
                                          </p>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        ),
                      )}
                    </div>
                  </div>
                </>
              )}

              {/* Shipment Details */}
              {!isNone(tracker.shipment) && (
                <>
                  <h2 className="text-xl font-semibold my-4">Shipment</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6 space-y-2">
                    <div className="flex items-center gap-3">
                      <span className="text-sm text-gray-600">Shipment ID</span>
                      <AppLink
                        className="text-sm text-blue-600 hover:text-blue-800 font-medium inline-flex items-center gap-1"
                        href={`/shipments/${tracker.shipment?.id}`}
                        target="_blank"
                      >
                        <span>{tracker.shipment?.id}</span>
                        <ExternalLink className="w-3 h-3" />
                      </AppLink>
                    </div>
                    {tracker.shipment?.service && (
                      <div className="flex items-center gap-3">
                        <span className="text-sm text-gray-600">Service</span>
                        <span className="text-sm font-medium">
                          {formatRef(
                            tracker.shipment?.meta?.service_name ||
                            tracker.shipment?.service
                          )}
                        </span>
                      </div>
                    )}
                    {tracker.shipment?.reference && (
                      <div className="flex items-center gap-3">
                        <span className="text-sm text-gray-600">Reference</span>
                        <span className="text-sm font-medium">
                          {tracker.shipment?.reference}
                        </span>
                      </div>
                    )}
                  </div>
                </>
              )}

              {/* Messages */}
              {(tracker.messages || []).length > 0 && (
                <>
                  <h2 className="text-xl font-semibold my-4">Messages</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6 space-y-2">
                    {(tracker.messages || []).map((msg, idx) => (
                      <div key={idx} className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                        <p className="text-sm text-yellow-800">{msg.message}</p>
                        {msg.code && (
                          <p className="text-xs text-yellow-600 mt-1">Code: {msg.code}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </>
              )}

              {/* Metadata Section - Mobile only */}
              <div className={isSheet ? "" : "lg:hidden"}>
                <h2 className="text-xl font-semibold my-4">Metadata</h2>
                <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                <div className="my-4">
                  <EnhancedMetadataEditor
                    value={tracker.metadata || {}}
                    onChange={handleMetadataChange}
                    placeholder="No metadata configured"
                    emptyStateMessage="Add key-value pairs to configure metadata"
                    allowEdit={true}
                    showTypeInference={true}
                    maxHeight="300px"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Activity Timeline section */}
          <h2 className="text-xl font-semibold my-4">Activity</h2>
          <ActivityTimeline
            logs={logs}
            events={events}
            stacked
          />
        </div>
      )}

      {query.isFetched && isNone(tracker) && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm my-6">
          <div className="p-6 text-center">
            <p>Uh Oh!</p>
            <p>{"We couldn't find any tracker with that reference"}</p>
          </div>
        </div>
      )}
    </>
  );
};

export default function Page(pageProps: { params: Promise<{ id?: string }> }) {
  const Component = (): JSX.Element => {
    const params = React.use(pageProps.params);
    const { id } = params;

    if (!id) return <></>;

    return <TrackerComponent trackerId={id} />;
  };

  return <Component />;
}
