"use client";
import { EnhancedMetadataEditor } from "@karrio/ui/components/enhanced-metadata-editor";
import { AddressDescription } from "@karrio/ui/components/address-description";
import { ParcelDescription } from "@karrio/ui/components/parcel-description";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { CopiableLink } from "@karrio/ui/components/copiable-link";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { usePickup, usePickupMutation } from "@karrio/hooks/pickup";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Spinner } from "@karrio/ui/components/spinner";
import { useSystemConnections } from "@karrio/hooks/system-connection";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { Button } from "@karrio/ui/components/ui/button";
import { formatDateTime, formatRef, isNone, errorToMessages } from "@karrio/lib";
import { ParcelType } from "@karrio/types";
import { useEvents } from "@karrio/hooks/event";
import { useLogs } from "@karrio/hooks/log";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/ui/components/ui/table";
import React from "react";

export const PickupComponent = ({
  pickupId,
  isPreview,
  isSheet,
}: {
  pickupId: string;
  isPreview?: boolean;
  isSheet?: boolean;
}): JSX.Element => {
  const { setLoading } = useLoader();
  const { toast } = useToast();
  const { user_connections } = useCarrierConnections();
  const { system_connections } = useSystemConnections();
  const entity_id = pickupId;
  const { query: logs } = useLogs({ entity_id });
  const { query: events } = useEvents({ entity_id });
  const {
    query: { data: { pickup } = {}, ...query },
  } = usePickup(entity_id);
  const { cancelPickup } = usePickupMutation(entity_id);

  const getCarrier = () =>
    (user_connections || []).find(
      (_) =>
        _.id === pickup?.pickup_carrier?.connection_id ||
        _.carrier_id === pickup?.carrier_id,
    ) ||
    (system_connections || []).find(
      (_) =>
        _.id === pickup?.pickup_carrier?.connection_id ||
        _.carrier_id === pickup?.carrier_id,
    );

  const handleCancelPickup = async () => {
    try {
      await cancelPickup.mutateAsync(pickupId);
      toast({
        title: "Pickup Cancelled",
        description: "The pickup has been successfully cancelled.",
      });
    } catch (error: any) {
      const messages = errorToMessages(error);
      toast({
        variant: "destructive",
        title: "Failed to cancel pickup",
        description: messages
          .map((m: any) => (typeof m === "string" ? m : m.message || JSON.stringify(m)))
          .join("; "),
      });
    }
  };

  React.useEffect(() => {
    setLoading(query.isFetching);
  }, [query.isFetching]);

  return (
    <>
      {!query.isFetched && query.isFetching && <Spinner />}

      {pickup && (
        <div className="space-y-4">
          {/* Header Section */}
          <div className="flex justify-between items-start gap-4">
            <div className="space-y-2 flex-1">
              <AppLink
                href="/pickups"
                className="text-sm font-semibold text-blue-600 tracking-wide hover:text-blue-800 transition-colors duration-150 flex items-center gap-1"
              >
                Pickups <i className="fas fa-chevron-right text-xs"></i>
              </AppLink>
              <div className="flex items-center gap-2">
                <span className="text-3xl font-bold">
                  {pickup.confirmation_number || "PENDING"}
                </span>
                <StatusBadge status={pickup.status || "scheduled"} />
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
                      href={`/pickups`}
                      target="_blank"
                    >
                      <i className="fas fa-external-link-alt text-xs"></i>
                    </AppLink>
                  </Button>
                )}
                {!["cancelled", "closed"].includes(pickup.status || "") && (
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-destructive hover:text-destructive"
                    onClick={handleCancelPickup}
                  >
                    Cancel Pickup
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
                    href={`/pickups`}
                    target="_blank"
                  >
                    <i className="fas fa-external-link-alt text-xs"></i>
                  </AppLink>
                </Button>
              )}
              {!["cancelled", "closed"].includes(pickup.status || "") && (
                <Button
                  variant="outline"
                  size="sm"
                  className="text-destructive hover:text-destructive"
                  onClick={handleCancelPickup}
                >
                  Cancel Pickup
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
                    <div className="text-xs mb-1 font-bold">Pickup ID</div>
                    <CopiableLink text={pickup.id as string} title="Copy ID" variant="outline" />
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Carrier</div>
                    <div className="flex items-center">
                      <CarrierImage
                        carrier_name={pickup.carrier_name || ""}
                        containerClassName="mt-1 ml-1 mr-2"
                        height={28}
                        width={28}
                        text_color={getCarrier()?.config?.text_color}
                        background={getCarrier()?.config?.brand_color}
                      />
                      <div className="text-ellipsis text-xs" style={{ maxWidth: "190px", lineHeight: "16px" }}>
                        <span className="text-blue-600 font-bold">
                          {pickup.carrier_name ? formatRef(pickup.carrier_name) : "-"}
                        </span>
                        <br />
                        <span className="text-ellipsis">
                          {pickup.carrier_id || "-"}
                        </span>
                      </div>
                    </div>
                  </div>
                  {!isNone(pickup.confirmation_number) && (
                    <div>
                      <div className="text-xs mb-1 font-bold">Confirmation #</div>
                      <div className="text-sm font-medium">
                        {pickup.confirmation_number}
                      </div>
                    </div>
                  )}
                  <div>
                    <div className="text-xs mb-1 font-bold">Status</div>
                    <StatusBadge status={pickup.status || "scheduled"} />
                  </div>
                </div>
                <div className="space-y-3">
                  <div>
                    <div className="text-xs mb-1 font-bold">Pickup Date</div>
                    <div className="text-sm font-medium">
                      {pickup.pickup_date || "-"}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Time Window</div>
                    <div className="text-sm font-medium">
                      {pickup.ready_time && pickup.closing_time
                        ? `${pickup.ready_time} - ${pickup.closing_time}`
                        : pickup.ready_time || pickup.closing_time || "-"}
                    </div>
                  </div>
                  {!isNone(pickup.package_location) && (
                    <div>
                      <div className="text-xs mb-1 font-bold">Package Location</div>
                      <div className="text-sm font-medium">
                        {pickup.package_location}
                      </div>
                    </div>
                  )}
                  {!isNone(pickup.instruction) && (
                    <div>
                      <div className="text-xs mb-1 font-bold">Instructions</div>
                      <div className="text-sm font-medium">
                        {pickup.instruction}
                      </div>
                    </div>
                  )}
                  <div>
                    <div className="text-xs mb-1 font-bold">Created At</div>
                    <div className="text-sm font-medium">
                      {formatDateTime(pickup.created_at)}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Last update</div>
                    <div className="text-sm">{formatDateTime(pickup.updated_at)}</div>
                  </div>
                </div>
              </div>

              {/* Metadata Section - Part of sidebar on desktop only */}
              <div className={isSheet ? "hidden" : "hidden lg:block mt-6"}>
                <h4 className="text-xl font-semibold mb-3">Metadata</h4>
                <EnhancedMetadataEditor
                  value={pickup.metadata || {}}
                  placeholder="No metadata configured"
                  emptyStateMessage="No metadata available"
                  allowEdit={false}
                  showTypeInference={true}
                  maxHeight="300px"
                />
              </div>
            </div>

            {/* Left Column - Main Content */}
            <div className={`space-y-6 order-1 mr-5 ${isSheet ? '' : 'lg:col-span-3 lg:col-start-1 lg:order-1'}`}>

              {/* Pickup Charge section */}
              {!isNone(pickup.pickup_charge) && pickup.pickup_charge?.amount && (
                <>
                  <h2 className="text-xl font-semibold my-4">Pickup Charge</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-900">
                        {pickup.pickup_charge?.name || "Pickup fee"}
                      </span>
                      <div className="text-sm text-gray-900 text-right">
                        <span className="mr-1">{pickup.pickup_charge?.amount}</span>
                        {!isNone(pickup.pickup_charge?.currency) && (
                          <span>{pickup.pickup_charge?.currency}</span>
                        )}
                      </div>
                    </div>
                  </div>
                </>
              )}

              {/* Address section */}
              {!isNone(pickup.address) && (
                <>
                  <h2 className="text-xl font-semibold my-4">Pickup Address</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6">
                    <div className="text-base py-1">
                      <AddressDescription address={pickup.address as any} />
                    </div>
                  </div>
                </>
              )}

              {/* Parcels section */}
              {(pickup.parcels || []).length > 0 && (
                <>
                  <h2 className="text-xl font-semibold my-4">
                    Parcels{" "}
                    <span className="text-lg">({pickup.parcels.length})</span>
                  </h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6">
                    {pickup.parcels.map((parcel: ParcelType, index: number) => (
                      <React.Fragment key={index + "parcel-info"}>
                        {index > 0 && <hr className="my-4" style={{ height: "1px" }} />}
                        <div className="text-base py-1">
                          <ParcelDescription parcel={parcel} />
                        </div>
                      </React.Fragment>
                    ))}
                  </div>
                </>
              )}

              {/* Related Shipments section */}
              {(pickup.shipments || []).length > 0 && (
                <>
                  <h2 className="text-xl font-semibold my-4">
                    Related Shipments{" "}
                    <span className="text-lg">({pickup.shipments.length})</span>
                  </h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6">
                    <div className="rounded-md border">
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Tracking #</TableHead>
                            <TableHead>Service</TableHead>
                            <TableHead>Shipment Status</TableHead>
                            <TableHead>Tracker Status</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {pickup.shipments.map((shipment) => (
                            <TableRow key={shipment.id}>
                              <TableCell>
                                <AppLink
                                  href={`/shipments/${shipment.id}`}
                                  className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                                  target="_blank"
                                >
                                  {shipment.tracking_number || shipment.id.substring(0, 12)}
                                </AppLink>
                              </TableCell>
                              <TableCell>
                                <span className="text-sm">
                                  {shipment.service ? formatRef(shipment.service) : "-"}
                                </span>
                              </TableCell>
                              <TableCell>
                                <StatusBadge status={shipment.status || "unknown"} />
                              </TableCell>
                              <TableCell>
                                {shipment.tracker ? (
                                  <StatusBadge status={shipment.tracker.status || "unknown"} />
                                ) : (
                                  <span className="text-xs text-muted-foreground">No tracker</span>
                                )}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>
                  </div>
                </>
              )}

              {/* Tracking Events from Related Shipments */}
              {(pickup.shipments || []).some((s) => s.tracker?.events?.length) && (
                <>
                  <h2 className="text-xl font-semibold my-4">Tracking Records</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6 space-y-4">
                    {pickup.shipments
                      .filter((s) => s.tracker?.events?.length)
                      .map((shipment) => (
                        <div key={shipment.id} className="space-y-2">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-semibold">
                              {shipment.tracking_number || shipment.id.substring(0, 12)}
                            </span>
                            {shipment.tracker && (
                              <StatusBadge status={shipment.tracker.status || "unknown"} />
                            )}
                            {shipment.tracker?.delivered && (
                              <span className="text-xs text-green-600 font-medium">Delivered</span>
                            )}
                            {shipment.tracker?.estimated_delivery && !shipment.tracker?.delivered && (
                              <span className="text-xs text-muted-foreground">
                                Est. {shipment.tracker.estimated_delivery}
                              </span>
                            )}
                          </div>
                          <div className="border rounded-md p-3 space-y-2">
                            {(shipment.tracker?.events || []).map((event, idx) => (
                              <div key={idx} className="flex items-start gap-3 text-sm">
                                <div className="text-xs text-muted-foreground whitespace-nowrap min-w-[100px]">
                                  {event.date} {event.time}
                                </div>
                                <div className="flex-1">
                                  <p className="text-sm">{event.description}</p>
                                  {event.location && (
                                    <p className="text-xs text-muted-foreground">{event.location}</p>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>
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
                    value={pickup.metadata || {}}
                    placeholder="No metadata configured"
                    emptyStateMessage="No metadata available"
                    allowEdit={false}
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
          />
        </div>
      )}

      {query.isFetched && isNone(pickup) && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm my-6">
          <div className="p-6 text-center">
            <p>Uh Oh!</p>
            <p>{"We couldn't find any pickup with that reference"}</p>
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

    return <PickupComponent pickupId={id} />;
  };

  return <Component />;
}
