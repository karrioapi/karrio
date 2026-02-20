"use client";
import { EnhancedMetadataEditor } from "@karrio/ui/components/enhanced-metadata-editor";
import { useMetadataMutation } from "@karrio/hooks/metadata";
import {
  formatAddressLocation,
  formatDateTime,
  formatRef,
  isNone,
} from "@karrio/lib";
import { CommodityDescription } from "@karrio/ui/core/components/commodity-description";
import { AddressDescription } from "@karrio/ui/core/components/address-description";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";
import { CopiableLink } from "@karrio/ui/components/copiable-link";
import { ShipmentsStatusBadge } from "@karrio/ui/components/shipments-status-badge";
import { OrderMenu } from "@karrio/ui/components/order-menu";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { MetadataObjectTypeEnum, NotificationType } from "@karrio/types";
import { useEvents } from "@karrio/hooks/event";
import { useOrder } from "@karrio/hooks/order";
import { useLogs } from "@karrio/hooks/log";
import { Table, TableBody, TableRow, TableCell } from "@karrio/ui/components/ui/table";
import { Button } from "@karrio/ui/components/ui/button";
import React from "react";


type OrderComponentProps = {
  orderId: string;
  isPreview?: boolean;
  isSheet?: boolean;
};

export const OrderComponent = ({
  orderId,
  isPreview,
  isSheet,
}: OrderComponentProps): JSX.Element => {
  const notifier = useNotifier();
  const { setLoading } = useLoader();
  const entity_id = orderId;
  const { query: logs } = useLogs({ entity_id });
  const { query: events } = useEvents({ entity_id });
  const {
    query: { data: { order } = {}, ...query },
  } = useOrder(entity_id);
  const { updateMetadata } = useMetadataMutation([
    "orders",
    entity_id,
  ]);

  const handleMetadataChange = async (newMetadata: any) => {
    try {
      const currentMetadata = order?.metadata || {};

      // Calculate added_values (new or changed metadata)
      const added_values = { ...newMetadata };

      // Calculate discarded_keys (keys that were removed)
      const discarded_keys = Object.keys(currentMetadata).filter(
        key => !(key in newMetadata)
      );

      await updateMetadata.mutateAsync({
        id: entity_id,
        object_type: MetadataObjectTypeEnum.order,
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
      {(!order || !order.order_id) && <Spinner />}

      {order && order.order_id && (
        <div className="space-y-4">
          {/* Header section */}
          <div className="flex justify-between items-start gap-4">
            <div className="space-y-2 flex-1">
              <AppLink
                href="/orders"
                className="text-sm font-semibold text-blue-600 tracking-wide hover:text-blue-800 transition-colors duration-150 flex items-center gap-1"
              >
                Orders <i className="fas fa-chevron-right text-xs"></i>
              </AppLink>
              <div className="flex items-center gap-2">
                <span className="text-3xl font-bold">{order?.order_id}</span>
                <ShipmentsStatusBadge status={order?.status} />
              </div>

              {/* Mobile OrderMenu - positioned after order_id line */}
              <div className={`flex justify-start items-center gap-1 md:hidden`}>
                {isPreview && isSheet && (
                  <Button variant="ghost" size="sm" asChild className="h-8">
                    <AppLink href={`/orders/${orderId}`} target="_blank">
                      <i className="fas fa-external-link-alt text-xs"></i>
                    </AppLink>
                  </Button>
                )}
                <OrderMenu order={order as any} isViewing variant="outline" />
              </div>
            </div>

            {/* Desktop OrderMenu - positioned in top-right corner */}
            <div className={`${isSheet ? 'hidden md:flex' : 'hidden md:flex'} items-center gap-1`}>
              {isPreview && (
                <Button variant="ghost" size="sm" asChild className="h-8">
                  <AppLink href={`/orders/${orderId}`} target="_blank">
                    <i className="fas fa-external-link-alt text-xs"></i>
                  </AppLink>
                </Button>
              )}
              <OrderMenu order={order as any} isViewing variant="outline" />
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
                    <div className="text-xs mb-1 font-bold">Order ID</div>
                    <CopiableLink text={order?.id as string} title="Copy ID" variant="outline" />
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Order Number</div>
                    <div className="text-sm font-medium">{order?.order_id}</div>
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Status</div>
                    <ShipmentsStatusBadge status={order?.status} />
                  </div>
                  {!isNone(order?.source) && (
                    <div>
                      <div className="text-xs mb-1 font-bold">Source</div>
                      <div className="text-sm font-medium text-blue-600">{order?.source}</div>
                    </div>
                  )}
                  {(order as any)?.request_id && (
                    <div>
                      <div className="text-xs mb-1 font-bold">Request ID</div>
                      <CopiableLink text={(order as any).request_id} title="Copy Request ID" variant="outline" />
                    </div>
                  )}
                </div>
                <div className="space-y-3">
                  <div>
                    <div className="text-xs mb-1 font-bold">Created At</div>
                    <div className="text-sm font-medium">{formatDateTime(order?.created_at)}</div>
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Last Update</div>
                    <div className="text-sm font-medium">{formatDateTime(order?.updated_at)}</div>
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Line Items</div>
                    <div className="text-sm font-medium">
                      {order?.line_items.reduce((acc, { quantity }) => acc + (quantity || 1), 0)} items
                    </div>
                  </div>
                  <div>
                    <div className="text-xs mb-1 font-bold">Shipments</div>
                    <div className="text-sm font-medium">{(order?.shipments || []).length} shipments</div>
                  </div>
                </div>
              </div>

              {/* Metadata Section - Part of sidebar on desktop only */}
              <div className={isSheet ? "hidden" : "hidden lg:block mt-6"}>
                <h4 className="text-xl font-semibold mb-3">Metadata</h4>
                <EnhancedMetadataEditor
                  value={order?.metadata || {}}
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
            <div className={`space-y-6 order-1 ${isSheet ? '' : 'lg:col-span-3 lg:col-start-1 lg:order-1 lg:mr-5'}`}>
              {/* Order Details section */}
              <div>
                <h2 className="text-xl font-semibold my-4">Order Details</h2>
                <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                <div className="mt-3 mb-6">
                  {/* address and line items section */}
                  <div className={`grid grid-cols-1 ${isSheet ? '' : 'md:grid-cols-2'} gap-6 my-0`}>
                    {/* Shipping Address section */}
                    <div className="text-xs py-1">
                      <p className="text-base font-semibold tracking-wide my-2">SHIP TO</p>
                      <div className="space-y-1">
                        <p className="text-xs my-1 font-semibold">{order?.shipping_to.person_name}</p>
                        <p className="text-xs my-1 font-semibold">{order?.shipping_to.company_name}</p>
                        <p className="text-xs my-1 font-semibold text-blue-600">{order?.shipping_to.email}</p>
                        <p className="text-xs my-1 font-semibold text-blue-600">{order?.shipping_to.phone_number}</p>
                        <p className="text-xs my-1 font-semibold text-gray-600">
                          <span>{order?.shipping_to.address_line1}</span>
                          {!isNone(order?.shipping_to.address_line2) && (
                            <span> {order?.shipping_to.address_line2}</span>
                          )}
                        </p>
                        <p className="text-xs my-1 font-semibold text-gray-600">{formatAddressLocation(order?.shipping_to)}</p>
                      </div>
                    </div>

                    {/* Line Items section */}
                    <div className="text-base py-1">
                      <p className="text-base font-semibold tracking-wide my-2">
                        LINE ITEMS ({order?.line_items.reduce((_, { quantity }) => _ + (quantity || 1), 0)})
                      </p>

                      <div className="py-2 pr-1 max-h-[40rem] overflow-auto">
                        {order?.line_items.map((item, index) => (
                          <React.Fragment key={index + "parcel-info"}>
                            <div className="border-t border-gray-200 mt-1 mb-2"></div>
                            <CommodityDescription commodity={item} />
                          </React.Fragment>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Options section */}
              {Object.values(order?.options as object).length > 0 && (
                <div>
                  <h2 className="text-xl font-semibold my-4">Order Options</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6">
                    <div className="space-y-1">
                      {Object.entries(order?.options).map(
                        ([key, value]: any, index) => (
                          <p key={index + "item-info"} className="text-sm text-gray-600">
                            <span className="font-semibold">
                              {formatRef(key).toLowerCase()}:
                            </span>{" "}
                            <span className="font-bold text-gray-900">{String(value)}</span>
                          </p>
                        ),
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Billing address section */}
              {order?.billing_address && (
                <div>
                  <h2 className="text-xl font-semibold my-4">Billing Address</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6">
                    <AddressDescription address={order?.billing_address} />
                  </div>
                </div>
              )}

              {/* Shipments section */}
              <div>
                <h2 className="text-xl font-semibold my-4">Shipments</h2>
                <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                {(order?.shipments || []).length == 0 && (
                  <p className="text-sm text-gray-600 mt-3">No shipments</p>
                )}

                {(order?.shipments || []).length > 0 && (
                  <>
                    {/* Mobile Card Layout */}
                    <div className="md:hidden space-y-3 mt-3 max-h-80 overflow-auto">
                      {(order?.shipments || []).map((shipment) => (
                        <AppLink
                          key={shipment.id}
                          href={`/shipments/${shipment.id}`}
                          className="block p-3 border rounded-lg hover:bg-gray-50 cursor-pointer"
                        >
                          <div className="flex items-center justify-between mb-2">
                            <ShipmentsStatusBadge status={shipment.status as string} />
                            <span className="text-xs text-gray-500">
                              {formatDateTime(shipment.created_at)}
                            </span>
                          </div>
                          <div className="text-sm font-semibold text-gray-700 truncate">
                            {shipment.id}
                          </div>
                          {shipment.tracking_number && (
                            <div className="text-xs text-gray-500 mt-1">
                              Tracking: {shipment.tracking_number}
                            </div>
                          )}
                        </AppLink>
                      ))}
                    </div>

                    {/* Desktop Table Layout */}
                    <div className="hidden md:block max-h-80 overflow-auto rounded-md border mt-3">
                      <Table>
                        <TableBody>
                          {(order?.shipments || []).map((shipment) => (
                            <TableRow
                              key={shipment.id}
                              className="cursor-pointer hover:bg-gray-50"
                            >
                              <TableCell className="p-0 px-2">
                                <AppLink
                                  href={`/shipments/${shipment.id}`}
                                  className="pr-2"
                                >
                                  <ShipmentsStatusBadge
                                    status={shipment.status as string}
                                  />
                                </AppLink>
                              </TableCell>
                              <TableCell className="p-0 px-2">
                                <AppLink
                                  href={`/shipments/${shipment.id}`}
                                  className="text-xs font-semibold text-gray-600 flex py-2"
                                >
                                  {shipment.id}
                                  {shipment.tracking_number &&
                                    ` - ${shipment.tracking_number}`}
                                </AppLink>
                              </TableCell>
                              <TableCell className="p-0 px-2 text-right">
                                <AppLink
                                  href={`/shipments/${shipment.id}`}
                                  className="text-xs font-semibold text-gray-600 flex justify-end py-2"
                                >
                                  <span>{formatDateTime(shipment.created_at)}</span>
                                </AppLink>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>
                  </>
                )}
              </div>

              {/* Metadata Section - Mobile only, positioned before timeline */}
              <div className={isSheet ? "" : "lg:hidden"}>
                <h2 className="text-xl font-semibold my-4">Metadata</h2>
                <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                <div className="my-4">
                  <EnhancedMetadataEditor
                    value={order?.metadata || {}}
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

          {/* Activity Timeline section - Full Width */}
          <h2 className="text-xl font-semibold my-4">Activity</h2>
          <ActivityTimeline
            logs={logs}
            events={events}
          />
        </div>
      )}

      {query.isFetched && isNone(order) && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm my-6">
          <div className="p-6 text-center">
            <p>Uh Oh!</p>
            <p>{"We couldn't find any order with that reference"}</p>
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

    return (
      <>
        <OrderComponent orderId={id} />
      </>
    );
  };

  return <Component />;
}
