"use client";

import * as React from "react";
import { format } from "date-fns";
import { MoreHorizontal, Package, Trash2 } from "lucide-react";
import {
  formatAddressLocationShort,
  formatAddressShort,
  formatDateTime,
  getURLSearchParams,
} from "@karrio/lib";
import { SchedulePickupDialog } from "@karrio/ui/components/schedule-pickup-dialog";
import { DeleteConfirmationDialog } from "@karrio/ui/components/delete-confirmation-dialog";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { useSystemConnections } from "@karrio/hooks/system-connection";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { usePickups, usePickupMutation } from "@karrio/hooks/pickup";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { get_pickups_pickups_edges_node, NotificationType } from "@karrio/types";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { useSearchParams } from "next/navigation";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/ui/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";

type PickupType = get_pickups_pickups_edges_node;

function formatErrorMessage(error: any): string {
  if (error?.data?.errors && Array.isArray(error.data.errors)) {
    return error.data.errors
      .map((e: any) => e.message || JSON.stringify(e))
      .join("; ");
  }
  if (error?.errors && Array.isArray(error.errors)) {
    return error.errors
      .map((e: any) => e.message || JSON.stringify(e))
      .join("; ");
  }
  if (error?.message) {
    return error.message;
  }
  if (typeof error === "string") {
    return error;
  }
  return "An unexpected error occurred";
}

export default function PickupsPage() {
  const searchParams = useSearchParams();
  const { setLoading } = useLoader();
  const { toast } = useToast();
  const { references } = useAPIMetadata();
  const [allChecked, setAllChecked] = React.useState(false);
  const [selection, setSelection] = React.useState<string[]>([]);
  const [cancelDialogOpen, setCancelDialogOpen] = React.useState(false);
  const [pickupToCancel, setPickupToCancel] = React.useState<PickupType | null>(null);
  const { user_connections } = useCarrierConnections();
  const { system_connections } = useSystemConnections();
  const { cancelPickup } = usePickupMutation();
  const {
    query: { data: { pickups } = {}, ...query },
    filter,
    setFilter,
  } = usePickups({
    setVariablesToURL: true,
    preloadNextPage: true,
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
    selectedPickups: string[],
    current: typeof pickups,
  ) => {
    const pickup_ids = (current?.edges || []).map(
      ({ node: pickup }) => pickup.id,
    );
    const selection = selectedPickups.filter((id) =>
      pickup_ids.includes(id),
    );
    const selected =
      selection.length > 0 &&
      selection.length === (pickup_ids || []).length;
    setAllChecked(selected);
    if (
      selectedPickups.filter((id) => !pickup_ids.includes(id)).length > 0
    ) {
      setSelection(selection);
    }
  };

  const handleSelectAll = (checked: boolean) => {
    setSelection(
      checked ? (pickups?.edges || []).map(({ node: { id } }) => id) : []
    );
  };

  const handleSelectOne = (id: string, checked: boolean) => {
    setSelection(
      checked
        ? [...selection, id]
        : selection.filter((s) => s !== id)
    );
  };

  const getCarrier = (pickup: PickupType) =>
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
    if (!pickupToCancel) return;
    try {
      await cancelPickup.mutateAsync(pickupToCancel.id);
      toast({
        title: "Pickup Cancelled",
        description: "The pickup has been successfully cancelled.",
      });
      setCancelDialogOpen(false);
      setPickupToCancel(null);
    } catch (error: any) {
      const errorMessage = formatErrorMessage(error);
      toast({
        variant: "destructive",
        title: "Failed to cancel pickup",
        description: errorMessage,
      });
    }
  };

  const openCancelDialog = (pickup: PickupType) => {
    setPickupToCancel(pickup);
    setCancelDialogOpen(true);
  };

  React.useEffect(() => {
    updateFilter();
  }, [searchParams]);

  React.useEffect(() => {
    setLoading(query.isLoading);
  }, [query.isLoading]);

  React.useEffect(() => {
    updatedSelection(selection, pickups);
  }, [selection, pickups]);

  return (
    <>
      {/* Header */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between px-0 pb-0 pt-4 mb-4">
        <div className="mb-4 sm:mb-0">
          <h1 className="text-2xl font-semibold text-gray-900">Pickups</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Manage scheduled carrier pickups for your shipments
          </p>
        </div>
        <div className="flex flex-row items-center gap-2">
          <SchedulePickupDialog onScheduled={() => query.refetch()} />
        </div>
      </header>

      {/* Loading State */}
      {!query.isFetched && query.isFetching && <Spinner />}

      {/* Pickups Table */}
      {query.isFetched && (pickups?.edges || []).length > 0 && (
        <>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-12">
                    <Checkbox
                      checked={allChecked}
                      onCheckedChange={handleSelectAll}
                      aria-label="Select all"
                    />
                  </TableHead>
                  <TableHead>Carrier</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Address</TableHead>
                  <TableHead>Pickup Date</TableHead>
                  <TableHead>Time Window</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="w-12"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {(pickups?.edges || []).map(({ node: pickup }) => {
                  const carrier = getCarrier(pickup);
                  return (
                    <TableRow key={pickup.id}>
                      <TableCell>
                        <Checkbox
                          checked={selection.includes(pickup.id)}
                          onCheckedChange={(checked) =>
                            handleSelectOne(pickup.id, !!checked)
                          }
                          aria-label={`Select ${pickup.id}`}
                        />
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <CarrierImage
                            carrier_name={pickup.carrier_name || ""}
                            height={28}
                            width={28}
                            text_color={carrier?.config?.text_color}
                            background={carrier?.config?.brand_color}
                          />
                          <div className="flex flex-col">
                            <span className="font-medium text-sm">
                              {pickup.confirmation_number || pickup.id}
                            </span>
                            <span className="text-xs text-muted-foreground">
                              {(pickup.tracking_numbers || [])[0] || pickup.carrier_name}
                            </span>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <StatusBadge status={pickup.status || "scheduled"} />
                      </TableCell>
                      <TableCell>
                        <div className="flex flex-col">
                          <span className="text-sm">
                            {formatAddressShort(pickup.address as any) || "-"}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            {formatAddressLocationShort(pickup.address as any)}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <span className="text-sm">
                          {pickup.pickup_date || "-"}
                        </span>
                      </TableCell>
                      <TableCell>
                        <span className="text-sm">
                          {pickup.ready_time && pickup.closing_time
                            ? `${pickup.ready_time} - ${pickup.closing_time}`
                            : pickup.ready_time || pickup.closing_time || "-"}
                        </span>
                      </TableCell>
                      <TableCell>
                        <span className="text-sm text-muted-foreground">
                          {formatDateTime(pickup.created_at)}
                        </span>
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-8 w-8"
                            >
                              <MoreHorizontal className="h-4 w-4" />
                              <span className="sr-only">Open menu</span>
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            {!["cancelled", "closed"].includes(pickup.status || "") && (
                              <DropdownMenuItem
                                onClick={() => openCancelDialog(pickup)}
                                className="text-destructive focus:text-destructive"
                              >
                                <Trash2 className="mr-2 h-4 w-4" />
                                Cancel Pickup
                              </DropdownMenuItem>
                            )}
                            {["cancelled", "closed"].includes(pickup.status || "") && (
                              <DropdownMenuItem disabled className="text-muted-foreground">
                                No actions available
                              </DropdownMenuItem>
                            )}
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between py-4">
            <span className="text-sm text-muted-foreground">
              {(pickups?.edges || []).length} results
            </span>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() =>
                  updateFilter({ offset: (filter.offset as number) - 20 })
                }
                disabled={filter.offset === 0}
              >
                Previous
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() =>
                  updateFilter({ offset: (filter.offset as number) + 20 })
                }
                disabled={!pickups?.page_info.has_next_page}
              >
                Next
              </Button>
            </div>
          </div>
        </>
      )}

      {/* Empty State */}
      {query.isFetched && (pickups?.edges || []).length === 0 && (
        <Card className="mt-6">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Package className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No pickups scheduled</h3>
            <p className="text-sm text-muted-foreground text-center max-w-md mb-6">
              Schedule a pickup to have carriers collect your shipments.
              You&apos;ll need at least one shipment with a purchased label.
            </p>
            <SchedulePickupDialog onScheduled={() => query.refetch()} />
          </CardContent>
        </Card>
      )}

      {/* Cancel Pickup Confirmation Dialog */}
      <DeleteConfirmationDialog
        open={cancelDialogOpen}
        onOpenChange={setCancelDialogOpen}
        title="Cancel Pickup"
        description={`Are you sure you want to cancel this pickup? Confirmation: ${pickupToCancel?.confirmation_number || pickupToCancel?.id || ""}`}
        confirmLabel="Cancel Pickup"
        cancelLabel="Go Back"
        onConfirm={handleCancelPickup}
      />
    </>
  );
}
