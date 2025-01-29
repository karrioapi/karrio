"use client";

import { CarrierConnectionsTable, Connection } from "@karrio/admin/components/carrier-connections-table";
import { GetRateSheets_rate_sheets_edges_node as RateSheet } from "@karrio/types/graphql/admin/types";
import { DeleteConfirmationDialog } from "@karrio/insiders/components/delete-confirmation-dialog";
import { CarrierConnectionDialog } from "@karrio/insiders/components/carrier-connection-dialog";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/insiders/components/ui/card";
import { RateSheetDialog } from "@karrio/insiders/components/rate-sheet-dialog";
import { RateSheetsTable } from "@karrio/admin/components/rate-sheets-table";
import { Button } from "@karrio/insiders/components/ui/button";
import { useToast } from "@karrio/insiders/hooks/use-toast";
import { trpc } from "@karrio/trpc/client";
import { Plus, Search, X, Filter } from "lucide-react";
import { useState } from "react";
import { Loader2 } from "lucide-react";
import { Input } from "@karrio/insiders/components/ui/input";
import { Label } from "@karrio/insiders/components/ui/label";
import { CarrierNameEnum } from "@karrio/types/graphql/admin/types";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/insiders/components/ui/select";

export default function CarrierConnections() {
  const utils = trpc.useContext();
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

  const { data: connections, isLoading } = trpc.admin.system_connections.list.useQuery({
    filter: {
      offset: (page - 1) * pageSize,
      first: pageSize,
      active: filters.active,
      carrier_name: filters.carrier_name.length > 0 ? filters.carrier_name : undefined,
      metadata_key: filters.search || undefined,
      metadata_value: filters.search || undefined,
    },
  });

  const createConnection = trpc.admin.system_connections.create.useMutation({
    onSuccess: () => {
      toast({ title: "Carrier connection created successfully" });
      setIsEditOpen(false);
      setSelectedConnection(null);
      utils.admin.system_connections.list.invalidate();
    },
    onError: (error) => {
      toast({
        title: "Failed to create carrier connection",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const updateConnection = trpc.admin.system_connections.update.useMutation({
    onSuccess: () => {
      toast({ title: "Carrier connection updated successfully" });
      setIsEditOpen(false);
      setSelectedConnection(null);
      utils.admin.system_connections.list.invalidate();
    },
    onError: (error) => {
      toast({
        title: "Failed to update carrier connection",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const deleteConnection = trpc.admin.system_connections.delete.useMutation({
    onSuccess: () => {
      toast({ title: "Carrier connection deleted successfully" });
      setIsDeleteOpen(false);
      setSelectedConnection(null);
      utils.admin.system_connections.list.invalidate();
    },
    onError: (error) => {
      toast({
        title: "Failed to delete carrier connection",
        description: error.message,
        variant: "destructive",
      });
    },
  });

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
      updateConnection.mutate({
        data: {
          id: selectedConnection.id,
          carrier_id: values.carrier_id === "" ? undefined : values.carrier_id,
          active: values.active,
          capabilities: values.capabilities,
          credentials,
          config,
          metadata,
        },
      });
    } else {
      // Create new connection
      createConnection.mutate({
        data: {
          carrier_name: values.carrier_name,
          carrier_id: values.carrier_id === "" ? undefined : values.carrier_id,
          active: values.active,
          capabilities: values.capabilities,
          credentials,
          config,
          metadata,
        },
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
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">
          Carrier Management
        </h1>
      </div>

      <div className="space-y-6">
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
                size="icon"
                onClick={() => {
                  setSelectedConnection(null);
                  setIsEditOpen(true);
                }}
                className="h-8 w-8"
              >
                <Plus className="h-4 w-4" />
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
                    <span>Status</span>
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
                    <span>Carrier</span>
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
                  updateConnection.mutate({
                    data: {
                      id: connection.id,
                      active,
                    },
                  });
                }}
                onCopy={handleCopy}
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Rate Sheets</CardTitle>
                <p className="text-sm text-muted-foreground">
                  Manage carrier rate sheets and service configurations.
                </p>
              </div>
              <Button
                size="icon"
                onClick={() => setIsEditOpen(true)}
                className="h-8 w-8"
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent className="min-h-[40vh] relative">
            <RateSheets />
          </CardContent>
        </Card>
      </div>

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
            deleteConnection.mutate({
              data: {
                id: selectedConnection.id,
              },
            });
          }
        }}
      />
    </div>
  );
}

function RateSheets() {
  const utils = trpc.useContext();
  const { toast } = useToast();
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedRateSheet, setSelectedRateSheet] = useState<RateSheet | null>(null);

  const { data: rateSheets, isLoading } = trpc.admin.rate_sheets.list.useQuery({
    filter: {},
  });

  const updateRateSheet = trpc.admin.rate_sheets.update.useMutation({
    onSuccess: () => {
      toast({ title: "Rate sheet updated successfully" });
      setIsEditOpen(false);
      setSelectedRateSheet(null);
      utils.admin.rate_sheets.list.invalidate();
    },
    onError: (error) => {
      toast({
        title: "Failed to update rate sheet",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const deleteRateSheet = trpc.admin.rate_sheets.delete.useMutation({
    onSuccess: () => {
      toast({ title: "Rate sheet deleted successfully" });
      setIsDeleteOpen(false);
      setSelectedRateSheet(null);
      utils.admin.rate_sheets.list.invalidate();
    },
    onError: (error) => {
      toast({
        title: "Failed to delete rate sheet",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleUpdate = async (values: any) => {
    return updateRateSheet.mutateAsync({
      data: {
        id: values.id,
        name: values.name,
        carrier_name: values.carrier_name,
        services: values.services,
      },
    });
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

  return (
    <div>
      {isLoading ? (
        <div className="absolute inset-0 flex items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      ) : (
        <RateSheetsTable
          rateSheets={rateSheets?.edges as { node: RateSheet }[]}
          onEdit={(sheet) => {
            const rateSheetWithMetadata = {
              ...sheet,
              metadata: sheet.metadata || {},
            };
            setSelectedRateSheet(rateSheetWithMetadata);
            setIsEditOpen(true);
          }}
          onDelete={(sheet) => {
            const rateSheetWithMetadata = {
              ...sheet,
              metadata: sheet.metadata || {},
            };
            setSelectedRateSheet(rateSheetWithMetadata);
            setIsDeleteOpen(true);
          }}
          onCopy={handleCopy}
        />
      )}

      <RateSheetDialog
        open={isEditOpen}
        onOpenChange={setIsEditOpen}
        selectedRateSheet={selectedRateSheet}
        onSubmit={handleUpdate}
      />

      <DeleteConfirmationDialog
        open={isDeleteOpen}
        onOpenChange={setIsDeleteOpen}
        title="Delete Rate Sheet"
        description="Are you sure you want to delete this rate sheet? This action cannot be undone."
        onConfirm={() => {
          if (selectedRateSheet) {
            deleteRateSheet.mutate({
              data: { id: selectedRateSheet.id },
            });
          }
        }}
      />
    </div>
  );
}
