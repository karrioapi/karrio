"use client";

import React, { useState, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import {
  Search,
  Filter,
  Copy,
  Server,
} from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { useSystemConnections, useSystemConnectionMutation } from "@karrio/hooks/system-connection";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { cn } from "@karrio/ui/lib/utils";

export default function SystemConnectionsPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [selectedTab, setSelectedTab] = useState("system");
  const [carrierSearch, setCarrierSearch] = useState("");
  const [carrierFilter, setCarrierFilter] = useState("all");

  // Hooks
  const { query: userQuery, user_carrier_connections } = useCarrierConnections();
  const { query: systemQuery, system_connections } = useSystemConnections();
  const { updateSystemConnection } = useSystemConnectionMutation();

  const isLoading = systemQuery.isLoading || userQuery.isLoading;

  // Convert connections data to proper format
  const systemConnections = useMemo(() => {
    if (!system_connections) return [];
    return system_connections.map((connection) => ({
      ...connection,
      connection_type: "system"
    }));
  }, [system_connections]);

  const userConnections = useMemo(() => {
    if (!user_carrier_connections) return [];
    return user_carrier_connections.map((connection) => ({
      ...connection,
      connection_type: "user"
    }));
  }, [user_carrier_connections]);

  // Filter connections
  const filteredConnections = useMemo(() => {
    const connections = systemConnections;

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
  }, [systemConnections, carrierSearch, carrierFilter]);

  const copyToClipboard = (text: string | undefined) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    toast({ title: "Copied to clipboard" });
  };

  const handleToggleSystemConnection = (connection: any) => {
    updateSystemConnection.mutate({
      id: connection.id,
      enable: !connection.enabled
    }, {
      onSuccess: () => {
        toast({
          title: `System connection ${!connection.enabled ? 'enabled' : 'disabled'} successfully`
        });
      },
      onError: (error: any) => {
        toast({
          title: "Failed to update system connection",
          description: error.message || "An error occurred",
          variant: "destructive",
        });
      }
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading system connections...</p>
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
            <AppLink
              href={`/connections`}
              className="hover:text-inherit"
            >
              Your Accounts ({userConnections.length})
            </AppLink>
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
            System Accounts ({systemConnections.length})
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
              <p className="text-sm text-gray-600">Total System Connections</p>
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
              <p className="text-sm text-gray-600">Available Carriers</p>
              <p className="text-2xl font-semibold text-gray-900">
                {new Set(filteredConnections.map(c => c.carrier_name)).size}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Carriers Header */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-medium text-gray-900">System Connections</h2>
            <p className="text-sm text-gray-600 mt-1">
              {systemQuery.data?.system_connections?.page_info?.count} system connections available
            </p>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 p-4 bg-gray-50 rounded-lg">
          <div className="flex-1">
            <div className="flex h-9 w-full items-center rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2">
              <Search className="h-4 w-4 text-muted-foreground mr-2 flex-shrink-0" />
              <Input
                placeholder="Search system carriers..."
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

        {/* System Connections List */}
        {filteredConnections.length === 0 ? (
          <div className="text-center py-12">
            <div className="mx-auto mb-4 text-gray-400">
              <Server className="h-12 w-12 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-500 mb-2">
              No system connections found
            </h3>
            <p className="text-sm text-gray-400">
              {carrierSearch || carrierFilter !== 'all'
                ? "No system connections match your current filters."
                : "System connections will appear here when configured by administrators."
              }
            </p>
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
                      carrier_name={connection.carrier_name}
                      width={48}
                      height={48}
                      className="rounded-lg"
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
                        <StatusBadge status={connection.enabled ? "active" : "inactive"} />
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

                {/* Right Side - Toggle */}
                <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
                  <Switch
                    checked={connection.enabled}
                    onCheckedChange={() => handleToggleSystemConnection(connection)}
                  />
                </div>

                {/* Connection Line Indicator */}
                <div className={`absolute left-0 top-0 bottom-0 w-1 rounded-l-lg ${connection.enabled
                  ? connection.test_mode
                    ? "bg-yellow-500"
                    : "bg-blue-500"
                  : "bg-gray-300"
                  }`} />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
