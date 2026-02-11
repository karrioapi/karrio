"use client";
import { EnhancedMetadataEditor } from "@karrio/ui/components/enhanced-metadata-editor";
import { useMetadataMutation } from "@karrio/hooks/metadata";
import {
  useUploadRecordMutation,
  useUploadRecords,
} from "@karrio/hooks/upload-record";
import { CustomsType, NotificationType, ParcelType, MetadataObjectTypeEnum } from "@karrio/types";
import { CustomsInfoDescription } from "@karrio/ui/components/customs-info-description";
import { ShipmentsStatusBadge } from "@karrio/ui/components/shipments-status-badge";
import { CommodityDescription } from "@karrio/ui/components/commodity-description";
import { AddressDescription } from "@karrio/ui/components/address-description";
import { ParcelDescription } from "@karrio/ui/components/parcel-description";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";
import { useShipment, useShipmentMutation } from "@karrio/hooks/shipment";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { RecentActivity } from "@karrio/ui/components/recent-activity";
import { CopiableLink } from "@karrio/ui/components/copiable-link";
import { ShipmentMenu } from "@karrio/ui/components/shipment-menu";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { formatDateTime, formatRef, isNone } from "@karrio/lib";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { DocumentUploadData } from "@karrio/types/rest/api";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Button } from "@karrio/ui/components/ui/button";
import { Spinner } from "@karrio/ui/components/spinner";
import { useEvents } from "@karrio/hooks/event";
import { useLogs } from "@karrio/hooks/log";
import React from "react";

type FileDataType = DocumentUploadData["document_files"][0];

export const ShipmentComponent = ({
  shipmentId,
  isPreview,
  isSheet,
}: {
  shipmentId: string;
  isPreview?: boolean;
  isSheet?: boolean;
}): JSX.Element => {
  const notifier = useNotifier();
  const { setLoading } = useLoader();
  const $fileInput = React.useRef<HTMLInputElement>(null);
  const [selectValue, setSelectValue] = React.useState<string>("other");
  const {
    references: { carrier_capabilities = {} },
  } = useAPIMetadata();
  const entity_id = shipmentId;
  const { query: logs } = useLogs({ entity_id });
  const { query: events } = useEvents({ entity_id });
  const {
    query: { data: { shipment } = {}, ...query },
  } = useShipment(entity_id);
  const { uploadDocument } = useUploadRecordMutation();
  const { updateShipment } = useShipmentMutation(entity_id);
  const { updateMetadata } = useMetadataMutation([
    "shipments",
    entity_id,
  ]);
  const {
    query: { data: { results: uploads } = {}, ...documents },
  } = useUploadRecords({ shipmentId: entity_id });
  const [fileData, setFileData] = React.useState<FileDataType>(
    {} as FileDataType,
  );

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    try {
      if (!!e.target.files && !!e.target.files[0]) {
        let file = e.target.files[0];
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
          let sections = (reader.result as string).split(",");
          let doc_file = sections[sections.length - 1];
          let doc_name = file.name;
          setFileData({ ...fileData, doc_name, doc_file });
        };
      } else {
        setFileData({ doc_file: fileData.doc_file } as FileDataType);
      }
    } catch (_) {
      setFileData({ doc_file: fileData.doc_file } as FileDataType);
    }
  };
  const uploadCustomsDocument = async () => {
    try {
      await uploadDocument.mutateAsync({
        shipment_id: entity_id,
        document_files: [fileData],
      });
      notifier.notify({
        type: NotificationType.success,
        message: `document updloaded successfully`,
      });
      if (!!$fileInput.current) $fileInput.current.value = "";
      setSelectValue("other");
    } catch (message: any) {
      notifier.notify({ type: NotificationType.error, message });
    }
  };

  const handleMetadataChange = async (newMetadata: any) => {
    try {
      const currentMetadata = shipment?.metadata || {};

      // Calculate added_values (new or changed metadata)
      const added_values = { ...newMetadata };

      // Calculate discarded_keys (keys that were removed)
      const discarded_keys = Object.keys(currentMetadata).filter(
        key => !(key in newMetadata)
      );

      await updateMetadata.mutateAsync({
        id: entity_id,
        object_type: MetadataObjectTypeEnum.shipment,
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

      {shipment && (
        <div className="space-y-4">
          {/* Header Section - Full Width */}
          <div className="flex justify-between items-start gap-4">
            <div className="space-y-2 flex-1">
              <AppLink
                href="/shipments"
                className="text-sm font-semibold text-blue-600 tracking-wide hover:text-blue-800 transition-colors duration-150 flex items-center gap-1"
              >
                Shipments <i className="fas fa-chevron-right text-xs"></i>
              </AppLink>
              <div className="flex items-center gap-2">
                <div className="flex items-baseline gap-1">
                  <span className="text-3xl font-bold">
                    {shipment.selected_rate?.total_charge !== undefined && shipment.selected_rate?.total_charge !== null
                      ? Number(shipment.selected_rate.total_charge).toFixed(2)
                      : (shipment.status === "purchased" ? "0.00"
                        : shipment.status === "draft" ? "DRAFT"
                          : "UNFULFILLED")}
                  </span>
                  {shipment.selected_rate?.currency && (
                    <span className="text-3xl text-gray-600">
                      {shipment.selected_rate?.currency}
                    </span>
                  )}
                </div>
                <ShipmentsStatusBadge status={shipment.status} />
              </div>

              {/* Mobile ShipmentMenu - positioned after cost/currency line */}
              <div className={`flex justify-start items-center gap-1 md:hidden`}>
                {isPreview && isSheet && (
                  <Button
                    variant="ghost"
                    size="sm"
                    asChild
                    className="h-8"
                  >
                    <AppLink
                      href={`/shipments/${shipmentId}`}
                      target="_blank"
                    >
                      <i className="fas fa-external-link-alt text-xs"></i>
                    </AppLink>
                  </Button>
                )}
                <ShipmentMenu shipment={shipment as any} isViewing variant="outline" />
              </div>
            </div>

            {/* Desktop ShipmentMenu - positioned in top-right corner */}
            <div className={`${isSheet ? 'hidden md:flex' : 'hidden md:flex'} items-center gap-1`}>
              {isPreview && (
                <Button
                  variant="ghost"
                  size="sm"
                  asChild
                  className="h-8"
                >
                  <AppLink
                    href={`/shipments/${shipmentId}`}
                    target="_blank"
                  >
                    <i className="fas fa-external-link-alt text-xs"></i>
                  </AppLink>
                </Button>
              )}
              <ShipmentMenu shipment={shipment as any} isViewing variant="outline" />
            </div>
          </div>


          {/* Main Content with Sidebar Layout */}
          <div className={`flex flex-col ${isSheet ? '' : 'lg:grid lg:grid-cols-4'} gap-6`}>
            {/* Right Sidebar - Details Section */}
            {!isNone(shipment.selected_rate) && (
              <div className={isSheet ? '' : 'lg:order-2 lg:col-span-1 lg:col-start-4'}>
                <h3 className={`text-xl font-semibold my-4 ${isSheet ? '' : 'lg:mb-4 lg:mt-0'}`}>
                  Details
                </h3>
                <div className={isSheet ? 'grid grid-cols-1 md:grid-cols-2 gap-4' : 'space-y-3'}>
                  <div className="space-y-3">
                    <div>
                      <div className="text-xs mb-1 font-bold">Shipment ID</div>
                      <CopiableLink text={shipment.id as string} title="Copy ID" variant="outline" />
                    </div>
                    <div>
                      <div className="text-xs mb-1 font-bold">Shipment method</div>
                      <div className="flex items-center">
                        <CarrierImage
                          carrier_name={(shipment.meta.custom_carrier_name || shipment.meta.carrier) as string}
                          containerClassName="mt-1 ml-1 mr-2"
                          height={28}
                          width={28}
                          text_color={(shipment.selected_rate_carrier as any)?.config?.text_color}
                          background={(shipment.selected_rate_carrier as any)?.config?.brand_color}
                        />
                        <div className="text-ellipsis text-xs" style={{ maxWidth: "190px", lineHeight: "16px" }}>
                          <span className="text-blue-600 font-bold">
                            {!isNone(shipment.tracking_number) && (
                              <span>{shipment.tracking_number}</span>
                            )}
                            {isNone(shipment.tracking_number) && (
                              <span>-</span>
                            )}
                          </span>
                          <br />
                          <span className="text-ellipsis">
                            {formatRef(
                              ((shipment.meta as any)?.service_name ||
                                shipment.service) as string,
                            )}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <div className="text-xs mb-1 font-bold">Service Level</div>
                      <div className="text-sm font-medium">
                        {formatRef(
                          ((shipment.meta as any)?.service_name ||
                            shipment.service) as string,
                        )}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs mb-1 font-bold">Rate Provider</div>
                      <div className="text-sm text-blue-600 font-medium">
                        {formatRef(shipment.meta.ext as string)}
                      </div>
                    </div>
                    {!isNone(shipment.reference) && (
                      <div>
                        <div className="text-xs mb-1 font-bold">Reference</div>
                        <div className="text-sm font-medium">
                          {shipment.reference}
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="space-y-3">
                    <div>
                      <div className="text-xs mb-1 font-bold">Tracking Number</div>
                      <div className="text-sm font-medium text-blue-600">
                        {shipment.tracking_number as string}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs mb-1 font-bold">Ship At</div>
                      <div className="text-sm font-medium">
                        {formatDateTime(shipment.options.shipping_date)}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs mb-1 font-bold">Created At</div>
                      <div className="text-sm font-medium">
                        {formatDateTime(shipment.created_at)}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs mb-1 font-bold">Last update</div>
                      <div className="text-sm">{formatDateTime(shipment.updated_at)}</div>
                    </div>
                  </div>
                </div>

                {/* Metadata Section - Part of sidebar on desktop only */}
                <div className={isSheet ? "hidden" : "hidden lg:block mt-6"}>
                  <h4 className="text-xl font-semibold mb-3">Metadata</h4>
                  <EnhancedMetadataEditor
                    value={shipment.metadata || {}}
                    onChange={handleMetadataChange}
                    placeholder="No metadata configured"
                    emptyStateMessage="Add key-value pairs to configure metadata"
                    allowEdit={true}
                    showTypeInference={true}
                    maxHeight="300px"
                  />
                </div>
              </div>
            )}

            {/* Left Column - Main Content */}
            <div className={`space-y-6 order-1 mr-5 ${isSheet ? '' : 'lg:col-span-3 lg:col-start-1 lg:order-1'}`}>

              {!isNone(shipment.tracker) && (
                <>
                  <div className="flex justify-between items-center my-4">
                    <h2 className="text-xl font-semibold">Recent Activity</h2>
                    <a
                      className="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1"
                      href={`/tracking/${shipment.tracker_id}`}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Tracking details
                      <i className="fas fa-external-link-alt text-xs"></i>
                    </a>
                  </div>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />
                  <div className="mt-3 mb-6">
                    <RecentActivity
                      tracker={shipment.tracker}
                    />
                  </div>
                </>
              )}

              {/* Charges section */}
              {!isNone(shipment.selected_rate) &&
                (shipment.selected_rate?.extra_charges || []).length > 0 && (
                  <>
                    <h2 className="text-xl font-semibold my-4">Charges breakdown</h2>

                    <div className="mt-1 mb-6">
                      <div className="space-y-2">
                        {/* Extra charges items */}
                        {(shipment.selected_rate?.extra_charges || []).map(
                          (charge, index) => (
                            <div key={index}>
                              <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-900">
                                  {charge?.name || 'Charge'}
                                </span>
                                <div className="text-sm text-gray-900 text-right">
                                  <span className="mr-1">{charge?.amount}</span>
                                  {!isNone(charge?.currency) && (
                                    <span>{charge?.currency}</span>
                                  )}
                                </div>
                              </div>
                              {index < (shipment.selected_rate?.extra_charges || []).length - 1 && (
                                <hr className="border-gray-200 mt-2" style={{ height: "1px" }} />
                              )}
                            </div>
                          )
                        )}

                        {/* Separator before total */}
                        {(shipment.selected_rate?.extra_charges || []).length > 0 && (
                          <hr className="border-gray-200" style={{ height: "1px" }} />
                        )}

                        {/* Total line */}
                        <div className="flex justify-between items-center">
                          <span className="text-sm font-semibold text-gray-900">
                            Total
                          </span>
                          <div className="text-sm font-semibold text-gray-900 text-right">
                            <span className="mr-1">
                              {Number(shipment.selected_rate?.total_charge).toFixed(2)}
                            </span>
                            {shipment.selected_rate?.currency && (
                              <span>{shipment.selected_rate?.currency}</span>
                            )}
                          </div>
                        </div>

                        {/* Line below total */}
                        <hr className="border-gray-200 mt-1" style={{ height: "1px" }} />
                      </div>
                    </div>
                  </>
                )}

              {/* Connection details section */}
              {(shipment.selected_rate_carrier?.connection_id ||
                shipment.selected_rate_carrier?.carrier_id ||
                shipment.selected_rate_carrier?.carrier_name) && (
                  <>
                    <h2 className="text-xl font-semibold my-4">Connection Details</h2>
                    <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                    <div className="mt-3 mb-6">
                      <div className={`grid grid-cols-1 ${isSheet ? '' : 'md:grid-cols-2'} gap-6 my-0`}>
                        <div className="space-y-2">
                          {/* Connection ID */}
                          <div className="flex flex-col xl:flex-row xl:items-center">
                            <div className="text-xs font-bold xl:w-32 mb-1 xl:mb-0">Connection ID</div>
                            <div className="text-sm font-medium break-all">
                              {shipment.selected_rate_carrier?.connection_id || '-'}
                            </div>
                          </div>

                          {/* Carrier ID */}
                          <div className="flex flex-col xl:flex-row xl:items-center">
                            <div className="text-xs font-bold xl:w-32 mb-1 xl:mb-0">Carrier ID</div>
                            <div className="text-sm font-medium break-all">
                              {shipment.selected_rate_carrier?.carrier_id || '-'}
                            </div>
                          </div>

                          {/* Type */}
                          <div className="flex flex-col xl:flex-row xl:items-center">
                            <div className="text-xs font-bold xl:w-32 mb-1 xl:mb-0">Type</div>
                            <div className="text-sm font-medium break-all">
                              {shipment.selected_rate_carrier?.carrier_name || '-'}
                            </div>
                          </div>

                          {/* Provider */}
                          <div className="flex flex-col xl:flex-row xl:items-center">
                            <div className="text-xs font-bold xl:w-32 mb-1 xl:mb-0">Provider</div>
                            <div className="text-sm font-medium break-all">
                              {shipment.selected_rate_carrier?.carrier_code || '-'}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </>
                )}

              {/* Return Shipment section */}
              {!isNone(shipment.return_shipment) && (
                <>
                  <h2 className="text-xl font-semibold my-4">Return Shipment</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6">
                    <div className={`grid grid-cols-1 ${isSheet ? '' : 'md:grid-cols-2'} gap-6 my-0`}>
                      <div className="space-y-2">
                        {shipment.return_shipment?.tracking_number && (
                          <div className="flex flex-col xl:flex-row xl:items-center">
                            <div className="text-xs font-bold xl:w-36 mb-1 xl:mb-0">Tracking Number</div>
                            <div className="text-sm font-medium break-all">
                              {shipment.return_shipment.tracking_url ? (
                                <a
                                  href={shipment.return_shipment.tracking_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:underline"
                                >
                                  {shipment.return_shipment.tracking_number}
                                </a>
                              ) : (
                                shipment.return_shipment.tracking_number
                              )}
                            </div>
                          </div>
                        )}

                        {shipment.return_shipment?.shipment_identifier && (
                          <div className="flex flex-col xl:flex-row xl:items-center">
                            <div className="text-xs font-bold xl:w-36 mb-1 xl:mb-0">Shipment ID</div>
                            <div className="text-sm font-medium break-all">
                              {shipment.return_shipment.shipment_identifier}
                            </div>
                          </div>
                        )}

                        {shipment.return_shipment?.service && (
                          <div className="flex flex-col xl:flex-row xl:items-center">
                            <div className="text-xs font-bold xl:w-36 mb-1 xl:mb-0">Service</div>
                            <div className="text-sm font-medium break-all">
                              {shipment.return_shipment.service}
                            </div>
                          </div>
                        )}

                        {shipment.return_shipment?.reference && (
                          <div className="flex flex-col xl:flex-row xl:items-center">
                            <div className="text-xs font-bold xl:w-36 mb-1 xl:mb-0">Reference</div>
                            <div className="text-sm font-medium break-all">
                              {shipment.return_shipment.reference}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </>
              )}

              {/* Summary section */}
              <h2 className="text-xl font-semibold my-4">Summary</h2>
              <hr className="mt-1 mb-2" style={{ height: "1px" }} />

              <div className="mt-3 mb-6">
                <div className="space-y-3">
                  {/* Shipping To section */}
                  <div className="text-base py-1">
                    <p className="text-base font-semibold tracking-wide my-2">
                      Shipped To
                    </p>

                    <AddressDescription address={shipment.recipient} />
                  </div>

                  {/* Shipped From section */}
                  {!isNone(shipment.shipper) && (
                    <div className="text-base py-1">
                      <p className="text-base font-semibold tracking-wide my-2">
                        Shipped From
                      </p>

                      <AddressDescription address={shipment.shipper} />
                    </div>
                  )}
                </div>
              </div>

              {/* Parcels section */}
              <h2 className="text-xl font-semibold my-4">Parcels</h2>
              <hr className="mt-1 mb-2" style={{ height: "1px" }} />

              <div className="mt-3 mb-6">
                {shipment.parcels.map((parcel: ParcelType, index) => (
                  <React.Fragment key={index + "parcel-info"}>
                    {index > 0 && <hr className="my-4" style={{ height: "1px" }} />}

                    <div className={`grid grid-cols-1 ${isSheet ? '' : 'md:grid-cols-2'} gap-6 mb-0`}>
                      {/* Parcel details */}
                      <div className="text-base py-1">
                        <ParcelDescription parcel={parcel} />
                      </div>

                      {/* Parcel items */}
                      {(parcel.items || []).length > 0 && (
                        <div className="text-base py-1">
                          <p className="text-base font-semibold uppercase tracking-wide my-2">
                            ITEMS{" "}
                            <span className="text-xs">
                              (
                              {(parcel.items || []).reduce(
                                (acc, { quantity }) => acc + (quantity || 0),
                                0,
                              )}
                              )
                            </span>
                          </p>

                          <div
                            className="py-2 pr-1 max-h-[40rem] overflow-auto"
                          >
                            {(parcel.items || []).map((item, index) => (
                              <React.Fragment key={index + "item-info"}>
                                <hr
                                  className="mt-1 mb-2"
                                  style={{ height: "1px" }}
                                />
                                <CommodityDescription commodity={item} />
                              </React.Fragment>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </React.Fragment>
                ))}
              </div>

              {/* Customs Declaration section */}
              {!isNone(shipment.customs) && (
                <>
                  <h2 className="text-xl font-semibold my-4">Customs Declaration</h2>
                  <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                  <div className="mt-3 mb-6">
                    <div className="text-base py-1">
                      <CustomsInfoDescription
                        customs={shipment.customs as CustomsType}
                      />
                    </div>
                  </div>
                </>
              )}

              {/* Commodities section */}
              {!isNone(shipment.customs) &&
                (shipment.customs?.commodities || []).length > 0 && (
                  <>
                    <h2 className="text-xl font-semibold my-4">
                      Commodities{" "}
                      <span className="text-lg">
                        (
                        {(shipment.customs?.commodities || []).reduce(
                          (acc, { quantity }) => acc + (quantity || 0),
                          0,
                        )}
                        )
                      </span>
                    </h2>
                    <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                    <div className="mt-3 mb-6">
                      {(shipment.customs?.commodities || []).map(
                        (commodity, index) => (
                          <React.Fragment key={index + "parcel-info"}>
                            {index > 0 && <hr className="mt-1 mb-2" style={{ height: "1px" }} />}
                            <CommodityDescription commodity={commodity} />
                          </React.Fragment>
                        ),
                      )}
                    </div>
                  </>
                )}

              {/* Metadata Section - Mobile only, positioned before timeline */}
              <div className={isSheet ? "" : "lg:hidden"}>
                <h2 className="text-xl font-semibold my-4">Metadata</h2>
                <hr className="mt-1 mb-2" style={{ height: "1px" }} />

                <div className="my-4">
                  <EnhancedMetadataEditor
                    value={shipment.metadata || {}}
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
          />

        </div>
      )}

      {query.isFetched && isNone(shipment) && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm my-6">
          <div className="p-6 text-center">
            <p>Uh Oh!</p>
            <p>{"We couldn't find any shipment with that reference"}</p>
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

    return <ShipmentComponent shipmentId={id} />;
  };

  return <Component />;
}
