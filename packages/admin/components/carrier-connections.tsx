import {
  useSystemConnections,
  useSystemConnectionMutation,
} from "@karrio/hooks/admin-system-connections";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { CarrierConnectionDialog } from "@karrio/ui/components/carrier-connection-dialog";
import { DeleteConfirmationDialog } from "@karrio/ui/components/delete-confirmation-dialog";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useState } from "react";
import { CarrierConnectionsTable } from "@karrio/admin/components/carrier-connections-table";
import { GetSystemConnections_system_carrier_connections_edges_node } from "@karrio/types/graphql/admin/types";

type Connection = Omit<GetSystemConnections_system_carrier_connections_edges_node, 'credentials' | 'config' | 'metadata'> & {
  credentials: Record<string, any>;
  config: Record<string, any>;
  metadata: Record<string, any>;
};

export default function CarrierConnections() {
  const { toast } = useToast();
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedConnection, setSelectedConnection] = useState<Connection | null>(null);
  const [page, setPage] = useState(1);

  const { query, system_carrier_connections: connectionsData } = useSystemConnections({});
  const { updateSystemConnection, deleteSystemConnection } = useSystemConnectionMutation();

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
      description: error.message,
      variant: "destructive",
    });
  };

  const handleUpdate = (values: any) => {
    updateSystemConnection.mutate(values, {
      onSuccess: handleUpdateSuccess,
      onError: (error) => handleError(error, "update"),
    });
  };

  const connections = connectionsData;

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">
          Carrier Management
        </h1>
      </div>

      <div className="space-y-6">
        <Card>
          <CardContent className="p-6">
            <CarrierConnectionsTable
              title="Carrier Connections"
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
                updateSystemConnection.mutate({
                  id: connection.id,
                  active,
                });
              }}
              onCopy={(text, description) => {
                navigator.clipboard.writeText(text);
                toast({
                  title: "Copied to clipboard",
                  description,
                });
              }}
            />
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
            deleteSystemConnection.mutate({ id: selectedConnection.id }, {
              onSuccess: handleDeleteSuccess,
              onError: (error) => handleError(error, "delete"),
            });
          }
        }}
      />
    </div>
  );
}
