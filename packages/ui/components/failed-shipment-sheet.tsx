"use client";

import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetClose,
} from "@karrio/ui/components/ui/sheet";
import { StatusCodeBadge } from "@karrio/ui/components/status-code-badge";
import { FailureReasons } from "@karrio/ui/components/failure-reasons";
import { formatDateTime, failsafe, jsonify } from "@karrio/lib";
import { useLocation } from "@karrio/hooks/location";
import { X, Copy, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "@karrio/ui/components/ui/button";
import type { get_logs_logs_edges_node } from "@karrio/types/graphql/types";
import React, { useState } from "react";

type FailedShipmentSheetContextType = {
  previewFailedShipment: (log: get_logs_logs_edges_node) => void;
};

interface FailedShipmentSheetComponent {
  children?: React.ReactNode;
}

export const FailedShipmentSheetContext =
  React.createContext<FailedShipmentSheetContextType>(
    {} as FailedShipmentSheetContextType,
  );

function parseLogData(data: any): any {
  if (!data) return null;
  if (typeof data === "string") {
    try { return JSON.parse(data); } catch { return null; }
  }
  return data;
}

function AddressSection({ label, address }: { label: string; address: any }) {
  if (!address) return null;

  const name = [address.person_name, address.company_name]
    .filter(Boolean)
    .join(" - ");
  const line = [
    address.address_line1,
    address.address_line2,
  ].filter(Boolean).join(", ");
  const location = [
    address.city,
    address.state_code,
    address.postal_code,
    address.country_code,
  ].filter(Boolean).join(", ");

  return (
    <div>
      <h4 className="text-xs font-semibold text-gray-500 uppercase mb-1">{label}</h4>
      {name && <p className="text-sm font-medium text-gray-900">{name}</p>}
      {line && <p className="text-sm text-gray-600">{line}</p>}
      {location && <p className="text-sm text-gray-600">{location}</p>}
      {address.email && (
        <p className="text-xs text-gray-500 mt-0.5">{address.email}</p>
      )}
      {address.phone_number && (
        <p className="text-xs text-gray-500">{address.phone_number}</p>
      )}
    </div>
  );
}

export const FailedShipmentSheet = ({
  children,
}: FailedShipmentSheetComponent): JSX.Element => {
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState(false);
  const [key, setKey] = useState(`failed-${Date.now()}`);
  const [log, setLog] = useState<get_logs_logs_edges_node | null>(null);
  const [rawExpanded, setRawExpanded] = useState(false);

  const previewFailedShipment = (logEntry: get_logs_logs_edges_node) => {
    setLog(logEntry);
    setIsActive(true);
    setKey(`failed-${Date.now()}`);
    addUrlParam("modal", String(logEntry.id));
  };

  const dismiss = () => {
    setLog(null);
    setIsActive(false);
    setRawExpanded(false);
    setKey(`failed-${Date.now()}`);
    removeUrlParam("modal");
  };

  const data = parseLogData(log?.data);
  const response = parseLogData(log?.response);

  return (
    <>
      <FailedShipmentSheetContext.Provider value={{ previewFailedShipment }}>
        {children}
      </FailedShipmentSheetContext.Provider>

      <Sheet open={isActive} onOpenChange={(open) => !open && dismiss()}>
        <SheetContent
          className="w-full sm:w-[800px] sm:max-w-[800px] p-0 shadow-none"
          side="right"
        >
          <div className="h-full flex flex-col" key={key}>
            <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
              <div className="flex items-center justify-between">
                <SheetTitle className="text-lg font-semibold">
                  Failed Shipment
                </SheetTitle>
                <SheetClose className="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2">
                  <X className="h-4 w-4" />
                  <span className="sr-only">Close</span>
                </SheetClose>
              </div>
            </SheetHeader>

            <div className="flex-1 overflow-y-auto px-4 py-4">
              {isActive && log && (
                <div className="space-y-6">
                  {/* Header: status + request_id + timestamp */}
                  <div className="flex items-center gap-3 flex-wrap">
                    <StatusCodeBadge code={log.status_code || 0} />
                    {log.request_id && (
                      <div className="flex items-center gap-1">
                        <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full font-mono">
                          {log.request_id}
                        </span>
                        <button
                          onClick={() =>
                            navigator.clipboard.writeText(log.request_id || "")
                          }
                          className="text-gray-400 hover:text-gray-600"
                          title="Copy request ID"
                        >
                          <Copy className="h-3 w-3" />
                        </button>
                      </div>
                    )}
                    {!log.request_id && (
                      <span className="text-xs text-gray-400">N/A</span>
                    )}
                    <span className="text-xs text-gray-500">
                      {log.requested_at
                        ? formatDateTime(log.requested_at)
                        : "Unknown"}
                    </span>
                  </div>

                  {/* Failure Reasons */}
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900 mb-3">
                      Failure Reasons
                    </h3>
                    <FailureReasons
                      response={response}
                      records={log.records || []}
                      requestedAt={log.requested_at}
                    />
                  </div>

                  {/* Request Details */}
                  {data && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-900 mb-3">
                        Request Details
                      </h3>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg border">
                        <AddressSection
                          label="Shipper"
                          address={data.shipper}
                        />
                        <AddressSection
                          label="Recipient"
                          address={data.recipient}
                        />
                      </div>

                      {/* Parcels summary */}
                      {data.parcels && data.parcels.length > 0 && (
                        <div className="mt-3 p-3 bg-gray-50 rounded-lg border">
                          <h4 className="text-xs font-semibold text-gray-500 uppercase mb-1">
                            Parcels ({data.parcels.length})
                          </h4>
                          {data.parcels.map((parcel: any, i: number) => (
                            <p key={i} className="text-sm text-gray-600">
                              {[
                                parcel.weight && `${parcel.weight} ${parcel.weight_unit || ""}`,
                                parcel.length && `${parcel.length}x${parcel.width}x${parcel.height} ${parcel.dimension_unit || ""}`,
                                parcel.packaging_type,
                              ].filter(Boolean).join(" - ") || "No dimensions"}
                            </p>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {!data && (
                    <div className="p-4 bg-gray-50 rounded-lg border">
                      <p className="text-sm text-gray-500">
                        Request data unavailable
                      </p>
                    </div>
                  )}

                  {/* Raw Response (collapsible) */}
                  <div>
                    <button
                      onClick={() => setRawExpanded(!rawExpanded)}
                      className="flex items-center gap-2 text-sm font-semibold text-gray-900 hover:text-gray-700"
                    >
                      Raw Response
                      {rawExpanded ? (
                        <ChevronUp className="h-4 w-4" />
                      ) : (
                        <ChevronDown className="h-4 w-4" />
                      )}
                    </button>
                    {rawExpanded && (
                      <div className="mt-2 relative">
                        <Button
                          variant="outline"
                          size="sm"
                          className="absolute top-2 right-2 h-7 px-2 z-10"
                          onClick={() => {
                            const text = failsafe(
                              () => jsonify(response),
                              JSON.stringify(response),
                            );
                            navigator.clipboard.writeText(text || "");
                          }}
                        >
                          <Copy className="h-3 w-3 mr-1" />
                          Copy
                        </Button>
                        <pre className="p-4 bg-gray-900 text-gray-100 rounded-lg text-xs overflow-x-auto max-h-96">
                          {failsafe(
                            () => jsonify(response),
                            JSON.stringify(response, null, 2),
                          )}
                        </pre>
                      </div>
                    )}
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