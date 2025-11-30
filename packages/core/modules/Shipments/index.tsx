"use client";
import {
  formatAddressShort,
  formatAddressLocationShort,
  formatDateTime,
  formatRef,
  getURLSearchParams,
  isNone,
  isNoneOrEmpty,
  formatCarrierSlug,
  preventPropagation,
} from "@karrio/lib";
import {
  ShipmentPreviewSheet,
  ShipmentPreviewSheetContext,
} from "@karrio/ui/components/shipment-preview-sheet";
import { useSystemConnections } from "@karrio/hooks/system-connection";
import { useDocumentTemplates } from "@karrio/hooks/document-template";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { useDocumentPrinter, FormatType } from "@karrio/hooks/resource-token";
import { ShipmentsFilter } from "@karrio/ui/components/shipments-filter";
import { AddressType, RateType, ShipmentType } from "@karrio/types";
import { ShipmentMenu } from "@karrio/ui/components/shipment-menu";
import { FiltersCard } from "@karrio/ui/components/filters-card";
import { ListPagination } from "@karrio/ui/components/list-pagination";
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
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Skeleton } from "@karrio/ui/components/ui/skeleton";
import { Loader2 } from "lucide-react";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { ShipmentsStatusBadge } from "@karrio/ui/components/shipments-status-badge";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { useShipments } from "@karrio/hooks/shipment";
import React, { useContext, useEffect } from "react";
import { useSearchParams } from "next/navigation";


export default function Page(pageProps: any) {
  const Component = (): JSX.Element => {
    const searchParams = useSearchParams();
    const { setLoading } = useLoader();
    const { references } = useAPIMetadata();
    const [allChecked, setAllChecked] = React.useState(false);
    const [initialized, setInitialized] = React.useState(false);
    const [selection, setSelection] = React.useState<string[]>([]);
    const { previewShipment } = useContext(ShipmentPreviewSheetContext);
    const { user_connections } = useCarrierConnections();
    const { system_connections } = useSystemConnections();
    const documentPrinter = useDocumentPrinter();
    const context = useShipments({
      status: [
        "purchased",
        "delivered",
        "in_transit",
        "cancelled",
        "needs_attention",
        "out_for_delivery",
        "delivery_failed",
      ] as any,
      setVariablesToURL: true,
      preloadNextPage: true,
    });
    const {
      query: { data: { shipments } = {}, ...query },
      filter,
      setFilter,
    } = context;
    const {
      query: { data: { document_templates } = {} },
    } = useDocumentTemplates({
      related_object: "shipment" as any,
      active: true,
    });

    const updateFilter = (extra: Partial<any> = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra,
      };

      setFilter(query);
    };
    const updatedSelection = (
      selectedShipments: string[],
      current: typeof shipments,
    ) => {
      const shipment_ids = (current?.edges || []).map(
        ({ node: shipment }) => shipment.id,
      );
      const selection = selectedShipments.filter((id) =>
        shipment_ids.includes(id),
      );
      const selected =
        selection.length > 0 &&
        selection.length === (shipment_ids || []).length;
      setAllChecked(selected);
      if (
        selectedShipments.filter((id) => !shipment_ids.includes(id)).length > 0
      ) {
        setSelection(selection);
      }
    };
    const handleCheckboxChange = (checked: boolean, name: string) => {
      if (name === "all") {
        setSelection(
          !checked
            ? []
            : (shipments?.edges || []).map(({ node: { id } }) => id),
        );
      } else {
        setSelection(
          checked
            ? [...selection, name]
            : selection.filter((id) => id !== name),
        );
      }
    };
    const computeDocFormat = (selection: string[]) => {
      const _shipment = (shipments?.edges || []).find(
        ({ node: shipment }) => shipment.id == selection[0],
      );
      return (_shipment?.node || {}).label_type;
    };
    const compatibleTypeSelection = (selection: string[]) => {
      const format = computeDocFormat(selection);
      return (
        (shipments?.edges || []).filter(
          ({ node: shipment }) =>
            selection.includes(shipment.id) && shipment.label_type == format,
        ).length === selection.length
      );
    };
    const draftSelection = (selection: string[]) => {
      return (
        (shipments?.edges || []).filter(
          ({ node: shipment }) =>
            selection.includes(shipment.id) && shipment.status == "draft",
        ).length === selection.length
      );
    };
    const getRate = (shipment: any) =>
      shipment.selected_rate ||
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
    
    // Define filter options for the cards
    const getFilterOptions = () => [
      {
        label: "All",
        value: ["purchased", "delivered", "in_transit", "cancelled", "needs_attention", "out_for_delivery", "delivery_failed"]
      },
      {
        label: "Purchased", 
        value: ["purchased", "in_transit", "out_for_delivery"]
      },
      {
        label: "Delivered",
        value: ["delivered"]
      },
      {
        label: "Exception",
        value: ["needs_attention", "delivery_failed"]
      },
      {
        label: "Cancelled", 
        value: ["cancelled"]
      },
      {
        label: "Draft",
        value: ["draft"]
      }
    ];

    useEffect(() => {
      updateFilter();
    }, [searchParams]);
    useEffect(() => {
      setLoading(query.isFetching);
    }, [query.isFetching]);
    useEffect(() => {
      updatedSelection(selection, shipments);
    }, [selection, shipments]);
    useEffect(() => {
      if (
        query.isFetched &&
        !initialized &&
        !isNoneOrEmpty(searchParams.get("modal"))
      ) {
        previewShipment(searchParams.get("modal") as string);
        setInitialized(true);
      }
    }, [searchParams.get("modal"), query.isFetched]);

    return (
      <>
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between px-0 pb-0 pt-4 mb-2">
          <div className="mb-4 sm:mb-0">
            <h1 className="text-2xl font-semibold text-gray-900">Shipments</h1>
          </div>
          <div className="flex flex-row items-center gap-1 flex-wrap">
            <Button asChild size="sm" className="mx-1 w-auto">
              <AppLink href="/create_label?shipment_id=new">
                Create Label
              </AppLink>
            </Button>
            <Button asChild size="sm" className="mx-1 w-auto">
              <AppLink href="/manifests/create_manifests">
                Manage manifests
              </AppLink>
            </Button>
            <ShipmentsFilter context={context} />
          </div>
        </header>

        <FiltersCard
          filters={getFilterOptions()}
          activeFilter={filter?.status || []}
          onFilterChange={(status) => updateFilter({ status, offset: 0 })}
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

        {query.isFetched && (shipments?.edges || []).length > 0 && (
          <>
            <StickyTableWrapper>
              <Table className="shipments-table">
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
                          className="px-3"
                          onClick={() => documentPrinter.openBatchLabels(
                            selection,
                            { format: (computeDocFormat(selection) || "pdf")?.toLowerCase() as FormatType, doc: "label" }
                          )}
                        >
                          {documentPrinter.isLoading && <Loader2 className="h-3 w-3 mr-1 animate-spin" />}
                          Print Labels
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          disabled={documentPrinter.isLoading}
                          className="px-3"
                          onClick={() => documentPrinter.openBatchLabels(
                            selection,
                            { format: "pdf", doc: "invoice" }
                          )}
                        >
                          {documentPrinter.isLoading && <Loader2 className="h-3 w-3 mr-1 animate-spin" />}
                          Print Invoices
                        </Button>
                        {(document_templates?.edges || []).map(
                          ({ node: template }) => (
                            <Button
                              key={template.id}
                              variant="outline"
                              size="sm"
                              disabled={documentPrinter.isLoading}
                              className="px-3"
                              onClick={() => documentPrinter.openTemplate(
                                template.id,
                                { shipments: selection.join(",") }
                              )}
                            >
                              {documentPrinter.isLoading && <Loader2 className="h-3 w-3 mr-1 animate-spin" />}
                              Print {template.name}
                            </Button>
                          ),
                        )}
                      </div>
                    </TableHead>
                  )}

                  {selection.length === 0 && (
                    <>
                      <TableHead className="service text-xs items-center">
                        SHIPPING SERVICE
                      </TableHead>
                      <TableHead className="status items-center"></TableHead>
                      <TableHead className="recipient text-xs items-center">
                        RECIPIENT
                      </TableHead>
                      <TableHead className="reference text-xs items-center">
                        REFERENCE
                      </TableHead>
                      <TableHead className="date text-xs items-center">DATE</TableHead>
                      <TableHead className="action sticky-right"></TableHead>
                    </>
                  )}
                </TableRow>
              </TableHeader>
              <TableBody>
                {(shipments?.edges || []).map(({ node: shipment }) => (
                  <TableRow 
                    key={shipment.id} 
                    className={`items cursor-pointer transition-colors duration-150 ease-in-out ${
                      selection.includes(shipment.id) 
                        ? 'bg-blue-50 hover:bg-blue-100' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <TableCell className="selector text-center items-center p-0 sticky-left">
                      <div className="py-3 pl-2 pr-4">
                        <Checkbox
                          checked={selection.includes(shipment.id)}
                          onCheckedChange={(checked) => handleCheckboxChange(checked as boolean, shipment.id)}
                        />
                      </div>
                    </TableCell>
                    <TableCell
                      className="service items-center py-1 px-0 text-xs font-bold text-gray-600"
                      onClick={() => previewShipment(shipment.id)}
                      title={
                        isNone(getRate(shipment))
                          ? "UNFULFILLED"
                          : formatRef(
                            ((shipment.meta as any)?.service_name ||
                              getRate(shipment).service) as string,
                          )
                      }
                    >
                        <div className="flex items-center">
                          <CarrierImage
                            carrier_name={
                              shipment.meta?.custom_carrier_name ||
                              shipment.meta?.carrier ||
                              getRate(shipment).meta?.rate_provider ||
                              getRate(shipment).carrier_name ||
                              formatCarrierSlug(references.APP_NAME)
                            }
                            containerClassName="mt-1 ml-1 mr-2"
                            height={28}
                            width={28}
                            text_color={
                              (
                                shipment.selected_rate_carrier ||
                                getCarrier(getRate(shipment))
                              )?.config?.text_color
                            }
                            background={
                              (
                                shipment.selected_rate_carrier ||
                                getCarrier(getRate(shipment))
                              )?.config?.brand_color
                            }
                          />
                          <div
                            className="text-ellipsis"
                            style={{ maxWidth: "190px", lineHeight: "16px" }}
                          >
                            <span className="text-blue-600 font-bold">
                              {!isNone(shipment.tracking_number) && (
                                <span>{shipment.tracking_number}</span>
                              )}
                              {isNone(shipment.tracking_number) && (
                                <span> - </span>
                              )}
                            </span>
                            <br />
                            <span className="text-ellipsis">
                              {!isNone(getRate(shipment).carrier_name) &&
                                formatRef(
                                  ((getRate(shipment).meta as any)
                                    ?.service_name ||
                                    getRate(shipment).service) as string,
                                )}
                              {isNone(getRate(shipment).carrier_name) &&
                                "UNFULFILLED"}
                            </span>
                          </div>
                        </div>
                    </TableCell>
                    <TableCell
                      className="status items-center"
                      onClick={() => previewShipment(shipment.id)}
                    >
                      <div style={{ paddingLeft: '7px', paddingRight: '7px' }}>
                        <ShipmentsStatusBadge
                          status={shipment.status as string}
                          className="w-full justify-center text-center"
                        />
                      </div>
                    </TableCell>
                    <TableCell
                      className="recipient items-center text-xs font-bold text-gray-600 relative"
                      onClick={() => previewShipment(shipment.id)}
                    >
                        <div
                          className="p-2"
                          style={{
                            position: "absolute",
                            maxWidth: "100%",
                            top: 0,
                            left: 0,
                          }}
                        >
                          <p
                            className="text-ellipsis"
                            title={formatAddressShort(
                              shipment.recipient as AddressType,
                            )}
                          >
                            {formatAddressShort(
                              shipment.recipient as AddressType,
                            )}
                          </p>
                          <p className="font-medium">
                            {formatAddressLocationShort(
                              shipment.recipient as AddressType,
                            )}
                          </p>
                        </div>
                    </TableCell>
                    <TableCell
                      className="reference items-center text-xs font-bold text-gray-600 text-ellipsis"
                      onClick={() => previewShipment(shipment.id)}
                    >
                      <span>{shipment.reference || ""}</span>
                    </TableCell>
                    <TableCell
                      className="date items-center px-1"
                      onClick={() => previewShipment(shipment.id)}
                    >
                      <p className="text-xs font-semibold text-gray-600">
                        {formatDateTime(shipment.created_at)}
                      </p>
                    </TableCell>
                    <TableCell className="action items-center px-0 sticky-right">
                      <ShipmentMenu
                        shipment={shipment as any}
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
                totalCount={shipments?.page_info?.count || 0}
                hasNextPage={shipments?.page_info?.has_next_page || false}
                onPageChange={(offset) => updateFilter({ offset })}
                className="px-2 py-3"
              />
            </div>
          </>
        )}

        {query.isFetched && (shipments?.edges || []).length == 0 && (
          <div className="bg-white rounded-lg shadow-sm border my-6">
            <div className="p-6 text-center">
              <p>No shipment found.</p>
            </div>
          </div>
        )}
      </>
    );
  };

  return (
    <ShipmentPreviewSheet>
      <Component />
    </ShipmentPreviewSheet>
  );
}
