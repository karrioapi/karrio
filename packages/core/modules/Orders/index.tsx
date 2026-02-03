"use client";
import {
  formatAddressLocationShort,
  formatAddressShort,
  formatCarrierSlug,
  formatDateTime,
  formatRef,
  getURLSearchParams,
  isListEqual,
  isNone,
  isNoneOrEmpty,
  preventPropagation,
} from "@karrio/lib";
import {
  OrderPreviewSheet,
  OrderPreviewSheetContext,
} from "@karrio/ui/components/order-preview-sheet";
import { GoogleGeocodingScript } from "@karrio/ui/core/components/google-geocoding-script";
import { useSystemConnections } from "@karrio/hooks/system-connection";
import { useDocumentTemplates } from "@karrio/hooks/document-template";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { useDocumentPrinter } from "@karrio/hooks/resource-token";
import { AddressType, RateType, ShipmentType } from "@karrio/types";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import React, { useContext, useEffect } from "react";
import { ShipmentsStatusBadge } from "@karrio/ui/components/shipments-status-badge";
import { OrdersFilter } from "@karrio/ui/components/orders-filter";
import { OrderMenu } from "@karrio/ui/components/order-menu";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { useSearchParams } from "next/navigation";
import { useOrders } from "@karrio/hooks/order";
import { Button } from "@karrio/ui/components/ui/button";
import { FiltersCard } from "@karrio/ui/components/filters-card";
import { ListPagination } from "@karrio/ui/components/list-pagination";
import { Skeleton } from "@karrio/ui/components/ui/skeleton";
import { StickyTableWrapper } from "@karrio/ui/components/sticky-table-wrapper";
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableRow,
  TableCell
} from "@karrio/ui/components/ui/table";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";


export default function OrdersPage() {
  const Component = (): JSX.Element => {
    const { setLoading } = useLoader();
    const searchParams = useSearchParams();
    const { references } = useAPIMetadata();
    const documentPrinter = useDocumentPrinter();
    const modal = searchParams.get("modal") as string;
    const { previewOrder } = useContext(OrderPreviewSheetContext);
    const [allChecked, setAllChecked] = React.useState(false);
    const [initialized, setInitialized] = React.useState(false);
    const [selection, setSelection] = React.useState<string[]>([]);
    const context = useOrders({
      setVariablesToURL: true,
      preloadNextPage: true,
    });
    const { user_connections } = useCarrierConnections();
    const { system_connections } = useSystemConnections();
    const {
      query: { data: { orders } = {}, ...query },
      filter,
      setFilter,
    } = context;
    const {
      query: { data: { document_templates } = {} },
    } = useDocumentTemplates({
      related_object: "order" as any,
    });

    // Define filter options for the cards
    const getFilterOptions = () => [
      {
        label: "All",
        value: []
      },
      {
        label: "Unfulfilled", 
        value: ["unfulfilled", "partial"]
      },
      {
        label: "Fulfilled",
        value: ["fulfilled", "delivered"]
      },
      {
        label: "Cancelled", 
        value: ["cancelled"]
      }
    ];

    const preventPropagation = (e: React.MouseEvent) => e.stopPropagation();
    const getRate = (shipment: any, default_rate?: any) =>
      default_rate ||
      shipment?.selected_rate ||
      (shipment?.rates || []).find(
        (_: RateType) => _.service === shipment?.options?.preferred_service,
      ) ||
      (shipment?.rates || [])[0] ||
      shipment;
    const getCarrier = (rate?: ShipmentType["rates"][0]) =>
      (user_connections || []).find(
        (_) =>
          _.id === (rate?.meta as any)?.carrier_connection_id ||
          _.carrier_id === rate?.carrier_id,
      ) ||
      (system_connections || []).find(
        (_) =>
          _.id === (rate?.meta as any)?.carrier_connection_id ||
          _.carrier_id === rate?.carrier_id,
      );
    const updatedSelection = (
      selectedOrders: string[],
      current: typeof orders,
    ) => {
      const order_ids = (current?.edges || []).map(
        ({ node: order }) => order.id,
      );
      const selection = selectedOrders.filter((id) => order_ids.includes(id));
      const selected =
        selection.length > 0 && selection.length === (order_ids || []).length;
      setAllChecked(selected);
      if (selectedOrders.filter((id) => !order_ids.includes(id)).length > 0) {
        setSelection(selection);
      }
    };
    const updateFilter = (extra: Partial<any> = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra,
      };

      setFilter(query);
    };
    const handleCheckboxChange = (checked: boolean, name: string) => {
      if (name === "all") {
        setSelection(
          !checked
            ? []
            : (orders?.edges || []).map(({ node: { id } }) => id),
        );
      } else {
        setSelection(
          checked
            ? [...selection, name]
            : selection.filter((id) => id !== name),
        );
      }
    };
    const unfulfilledSelection = (selection: string[]) => {
      return (
        (orders?.edges || []).filter(
          ({ node: order }) =>
            selection.includes(order.id) &&
            !["cancelled", "fulfilled"].includes(order.status),
        ).length === selection.length
      );
    };
    const computeDocFormat = (selection: string[]): string | null => {
      const _order = (orders?.edges || []).find(
        ({ node: order }) => order.id == selection[0],
      );
      return (_order?.node?.shipments || [])[0]?.label_type;
    };
    const compatibleTypeSelection = (selection: string[]) => {
      const format = computeDocFormat(selection);
      return (
        (orders?.edges || []).filter(
          ({ node: order }) =>
            selection.includes(order.id) &&
            !!order.shipments.find(({ label_type }) => label_type === format),
        ).length === selection.length
      );
    };
    const computeOrderService = (order: any) => {
      const shipment =
        order.shipments.find(
          ({ status, tracking_number }: ShipmentType) =>
            !!tracking_number && !["cancelled", "draft"].includes(status),
        ) ||
        order.shipments.find(({ status }: ShipmentType) =>
          ["draft"].includes(status),
        );
      const rate = getRate(shipment);

      if (!shipment) {
        const _shipment =
          order.shipments.find(
            ({ status }: ShipmentType) =>
              !["cancelled", "draft"].includes(status),
          ) ||
          order.shipments.find(
            ({ status }: ShipmentType) => !["draft"].includes(status),
          );
        const _rate = getRate(_shipment);

        return (
          <>
            <CarrierImage
              carrier_name={
                _shipment?.meta?.carrier ||
                _rate?.meta?.rate_provider ||
                _rate?.carrier_name ||
                formatCarrierSlug(references.APP_NAME)
              }
              containerClassName="mt-1 ml-1 mr-2"
              height={28}
              width={28}
              text_color={getCarrier(_rate)?.config?.text_color}
              background={getCarrier(_rate)?.config?.background}
            />
            <div
              className="text-ellipsis"
              style={{ maxWidth: "190px", lineHeight: "15px" }}
            >
              <span className="text-blue-600 font-bold">
                <span>{` - `}</span>
              </span>
              <br />
              <span className="text-ellipsis">
                {!isNone(_rate?.carrier_name) &&
                  formatRef(
                    (_rate.meta?.service_name || _rate.service) as string,
                  )}
                {isNone(_rate?.carrier_name) && "UNFULFILLED"}
              </span>
            </div>
          </>
        );
      }

      return (
        <>
          <CarrierImage
            carrier_name={
              shipment.meta?.carrier ||
              rate.meta?.carrier_name ||
              rate.carrier_name ||
              formatCarrierSlug(references.APP_NAME)
            }
            containerClassName="mt-1 ml-1 mr-2"
            height={28}
            width={28}
            text_color={getCarrier(rate)?.config?.text_color}
            background={getCarrier(rate)?.config?.background}
          />
          <div
            className="text-ellipsis"
            style={{ maxWidth: "190px", lineHeight: "15px" }}
          >
            <span className="text-blue-600 font-bold">
              {!isNone(shipment.carrier_name) && (
                <span>{shipment.tracking_number}</span>
              )}
              {isNone(shipment.carrier_name) && <span>{` - `}</span>}
            </span>
            <br />
            <span className="text-ellipsis">
              {!isNone(rate.carrier_name) &&
                formatRef((rate.meta?.service_name || rate.service) as string)}
              {isNone(rate.carrier_name) && "UNFULFILLED"}
            </span>
          </div>
        </>
      );
    };

    const searchParamsString = searchParams?.toString() ?? "";
    useEffect(() => {
      updateFilter();
    }, [searchParamsString]);
    useEffect(() => {
      setLoading(query.isFetching);
    }, [query.isFetching]);
    useEffect(() => {
      updatedSelection(selection, orders);
    }, [selection, orders]);
    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(modal)) {
        previewOrder(modal as string);
        setInitialized(true);
      }
    }, [modal, query.isFetched]);

    return (
      <>
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between px-0 pb-0 pt-4 mb-2">
          <div className="mb-4 sm:mb-0">
            <h1 className="text-2xl font-semibold text-gray-900">Orders</h1>
          </div>
          <div className="flex flex-row items-center gap-1 flex-wrap">
            <Button asChild size="sm" className="mx-1 w-auto">
              <AppLink href="/draft_orders/new">
                Draft order
              </AppLink>
            </Button>
            <Button asChild size="sm" className="mx-1 w-auto">
              <AppLink href="/manifests">
                Manage manifests
              </AppLink>
            </Button>
            <OrdersFilter context={context} />
          </div>
        </header>

        <FiltersCard
          filters={getFilterOptions()}
          activeFilter={filter?.status || []}
          onFilterChange={(status) => updateFilter({ status, source: null, offset: 0 })}
        />

        {!query.isFetched && (
          <div className="bg-white rounded-lg shadow-sm border my-6 p-6">
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="flex items-center space-x-4">
                  <Skeleton className="h-4 w-4" />
                  <Skeleton className="h-4 w-[100px]" />
                  <Skeleton className="h-4 w-[80px]" />
                  <Skeleton className="h-4 w-[120px]" />
                  <Skeleton className="h-4 w-[100px]" />
                  <Skeleton className="h-4 w-[80px]" />
                  <Skeleton className="h-4 w-6" />
                </div>
              ))}
            </div>
          </div>
        )}

        {query.isFetched && (orders?.edges || []).length > 0 && (
          <>
            <StickyTableWrapper>
              <Table className="orders-table">
              <TableHeader>
                <TableRow>
                  <TableHead
                    className="selector text-center p-0 items-center sticky-left"
                    onClick={preventPropagation}
                  >
                    <div className="py-2 pl-2 pr-4">
                      <Checkbox
                        checked={allChecked}
                        onCheckedChange={(checked) => handleCheckboxChange(checked as boolean, "all")}
                      />
                    </div>
                  </TableHead>

                  {selection.length > 0 && (
                    <TableHead className="p-2" colSpan={6}>
                      <div className="flex items-center gap-2 flex-wrap">
                        <Button
                          variant="outline"
                          size="sm"
                          disabled={!compatibleTypeSelection(selection) || documentPrinter.isLoading}
                          className={`px-3 ${!compatibleTypeSelection(selection) ? 'opacity-40 pointer-events-none' : ''}`}
                          onClick={() => documentPrinter.openOrderLabels(selection, { format: (computeDocFormat(selection) || "pdf")?.toLowerCase() as any })}
                        >
                          Print Labels
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          className="px-3"
                          disabled={documentPrinter.isLoading}
                          onClick={() => documentPrinter.openOrderLabels(selection, { doc: "invoice" })}
                        >
                          Print Invoices
                        </Button>
                        {(document_templates?.edges || []).map(
                          ({ node: template }) => (
                            <Button
                              key={template.id}
                              variant="outline"
                              size="sm"
                              className="px-3"
                              disabled={documentPrinter.isLoading}
                              onClick={() => documentPrinter.openTemplate(template.id, { orders: selection.join(",") })}
                            >
                              Print {template.name}
                            </Button>
                          ),
                        )}
                      </div>
                    </TableHead>
                  )}

                  {selection.length === 0 && (
                    <>
                      <TableHead className="order text-xs items-center">
                        ORDER #
                      </TableHead>
                      <TableHead className="status items-center"></TableHead>
                      <TableHead className="line-items text-xs items-center">
                        ITEMS
                      </TableHead>
                      <TableHead className="customer text-xs items-center">
                        SHIP TO
                      </TableHead>
                      <TableHead className="total text-xs items-center">TOTAL</TableHead>
                      <TableHead className="date text-xs items-center">DATE</TableHead>
                      <TableHead className="service text-xs items-center">
                        SHIPPING SERVICE
                      </TableHead>
                      <TableHead className="action sticky-right"></TableHead>
                    </>
                  )}
                </TableRow>
              </TableHeader>
              <TableBody>
                {(orders?.edges || []).map(({ node: order }) => (
                  <TableRow 
                    key={order.id} 
                    className={`items cursor-pointer transition-colors duration-150 ease-in-out ${
                      selection.includes(order.id) 
                        ? 'bg-blue-50 hover:bg-blue-100' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <TableCell className="selector text-center items-center p-0 sticky-left">
                      <div className="py-2 pl-2 pr-4">
                        <Checkbox
                          checked={selection.includes(order.id)}
                          onCheckedChange={(checked) => handleCheckboxChange(checked as boolean, order.id)}
                        />
                      </div>
                    </TableCell>
                    <TableCell
                      className="order text-xs items-center relative"
                      onClick={() => previewOrder(order.id)}
                    >
                      <div className="py-1 px-2">
                        <p className="text-xs font-bold text-gray-700 text-ellipsis">
                          {order.order_id}
                        </p>
                        <p className="text-xs text-gray-600 lowercase text-ellipsis">
                          {order.source}
                        </p>
                      </div>
                    </TableCell>
                    <TableCell
                      className="status items-center"
                      onClick={() => previewOrder(order.id)}
                    >
                      <div style={{ paddingLeft: '7px', paddingRight: '7px' }}>
                        <ShipmentsStatusBadge
                          status={order.status as string}
                          className="w-full justify-center text-center"
                        />
                      </div>
                    </TableCell>
                    <TableCell
                      className="line-items text-xs items-center relative"
                      onClick={() => previewOrder(order.id)}
                    >
                      <div className="py-1 px-2">
                        <p className="text-xs font-bold text-gray-600 text-ellipsis">
                          {((items: number): any =>
                            `${items} item${items === 1 ? "" : "s"}`)(
                              order.line_items.reduce(
                                (acc, item) =>
                                  acc + (item.quantity as number) || 1,
                                0,
                              ),
                            )}
                        </p>
                        <p className="text-xs text-gray-600 text-ellipsis">
                          {order.line_items.length > 1
                            ? "(Multiple)"
                            : order.line_items[0].title ||
                            order.line_items[0].description ||
                            order.line_items[0].sku}
                        </p>
                      </div>
                    </TableCell>
                    <TableCell
                      className="customer text-xs items-center font-bold text-gray-600 relative"
                      onClick={() => previewOrder(order.id)}
                    >
                      <div className="py-1 px-2">
                        <p
                          className="text-ellipsis"
                          title={formatAddressShort(
                            order.shipping_to as AddressType,
                          )}
                        >
                          {formatAddressShort(
                            order.shipping_to as AddressType,
                          )}
                        </p>
                        <p className="font-medium">
                          {formatAddressLocationShort(
                            order.shipping_to as AddressType,
                          )}
                        </p>
                      </div>
                    </TableCell>
                      <TableCell
                        className="total items-center px-1 cursor-pointer"
                        onClick={() => previewOrder(order.id)}
                      >
                        <p className="text-xs font-semibold text-gray-600">
                          {order.line_items.reduce(
                            (acc, item) =>
                              acc +
                              (item.quantity as number) *
                              (item.value_amount as number),
                            0,
                          )}
                          {` `}
                          {order.options.currency ||
                            order.line_items[0].value_currency}
                        </p>
                      </TableCell>
                      <TableCell
                        className="date items-center px-1 cursor-pointer"
                        onClick={() => previewOrder(order.id)}
                      >
                        <p className="text-xs font-semibold text-gray-600">
                          {formatDateTime(order.created_at)}
                        </p>
                      </TableCell>
                      <TableCell className="service items-center py-1 px-0 text-xs font-bold text-gray-600">
                        <div className="flex items-center">
                          {computeOrderService(order)}
                        </div>
                      </TableCell>
                      <TableCell className="action items-center px-0 sticky-right">
                        <OrderMenu
                          order={order as any}
                          className="w-full"
                        />
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
                totalCount={orders?.page_info?.count || 0}
                hasNextPage={orders?.page_info?.has_next_page || false}
                onPageChange={(offset) => updateFilter({ offset })}
                className="px-2 py-3"
              />
            </div>
          </>
        )}

        {query.isFetched && (orders?.edges || []).length == 0 && (
          <div className="bg-white rounded-lg shadow-sm border my-6">
            <div className="p-6 text-center">
              <p>No order found.</p>
            </div>
          </div>
        )}
      </>
    );
  };

  return (
    <>
      <GoogleGeocodingScript />
      <OrderPreviewSheet>
        <Component />
      </OrderPreviewSheet>
    </>
  );
}
