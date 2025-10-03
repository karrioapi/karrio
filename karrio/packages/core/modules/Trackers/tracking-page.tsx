import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { TrackingEvent, TrackingStatus } from "@karrio/types/rest/api";
import { formatDayDate, isNone, KARRIO_API, url$ } from "@karrio/lib";
import { Collection, KarrioClient } from "@karrio/types";
import { loadMetadata, getCurrentDomain } from "@karrio/core/context/main";
import {
  AlertCircle,
  MapPin,
  CheckCircle,
  Package,
  Clock,
  Truck,
  Calendar
} from "lucide-react";
import { Card, CardContent, CardHeader } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import Link from "next/link";

type DayEvents = { [k: string]: TrackingEvent[] };

export default async function Page({ params }: { params: Promise<Collection> }) {
  const query = await params;
  const id = query?.id as string;
  const domain = await getCurrentDomain();
  const { metadata } = await loadMetadata(domain!);
  const client = new KarrioClient({
    basePath: url$`${(metadata?.HOST as string) || KARRIO_API}`,
  });

  const { data: tracker, message } = await client.trackers
    .retrieve({ idOrTrackingNumber: id })
    .then(({ data }) => ({ data, message: null }))
    .catch((_) => {
      console.log(_.response?.data?.errors || _.response);
      return { data: null, message: `No Tracker ID nor Tracking Number found for ${id}` };
    });

  const computeEvents = (tracker: TrackingStatus): DayEvents => {
    return (tracker?.events || []).reduce((days, event: TrackingEvent) => {
      const daydate = formatDayDate(event.date as string);
      return { ...days, [daydate]: [...(days[daydate] || []), event] };
    }, {} as DayEvents);
  };

  const getStatusColor = (status?: string) => {
    if (status === "delivered") return "bg-green-500";
    if (status === "in_transit") return "bg-blue-500";
    if (status === "out_for_delivery") return "bg-orange-500";
    return "bg-gray-500";
  };

  const getStatusText = (status?: string) => {
    if (status === "delivered") return "Delivered";
    if (status === "in_transit") return "In Transit";
    if (status === "out_for_delivery") return "Out for Delivery";
    return "Pending";
  };

  const getStatusIcon = (status?: string) => {
    if (status === "delivered") return <CheckCircle className="h-5 w-5" />;
    if (status === "in_transit") return <Truck className="h-5 w-5" />;
    if (status === "out_for_delivery") return <Package className="h-5 w-5" />;
    return <Clock className="h-5 w-5" />;
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

  if (!tracker) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4 bg-gray-50">
        <div className="w-full max-w-md">
          <Alert className="border-red-200 bg-red-50">
            <AlertCircle className="h-5 w-5 text-red-600" />
            <AlertDescription className="text-red-800 font-medium">
              {message}
            </AlertDescription>
          </Alert>
        </div>
      </div>
    );
  }

  const eventDays = Object.entries(computeEvents(tracker as TrackingStatus));
  const totalEvents = Object.values(computeEvents(tracker as TrackingStatus)).flat().length;

  return (
    <div className="min-h-screen bg-gray-50 py-4 px-4">
      <div className="max-w-lg mx-auto">
        {!isNone(tracker) && (
          <>
            {/* Header Card with Tracking Info */}
            <Card className="mb-4 shadow-sm border overflow-hidden">
              <CardContent className="p-0">
                {/* Carrier & Info Section */}
                <div className="bg-white p-6 text-center">
                  <div className="flex justify-center mb-4">
                    <div className="p-3 bg-gray-50 rounded-xl">
                      <CarrierImage
                        carrier_name={tracker!.carrier_name}
                        width={48}
                        height={48}
                      />
                    </div>
                  </div>

                  <div className="space-y-1 mb-4">
                    <div className="flex justify-center items-center gap-1 text-xs text-gray-500">
                      <Package className="h-3 w-3" />
                      <span>Tracking Number</span>
                    </div>
                    <div className="font-mono text-sm font-bold text-gray-900 bg-gray-50 px-3 py-1 rounded inline-block">
                      {tracker?.tracking_number}
                    </div>
                  </div>

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
                </div>

                {/* Status Banner */}
                <div className={`${getStatusColor(tracker?.status)} text-white py-3 px-6`}>
                  <div className="flex items-center justify-center gap-2 text-lg font-medium">
                    {getStatusIcon(tracker?.status)}
                    {getStatusText(tracker?.status)}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Progress Summary */}
            <Card className="mb-4 shadow-sm border">
              <CardContent className="p-3">
                <div className="flex items-center justify-between text-xs text-gray-600">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-3 w-3" />
                    <span>{eventDays.length} tracking days</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <MapPin className="h-3 w-3" />
                    <span>{totalEvents} events recorded</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Timeline */}
            <Card className="shadow-sm border overflow-hidden">
              <CardHeader className="bg-white border-b p-3">
                <div className="flex items-center gap-2">
                  <Truck className="h-4 w-4 text-gray-700" />
                  <h2 className="text-sm font-medium text-gray-900">Tracking Timeline</h2>
                </div>
              </CardHeader>
              <CardContent className="p-0">
                <div className="bg-white">
                  {eventDays.map(([day, events], dayIndex) => (
                    <div key={dayIndex} className="border-b border-gray-100 last:border-b-0">
                      {/* Date Header */}
                      <div className="bg-blue-50 px-4 py-2 border-b border-blue-100">
                        <div className="flex items-center gap-2">
                          <Calendar className="h-3 w-3 text-blue-600" />
                          <div>
                            <h3 className="font-medium text-gray-900 text-sm capitalize">{day}</h3>
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

                            <div className="flex gap-3 p-3 hover:bg-gray-25 transition-colors">
                              {/* Timeline dot with icon */}
                              <div className="flex-shrink-0 relative z-10 mt-0.5">
                                <div className="w-5 h-5 bg-white border border-gray-300 rounded-full flex items-center justify-center">
                                  {getEventIcon(event.description)}
                                </div>
                              </div>

                              {/* Event content */}
                              <div className="flex-1 min-w-0">
                                <div className="flex items-start justify-between gap-2 mb-1">
                                  <div className="flex-1">
                                    <Badge variant="outline" className="text-xs font-mono bg-blue-50 text-blue-700 border-blue-200 mb-1">
                                      {event.time}
                                    </Badge>

                                    {event.location && (
                                      <div className="flex items-center gap-1 mb-1">
                                        <MapPin className="h-2.5 w-2.5 text-gray-400" />
                                        <span className="text-xs font-medium text-gray-600">
                                          {event.location}
                                        </span>
                                      </div>
                                    )}

                                    <p className="text-xs text-gray-800 leading-relaxed">
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
                  ))}
                </div>
              </CardContent>
            </Card>
          </>
        )}

        {!isNone(message) && (
          <Card className="mb-4 shadow-sm border">
            <CardContent className="py-8 text-center">
              <AlertCircle className="h-8 w-8 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-600">{message}</p>
            </CardContent>
          </Card>
        )}

        {/* Footer */}
        <div className="text-center mt-6 pt-4 border-t border-gray-200">
          <Link
            href="/"
            className="text-xs text-gray-500 hover:text-gray-700 transition-colors inline-flex items-center gap-1"
          >
            <Package className="h-3 w-3" />
            <span>Powered by {metadata?.APP_NAME}</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
