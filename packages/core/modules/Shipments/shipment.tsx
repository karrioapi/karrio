"use client";
import { EnhancedMetadataEditor } from "@karrio/ui/components/enhanced-metadata-editor";
import { useMetadataMutation } from "@karrio/hooks/metadata";
import {
  useUploadRecordMutation,
  useUploadRecords,
} from "@karrio/hooks/upload-record";
import { CustomsInfoDescription } from "@karrio/ui/core/components/customs-info-description";
import { CommodityDescription } from "@karrio/ui/core/components/commodity-description";
import { OptionsDescription } from "@karrio/ui/core/components/options-description";
import { AddressDescription } from "@karrio/ui/core/components/address-description";
import { ParcelDescription } from "@karrio/ui/core/components/parcel-description";
import { formatDateTime, formatDayDate, formatRef, isNone } from "@karrio/lib";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";
import { CustomsType, NotificationType, ParcelType, MetadataObjectTypeEnum } from "@karrio/types";
import { CopiableLink } from "@karrio/ui/components/copiable-link";
import { CarrierBadge } from "@karrio/ui/core/components/carrier-badge";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { ShipmentMenu } from "@karrio/ui/components/shipment-menu";
import { ShipmentsStatusBadge } from "@karrio/ui/components/shipments-status-badge";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Table, TableBody, TableCell, TableRow } from "@karrio/ui/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { DocumentUploadData } from "@karrio/types/rest/api";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { useShipment, useShipmentMutation } from "@karrio/hooks/shipment";
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
  const $fileInput = React.useRef<HTMLInputElement>(undefined);
  const $fileSelectInput = React.useRef<HTMLSelectElement>(undefined);
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
      if (!!$fileSelectInput.current) $fileSelectInput.current.value = "other";
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
        <div className="flex flex-col lg:grid lg:grid-cols-4 gap-6">
          {/* Service Details Section - Desktop ONLY: RIGHT sidebar */}
          {!isNone(shipment.selected_rate) && (
            <div className="hidden lg:block lg:order-2 lg:col-span-1 lg:col-start-4">
              <h3 className="text-xl lg:text-lg font-semibold my-4 lg:mb-4 lg:mt-0">
                Details
              </h3>
              <hr className="mt-1 mb-2 lg:hidden" style={{ height: "1px" }} />
              
              <div className="mt-3 mb-6 lg:mt-0 space-y-3">
                <div>
                  <div className="text-xs text-gray-600 mb-1">Shipment ID</div>
                  <CopiableLink text={shipment.id as string} title="Copy ID" variant="outline" />
                </div>
                <div>
                  <div className="text-xs text-gray-600 mb-1">Shipment method</div>
                  <div className="flex items-center">
                    <CarrierImage
                      carrier_name={shipment.meta.carrier as string}
                      containerClassName="mt-1 ml-1 mr-2"
                      height={28}
                      width={28}
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
                  <div className="text-xs text-gray-600 mb-1">Rate</div>
                  <div className="text-sm">
                    <span className="font-medium mr-1">
                      {shipment.selected_rate?.total_charge}
                    </span>
                    <span>{shipment.selected_rate?.currency}</span>
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-600 mb-1">Tracking Number</div>
                  <div className="text-sm font-medium text-blue-600">
                    {shipment.tracking_number as string}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-600 mb-1">Rate Provider</div>
                  <div className="text-sm text-blue-600 font-medium">
                    {formatRef(shipment.meta.ext as string)}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-600 mb-1">Last updated</div>
                  <div className="text-sm">{formatDateTime(shipment.created_at)}</div>
                </div>
                
                {/* Metadata Section - Part of sidebar on desktop, separate on mobile */}
                <div className="hidden lg:block mt-6">
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
          )}

          {/* Left Column - Main Content */}
          <div className="lg:col-span-3 lg:col-start-1 space-y-6 order-1 lg:order-1">
            {/* Header Section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-1">
            <div className="space-y-2">
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
                      : (shipment.status === "purchased" ? "0.00" : "UNFULFILLED")}
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
              <div className="flex justify-start md:hidden">
                <ShipmentMenu shipment={shipment as any} isViewing variant="outline" />
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-end items-center gap-1">
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

                {/* Desktop ShipmentMenu - hidden on mobile */}
                <div className="hidden md:block">
                  <ShipmentMenu shipment={shipment as any} isViewing variant="outline" />
                </div>
              </div>
            </div>
          </div>

          <hr className="mt-1 mb-0" style={{ height: "1px" }} />

          {/* Reference and highlights section */}
          <div className="flex flex-col md:flex-row md:flex-wrap gap-0 mb-4">
            <div className="p-4 mr-4">
              <span className="text-xs text-gray-600 my-4">Date</span>
              <br />
              <span className="text-xs mt-1 font-semibold">
                {formatDateTime(shipment.created_at)}
              </span>
            </div>

            {!isNone(shipment.service) && (
              <>
                <div className="hidden md:block w-px bg-gray-300 my-1"></div>
                <div className="p-4 mr-4">
                  <span className="text-xs text-gray-600 my-4">Courier</span>
                  <br />
                  <CarrierBadge
                    carrier_name={shipment.meta.carrier as string}
                    text_color={
                      shipment.selected_rate_carrier?.config?.text_color
                    }
                    background={
                      shipment.selected_rate_carrier?.config?.brand_color
                    }
                  />
                </div>

                <div className="hidden md:block w-px bg-gray-300 my-1"></div>
                <div className="p-4 mr-4">
                  <span className="text-xs text-gray-600 my-4">Service Level</span>
                  <br />
                  <span className="text-xs mt-1 font-semibold">
                    {formatRef(
                      ((shipment.meta as any)?.service_name ||
                        shipment.service) as string,
                    )}
                  </span>
                </div>
              </>
            )}

            {!isNone(shipment.reference) && (
              <>
                <div className="hidden md:block w-px bg-gray-300 my-1"></div>
                <div className="p-4 mr-4">
                  <span className="text-xs text-gray-600 my-4">Reference</span>
                  <br />
                  <span className="text-xs font-semibold">
                    {shipment.reference}
                  </span>
                </div>
              </>
            )}
          </div>

          {/* Service Details - Mobile ONLY: positioned before tracking */}
          {!isNone(shipment.selected_rate) && (
            <div className="lg:hidden">
              <h2 className="text-xl font-semibold my-4">Details</h2>
              <hr className="mt-1 mb-2" style={{ height: "1px" }} />
              
              <div className="mt-3 mb-6 space-y-3">
                <div>
                  <div className="text-xs text-gray-600 mb-1">Shipment ID</div>
                  <CopiableLink text={shipment.id as string} title="Copy ID" variant="outline" />
                </div>
                <div>
                  <div className="text-xs text-gray-600 mb-1">Shipment method</div>
                  <div className="flex items-center">
                    <CarrierImage
                      carrier_name={shipment.meta.carrier as string}
                      containerClassName="mt-1 ml-1 mr-2"
                      height={28}
                      width={28}
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
                  <div className="text-xs text-gray-600 mb-1">Rate</div>
                  <div className="text-sm">
                    <span className="font-medium mr-1">
                      {shipment.selected_rate?.total_charge}
                    </span>
                    <span>{shipment.selected_rate?.currency}</span>
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-600 mb-1">Tracking Number</div>
                  <div className="text-sm font-medium text-blue-600">
                    {shipment.tracking_number as string}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-600 mb-1">Rate Provider</div>
                  <div className="text-sm text-blue-600 font-medium">
                    {formatRef(shipment.meta.ext as string)}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-600 mb-1">Last updated</div>
                  <div className="text-sm">{formatDateTime(shipment.created_at)}</div>
                </div>
              </div>
            </div>
          )}

          {!isNone(shipment.tracker) && (
            <>
              <h2 className="text-xl font-semibold my-4">
                <span>Tracking Details</span>
                <a
                  className="p-0 mx-2 my-0 text-base font-semibold"
                  href={`/tracking/${shipment.tracker_id}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  <span>
                    <i className="fas fa-external-link-alt"></i>
                  </span>
                </a>
              </h2>
              <hr className="mt-1 mb-2" style={{ height: "1px" }} />
              <div className="mt-3 mb-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 py-1">
                  <div className="text-sm">
                    {!isNone(shipment.tracker?.estimated_delivery) && (
                      <div className="grid grid-cols-3 gap-2 my-0">
                        <div className="text-base py-0">
                          {shipment.tracker?.delivered
                            ? "Delivered"
                            : "Estimated Delivery"}
                        </div>
                        <div className="col-span-2 text-xs font-semibold py-1">
                          {formatDayDate(
                            shipment.tracker!.estimated_delivery as string,
                          )}
                        </div>
                      </div>
                    )}
                    <div className="grid grid-cols-3 gap-2 my-0">
                      <div className="text-base py-0">
                        Last event
                      </div>
                      <div className="col-span-2 text-xs font-semibold py-1">
                        <p className="capitalize">
                          {formatDayDate(
                            (shipment.tracker?.events || [])[0]?.date as string,
                          )}{" "}
                          <code>
                            {(shipment.tracker?.events || [])[0]?.time}
                          </code>
                        </p>
                      </div>
                    </div>
                    {!isNone((shipment.tracker?.events || [])[0]?.location) && (
                      <div className="grid grid-cols-3 gap-2 my-0">
                        <div></div>
                        <div className="col-span-2 text-xs font-semibold py-1">
                          {(shipment.tracker?.events || [])[0]?.location}
                        </div>
                      </div>
                    )}
                    {!isNone(
                      (shipment.tracker?.events || [])[0]?.description,
                    ) && (
                        <div className="grid grid-cols-3 gap-2 my-0">
                          <div></div>
                          <div className="col-span-2 text-xs font-semibold py-1">
                            {(shipment.tracker?.events || [])[0]?.description}
                          </div>
                        </div>
                      )}
                  </div>
                </div>
              </div>
            </>
          )}

          {/* Shipment details section */}
          <h2 className="text-xl font-semibold my-4">Shipment Details</h2>
          <hr className="mt-1 mb-2" style={{ height: "1px" }} />

          <div className="mt-3 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 my-0">
              {/* Recipient Address section */}
              <div className="text-base py-1">
                <p className="text-base font-semibold uppercase tracking-wide my-2">
                  ADDRESS
                </p>

                <AddressDescription address={shipment.recipient} />
              </div>

              {/* Options section */}
              {Object.values(shipment.options as object).length > 0 && (
                <div className="text-base py-1">
                  <p className="text-base font-semibold uppercase tracking-wide my-2">
                    OPTIONS
                  </p>

                  <OptionsDescription options={shipment.options} />
                </div>
              )}
            </div>

            {/* Parcels section */}
            <div className="mt-6 mb-0">
              <p className="text-base font-semibold uppercase tracking-wide my-2">
                PARCEL{shipment.parcels.length > 1 && "S"}
              </p>

              {shipment.parcels.map((parcel: ParcelType, index) => (
                <React.Fragment key={index + "parcel-info"}>
                  <hr className="my-4" style={{ height: "1px" }} />

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-0">
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

            {/* Customs section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6 mb-0">
              {/* Customs details */}
              {!isNone(shipment.customs) && (
                <div className="text-base py-1">
                  <p className="text-base font-semibold uppercase tracking-wide my-2">
                    CUSTOMS DECLARATION
                  </p>

                  <CustomsInfoDescription
                    customs={shipment.customs as CustomsType}
                  />
                </div>
              )}

              {/* Customs commodities */}
              {!isNone(shipment.customs) &&
                (shipment.customs?.commodities || []).length > 0 && (
                  <div className="text-base py-1">
                    <p className="text-base font-semibold uppercase tracking-wide my-2">
                      COMMODITIES{" "}
                      <span className="text-xs">
                        (
                        {(shipment.customs?.commodities || []).reduce(
                          (acc, { quantity }) => acc + (quantity || 0),
                          0,
                        )}
                        )
                      </span>
                    </p>

                    {(shipment.customs?.commodities || []).map(
                      (commodity, index) => (
                        <React.Fragment key={index + "parcel-info"}>
                          <hr className="mt-1 mb-2" style={{ height: "1px" }} />
                          <CommodityDescription commodity={commodity} />
                        </React.Fragment>
                      ),
                    )}
                  </div>
                )}
            </div>
          </div>

          {/* Document section */}
          {(
            (carrier_capabilities[shipment.carrier_name as string] || []) as any
          ).includes("paperless") &&
            "paperless_trade" in shipment.options && (
              <>
                <h2 className="text-xl font-semibold my-4">Paperless Trade Documents</h2>

                {!documents.isFetched && documents.isFetching && <Spinner />}

                {documents.isFetched &&
                  !documents.isFetching &&
                  [...(uploads || []), ...(shipment.options.doc_files || [])]
                    .length == 0 && (
                    <>
                      <hr className="mt-1 mb-3" style={{ height: "1px" }} />
                      <div className="pb-3">No documents uploaded</div>
                    </>
                  )}

                {documents.isFetched &&
                  [...(uploads || []), ...(shipment.options.doc_files || [])]
                    .length > 0 && (
                    <div className="w-full">
                      <Table>
                        <TableBody>
                          {(uploads || []).map((upload) => (
                            <React.Fragment key={shipment.id}>
                              {(upload.documents || []).map((doc) => (
                                <TableRow key={doc.doc_id}>
                                  <TableCell className="p-0">
                                    <span>{doc.file_name}</span>
                                  </TableCell>
                                  <TableCell className="p-0">
                                    <Badge variant="default" className="my-2">
                                      uploaded
                                    </Badge>
                                  </TableCell>
                                </TableRow>
                              ))}
                            </React.Fragment>
                          ))}
                          {(shipment.options.doc_files || []).map(
                            (doc: any, idx: number) => (
                              <TableRow
                                key={`${new Date()}-${idx}`}
                              >
                                <TableCell className="p-0">
                                  <span>{doc.doc_name}</span>
                                </TableCell>
                                <TableCell className="p-0">
                                  <Badge variant="default" className="my-2">
                                    uploaded
                                  </Badge>
                                </TableCell>
                              </TableRow>
                            ),
                          )}
                        </TableBody>
                      </Table>
                    </div>
                  )}

                <div className="flex justify-between">
                  <div className="flex">
                    <Select
                      onValueChange={(value) =>
                        setFileData({ ...fileData, doc_type: value })
                      }
                      defaultValue="other"
                    >
                      <SelectTrigger className="w-full">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="other">other</SelectItem>
                        <SelectItem value="commercial_invoice">
                          Commercial invoice
                        </SelectItem>
                        <SelectItem value="pro_forma_invoice">
                          Pro forma invoice
                        </SelectItem>
                        <SelectItem value="packing_list">Packing list</SelectItem>
                        <SelectItem value="certificate_of_origin">
                          Certificate of origin
                        </SelectItem>
                      </SelectContent>
                    </Select>
                    <Input
                      className="mx-2"
                      type="file"
                      onChange={handleFileChange}
                    />
                  </div>

                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className="self-center"
                    disabled={
                      (uploads || [])?.length > 4 ||
                      !fileData.doc_file ||
                      documents.isFetching ||
                      uploadDocument.isLoading
                    }
                    onClick={() => uploadCustomsDocument()}
                  >
                    <span className="inline-flex items-center justify-center w-4 h-4">
                      <i className="fas fa-upload"></i>
                    </span>
                    <span>Upload</span>
                  </Button>
                </div>

                <div className="my-3 pt-1"></div>
              </>
            )}

          {/* Metadata Section - Mobile only, positioned before timeline */}
          <div className="lg:hidden">
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

          {/* Activity Timeline section */}
          <h2 className="text-xl font-semibold my-4">Activity</h2>

            <ActivityTimeline
              logs={logs}
              events={events}
            />
          </div>

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

    return (
      <>
        <ShipmentComponent shipmentId={id} />
      </>
    );
  };

  return <Component />;
}
