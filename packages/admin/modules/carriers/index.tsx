"use client";

import { CarrierConnectionsTable, Connection } from "@karrio/admin/components/carrier-connections-table";
import { GetRateSheets_rate_sheets_edges_node as RateSheet } from "@karrio/types/graphql/admin/types";
import { DeleteConfirmationDialog } from "@karrio/ui/components/delete-confirmation-dialog";
import { CarrierConnectionDialog } from "@karrio/ui/components/carrier-connection-dialog";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { RateSheetDialog } from "@karrio/ui/components/rate-sheet-dialog";
import { RateSheetsTable } from "@karrio/admin/components/rate-sheets-table";
import { CarrierNameEnum } from "@karrio/types/graphql/admin/types";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { Plus, Search, X, Filter } from "lucide-react";
import { useSystemConnections, useSystemConnectionMutation } from "@karrio/hooks/admin-system-connections";
import { useRateSheets, useRateSheetMutation } from "@karrio/hooks/admin-rate-sheets";
import { Loader2 } from "lucide-react";
import { useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";

export default function CarrierNetwork() {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">
          Carriers Network
        </h1>
      </div>

      <div className="space-y-6">
        <CarrierConnectionManagement />
        <RateSheetManagement />
      </div>
    </div>
  );
}

function CarrierConnectionManagement() {
  const { toast } = useToast();
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedConnection, setSelectedConnection] = useState<Connection | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [filters, setFilters] = useState({
    active: undefined as boolean | undefined,
    search: "" as string,
    carrier_name: [] as string[],
  });

  const { query, system_carrier_connections } = useSystemConnections({
    offset: (page - 1) * pageSize,
    first: pageSize,
    active: filters.active,
    carrier_name: filters.carrier_name.length > 0 ? filters.carrier_name : undefined,
    metadata_key: filters.search || undefined,
    metadata_value: filters.search || undefined,
  });

  const connections = system_carrier_connections;
  const isLoading = query.isLoading;

  const { createSystemConnection, updateSystemConnection, deleteSystemConnection } = useSystemConnectionMutation();

  const handleCreateSuccess = () => {
    toast({ title: "Carrier connection created successfully" });
    setIsEditOpen(false);
    setSelectedConnection(null);
  };

  const handleUpdateSuccess = () => {
    toast({ title: "Carrier connection updated successfully" });
    setIsEditOpen(false);
    setSelectedConnection(null);
  };

  const handleDeleteSuccess = () => {
    toast({ title: "Carrier connection deleted successfully" });
    setIsDeleteOpen(false);
    setSelectedConnection(null);
  };

  const handleError = (error: any, action: string) => {
    toast({
      title: `Failed to ${action} carrier connection`,
      description: error.message || "An error occurred",
      variant: "destructive",
    });
  };

  const handleUpdate = (values: any) => {
    // Convert empty strings to undefined in credentials
    const credentials = Object.entries(values.credentials || {}).reduce((acc, [key, value]) => ({
      ...acc,
      [key]: value === "" ? undefined : value,
    }), {});

    // Convert empty strings to undefined in config
    const config = Object.entries(values.config || {}).reduce((acc, [key, value]) => ({
      ...acc,
      [key]: value === "" ? undefined : value,
    }), {});

    // Convert empty strings to undefined in metadata
    const metadata = Object.entries(values.metadata || {}).reduce((acc, [key, value]) => ({
      ...acc,
      [key]: value === "" ? undefined : value,
    }), {});

    if (selectedConnection) {
      // Update existing connection
      updateSystemConnection.mutate({
        id: selectedConnection.id,
        carrier_id: values.carrier_id === "" ? undefined : values.carrier_id,
        active: values.active,
        capabilities: values.capabilities,
        credentials,
        config,
        metadata,
      }, {
        onSuccess: handleUpdateSuccess,
        onError: (error) => handleError(error, "update")
      });
    } else {
      // Create new connection
      createSystemConnection.mutate({
        carrier_name: values.carrier_name,
        carrier_id: values.carrier_id === "" ? undefined : values.carrier_id,
        active: values.active,
        capabilities: values.capabilities,
        credentials,
        config,
        metadata,
      }, {
        onSuccess: handleCreateSuccess,
        onError: (error) => handleError(error, "create")
      });
    }
  };

  const handleCopy = async (text: string, description: string) => {
    try {
      await navigator.clipboard.writeText(text);
      toast({
        title: "Copied to clipboard",
        description,
      });
    } catch (error) {
      toast({
        title: "Failed to copy to clipboard",
        description: "Please copy the text manually",
        variant: "destructive",
      });
    }
  };

  // Reset page when filters change
  const handleFilterChange = (newFilters: typeof filters) => {
    setPage(1);
    setFilters(newFilters);
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>System Carrier Connections</CardTitle>
            <p className="text-sm text-muted-foreground">
              Manage system-wide carrier connections that are available to all organizations.
            </p>
          </div>
          <Button
            size="sm"
            onClick={() => {
              setSelectedConnection(null);
              setIsEditOpen(true);
            }}
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Connection
          </Button>
        </div>
      </CardHeader>
      <CardContent className="min-h-[40vh] relative space-y-4">
        <div className="flex items-center space-x-2">
          <div className="relative flex-1">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Filter tasks..."
              value={filters.search}
              onChange={(e) => handleFilterChange({
                ...filters,
                search: e.target.value,
              })}
              className="pl-8 pr-8"
            />
            {filters.search && (
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-0 top-0 h-9 w-9 hover:bg-transparent"
                onClick={() => handleFilterChange({
                  ...filters,
                  search: "",
                })}
              >
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>

          <Select
            value={filters.active === undefined ? "all" : filters.active ? "active" : "inactive"}
            onValueChange={(value) => handleFilterChange({
              ...filters,
              active: value === "all" ? undefined : value === "active",
            })}
          >
            <SelectTrigger className="w-[130px]">
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4" />
                <SelectValue placeholder="Status" />
              </div>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All</SelectItem>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="inactive">Inactive</SelectItem>
            </SelectContent>
          </Select>

          <Select
            value={filters.carrier_name.length === 1 ? filters.carrier_name[0] : "all"}
            onValueChange={(value) => handleFilterChange({
              ...filters,
              carrier_name: value === "all" ? [] : [value],
            })}
          >
            <SelectTrigger className="w-[130px]">
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4" />
                <SelectValue placeholder="Carrier" />
              </div>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All carriers</SelectItem>
              {Object.entries(CarrierNameEnum).map(([key, value]) => (
                <SelectItem key={value} value={value}>
                  {key.split('_').map(word => word.charAt(0) + word.slice(1).toLowerCase()).join(' ')}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {(filters.active !== undefined || filters.carrier_name.length > 0) && (
            <Button
              variant="ghost"
              className="h-9 px-3"
              onClick={() => handleFilterChange({
                ...filters,
                active: undefined,
                carrier_name: [],
              })}
            >
              Reset
              <X className="ml-2 h-4 w-4" />
            </Button>
          )}
        </div>

        {isLoading ? (
          <div className="absolute inset-0 flex items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <CarrierConnectionsTable
            onCreateNew={() => {
              setSelectedConnection(null);
              setIsEditOpen(true);
            }}
            connections={connections?.edges?.map(edge => ({
              ...edge.node,
              credentials: edge.node.credentials || {},
              config: edge.node.config || {},
              metadata: edge.node.metadata || {},
            }))}
            pagination={connections ? {
              count: connections.edges.length + ((page - 1) * pageSize),
              hasNext: connections.page_info.has_next_page,
              page,
              pageSize,
            } : undefined}
            onPageChange={setPage}
            onPageSizeChange={setPageSize}
            onEdit={(connection) => {
              setSelectedConnection(connection);
              setIsEditOpen(true);
            }}
            onDelete={(connection) => {
              setSelectedConnection(connection);
              setIsDeleteOpen(true);
            }}
            onStatusChange={(connection, active) => {
              updateSystemConnection.mutate({
                id: connection.id,
                active,
              });
            }}
            onCopy={handleCopy}
          />
        )}

        <CarrierConnectionDialog
          open={isEditOpen}
          onOpenChange={setIsEditOpen}
          selectedConnection={selectedConnection as any}
          onSubmit={handleUpdate}
        />

        <DeleteConfirmationDialog
          open={isDeleteOpen}
          onOpenChange={setIsDeleteOpen}
          title="Delete Connection"
          description="Are you sure you want to delete this carrier connection? This action cannot be undone."
          onConfirm={() => {
            if (selectedConnection) {
              deleteSystemConnection.mutate({
                id: selectedConnection.id,
              }, {
                onSuccess: handleDeleteSuccess,
                onError: (e) => handleError(e, "delete connection")
              });
            }
          }}
        />
      </CardContent>
    </Card>
  );
}

function RateSheetManagement() {
  const { toast } = useToast();
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedRateSheet, setSelectedRateSheet] = useState<RateSheet | null>(null);

  const { query, rate_sheets: rateSheetsData } = useRateSheets({});
  const rateSheets = rateSheetsData?.edges || [];
  const isLoading = query.isLoading;

  const { createRateSheet, updateRateSheet, deleteRateSheet } = useRateSheetMutation();

  const handleCreateSuccess = () => {
    toast({ title: "Rate sheet created successfully" });
    setIsEditOpen(false);
  };

  const handleUpdateSuccess = () => {
    toast({ title: "Rate sheet updated successfully" });
    setIsEditOpen(false);
    setSelectedRateSheet(null);
  };

  const handleDeleteSuccess = () => {
    toast({ title: "Rate sheet deleted successfully" });
    setIsDeleteOpen(false);
    setSelectedRateSheet(null);
  };

  const handleError = (error: any, action: string) => {
    toast({
      title: `Failed to ${action} rate sheet`,
      description: error.message || "An error occurred",
      variant: "destructive",
    });
  };

  const handleUpdate = async (values: any) => {
    const data = {
      ...values,
      services: JSON.stringify(values.services),
    };

    if (selectedRateSheet) {
      updateRateSheet.mutate({ ...data, id: selectedRateSheet.id }, {
        onSuccess: handleUpdateSuccess,
        onError: (e) => handleError(e, "update")
      });
    } else {
      createRateSheet.mutate(data, {
        onSuccess: handleCreateSuccess,
        onError: (e) => handleError(e, "create")
      });
    }
  };

  const handleCopy = async (text: string, description: string) => {
    try {
      await navigator.clipboard.writeText(text);
      toast({
        title: "Copied to clipboard",
        description,
      });
    } catch (error) {
      toast({
        title: "Failed to copy to clipboard",
        description: "Please copy the text manually",
        variant: "destructive",
      });
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center my-6">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Rate Sheets</CardTitle>
            <p className="text-sm text-muted-foreground">
              Manage custom rate sheets for your carrier network.
            </p>
          </div>
          <Button
            size="sm"
            onClick={() => {
              setSelectedRateSheet(null);
              setIsEditOpen(true);
            }}
          >
            <Plus className="mr-2 h-4 w-4" />
            Add Rate Sheet
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <RateSheetsTable
          rateSheets={rateSheets as { node: RateSheet }[]}
          onEdit={(sheet) => {
            setSelectedRateSheet(sheet);
            setIsEditOpen(true);
          }}
          onDelete={(sheet) => {
            setSelectedRateSheet(sheet);
            setIsDeleteOpen(true);
          }}
          onCopy={() => { }}
          onCreateNew={() => {
            setSelectedRateSheet(null);
            setIsEditOpen(true);
          }}
        />
      </CardContent>

      <RateSheetDialog
        open={isEditOpen}
        onOpenChange={setIsEditOpen}
        onSubmit={handleUpdate}
        selectedRateSheet={selectedRateSheet}
        isLoading={createRateSheet.isLoading || updateRateSheet.isLoading}
      />

      <DeleteConfirmationDialog
        open={isDeleteOpen}
        onOpenChange={setIsDeleteOpen}
        onConfirm={() => {
          if (selectedRateSheet) {
            deleteRateSheet.mutate({ id: selectedRateSheet.id }, {
              onSuccess: handleDeleteSuccess,
              onError: (e) => handleError(e, "delete")
            });
          }
        }}
        title="Delete Rate Sheet"
        description={`Are you sure you want to delete the rate sheet: ${selectedRateSheet?.name}?`}
      />
    </Card>
  );
}
