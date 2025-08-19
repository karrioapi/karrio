"use client";

import React, { useState, useMemo } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  Plus,
  Search,
  Filter,
  MoreHorizontal,
  Settings,
  Copy,
  Trash2,
  Edit3,
  Eye,
  FileText,
} from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { CarrierConnectionDialog } from "@karrio/ui/components/carrier-connection-dialog";
import { ConfirmationDialog } from "@karrio/ui/components/confirmation-dialog";
import { useCarrierConnections, useCarrierConnectionMutation, useCarrierConnectionForm } from "@karrio/hooks/user-connection";
import { useSystemConnections } from "@karrio/hooks/system-connection";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Switch } from "@karrio/ui/components/ui/switch";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { RateSheetEditor } from "@karrio/ui/components/rate-sheet-editor";
import { LinkRateSheetDialog } from "@karrio/ui/components/rate-sheet-dialog";
import { useRateSheets, useRateSheetMutation, useRateSheet } from "@karrio/hooks/rate-sheet";
import { cn } from "@karrio/ui/lib/utils";
import { supportsRateSheets } from "@karrio/lib/carrier-utils";
// Note: carrier-utils normalization removed; backend provides canonical names

export default function ConnectionsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { toast } = useToast();
  const [selectedTab, setSelectedTab] = useState("connections");
  const [carrierSearch, setCarrierSearch] = useState("");
  const [carrierFilter, setCarrierFilter] = useState("all");
  const [isConnectionDialogOpen, setIsConnectionDialogOpen] = useState(false);
  const [selectedConnection, setSelectedConnection] = useState<any>(null);
  const [isRateSheetDialogOpen, setIsRateSheetDialogOpen] = useState(false);
  const [selectedRateSheet, setSelectedRateSheet] = useState<any>(null);
  const [isLinkDialogOpen, setIsLinkDialogOpen] = useState(false);
  const [linkConnection, setLinkConnection] = useState<any>(null);

  // Hooks
  const { query: carrierQuery, user_connections } = useCarrierConnections();
  const { query: systemQuery, system_connections } = useSystemConnections();
  const { query: rateSheetsQuery, rate_sheets } = useRateSheets();
  const mutation = useCarrierConnectionMutation();
  const rateSheetMutation = useRateSheetMutation();
  const { handleSubmit: submitCarrierConnection } = useCarrierConnectionForm();
  const { references } = useAPIMetadata();

  const isLoading = carrierQuery.isLoading || systemQuery.isLoading;

  // Handle URL modal parameter
  React.useEffect(() => {
    const modal = searchParams.get("modal");
    if (modal === "new") {
      setSelectedConnection(null);
      setIsConnectionDialogOpen(true);
    }
  }, [searchParams]);

  // Convert connections data to proper format
  const userConnections = useMemo(() => {
    if (!user_connections) return [];
    return user_connections.map((connection) => ({
      ...connection,
      connection_type: "user"
    }));
  }, [user_connections]);

  const systemConnections = useMemo(() => {
    if (!system_connections) return [];
    return system_connections.map((connection) => ({
      ...connection,
      connection_type: "system"
    }));
  }, [system_connections]);

  // Filter connections
  const filteredConnections = useMemo(() => {
    const connections = selectedTab === "connections" ? userConnections : systemConnections;

    return connections.filter(connection => {
      const matchesSearch =
        connection.display_name?.toLowerCase().includes(carrierSearch.toLowerCase()) ||
        connection.carrier_name.toLowerCase().includes(carrierSearch.toLowerCase()) ||
        connection.carrier_id?.toLowerCase().includes(carrierSearch.toLowerCase());

      const matchesFilter = carrierFilter === 'all' ||
        (carrierFilter === 'active' && connection.active) ||
        (carrierFilter === 'inactive' && !connection.active);

      return matchesSearch && matchesFilter;
    });
  }, [selectedTab, userConnections, systemConnections, carrierSearch, carrierFilter]);

  const handleConnectionSuccess = () => {
    setIsConnectionDialogOpen(false);
    setSelectedConnection(null);
    // The cache invalidation is handled by the dialog's mutation hooks
  };

  const [confirmOpen, setConfirmOpen] = useState(false);
  const [pendingDelete, setPendingDelete] = useState<any>(null);
  const handleAskDelete = (connection: any) => {
    setPendingDelete(connection);
    setConfirmOpen(true);
  };
  const handleDeleteConfirmed = async () => {
    if (!pendingDelete) return;
    try {
      await mutation.deleteCarrierConnection.mutateAsync({ id: pendingDelete.id });
      toast({ title: "Carrier connection deleted successfully" });
    } catch (error: any) {
      toast({ title: "Error deleting connection", description: error.message || "An error occurred", variant: "destructive" });
    } finally {
      setPendingDelete(null);
    }
  };

  const copyToClipboard = (text: string | undefined) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    toast({ title: "Copied to clipboard" });
  };

  const handleToggleConnection = (connection: any, active: boolean) => {
    mutation.updateCarrierConnection.mutate({
      id: connection.id,
      active
    }, {
      onSuccess: () => {
        toast({
          title: `Connection ${active ? 'enabled' : 'disabled'} successfully`
        });
      },
      onError: (error: any) => {
        toast({
          title: "Error updating connection",
          description: error.message || "An error occurred",
          variant: "destructive",
        });
      }
    });
  };

  const handleOpenRateSheet = async (connection: any) => {
    try {
      // Prefer an explicitly linked sheet if present, otherwise find by carrier_name
      const existingSheet = rate_sheets?.edges?.find(({ node }) => (
        node.id === connection.rate_sheet?.id
      ));

      if (existingSheet) {
        setSelectedRateSheet(existingSheet.node);
      } else {
        // Create default rate sheet structure using the connection carrier_name
        setSelectedRateSheet({
          carrier_name: connection.carrier_name,
          name: `${connection.display_name} Rate Sheet`,
          services: [],
          carriers: [connection]
        });
      }

      setIsRateSheetDialogOpen(true);
    } catch (error: any) {
      toast({
        title: "Error opening rate sheet",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    }
  };

  const askLinkRateSheet = (connection: any) => {
    setLinkConnection(connection);
    setIsLinkDialogOpen(true);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading carrier connections...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Carrier Connections</h1>
          <p className="text-sm text-gray-600 mt-1">
            View and manage carrier connections
          </p>
        </div>
        <Button
          onClick={() => {
            setSelectedConnection(null);
            setIsConnectionDialogOpen(true);
          }}
        >
          <Plus className="mr-2 h-4 w-4" />
          Register Carrier
        </Button>
      </div>

      {/* Tab Navigation */}
      <div className="flex items-center justify-between border-b border-gray-200">
        <nav className="flex space-x-8 overflow-x-auto">
          <button
            className={cn(
              "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
              selectedTab === "connections"
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => setSelectedTab("connections")}
          >
            Your Accounts ({userConnections.length})
          </button>
          <button
            className={cn(
              "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
              selectedTab === "system"
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => setSelectedTab("system")}
          >
            <AppLink
              href={`/connections/system`}
              className="hover:text-inherit"
            >
              System Accounts ({systemConnections.length})
            </AppLink>
          </button>
          <button
            className={cn(
              "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
              selectedTab === "rate-sheets"
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => setSelectedTab("rate-sheets")}
          >
            <AppLink
              href={`/connections/rate-sheets`}
              className="hover:text-inherit"
            >
              Rate Sheets
            </AppLink>
          </button>
        </nav>
      </div>

      <div className="space-y-6">
        {/* Summary Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border shadow-none">
            <CardContent className="p-4">
              <p className="text-sm text-gray-600">Total Connections</p>
              <p className="text-2xl font-semibold text-gray-900">
                {filteredConnections.length}
              </p>
            </CardContent>
          </Card>

          <Card className="border shadow-none">
            <CardContent className="p-4">
              <p className="text-sm text-gray-600">Active Connections</p>
              <p className="text-2xl font-semibold text-gray-900">
                {filteredConnections.filter(c => c.active).length}
              </p>
            </CardContent>
          </Card>

          <Card className="border shadow-none">
            <CardContent className="p-4">
              <p className="text-sm text-gray-600">Test Mode</p>
              <p className="text-2xl font-semibold text-gray-900">
                {filteredConnections.filter(c => c.test_mode).length}
              </p>
            </CardContent>
          </Card>

          <Card className="border shadow-none">
            <CardContent className="p-4">
              <p className="text-sm text-gray-600">Unique Carriers</p>
              <p className="text-2xl font-semibold text-gray-900">
                {new Set(filteredConnections.map(c => c.carrier_name)).size}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Carriers Header */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-medium text-gray-900">
              {selectedTab === "connections" ? "Your Carrier Connections" : "System Connections"}
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              {filteredConnections.length} total connections
            </p>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 p-4 bg-gray-50 rounded-lg">
          <div className="flex-1">
            <div className="flex h-9 w-full items-center rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2">
              <Search className="h-4 w-4 text-muted-foreground mr-2 flex-shrink-0" />
              <Input
                placeholder="Search carriers..."
                value={carrierSearch}
                onChange={(e) => setCarrierSearch(e.target.value)}
                className="flex-1 bg-transparent border-0 px-0 py-0 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-0 focus-visible:ring-0 disabled:cursor-not-allowed disabled:opacity-50"
                autoComplete="off"
              />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-gray-500" />
            <Select value={carrierFilter} onValueChange={setCarrierFilter}>
              <SelectTrigger className="w-full sm:w-[120px] h-9">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="inactive">Inactive</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Connections List */}
        {filteredConnections.length === 0 ? (
          <div className="text-center py-12">
            <div className="mx-auto mb-4 text-gray-400">
              <Settings className="h-12 w-12 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-500 mb-2">
              No connections found
            </h3>
            <p className="text-sm text-gray-400 mb-4">
              {carrierSearch || carrierFilter !== 'all'
                ? "No connections match your current filters."
                : "Get started by registering your first carrier connection."
              }
            </p>
            {!carrierSearch && carrierFilter === 'all' && (
              <Button onClick={() => {
                setSelectedConnection(null);
                setIsConnectionDialogOpen(true);
              }}>
                <Plus className="mr-2 h-4 w-4" />
                Register Your First Carrier
              </Button>
            )}
          </div>
        ) : (
          <div className="space-y-3">
            {filteredConnections.map((connection) => (
              <div
                key={connection.id}
                className="group relative flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all duration-200 bg-white gap-3"
              >
                {/* Main Content */}
                <div className="flex items-start sm:items-center gap-3 flex-1 w-full sm:w-auto">
                  {/* Carrier Logo */}
                  <div className="flex-shrink-0">
                    <CarrierImage
                      carrier_name={connection.credentials?.custom_carrier_name || connection.carrier_name}
                      width={48}
                      height={48}
                      className="rounded-lg"
                      text_color={connection.config?.text_color}
                      background={connection.config?.brand_color}
                    />
                  </div>

                  {/* Carrier Details */}
                  <div className="flex-1 min-w-0">
                    {/* Row 1: Name and Status */}
                    <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                      <h3 className="font-medium text-gray-900 text-base">
                        {connection.display_name || connection.carrier_name}
                      </h3>
                      <div className="flex items-center gap-1.5">
                        <StatusBadge status={connection.active ? "active" : "inactive"} />
                        {connection.test_mode && (
                          <StatusBadge status="test" />
                        )}
                      </div>
                    </div>

                    {/* Row 2: Carrier ID and Capabilities */}
                    <div className="flex flex-col sm:flex-row sm:items-center gap-2 text-sm">
                      <div className="flex items-center gap-1.5">
                        <span className="text-gray-600 font-mono">
                          {connection.carrier_id}
                        </span>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-4 w-4 p-0 hover:bg-gray-100 opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={() => copyToClipboard(connection.carrier_id)}
                        >
                          <Copy className="h-3 w-3" />
                        </Button>
                      </div>
                      <span className="hidden sm:inline text-gray-400">•</span>
                      <div className="flex flex-wrap gap-1">
                        {connection.capabilities && connection.capabilities.length > 0 ? (
                          <>
                            {connection.capabilities.slice(0, 2).map((capability) => (
                              <span
                                key={capability}
                                className="text-xs px-2 py-0.5 bg-gray-100 text-gray-700 rounded"
                              >
                                {capability}
                              </span>
                            ))}
                            {connection.capabilities.length > 2 && (
                              <span
                                className="text-xs px-2 py-0.5 border border-gray-300 text-gray-600 rounded"
                              >
                                +{connection.capabilities.length - 2}
                              </span>
                            )}
                          </>
                        ) : (
                          <span className="text-xs text-gray-500 italic">No capabilities</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
                  {/* Toggle Switch */}
                  <div className="flex items-center gap-2">
                    <Switch
                      checked={connection.active}
                      onCheckedChange={(checked) => handleToggleConnection(connection, checked)}
                    />
                  </div>

                  {/* Rate Sheet Button - Only show for user connections and compatible carriers */}
                  {connection.connection_type === "user" && supportsRateSheets(connection, references) && (
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-9 w-9 hover:bg-muted"
                      onClick={() => handleOpenRateSheet(connection)}
                      title="Manage Rate Sheet"
                    >
                      <FileText className="h-4 w-4" />
                    </Button>
                  )}

                  {/* Menu - Only show for user connections */}
                  {connection.connection_type === "user" && (
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-9 w-9 hover:bg-muted"
                        >
                          <MoreHorizontal className="h-4 w-4" />
                          <span className="sr-only">Open menu</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        {supportsRateSheets(connection, references) && (
                          <DropdownMenuItem onClick={() => askLinkRateSheet(connection)}>
                            <FileText className="mr-2 h-4 w-4" />
                            Link Rate Sheet
                          </DropdownMenuItem>
                        )}
                        <DropdownMenuItem onClick={() => {
                          setSelectedConnection(connection);
                          setIsConnectionDialogOpen(true);
                        }}>
                          <Edit3 className="mr-2 h-4 w-4" />
                          Edit Connection
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => copyToClipboard(connection.id)}>
                          <Copy className="mr-2 h-4 w-4" />
                          Copy ID
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem
                          className="text-red-600"
                          onClick={() => handleAskDelete(connection)}
                        >
                          <Trash2 className="mr-2 h-4 w-4" />
                          Delete Connection
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  )}
                </div>

                {/* Connection Line Indicator */}
                <div className={`absolute left-0 top-0 bottom-0 w-1 rounded-l-lg ${connection.active
                  ? connection.test_mode
                    ? "bg-yellow-500"
                    : "bg-green-500"
                  : "bg-gray-300"
                  }`} />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Connection Dialog */}
      <CarrierConnectionDialog
        open={isConnectionDialogOpen}
        onOpenChange={setIsConnectionDialogOpen}
        selectedConnection={selectedConnection}
        onSuccess={handleConnectionSuccess}
        onSubmit={submitCarrierConnection}
        references={references}
      />

      <ConfirmationDialog
        open={confirmOpen}
        onOpenChange={setConfirmOpen}
        title="Delete Connection"
        description={`Are you sure you want to delete ${pendingDelete?.display_name || pendingDelete?.carrier_name}? This action cannot be undone.`}
        confirmLabel="Delete"
        onConfirm={handleDeleteConfirmed}
      />

      {/* Rate Sheet Editor */}
      {isRateSheetDialogOpen && selectedRateSheet && (
        <RateSheetEditor
          rateSheetId={selectedRateSheet?.id || 'new'}
          onClose={() => {
            setIsRateSheetDialogOpen(false);
            setSelectedRateSheet(null);
            rateSheetsQuery.refetch();
          }}
          preloadCarrier={selectedRateSheet?.carrier_name}
          linkConnectionId={selectedRateSheet?.carriers?.[0]?.id}
          isAdmin={false}
          useRateSheet={useRateSheet}
          useRateSheetMutation={useRateSheetMutation}
        />
      )}

      {/* Link to existing Rate Sheet */}
      {isLinkDialogOpen && linkConnection && (
        <LinkRateSheetDialog
          open={isLinkDialogOpen}
          onOpenChange={setIsLinkDialogOpen}
          connection={{ id: linkConnection.id, carrier_name: linkConnection.carrier_name, display_name: linkConnection.display_name }}
          rateSheets={(rate_sheets?.edges || []).map(({ node }) => node).filter((rs) => rs.carrier_name === linkConnection.carrier_name)}
          linkedRateSheets={(rate_sheets?.edges || []).map(({ node }) => node).filter((rs) => (rs.carriers || []).some((c: any) => c.id === linkConnection.id))}
          onEditRateSheet={(id: string) => {
            const rs = (rate_sheets?.edges || []).map(({ node }) => node).find((r) => r.id === id);
            if (rs) {
              setSelectedRateSheet(rs);
              setIsRateSheetDialogOpen(true);
            }
          }}
          onCreateNew={() => {
            setSelectedRateSheet({ carrier_name: linkConnection.carrier_name, name: `${linkConnection.display_name || linkConnection.carrier_name} Rate Sheet`, services: [], carriers: [linkConnection] });
            setIsRateSheetDialogOpen(true);
          }}
          onLink={async ({ connection_id, rate_sheet_id }) => {
            const sheet = (rate_sheets?.edges || []).map(({ node }) => node).find((rs) => rs.id === rate_sheet_id);
            const existing = (sheet?.carriers || []).map((c: any) => c.id);
            const carriers = Array.from(new Set([...(existing || []), connection_id]));
            await rateSheetMutation.updateRateSheet.mutateAsync({ id: rate_sheet_id, carriers });
            toast({ title: "Linked to rate sheet" });
            setIsLinkDialogOpen(false);
            rateSheetsQuery.refetch();
          }}
        />
      )}
    </div>
  );
}
