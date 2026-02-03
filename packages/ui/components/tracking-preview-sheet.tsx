"use client";
import {
  formatAddressRegion,
  formatDayDate,
  formatRef,
  isNone,
} from "@karrio/lib";
import {
  TrackerStatusEnum,
  TrackerType,
  TrackingEventType,
} from "@karrio/types";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import React, { useRef, useState, useContext } from "react";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { useLocation } from "@karrio/hooks/location";
import { useEvents } from "@karrio/hooks/event";
import { useLogs } from "@karrio/hooks/log";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetClose
} from "@karrio/ui/components/ui/sheet";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import {
  X,
  Copy,
  ExternalLink,
  CheckCircle,
  Truck,
  MapPin,
  Package,
  Calendar,
  Clock
} from "lucide-react";

type DayEvents = { [k: string]: TrackingEventType[] };
type TrackingPreviewContextType = {
  previewTracker: (tracker: TrackerType) => void;
};

interface TrackingPreviewComponent {
  children?: React.ReactNode;
}

export const TrackingPreviewContext =
  React.createContext<TrackingPreviewContextType>(
    {} as TrackingPreviewContextType,
  );

export const TrackingPreview = ({
  children,
}: TrackingPreviewComponent): JSX.Element => {
  const link = useRef<HTMLAnchorElement>(null);
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [sharingLink, setSharingLink] = useState<string>("");
  const [key, setKey] = useState<string>(`tracker-${Date.now()}`);
  const [tracker, setTracker] = useState<TrackerType>();

  const previewTracker = (tracker: TrackerType) => {
    setTracker(tracker);
    setIsActive(true);
    setKey(`tracker-${Date.now()}`);
    link.current?.setAttribute("href", `/tracking/${tracker.id}`);
    setSharingLink(link.current?.href as string);
    addUrlParam("modal", tracker.id);
  };

  const dismiss = (_?: any) => {
    setIsActive(false);
    setTracker(undefined);
    setKey(`tracker-${Date.now()}`);
    removeUrlParam("modal");
  };

  const copy = (_: React.MouseEvent) => {
    navigator.clipboard.writeText(sharingLink);
  };

  const computeColor = (tracker: TrackerType) => {
    if (tracker?.delivered) return "bg-green-500";
    else if (tracker?.status === TrackerStatusEnum.pending.toString())
      return "bg-gray-600";
    else if (
      [
        TrackerStatusEnum.on_hold.toString(),
        TrackerStatusEnum.delivery_delayed.toString(),
      ].includes(tracker?.status as string)
    )
      return "bg-yellow-500";
    else if (
      [TrackerStatusEnum.unknown.toString()].includes(tracker?.status as string)
    )
      return "bg-gray-400";
    else if (
      [TrackerStatusEnum.delivery_failed.toString()].includes(
        tracker?.status as string,
      )
    )
      return "bg-red-500";
    else return "bg-blue-500";
  };

  const computeStatus = (tracker: TrackerType) => {
    if (tracker?.delivered) return "Delivered";
    else if (tracker?.status === TrackerStatusEnum.pending.toString())
      return "Pending";
    else if (
      [
        TrackerStatusEnum.on_hold.toString(),
        TrackerStatusEnum.delivery_delayed.toString(),
        TrackerStatusEnum.ready_for_pickup.toString(),
        TrackerStatusEnum.unknown.toString(),
        TrackerStatusEnum.delivery_failed.toString(),
      ].includes(tracker?.status as string)
    )
      return formatRef(tracker!.status as string);
    else return "In-Transit";
  };

  const computeEvents = (tracker: TrackerType): DayEvents => {
    return (tracker?.events || []).reduce(
      (days: any, event: TrackingEventType) => {
        const daydate = formatDayDate(event.date as string);
        return { ...days, [daydate]: [...(days[daydate] || []), event] };
      },
      {} as DayEvents,
    );
  };

  const getStatusIcon = (status?: string) => {
    if (status === "delivered") return <CheckCircle className="h-4 w-4" />;
    if (status === "in_transit") return <Truck className="h-4 w-4" />;
    if (status === "out_for_delivery") return <Package className="h-4 w-4" />;
    return <Clock className="h-4 w-4" />;
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

  return (
    <>
      <TrackingPreviewContext.Provider value={{ previewTracker }}>
        {children}
      </TrackingPreviewContext.Provider>

      <Sheet key={key} open={isActive} onOpenChange={(open) => !open && dismiss()}>
        <a ref={link} className="hidden"></a>
        <SheetContent
          className="w-full sm:w-[450px] sm:max-w-[450px] p-0 shadow-none"
          side="right"
        >
          <div className="h-full flex flex-col">
            <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
              <div className="flex items-center justify-between">
                <SheetTitle className="text-lg font-semibold">
                  Tracking Details
                </SheetTitle>
                <SheetClose className="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none">
                  <X className="h-4 w-4" />
                  <span className="sr-only">Close</span>
                </SheetClose>
              </div>
            </SheetHeader>

            <div className="flex-1 overflow-y-auto px-4 py-4">
              {!isNone(tracker) && (
                <div className="space-y-6">
                  {/* Carrier Image & Tracking Number */}
                  <div className="text-center mb-4">
                    <div className="flex justify-center mb-4">
                      <div className="p-3 bg-gray-50 rounded-xl">
                        <CarrierImage
                          carrier_name={
                            (tracker?.meta as any)?.carrier || tracker?.carrier_name
                          }
                          width={48}
                          height={48}
                          text_color={(tracker?.tracking_carrier as any)?.config?.text_color}
                          background={(tracker?.tracking_carrier as any)?.config?.brand_color}
                        />
                      </div>
                    </div>

                    <div className="space-y-1">
                      <div className="flex justify-center items-center gap-1 text-xs text-gray-500">
                        <Package className="h-3 w-3" />
                        <span>Tracking Number</span>
                      </div>
                      <div className="font-mono text-sm font-bold text-gray-900 bg-gray-50 px-3 py-1 rounded inline-block">
                        {tracker?.tracking_number}
                      </div>
                    </div>
                  </div>

                  {/* Estimated Delivery */}
                  {!isNone(tracker?.estimated_delivery) && (
                    <div className="text-center mb-3">
                      <div className="text-xs text-gray-500">
                        {tracker?.delivered ? "Delivered on" : "Estimated Delivery"}
                      </div>
                      <div className="font-medium text-gray-900 text-sm">
                        {formatDayDate(tracker!.estimated_delivery as string)}
                      </div>
                    </div>
                  )}

                  {/* Status Badge */}
                  <div className={`${computeColor(tracker as TrackerType)} text-white text-center py-2 rounded`}>
                    <div className="flex items-center justify-center gap-2 text-sm font-medium">
                      {getStatusIcon(tracker?.status)}
                      {computeStatus(tracker as TrackerType)}
                    </div>
                  </div>

                  {/* Events Timeline */}
                  <div className="border-t pt-4 space-y-4">
                    <h3 className="text-lg font-semibold">Tracking Timeline</h3>
                    <div className="max-h-96 overflow-y-auto">
                      {Object.entries(computeEvents(tracker as TrackerType)).map(
                        ([day, events], dayIndex) => (
                          <div key={dayIndex} className="border-b border-gray-100 last:border-b-0">
                            {/* Date Header */}
                            <div className="bg-blue-50 px-4 py-3 border-b border-blue-100">
                              <div className="flex items-center gap-2">
                                <Calendar className="h-3 w-3 text-blue-600" />
                                <div>
                                  <h3 className="text-sm font-medium text-gray-900 capitalize">{day}</h3>
                                  <p className="text-xs text-gray-500">{events.length} events</p>
                                </div>
                              </div>
                            </div>

                            {/* Events */}
                            <div className="relative">
                              {events.map((event, eventIndex) => (
                                <div key={eventIndex} className="relative">
                                  {/* Timeline line */}
                                  {eventIndex < events.length - 1 && (
                                    <div className="absolute left-6 top-10 bottom-0 w-px bg-gray-200" />
                                  )}

                                  <div className="flex gap-3 p-3 hover:bg-gray-50 transition-colors">
                                    {/* Timeline dot with icon */}
                                    <div className="flex-shrink-0 relative z-10 mt-0.5">
                                      <div className="w-5 h-5 bg-white border border-gray-300 rounded-full flex items-center justify-center">
                                        {getEventIcon(event.description || undefined)}
                                      </div>
                                    </div>

                                    {/* Event content */}
                                    <div className="flex-1 min-w-0">
                                      <div className="flex items-start justify-between gap-2 mb-1">
                                        <div className="flex-1">
                                          <Badge
                                            variant="outline"
                                            className="text-xs font-mono bg-blue-50 text-blue-700 border-blue-200 mb-2"
                                          >
                                            {event.time}
                                          </Badge>

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

                  {/* Messages */}
                  {(tracker?.messages || []).length > 0 && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                      <p className="text-sm text-yellow-800">
                        {(tracker?.messages || [{}])[0].message}
                      </p>
                    </div>
                  )}

                  {/* Shipment Details */}
                  {!isNone(tracker?.shipment) && (
                    <div className="border-t pt-4 space-y-4">
                      <h3 className="text-lg font-semibold">Shipment Details</h3>

                      {/* Shipment ID */}
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-4 sm:items-center">
                        <div className="text-sm text-gray-600">Shipment ID</div>
                        <div className="col-span-2">
                          <AppLink
                            className="text-blue-600 hover:text-blue-800 text-sm font-medium inline-flex items-center gap-1"
                            href={`/shipments/${tracker?.shipment?.id}`}
                            target="_blank"
                          >
                            <span>{tracker?.shipment?.id}</span>
                            <ExternalLink className="w-3 h-3" />
                          </AppLink>
                        </div>
                      </div>

                      {/* Origin/Destination */}
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-4 sm:items-center">
                        <div className="text-sm text-gray-600">Origin/Destination</div>
                        <div className="col-span-2 text-sm font-medium flex items-center gap-2">
                          <span>{formatAddressRegion(tracker?.shipment?.shipper as any)}</span>
                          <span>→</span>
                          <span>{formatAddressRegion(tracker?.shipment?.recipient as any)}</span>
                        </div>
                      </div>

                      {/* Service */}
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-4 sm:items-center">
                        <div className="text-sm text-gray-600">Service</div>
                        <div className="col-span-2 text-sm font-medium">
                          {formatRef(
                            tracker?.info?.shipment_service ||
                            tracker?.shipment?.meta?.service_name ||
                            tracker?.shipment?.service,
                          )}
                        </div>
                      </div>

                      {/* Reference */}
                      {tracker?.shipment?.reference && (
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-4 sm:items-center">
                          <div className="text-sm text-gray-600">Reference</div>
                          <div className="col-span-2 text-sm font-medium">
                            {tracker?.shipment?.reference}
                          </div>
                        </div>
                      )}

                    </div>
                  )}

                  {/* Activity Section */}
                  {tracker?.id && (
                    <div className="border-t pt-4 space-y-3">
                      <div className="flex items-center justify-between">
                        <h3 className="text-lg font-semibold">Activity</h3>
                        <AppLink
                          href={`/trackers/${tracker.id}`}
                          className="text-sm text-blue-600 hover:text-blue-800 font-medium inline-flex items-center gap-1"
                        >
                          View all
                          <ExternalLink className="w-3 h-3" />
                        </AppLink>
                      </div>
                      <TrackerActivityPreview trackerId={tracker.id} />
                    </div>
                  )}

                  {/* Share Section */}
                  <div className="border-t pt-4 space-y-3">
                    <Label className="text-sm font-medium">Share</Label>
                    <div className="flex gap-2">
                      <Input
                        type="text"
                        value={sharingLink}
                        readOnly
                        className="flex-1"
                        title="Click to Copy"
                      />
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={copy}
                      >
                        <Copy className="w-4 h-4" />
                      </Button>
                      <Button
                        asChild
                        variant="outline"
                        size="sm"
                      >
                        <a href={sharingLink} target="_blank" rel="noopener noreferrer">
                          <ExternalLink className="w-4 h-4" />
                        </a>
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </SheetContent>
      </Sheet>
    </>
  );
};

const TrackerActivityPreview = ({ trackerId }: { trackerId: string }) => {
  const { query: logs } = useLogs({ entity_id: trackerId });
  const { query: events } = useEvents({ entity_id: trackerId });

  return (
    <ActivityTimeline
      logs={logs}
      events={events}
      stacked
    />
  );
};

export function useTrackingPreview() {
  return useContext(TrackingPreviewContext);
}