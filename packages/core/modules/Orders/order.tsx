"use client";
import {
  MetadataEditor,
  MetadataEditorContext,
} from "@karrio/ui/core/forms/metadata-editor";
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
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { MetadataObjectTypeEnum } from "@karrio/types";
import { useEvents } from "@karrio/hooks/event";
import { useOrder } from "@karrio/hooks/order";
import { useLogs } from "@karrio/hooks/log";
import { Table, TableHeader, TableBody, TableHead, TableRow, TableCell } from "@karrio/ui/components/ui/table";
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
  const { setLoading } = useLoader();
  const entity_id = orderId;
  const { query: logs } = useLogs({ entity_id });
  const { query: events } = useEvents({ entity_id });
  const {
    query: { data: { order } = {}, ...query },
  } = useOrder(entity_id);

  React.useEffect(() => {
    setLoading(query.isFetching);
  }, [query.isFetching]);

  return (
    <>
      {!query.isFetched && query.isFetching && <Spinner />}

      {order && (
        <>
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
                <OrderMenu order={order as any} isViewing />
              </div>
            </div>

            {/* Desktop OrderMenu - positioned in top-right corner */}
            <div className={`${isSheet ? 'hidden md:flex' : 'hidden md:flex'} items-center gap-1`}>
              <CopiableLink text={order?.id as string} title="Copy ID" variant="outline" />
              {isPreview && (
                <Button variant="ghost" size="sm" asChild className="h-8">
                  <AppLink href={`/orders/${orderId}`} target="_blank">
                    <i className="fas fa-external-link-alt text-xs"></i>
                  </AppLink>
                </Button>
              )}
              <OrderMenu order={order as any} isViewing />
            </div>
          </div>

          {/* Reference and highlights section */}
          <hr className="mt-1 mb-2" style={{ height: "1px" }} />

          <div className="columns mb-4">
            <div className="p-4 mr-4">
              <span className="subtitle is-size-7 my-4">Date</span>
              <br />
              <span className="subtitle is-size-7 mt-1 has-text-weight-semibold">
                {formatDateTime(order?.created_at)}
              </span>
            </div>

            {!isNone(order?.source) && (
              <>
                <div
                  className="my-2"
                  style={{ width: "1px", backgroundColor: "#ddd" }}
                ></div>
                <div className="p-4 mr-4">
                  <span className="subtitle is-size-7 my-4">Source</span>
                  <br />
                  <span className="subtitle is-size-7 has-text-weight-semibold">
                    {order?.source}
                  </span>
                </div>
              </>
            )}
          </div>

          <h2 className="title is-5 my-5">Order Details</h2>
          <hr className="mt-1 mb-2" style={{ height: "1px" }} />

          <div className="mt-3 mb-6">
            {/* address and line items section */}
            <div className="columns my-0 is-multiline">
              {/* Shipping Address section */}
              <div className="column is-6 is-size-6 py-1">
                <p className="is-title is-size-6 my-2 has-text-weight-semibold">
                  ADDRESS
                </p>

                <p className="is-size-6 my-1">
                  {order?.shipping_to.person_name}
                </p>
                <p className="is-size-6 my-1">
                  {order?.shipping_to.company_name}
                </p>
                <p className="is-size-6 my-1 has-text-info">
                  {order?.shipping_to.email}
                </p>
                <p className="is-size-6 my-1 has-text-info">
                  {order?.shipping_to.phone_number}
                </p>
                <p className="is-size-6 my-1">
                  <span>{order?.shipping_to.address_line1}</span>
                  {!isNone(order?.shipping_to.address_line2) && (
                    <span>{order?.shipping_to.address_line2}</span>
                  )}
                </p>
                <p className="is-size-6 my-1">
                  {formatAddressLocation(order?.shipping_to)}
                </p>
              </div>

              {/* Line Items section */}
              <div className="column is-6 is-size-6 py-1">
                <p className="is-title is-size-6 my-2 has-text-weight-semibold">
                  LINE ITEMS (
                  {order?.line_items.reduce(
                    (_, { quantity }) => _ + (quantity || 1),
                    0,
                  )}
                  )
                </p>

                <div
                  className="menu-list py-2 pr-1"
                  style={{ maxHeight: "40em", overflow: "auto" }}
                >
                  {order?.line_items.map((item, index) => (
                    <React.Fragment key={index + "parcel-info"}>
                      <hr className="mt-1 mb-2" style={{ height: "1px" }} />
                      <CommodityDescription commodity={item} />
                    </React.Fragment>
                  ))}
                </div>
              </div>
            </div>

            {/* Options section */}
            <div className="columns mt-6 mb-0 is-multiline">
              {Object.values(order?.options as object).length > 0 && (
                <div className="column is-6 is-size-6 py-1">
                  <p className="is-title is-size-6 my-2 has-text-weight-semibold">
                    ORDER OPTIONS
                  </p>

                  {Object.entries(order?.options).map(
                    ([key, value]: any, index) => (
                      <React.Fragment key={index + "item-info"}>
                        <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                          <span>
                            {formatRef(key).toLowerCase()}:{" "}
                            <strong>{String(value)}</strong>
                          </span>
                        </p>
                      </React.Fragment>
                    ),
                  )}
                </div>
              )}
            </div>

            {/* Billing address section */}
            <div className="columns mt-6 mb-0 is-multiline">
              {order?.billing_address && (
                <div className="column is-6 is-size-6 py-1">
                  <p className="is-title is-size-6 my-2 has-text-weight-semibold">
                    BILL TO
                  </p>

                  <AddressDescription address={order?.billing_address} />
                </div>
              )}
            </div>
          </div>

          {/* Metadata section */}
          <MetadataEditor
            id={order?.id}
            object_type={MetadataObjectTypeEnum.order}
            metadata={order?.metadata}
          >
            {/* @ts-ignore */}
            <MetadataEditorContext.Consumer>
              {({ isEditing, editMetadata }) => (
                <>
                  <div className="is-flex is-justify-content-space-between">
                    <h2 className="title is-5 my-4">Metadata</h2>

                    <button
                      type="button"
                      className="button is-default is-small is-align-self-center"
                      disabled={isEditing}
                      onClick={() => editMetadata()}
                    >
                      <span className="icon is-small">
                        <i className="fas fa-pen"></i>
                      </span>
                      <span>Edit metadata</span>
                    </button>
                  </div>

                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />
                </>
              )}
            </MetadataEditorContext.Consumer>
          </MetadataEditor>

          <div className="my-6 pt-1"></div>

          {/* Shipments section */}
          <h2 className="title is-5 my-4">Shipments</h2>

          {(order?.shipments || []).length == 0 && <div>No shipments</div>}

          {(order?.shipments || []).length > 0 && (
            <div
              className="table-container"
              style={{ maxHeight: "20em", overflow: "auto" }}
            >
              <table className="related-item-table table is-hoverable is-fullwidth">
                <tbody>
                  {(order?.shipments || []).map((shipment) => (
                    <tr key={shipment.id} className="items is-clickable">
                      <td className="status is-vcentered p-0 px-2">
                        <AppLink
                          href={`/shipments/${shipment.id}`}
                          className="pr-2"
                        >
                          <ShipmentsStatusBadge
                            status={shipment.status as string}
                          />
                        </AppLink>
                      </td>
                      <td className="description is-vcentered p-0 px-2">
                        <AppLink
                          href={`/shipments/${shipment.id}`}
                          className="is-size-7 has-text-weight-semibold has-text-grey is-flex py-2"
                        >
                          {shipment.id}
                          {shipment.tracking_number &&
                            ` - ${shipment.tracking_number}`}
                        </AppLink>
                      </td>
                      <td className="date is-vcentered p-0 px-2">
                        <AppLink
                          href={`/shipments/${shipment.id}`}
                          className="is-size-7 has-text-weight-semibold has-text-grey is-flex is-justify-content-right py-2"
                        >
                          <span>{formatDateTime(shipment.created_at)}</span>
                        </AppLink>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <div className="my-6 pt-1"></div>

          {/* Activity Timeline section */}
          <h2 className="title is-5 my-4">Activity</h2>

          <ActivityTimeline
            logs={logs}
            events={events}
          />
        </>
      )}

      {query.isFetched && isNone(order) && (
        <div className="card my-6">
          <div className="card-content has-text-centered">
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
