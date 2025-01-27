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
import { useState } from "react";

export default function CarrierConnections() {
  const utils = trpc.useContext();
  const { toast } = useToast();
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedConnection, setSelectedConnection] = useState<Connection | null>(null);
  const [page, setPage] = useState(1);

  const { data: connections, isLoading } = trpc.admin.system_connections.list.useQuery({
    filter: {},
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
    updateConnection.mutate({
      data: {
        id: values.id,
        carrier_name: values.carrier_name,
        display_name: values.display_name,
        test_mode: values.test_mode,
        active: values.active,
        capabilities: values.capabilities,
        credentials: values.credentials || {},
        config: values.config || {},
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
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">
          Carrier Management
        </h1>
      </div>

      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>System Carrier Connections</CardTitle>
            <p className="text-sm text-muted-foreground">
              Manage system-wide carrier connections that are available to all organizations.
            </p>
          </CardHeader>
          <CardContent>
            <CarrierConnectionsTable
              onCreateNew={() => setIsEditOpen(true)}
              connections={connections?.edges?.map(edge => ({
                ...edge.node,
                credentials: edge.node.credentials || {},
                config: edge.node.config || {},
                metadata: edge.node.metadata || {},
              }))}
              pagination={connections ? {
                count: connections.edges.length,
                hasNext: connections.page_info.has_next_page,
                page,
              } : undefined}
              onPageChange={setPage}
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
                    carrier_name: connection.carrier_name,
                    display_name: connection.display_name || "",
                    test_mode: connection.test_mode,
                    capabilities: connection.capabilities || [],
                    credentials: connection.credentials || {},
                    config: connection.config || {},
                    metadata: connection.metadata || {},
                  },
                });
              }}
              onCopy={handleCopy}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Rate Sheets</CardTitle>
            <p className="text-sm text-muted-foreground">
              Manage carrier rate sheets and service configurations.
            </p>
          </CardHeader>
          <CardContent>
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
      <div className="mb-4 flex items-center justify-between">
        <Button onClick={() => setIsEditOpen(true)}>Add Rate Sheet</Button>
      </div>

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
