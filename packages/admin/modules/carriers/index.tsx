"use client";

import React, { useState, useMemo } from 'react';
import { useRateSheet as useAdminRateSheet, useRateSheetMutation as useAdminRateSheetMutation } from "@karrio/hooks/admin-rate-sheets";
import { useMarkups, useMarkupMutation } from "@karrio/hooks/admin-markups";
import { GetSystemConnections_system_carrier_connections_edges_node as Connection } from "@karrio/types/graphql/admin/types";
import { useSystemConnections, useSystemConnectionMutation } from "@karrio/hooks/admin-system-connections";
import { GetRateSheets_rate_sheets_edges_node as RateSheet } from "@karrio/types/graphql/admin/types";
import { DeleteConfirmationDialog } from "@karrio/ui/components/delete-confirmation-dialog";
import { CarrierConnectionDialog } from "@karrio/ui/components/carrier-connection-dialog";
import { useRateSheets, useRateSheetMutation } from "@karrio/hooks/admin-rate-sheets";
import { RateSheetEditor } from "@karrio/ui/components/rate-sheet-editor";
import { LinkRateSheetDialog } from "@karrio/ui/components/rate-sheet-dialog";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Button } from "@karrio/ui/components/ui/button";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Input } from "@karrio/ui/components/ui/input";
import { useToast } from "@karrio/ui/hooks/use-toast";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import {
  Plus,
  Search,
  Filter,
  MoreHorizontal,
  Copy,
  Trash2,
  Edit3,
  X,
  Loader2,
  Network,
  FileText,
} from 'lucide-react';
import { cn } from "@karrio/ui/lib/utils";
import { supportsRateSheets, getEffectiveCarrierName, isGenericCarrier } from "@karrio/lib/carrier-utils";

export default function CarrierNetwork() {
  const [selectedTab, setSelectedTab] = useState("connections");

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Carrier Network
          </h1>
          <p className="text-muted-foreground">
            Manage system-wide carrier connections and custom rate sheets
          </p>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b">
        <nav className="flex space-x-8">
          <button
            className={cn(
              "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
              selectedTab === "connections"
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => setSelectedTab("connections")}
          >
            System Connections
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
            Rate Sheets
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="mt-6">
        {selectedTab === "connections" && <CarrierConnectionManagement />}
        {selectedTab === "rate-sheets" && <RateSheetManagement />}
      </div>
    </div>
  );
}

function CarrierConnectionManagement() {
  const { toast } = useToast();
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedConnection, setSelectedConnection] = useState<Connection | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [carrierFilter, setCarrierFilter] = useState("all");
  const [isLinkDialogOpen, setIsLinkDialogOpen] = useState(false);
  const [linkConnection, setLinkConnection] = useState<Connection | null>(null);
  const [isRateSheetEditorOpen, setIsRateSheetEditorOpen] = useState(false);
  const [selectedRateSheet, setSelectedRateSheet] = useState<RateSheet | null>(null);
  const [selectedRateSheetId, setSelectedRateSheetId] = useState<string | null>(null);

  const { query: connectionsQuery, system_connections } = useSystemConnections({});
  const { query: rateSheetsQuery, rate_sheets } = useRateSheets({});
  const isLoading = connectionsQuery.isLoading || rateSheetsQuery.isLoading;
  const { references } = useAPIMetadata();

  const { createSystemConnection, updateSystemConnection, deleteSystemConnection } = useSystemConnectionMutation();
  const rateSheetMutation = useRateSheetMutation();
  const { markups: markupsData } = useMarkups();
  const markupMutationHooks = useMarkupMutation();
  const adminMarkupsList = useMemo(
    () => markupsData?.edges?.map((e: any) => e.node) || [],
    [markupsData]
  );

  // Helper function to get the correct carrier name for rate sheets
  const getRateSheetCarrierName = (connection: Connection): string => {
    // Freeze to the connection's own carrier_name; generic stays "generic"
    return connection.carrier_name;
  };

  // Filter connections
  const filteredConnections = useMemo(() => {
    return system_connections.filter((connection) => {
      const matchesSearch =
        connection.display_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        connection.carrier_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        connection.carrier_id?.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesStatus = statusFilter === 'all' ||
        (statusFilter === 'active' && connection.active) ||
        (statusFilter === 'inactive' && !connection.active);

      const matchesCarrier = carrierFilter === 'all' || connection.carrier_name === carrierFilter;

      return matchesSearch && matchesStatus && matchesCarrier;
    });
  }, [system_connections, searchQuery, statusFilter, carrierFilter]);

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

  const handleUpdate = async (values: any, connection: Connection | null) => {
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

    // Handle custom carriers: if carrier_name is not a standard carrier, treat it as a generic carrier
    const isCustomCarrier = values.carrier_name && !references?.carriers?.[values.carrier_name];
    let finalCarrierName = values.carrier_name;
    let finalCredentials = credentials;

    if (isCustomCarrier) {
      // For custom carriers, use "generic" as carrier_name and store the custom name in credentials
      finalCarrierName = "generic";
      finalCredentials = {
        ...credentials,
        custom_carrier_name: values.carrier_name,
      };
    }

    if (connection) {
      // Update existing connection
      await updateSystemConnection.mutateAsync({
        id: connection.id,
        carrier_id: values.carrier_id === "" ? undefined : values.carrier_id,
        active: values.active,
        capabilities: values.capabilities,
        credentials: finalCredentials,
        config,
        metadata,
      });
    } else {
      // Create new connection
      await createSystemConnection.mutateAsync({
        carrier_name: finalCarrierName,
        carrier_id: values.carrier_id === "" ? undefined : values.carrier_id,
        active: values.active,
        capabilities: values.capabilities,
        credentials: finalCredentials,
        config,
        metadata,
      });
    }
  };

  const handleStatusToggle = (connection: Connection, active: boolean) => {
    updateSystemConnection.mutate({
      id: connection.id,
      active,
    }, {
      onSuccess: () => {
        toast({
          title: `Connection ${active ? 'activated' : 'deactivated'} successfully`
        });
      },
      onError: (error) => handleError(error, "update status")
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

  const clearFilters = () => {
    setSearchQuery("");
    setStatusFilter("all");
    setCarrierFilter("all");
  };

  const askLinkRateSheet = (connection: Connection) => {
    setLinkConnection(connection);
    setIsLinkDialogOpen(true);
  };

  const openRateSheetEditor = async (connection: Connection) => {
    try {
      // Check if carrier supports rate sheets using centralized utility
      if (!supportsRateSheets(connection, references)) {
        toast({
          title: "Rate sheets not available for this carrier",
          description: "This carrier does not support custom rate sheets",
          variant: "destructive",
        });
        return;
      }

      // Freeze to the connection's carrier_name and preload this in the editor
      const rateSheetCarrierName = getRateSheetCarrierName(connection);

      const existingSheet = rate_sheets?.edges?.find(
        ({ node }) => node.id === connection.rate_sheet?.id
      );

      if (existingSheet) {
        setSelectedRateSheetId(existingSheet.node.id);
      } else {
        // Create default rate sheet structure using the correct carrier name
        const displayName = connection.display_name ||
          (connection.credentials?.custom_carrier_name && isGenericCarrier(connection)
            ? connection.credentials.custom_carrier_name
            : connection.carrier_name);

        setSelectedRateSheet({
          carrier_name: rateSheetCarrierName,
          name: `${displayName} Rate Sheet`,
          // carry the connection id so the editor can link it on create
          carriers: [{ id: connection.id }] as any,
        } as RateSheet);
        setSelectedRateSheetId('new');
      }
      setIsRateSheetEditorOpen(true);
    } catch (error: any) {
      toast({
        title: "Error opening rate sheet",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    }
  };

  const hasActiveFilters = searchQuery || statusFilter !== "all" || carrierFilter !== "all";

  return (
    <div className="space-y-6">
      {/* Header and Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-medium text-gray-900">System Carrier Connections</h2>
          <p className="text-sm text-gray-500 mt-1">
            Manage carrier connections available to all organizations
          </p>
        </div>
        <Button onClick={() => {
          setSelectedConnection(null);
          setIsEditOpen(true);
        }}>
          <Plus className="h-4 w-4 mr-2" />
          Add Connection
        </Button>
      </div>

      {/* Search and Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-3 p-4 bg-gray-50 rounded-lg">
        <div className="flex-1">
          <div className="flex h-9 w-full items-center rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2">
            <Search className="h-4 w-4 text-muted-foreground mr-2 flex-shrink-0" />
            <Input
              placeholder="Search connections..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 bg-transparent border-0 px-0 py-0 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-0 focus-visible:ring-0 disabled:cursor-not-allowed disabled:opacity-50"
              autoComplete="off"
            />
            {searchQuery && (
              <Button
                variant="ghost"
                size="sm"
                className="h-6 w-6 p-0 hover:bg-transparent"
                onClick={() => setSearchQuery("")}
              >
                <X className="h-3 w-3" />
              </Button>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-gray-500" />
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-full sm:w-[140px] h-9">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="inactive">Inactive</SelectItem>
            </SelectContent>
          </Select>

          <Select value={carrierFilter} onValueChange={setCarrierFilter}>
            <SelectTrigger className="w-full sm:w-[140px] h-9">
              <SelectValue placeholder="Carrier" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Carriers</SelectItem>
              {Object.keys(references?.carriers || {}).sort().map((carrier) => (
                <SelectItem key={carrier} value={carrier}>
                  {references?.carriers?.[carrier] || carrier}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {hasActiveFilters && (
          <Button variant="ghost" size="sm" onClick={clearFilters} className="h-9">
            Reset
            <X className="ml-2 h-3 w-3" />
          </Button>
        )}
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      )}

      {/* Empty State */}
      {!isLoading && filteredConnections.length === 0 && !hasActiveFilters && (
        <div className="text-center py-12">
          <Network className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-500 mb-2">
            No carrier connections
          </h3>
          <p className="text-sm text-gray-400 mb-6">
            Create your first system carrier connection to get started.
          </p>
          <Button onClick={() => {
            setSelectedConnection(null);
            setIsEditOpen(true);
          }}>
            <Plus className="h-4 w-4 mr-2" />
            Add Connection
          </Button>
        </div>
      )}

      {/* No Results State */}
      {!isLoading && filteredConnections.length === 0 && hasActiveFilters && (
        <div className="text-center py-12">
          <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-500 mb-2">
            No connections found
          </h3>
          <p className="text-sm text-gray-400 mb-6">
            Try adjusting your search or filter criteria.
          </p>
          <Button variant="outline" onClick={clearFilters}>
            Clear filters
          </Button>
        </div>
      )}

      {/* Connections List (aligned with user connections design) */}
      {!isLoading && filteredConnections.length > 0 && (
        <div className="space-y-3">
          {filteredConnections.map((connection) => (
            <div
              key={connection.id}
              className="group relative flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all duration-200 bg-white gap-3"
            >
              {/* Main Content */}
              <div className="flex items-start sm:items-center gap-3 flex-1 w-full sm:w-auto">
                <div className="flex-shrink-0">
                  <CarrierImage carrier_name={connection.credentials?.custom_carrier_name || connection.carrier_name} width={48} height={48} className="rounded-lg" text_color={connection.config?.text_color} background={connection.config?.brand_color} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                    <h3 className="font-medium text-gray-900 text-base">
                      {connection.display_name || connection.carrier_name}
                    </h3>
                    <div className="flex items-center gap-1.5">
                      <StatusBadge status={connection.active ? "active" : "inactive"} />
                      {connection.test_mode && <StatusBadge status="test" />}
                    </div>
                  </div>
                  <div className="flex flex-col sm:flex-row sm:items-center gap-2 text-sm">
                    <div className="flex items-center gap-1.5">
                      <span className="text-gray-600 font-mono">{connection.carrier_id || connection.id}</span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-4 w-4 p-0 hover:bg-gray-100 opacity-0 group-hover:opacity-100 transition-opacity"
                        onClick={() => handleCopy(connection.id, "Connection ID copied")}
                      >
                        <Copy className="h-3 w-3" />
                      </Button>
                    </div>
                    <span className="hidden sm:inline text-gray-400">•</span>
                    <div className="flex flex-wrap gap-1">
                      {connection.capabilities && connection.capabilities.length > 0 ? (
                        <>
                          {connection.capabilities.slice(0, 2).map((capability) => (
                            <span key={capability} className="text-xs px-2 py-0.5 bg-gray-100 text-gray-700 rounded">
                              {capability}
                            </span>
                          ))}
                          {connection.capabilities.length > 2 && (
                            <span className="text-xs px-2 py-0.5 border border-gray-300 text-gray-600 rounded">
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
                <div className="flex items-center gap-2">
                  <Switch checked={connection.active} onCheckedChange={(checked) => handleStatusToggle(connection, checked)} />
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-9 w-9 hover:bg-muted">
                      <MoreHorizontal className="h-4 w-4" />
                      <span className="sr-only">Open menu</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Actions</DropdownMenuLabel>
                    <DropdownMenuItem onClick={() => { setSelectedConnection(connection); setIsEditOpen(true); }}>
                      <Edit3 className="mr-2 h-4 w-4" />
                      Edit Connection
                    </DropdownMenuItem>
                    {/* Only show rate sheet options for compatible carriers */}
                    {supportsRateSheets(connection, references) && (
                      <>
                        <DropdownMenuItem onClick={() => askLinkRateSheet(connection)}>
                          <FileText className="mr-2 h-4 w-4" />
                          Link Rate Sheet
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => openRateSheetEditor(connection)}>
                          <Edit3 className="mr-2 h-4 w-4" />
                          Edit Rate Sheet
                        </DropdownMenuItem>
                      </>
                    )}
                    <DropdownMenuItem onClick={() => handleCopy(connection.id, "Connection ID copied")}>
                      <Copy className="mr-2 h-4 w-4" />
                      Copy ID
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem className="text-red-600" onClick={() => { setSelectedConnection(connection); setIsDeleteOpen(true); }}>
                      <Trash2 className="mr-2 h-4 w-4" />
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>

              <div className={`absolute left-0 top-0 bottom-0 w-1 rounded-l-lg ${connection.active ? (connection.test_mode ? "bg-yellow-500" : "bg-green-500") : "bg-gray-300"}`} />
            </div>
          ))}
        </div>
      )}

      {/* Results Count */}
      {!isLoading && filteredConnections.length > 0 && (
        <div className="flex items-center justify-between text-sm text-gray-600">
          <span>
            Showing {filteredConnections.length} of {connectionsQuery.data?.system_carrier_connections?.edges?.length || 0} connections
          </span>
          {hasActiveFilters && (
            <Button variant="ghost" size="sm" onClick={clearFilters}>
              Clear all filters
            </Button>
          )}
        </div>
      )}

      {/* Dialogs */}
      <CarrierConnectionDialog
        open={isEditOpen}
        onOpenChange={setIsEditOpen}
        selectedConnection={selectedConnection as any}
        onSubmit={handleUpdate}
        references={references}
        onSuccess={() => {
          setIsEditOpen(false);
          setSelectedConnection(null);
        }}
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

      {/* Link to existing Rate Sheet */}
      {isLinkDialogOpen && linkConnection && (
        <LinkRateSheetDialog
          open={isLinkDialogOpen}
          onOpenChange={setIsLinkDialogOpen}
          connection={{
            id: linkConnection.id,
            carrier_name: linkConnection.carrier_name,
            display_name: linkConnection.display_name
          }}
          rateSheets={(rate_sheets?.edges || []).map(({ node }) => node).filter((rs) => {
            // For generic/custom carriers, match with "generic" rate sheets
            const linkCarrierName = getRateSheetCarrierName(linkConnection);
            return rs.carrier_name === linkCarrierName;
          })}
          linkedRateSheets={(rate_sheets?.edges || []).map(({ node }) => node).filter((rs) => (rs.carriers || []).some((c: any) => c.id === linkConnection.id))}
          onEditRateSheet={(id: string) => {
            const rs = (rate_sheets?.edges || []).map(({ node }) => node).find((r) => r.id === id);
            if (rs) {
              setSelectedRateSheet(rs);
              setSelectedRateSheetId(rs.id);
              setIsRateSheetEditorOpen(true);
              setIsLinkDialogOpen(false);
            }
          }}
          onCreateNew={() => {
            // Freeze to the connection's carrier_name and preload defaults
            const rateSheetCarrierName = getRateSheetCarrierName(linkConnection);
            setSelectedRateSheet({
              carrier_name: rateSheetCarrierName,
              name: `${linkConnection.display_name || linkConnection.carrier_name} Rate Sheet`,
              carriers: [{ id: linkConnection.id }] as any,
            } as RateSheet);
            setSelectedRateSheetId('new');
            setIsRateSheetEditorOpen(true);
            setIsLinkDialogOpen(false);
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

      {/* Rate Sheet Editor */}
      {isRateSheetEditorOpen && selectedRateSheetId && (
        <RateSheetEditor
          rateSheetId={selectedRateSheetId}
          onClose={() => {
            setIsRateSheetEditorOpen(false);
            setSelectedRateSheetId(null);
            setSelectedRateSheet(null);
            rateSheetsQuery.refetch();
          }}
          isAdmin={true}
          useRateSheet={useAdminRateSheet}
          useRateSheetMutation={useAdminRateSheetMutation}
          markups={adminMarkupsList}
          markupMutations={markupMutationHooks}
          // Freeze and preload defaults based on the launching connection's carrier
          preloadCarrier={selectedRateSheet?.carrier_name}
          linkConnectionId={(selectedRateSheet as any)?.carriers?.[0]?.id}
        />
      )}
    </div>
  );
}

function RateSheetManagement() {
  const { toast } = useToast();
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedRateSheet, setSelectedRateSheet] = useState<RateSheet | null>(null);
  const [selectedRateSheetId, setSelectedRateSheetId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  const { query, rate_sheets: rateSheetsData } = useRateSheets({});
  const rateSheets = rateSheetsData?.edges || [];
  const isLoading = query.isLoading;

  const { deleteRateSheet } = useRateSheetMutation();
  const { markups: markupsData2 } = useMarkups();
  const markupMutationHooks2 = useMarkupMutation();
  const adminMarkupsList2 = useMemo(
    () => markupsData2?.edges?.map((e: any) => e.node) || [],
    [markupsData2]
  );

  // Filter rate sheets
  const filteredRateSheets = useMemo(() => {
    return rateSheets.filter(({ node: sheet }) => {
      const matchesSearch =
        sheet.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        sheet.id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        sheet.carrier_name?.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesStatus = statusFilter === 'all' ||
        (statusFilter === 'active' && sheet.carriers?.some(c => c.active)) ||
        (statusFilter === 'inactive' && !sheet.carriers?.some(c => c.active));

      return matchesSearch && matchesStatus;
    });
  }, [rateSheets, searchQuery, statusFilter]);

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

  const openRateSheetEditor = (rateSheet?: RateSheet | null) => {
    if (rateSheet) {
      setSelectedRateSheetId(rateSheet.id);
    } else {
      setSelectedRateSheetId('new');
    }
    setIsEditOpen(true);
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

  const clearFilters = () => {
    setSearchQuery("");
    setStatusFilter("all");
  };

  const hasActiveFilters = searchQuery || statusFilter !== "all";

  return (
    <div className="space-y-6">
      {/* Header and Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-medium text-gray-900">Rate Sheets</h2>
          <p className="text-sm text-gray-500 mt-1">
            Manage custom rate sheets for your carrier network
          </p>
        </div>
        <Button onClick={() => openRateSheetEditor(null)}>
          <Plus className="h-4 w-4 mr-2" />
          Create Rate Sheet
        </Button>
      </div>

      {/* Search and Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-3 p-4 bg-gray-50 rounded-lg">
        <div className="flex-1">
          <div className="flex h-9 w-full items-center rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2">
            <Search className="h-4 w-4 text-muted-foreground mr-2 flex-shrink-0" />
            <Input
              placeholder="Search rate sheets..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 bg-transparent border-0 px-0 py-0 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-0 focus-visible:ring-0 disabled:cursor-not-allowed disabled:opacity-50"
              autoComplete="off"
            />
            {searchQuery && (
              <Button
                variant="ghost"
                size="sm"
                className="h-6 w-6 p-0 hover:bg-transparent"
                onClick={() => setSearchQuery("")}
              >
                <X className="h-3 w-3" />
              </Button>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-gray-500" />
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-full sm:w-[140px] h-9">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="inactive">Inactive</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {hasActiveFilters && (
          <Button variant="ghost" size="sm" onClick={clearFilters} className="h-9">
            Reset
            <X className="ml-2 h-3 w-3" />
          </Button>
        )}
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      )}

      {/* Empty State */}
      {!isLoading && filteredRateSheets.length === 0 && !hasActiveFilters && (
        <div className="text-center py-12">
          <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-500 mb-2">
            No rate sheets
          </h3>
          <p className="text-sm text-gray-400 mb-6">
            Create your first custom rate sheet to get started.
          </p>
          <Button onClick={() => openRateSheetEditor(null)}>
            <Plus className="h-4 w-4 mr-2" />
            Create Rate Sheet
          </Button>
        </div>
      )}

      {/* No Results State */}
      {!isLoading && filteredRateSheets.length === 0 && hasActiveFilters && (
        <div className="text-center py-12">
          <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-500 mb-2">
            No rate sheets found
          </h3>
          <p className="text-sm text-gray-400 mb-6">
            Try adjusting your search or filter criteria.
          </p>
          <Button variant="outline" onClick={clearFilters}>
            Clear filters
          </Button>
        </div>
      )}

      {/* Rate Sheets List (aligned with user connections design) */}
      {!isLoading && filteredRateSheets.length > 0 && (
        <div className="space-y-3">
          {filteredRateSheets.map(({ node: sheet }) => (
            <div
              key={sheet.id}
              className="group relative flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all duration-200 bg-white gap-3"
            >
              <div className="flex items-start sm:items-center gap-3 flex-1 w-full sm:w-auto">
                <div className="flex-shrink-0">
                  <CarrierImage carrier_name={sheet.carrier_name} width={48} height={48} className="rounded-lg" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-gray-900 text-base mb-1">{sheet.name}</h3>
                  <p className="text-sm text-gray-500">{sheet.carrier_name}</p>
                </div>
              </div>
              <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
                <div className="flex items-center gap-3">
                  <div className="text-sm text-gray-600">
                    {(sheet.services?.length ?? 0)} services
                  </div>
                  <StatusBadge status={sheet.carriers?.some(c => c.active) ? "active" : "inactive"} />
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-9 w-9 hover:bg-muted">
                      <MoreHorizontal className="h-4 w-4" />
                      <span className="sr-only">Open menu</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Actions</DropdownMenuLabel>
                    <DropdownMenuItem onClick={() => openRateSheetEditor(sheet)}>
                      <Edit3 className="mr-2 h-4 w-4" />
                      Edit Rate Sheet
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleCopy(sheet.id, "Rate sheet ID copied")}>
                      <Copy className="mr-2 h-4 w-4" />
                      Copy ID
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem className="text-red-600" onClick={() => { setSelectedRateSheet(sheet); setIsDeleteOpen(true); }}>
                      <Trash2 className="mr-2 h-4 w-4" />
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Results Count */}
      {!isLoading && filteredRateSheets.length > 0 && (
        <div className="flex items-center justify-between text-sm text-gray-600">
          <span>
            Showing {filteredRateSheets.length} of {rateSheets.length} rate sheets
          </span>
          {hasActiveFilters && (
            <Button variant="ghost" size="sm" onClick={clearFilters}>
              Clear all filters
            </Button>
          )}
        </div>
      )}

      {/* Dialogs */}
      {isEditOpen && selectedRateSheetId && (
        <RateSheetEditor
          rateSheetId={selectedRateSheetId}
          onClose={() => {
            setIsEditOpen(false);
            setSelectedRateSheetId(null);
            query.refetch();
          }}
          isAdmin={true}
          useRateSheet={useAdminRateSheet}
          useRateSheetMutation={useAdminRateSheetMutation}
          markups={adminMarkupsList2}
          markupMutations={markupMutationHooks2}
        />
      )}

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
        description={`Are you sure you want to delete the rate sheet: ${selectedRateSheet?.name}? This action cannot be undone.`}
      />
    </div>
  );
}
