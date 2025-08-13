"use client";

import React, { useState, useMemo } from 'react';
import { useRateSheet as useAdminRateSheet, useRateSheetMutation as useAdminRateSheetMutation } from "@karrio/hooks/admin-rate-sheets";
import { GetSystemConnections_system_carrier_connections_edges_node as Connection } from "@karrio/types/graphql/admin/types";
import { useSystemConnections, useSystemConnectionMutation } from "@karrio/hooks/admin-system-connections";
import { GetRateSheets_rate_sheets_edges_node as RateSheet } from "@karrio/types/graphql/admin/types";
import { DeleteConfirmationDialog } from "@karrio/ui/components/delete-confirmation-dialog";
import { CarrierConnectionDialog } from "@karrio/ui/components/carrier-connection-dialog";
import { useRateSheets, useRateSheetMutation } from "@karrio/hooks/admin-rate-sheets";
import { RateSheetEditor } from "@karrio/ui/components/rate-sheet-editor";
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

  const { query, system_carrier_connections } = useSystemConnections({});
  const connections = system_carrier_connections?.edges || [];
  const isLoading = query.isLoading;
  const { references } = useAPIMetadata();

  const { createSystemConnection, updateSystemConnection, deleteSystemConnection } = useSystemConnectionMutation();

  // Filter connections
  const filteredConnections = useMemo(() => {
    return connections.filter(({ node: connection }) => {
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
  }, [connections, searchQuery, statusFilter, carrierFilter]);

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
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search connections..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 pr-10"
          />
          {searchQuery && (
            <Button
              variant="ghost"
              size="sm"
              className="absolute right-1 top-1/2 h-7 w-7 -translate-y-1/2 p-0"
              onClick={() => setSearchQuery("")}
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>

        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[140px]">
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4" />
              <SelectValue placeholder="Status" />
            </div>
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="inactive">Inactive</SelectItem>
          </SelectContent>
        </Select>

        <Select value={carrierFilter} onValueChange={setCarrierFilter}>
          <SelectTrigger className="w-[140px]">
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4" />
              <SelectValue placeholder="Carrier" />
            </div>
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

        {hasActiveFilters && (
          <Button variant="ghost" onClick={clearFilters}>
            Reset
            <X className="ml-2 h-4 w-4" />
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
          {filteredConnections.map(({ node: connection }) => (
            <div
              key={connection.id}
              className="group relative flex items-center justify-between p-3 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all duration-200 bg-white"
            >
              {/* Main Content */}
              <div className="flex items-center space-x-3 flex-1">
                <div className="flex-none">
                  <CarrierImage carrier_name={connection.carrier_name} width={40} height={40} className="rounded-lg" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-medium text-gray-900 truncate text-sm">
                      {connection.display_name || connection.carrier_name}
                    </h3>
                    <div className="flex items-center gap-1.5">
                      <StatusBadge status={connection.active ? "active" : "inactive"} />
                      {connection.test_mode && <StatusBadge status="test" />}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-1.5">
                      <span className="text-xs text-gray-600 font-mono">{connection.carrier_id || connection.id}</span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-3 w-3 p-0 hover:bg-gray-100 opacity-0 group-hover:opacity-100 transition-opacity"
                        onClick={() => handleCopy(connection.id, "Connection ID copied")}
                      >
                        <Copy className="h-2.5 w-2.5" />
                      </Button>
                    </div>
                    <span className="text-gray-400">•</span>
                    <div className="flex flex-wrap gap-1">
                      {connection.capabilities && connection.capabilities.length > 0 ? (
                        <>
                          {connection.capabilities.slice(0, 2).map((capability) => (
                            <span key={capability} className="text-[10px] px-1.5 py-0.5 bg-gray-100 text-gray-700 rounded border-0">
                              {capability}
                            </span>
                          ))}
                          {connection.capabilities.length > 2 && (
                            <span className="text-[10px] px-1.5 py-0.5 border border-gray-300 text-gray-600 rounded">
                              +{connection.capabilities.length - 2}
                            </span>
                          )}
                        </>
                      ) : (
                        <span className="text-[10px] text-gray-500 italic">No capabilities</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-2">
                  <Switch checked={connection.active} onCheckedChange={(checked) => handleStatusToggle(connection, checked)} />
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8 p-0 hover:bg-muted">
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
            Showing {filteredConnections.length} of {connections.length} connections
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
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search rate sheets..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 pr-10"
          />
          {searchQuery && (
            <Button
              variant="ghost"
              size="sm"
              className="absolute right-1 top-1/2 h-7 w-7 -translate-y-1/2 p-0"
              onClick={() => setSearchQuery("")}
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>

        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[140px]">
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4" />
              <SelectValue placeholder="Status" />
            </div>
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="inactive">Inactive</SelectItem>
          </SelectContent>
        </Select>

        {hasActiveFilters && (
          <Button variant="ghost" onClick={clearFilters}>
            Reset
            <X className="ml-2 h-4 w-4" />
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
              className="group relative flex items-center justify-between p-3 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all duration-200 bg-white"
            >
              <div className="flex items-center space-x-3 flex-1">
                <div className="flex-none">
                  <CarrierImage carrier_name={sheet.carrier_name} width={40} height={40} className="rounded-lg" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-gray-900 truncate text-sm">{sheet.name}</h3>
                  <p className="text-xs text-gray-500 truncate">{sheet.carrier_name}</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-xs text-gray-600">
                  {(sheet.services?.length ?? 0)} services
                </div>
                <StatusBadge status={sheet.carriers?.some(c => c.active) ? "active" : "inactive"} />
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8 p-0 hover:bg-muted">
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
