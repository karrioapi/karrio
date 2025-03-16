import { trpc } from "@karrio/trpc/client";
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
        metadata: values.metadata || {},
      },
    });
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
