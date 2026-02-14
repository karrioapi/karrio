import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { KarrioEmbedProvider } from "../providers/karrio-embed-provider";
import { APIMetadataEmbedProvider } from "../providers/api-metadata-embed-provider";
import { useAPIMetadata } from "../providers/api-metadata-embed-provider";
import { CarrierConnectionDialog } from "@karrio/ui/components/carrier-connection-dialog";
import { useCarrierConnections, useCarrierConnectionForm } from "@karrio/hooks/user-connection";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import RateSheetEditor from "@karrio/ui/components/rate-sheet-editor";
import { useRateSheet, useRateSheetMutation } from "../hooks/embed-rate-sheet";
import { Toaster } from "@karrio/ui/components/ui/toaster";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Plus, Pencil, Trash2, Loader2, FileSpreadsheet } from "lucide-react";
import "../styles/globals.css";

interface InitConfig {
  host: string;
  token: string;
  admin?: boolean;
  connectionId?: string;
  carrier?: string;
}

function ConnectionsApp({ config }: { config: InitConfig }) {
  const { references } = useAPIMetadata();
  const { query, user_connections } = useCarrierConnections();
  const { handleSubmit, mutation } = useCarrierConnectionForm();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedConnection, setSelectedConnection] = useState<any>(null);
  const [rateSheetView, setRateSheetView] = useState<{
    rateSheetId: string;
    carrier: string;
    connectionId: string;
  } | null>(null);

  // If a specific connectionId was provided, open it for editing once data loads
  useEffect(() => {
    if (config.connectionId && user_connections.length > 0 && !dialogOpen) {
      const conn = user_connections.find((c: any) => c.id === config.connectionId);
      if (conn) {
        setSelectedConnection(conn);
        setDialogOpen(true);
      }
    }
  }, [config.connectionId, user_connections]);

  // If carrier is specified and no connectionId, open the add dialog with carrier pre-selected
  useEffect(() => {
    if (config.carrier && !config.connectionId && !dialogOpen) {
      setDialogOpen(true);
    }
  }, [config.carrier]);

  const handleAdd = () => {
    setSelectedConnection(null);
    setDialogOpen(true);
  };

  const handleEdit = (connection: any) => {
    setSelectedConnection(connection);
    setDialogOpen(true);
  };

  const handleDelete = async (connection: any) => {
    try {
      await mutation.deleteCarrierConnection.mutateAsync({ id: connection.id });
      notifyHost("save", { action: "delete", connectionId: connection.id });
    } catch {
      // Error handling via toast
    }
  };

  const handleFormSubmit = async (values: any, conn: any) => {
    await handleSubmit(values, conn);
    notifyHost("save", {
      action: conn ? "update" : "create",
      carrier_name: values.carrier_name,
      carrier_id: values.carrier_id,
    });
  };

  const handleDialogClose = (open: boolean) => {
    setDialogOpen(open);
    if (!open) {
      setSelectedConnection(null);
    }
  };

  const handleSuccess = () => {
    query.refetch();
  };

  const notifyHost = (event: string, payload?: any) => {
    window.parent.postMessage(
      { source: "karrio-embed", type: "EVENT", event, payload },
      "*",
    );
  };

  if (query.isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  // Show rate sheet editor when a rate sheet is selected
  if (rateSheetView) {
    return (
      <div className="bg-background text-foreground min-h-screen">
        <RateSheetEditor
          rateSheetId={rateSheetView.rateSheetId || "new"}
          onClose={() => {
            setRateSheetView(null);
            query.refetch();
          }}
          preloadCarrier={rateSheetView.carrier}
          linkConnectionId={rateSheetView.connectionId}
          isAdmin={config.admin}
          useRateSheet={useRateSheet}
          useRateSheetMutation={useRateSheetMutation}
        />
        <Toaster />
      </div>
    );
  }

  return (
    <div className="bg-background text-foreground min-h-screen">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-semibold">Carrier Connections</h2>
            <p className="text-sm text-muted-foreground">
              Manage your carrier account integrations
            </p>
          </div>
          <Button onClick={handleAdd} size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Add Connection
          </Button>
        </div>

        {/* Connections List */}
        {user_connections.length === 0 ? (
          <div className="rounded-lg border border-dashed p-8 text-center">
            <p className="text-sm text-muted-foreground mb-4">
              No carrier connections configured yet.
            </p>
            <Button onClick={handleAdd} variant="outline" size="sm">
              <Plus className="h-4 w-4 mr-2" />
              Add your first connection
            </Button>
          </div>
        ) : (
          <div className="rounded-lg border divide-y">
            {user_connections.map((connection: any) => (
              <div
                key={connection.id}
                className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <CarrierImage
                    carrier_name={connection.carrier_name}
                    width={32}
                    height={32}
                    containerClassName=""
                  />
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-sm">
                        {connection.carrier_id}
                      </span>
                      <Badge
                        variant={connection.active ? "default" : "secondary"}
                        className="text-[10px] px-1.5 py-0"
                      >
                        {connection.active ? "Active" : "Inactive"}
                      </Badge>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {(references as any)?.carriers?.[connection.carrier_name] || connection.carrier_name}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-1">
                  {connection.rate_sheet && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setRateSheetView({
                        rateSheetId: connection.rate_sheet?.id,
                        carrier: connection.carrier_name,
                        connectionId: connection.id,
                      })}
                      className="h-8 w-8 p-0"
                      title="Edit rate sheet"
                    >
                      <FileSpreadsheet className="h-4 w-4" />
                    </Button>
                  )}
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleEdit(connection)}
                    className="h-8 w-8 p-0"
                  >
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(connection)}
                    className="h-8 w-8 p-0 text-muted-foreground hover:text-destructive"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Connection Dialog */}
      <CarrierConnectionDialog
        open={dialogOpen}
        onOpenChange={handleDialogClose}
        selectedConnection={selectedConnection}
        references={references}
        onSubmit={handleFormSubmit}
        onSuccess={handleSuccess}
      />

      <Toaster />
    </div>
  );
}

function App() {
  const [config, setConfig] = useState<InitConfig | null>(null);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      const { data } = event;
      if (data?.source !== "karrio-host") return;

      if (data.type === "INIT") {
        setConfig({
          host: data.host,
          token: data.token,
          admin: data.admin ?? false,
          connectionId: data.connectionId,
          carrier: data.carrier,
        });
      }
    };

    window.addEventListener("message", handleMessage);

    // Signal to host that iframe is ready to receive INIT
    window.parent.postMessage(
      { source: "karrio-embed", type: "READY" },
      "*",
    );

    return () => window.removeEventListener("message", handleMessage);
  }, []);

  useEffect(() => {
    // Auto-resize: notify host of iframe content height changes
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        window.parent.postMessage(
          {
            source: "karrio-embed",
            type: "RESIZE",
            height: entry.contentRect.height,
          },
          "*",
        );
      }
    });

    observer.observe(document.body);
    return () => observer.disconnect();
  }, []);

  if (!config) {
    return (
      <div className="flex items-center justify-center h-screen bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-400" />
      </div>
    );
  }

  return (
    <KarrioEmbedProvider host={config.host} token={config.token} admin={config.admin}>
      <APIMetadataEmbedProvider>
        <ConnectionsApp config={config} />
      </APIMetadataEmbedProvider>
    </KarrioEmbedProvider>
  );
}

const root = createRoot(document.getElementById("root")!);
root.render(<App />);
