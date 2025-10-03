import * as React from "react";
import { useState } from "react";
import { useKarrio } from "../../provider/karrio-provider";
import { useShipments, ShipmentStatus } from "../../hooks/use-shipments";
import { ShipmentsTable, Shipment } from "./shipments-table";
import { ShipmentsPagination } from "./shipments-pagination";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";

export interface ShipmentsContainerProps {
  defaultPageSize?: number;
  defaultStatus?: ShipmentStatus[];
  onShipmentSelect?: (id: string) => void;
}

export function ShipmentsContainer({
  defaultPageSize = 20,
  defaultStatus = ["purchased", "in_transit", "out_for_delivery", "delivery_failed"],
  onShipmentSelect,
}: ShipmentsContainerProps) {
  const { isAuthenticated, isLoading } = useKarrio();

  // Local state
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState(1);

  // Set up filter with current page and status
  const {
    query,
    filter,
    setFilter,
  } = useShipments({
    first: defaultPageSize,
    offset: (currentPage - 1) * defaultPageSize,
    status: defaultStatus,
    enabled: isAuthenticated,
    preloadNextPage: true,
  });

  // Extract data from query result
  const isDataLoading = query.isLoading || query.isFetching;
  const shipments = query.data?.shipments?.edges?.map(
    ({ node }: any) => node as Shipment
  ) || [];
  const totalCount = query.data?.shipments?.page_info?.count || 0;

  // Handle pagination
  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    setFilter({
      ...filter,
      offset: (page - 1) * defaultPageSize,
    });
  };

  // Handle status filter
  const handleStatusFilter = (statuses: ShipmentStatus[]) => {
    setCurrentPage(1);
    setFilter({
      ...filter,
      offset: 0,
      status: statuses,
    });
  };

  // Handle search
  const handleSearch = (search: string) => {
    setCurrentPage(1);
    setFilter({
      ...filter,
      offset: 0,
      search: search || undefined,
    });
  };

  // Handle refresh
  const handleRefresh = () => {
    query.refetch();
  };

  // Handle selection
  const handleSelectChange = (ids: string[]) => {
    setSelectedIds(ids);
  };

  // Handle view shipment
  const handleViewShipment = (id: string) => {
    if (onShipmentSelect) {
      onShipmentSelect(id);
    }
  };

  // Show loading state while authentication is being determined
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Shipments</CardTitle>
        </CardHeader>
        <CardContent>
          <Alert>
            <AlertDescription>
              Loading authentication information...
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  // Show message when not authenticated
  if (!isAuthenticated) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Shipments</CardTitle>
        </CardHeader>
        <CardContent>
          <Alert>
            <AlertDescription>
              Please log in to view your shipments.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Shipments</CardTitle>
      </CardHeader>
      <CardContent>
        <ShipmentsTable
          isLoading={isDataLoading}
          shipments={shipments}
          selectedIds={selectedIds}
          onSelectChange={handleSelectChange}
          onRefresh={handleRefresh}
          onViewShipment={handleViewShipment}
          onStatusFilter={handleStatusFilter}
          onSearchChange={handleSearch}
        />

        {!isDataLoading && shipments.length > 0 && (
          <ShipmentsPagination
            currentPage={currentPage}
            totalItems={totalCount}
            pageSize={defaultPageSize}
            onPageChange={handlePageChange}
          />
        )}
      </CardContent>
    </Card>
  );
}
