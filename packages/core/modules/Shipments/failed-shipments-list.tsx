"use client";

import { StatusCodeBadge } from "@karrio/ui/components/status-code-badge";
import { FailedShipmentSheetContext } from "@karrio/ui/components/failed-shipment-sheet";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { ListPagination } from "@karrio/ui/components/list-pagination";
import { StickyTableWrapper } from "@karrio/ui/components/sticky-table-wrapper";
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
} from "@karrio/ui/components/ui/table";
import { Skeleton } from "@karrio/ui/components/ui/skeleton";
import { formatDateTime, getURLSearchParams } from "@karrio/lib";
import { useLogs } from "@karrio/hooks/log";
import type { get_logs_logs_edges_node } from "@karrio/types/graphql/types";
import React, { useContext, useEffect } from "react";
import { useLoader } from "@karrio/ui/core/components/loader";

function parseData(data: any): any {
  if (!data) return null;
  if (typeof data === "string") {
    try { return JSON.parse(data); } catch { return null; }
  }
  return data;
}

function extractCarrier(log: get_logs_logs_edges_node): string | null {
  const data = parseData(log.data);
  if (!data) return null;
  return (
    data.carrier_name ||
    data.selected_rate?.carrier_name ||
    data.rates?.[0]?.carrier_name ||
    null
  );
}

function extractRecipient(log: get_logs_logs_edges_node): string {
  const data = parseData(log.data);
  if (!data?.recipient) return "-";
  const { city, country_code, person_name } = data.recipient;
  return [person_name, city, country_code].filter(Boolean).join(", ") || "-";
}

function extractFirstError(log: get_logs_logs_edges_node): string {
  const response = parseData(log.response);
  if (!response) return "-";

  const errors = response.errors || response.messages || [];
  if (Array.isArray(errors) && errors.length > 0) {
    const err = errors[0];
    return typeof err === "string"
      ? err
      : err.message || err.details || err.detail || "-";
  }
  if (response.error || response.message || response.detail) {
    return response.error || response.message || response.detail;
  }
  return "-";
}

export function FailedShipmentsList() {
  const { setLoading } = useLoader();
  const { previewFailedShipment } = useContext(FailedShipmentSheetContext);
  const context = useLogs({
    method: ["POST"] as any,
    api_endpoint: "/v1/shipments",
    status: "failed" as any,
    setVariablesToURL: false,
  });
  const {
    query: { data: { logs } = {}, ...query },
    filter,
    setFilter,
  } = context;

  const updateFilter = (extra: Partial<any> = {}) => {
    setFilter({ ...filter, ...extra });
  };

  useEffect(() => {
    setLoading(query.isFetching);
  }, [query.isFetching]);

  return (
    <>
      {!query.isFetched && (
        <div className="bg-white rounded-lg shadow-sm border my-6 p-6">
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex items-center space-x-4">
                <Skeleton className="h-4 w-[60px]" />
                <Skeleton className="h-4 w-[80px]" />
                <Skeleton className="h-4 w-[120px]" />
                <Skeleton className="h-4 w-[200px]" />
                <Skeleton className="h-4 w-[100px]" />
                <Skeleton className="h-4 w-[80px]" />
              </div>
            ))}
          </div>
        </div>
      )}

      {query.isFetched && (logs?.edges || []).length > 0 && (
        <>
          <StickyTableWrapper>
            <Table className="failed-shipments-table">
              <TableHeader>
                <TableRow>
                  <TableHead className="text-xs items-center w-[70px]">
                    STATUS
                  </TableHead>
                  <TableHead className="text-xs items-center">
                    CARRIER
                  </TableHead>
                  <TableHead className="text-xs items-center">
                    RECIPIENT
                  </TableHead>
                  <TableHead className="text-xs items-center">
                    ERROR
                  </TableHead>
                  <TableHead className="text-xs items-center w-[140px]">
                    REQUEST ID
                  </TableHead>
                  <TableHead className="text-xs items-center w-[140px]">
                    DATE
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {(logs?.edges || []).map(({ node: log }) => {
                  const carrier = extractCarrier(log);
                  return (
                    <TableRow
                      key={log.id}
                      className="cursor-pointer transition-colors duration-150 ease-in-out hover:bg-gray-50"
                      onClick={() => previewFailedShipment(log)}
                    >
                      <TableCell className="py-3">
                        <StatusCodeBadge code={log.status_code || 0} />
                      </TableCell>
                      <TableCell className="py-3 text-xs text-gray-600">
                        <div className="flex items-center gap-2">
                          {carrier && (
                            <CarrierImage
                              carrier_name={carrier}
                              height={20}
                              width={20}
                            />
                          )}
                          <span className="font-medium">
                            {carrier || "-"}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell className="py-3 text-xs font-medium text-gray-600">
                        {extractRecipient(log)}
                      </TableCell>
                      <TableCell className="py-3 text-xs text-gray-600 max-w-[300px]">
                        <span
                          className="block truncate"
                          title={extractFirstError(log)}
                        >
                          {extractFirstError(log)}
                        </span>
                      </TableCell>
                      <TableCell className="py-3">
                        {log.request_id ? (
                          <span
                            className="text-xs font-mono text-gray-500 block truncate max-w-[130px]"
                            title={log.request_id}
                          >
                            {log.request_id}
                          </span>
                        ) : (
                          <span className="text-xs text-gray-400">N/A</span>
                        )}
                      </TableCell>
                      <TableCell className="py-3">
                        <span className="text-xs text-gray-600">
                          {log.requested_at
                            ? formatDateTime(log.requested_at)
                            : "-"}
                        </span>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </StickyTableWrapper>

          <div className="sticky bottom-0 left-0 right-0 z-10 bg-white border-t border-gray-200 pb-16 md:pb-0">
            <ListPagination
              currentOffset={(filter.offset as number) || 0}
              pageSize={20}
              totalCount={logs?.page_info?.count || 0}
              hasNextPage={logs?.page_info?.has_next_page || false}
              onPageChange={(offset) => updateFilter({ offset })}
              className="px-2 py-3"
            />
          </div>
        </>
      )}

      {query.isFetched && (logs?.edges || []).length === 0 && (
        <div className="bg-white rounded-lg shadow-sm border my-6">
          <div className="p-6 text-center">
            <p className="text-gray-500">
              No failed shipment attempts found.
            </p>
          </div>
        </div>
      )}
    </>
  );
}