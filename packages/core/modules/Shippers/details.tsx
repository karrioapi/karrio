"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  Building2,
  Package,
  MapPin,
  Truck,
  ArrowLeft,
  Settings,
  Copy,
  Search,
  Filter,
  Users,
  Calendar,
  Activity,
} from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/ui/components/ui/table";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import {
  useSystemShipments,
  useSystemTrackers,
  useDateRangeFilter,
  useAccountCarrierConnections,
  usePagination,
  SystemTrackerNode
} from "@karrio/hooks/admin-shipments";
import { useOrganizationAccountDetails } from "@karrio/hooks/admin-accounts";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { Button } from "@karrio/ui/components/ui/button";
import { useUser } from "@karrio/hooks/user";
import { cn } from "@karrio/ui/lib/utils";

interface ShippersAccountDetailProps {
  accountId: string;
}

function ShippersAccountDetail({ accountId }: ShippersAccountDetailProps) {
  const router = useRouter();
  const [dateRange, setDateRange] = useState("30d");
  const [selectedTab, setSelectedTab] = useState("overview");
  const [carrierSearch, setCarrierSearch] = useState("");
  const [carrierFilter, setCarrierFilter] = useState("all");

  const handleDateRangeChange = (value: string) => {
    setDateRange(value);
  };

  // Get current admin user
  const { query: { data: { user } = {} } } = useUser();
  const isAdmin = user?.is_staff || user?.is_superuser;

  const copyToClipboard = (text: string | undefined) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
  };

  // Use extracted hooks
  const { getUsageFilter } = useDateRangeFilter(accountId);
  const usageFilter = React.useMemo(() => getUsageFilter(dateRange), [getUsageFilter, dateRange]);

  // Pagination hooks
  const shipmentsPagination = usePagination(1, 20);
  const trackersPagination = usePagination(1, 20);

  // Get organization account details with usage data
  const { query: accountDetailsQuery, account: accountDetails } = useOrganizationAccountDetails(accountId, usageFilter);

  // Get account carrier connections for this organization
  const { query: accountCarriersQuery, useFilteredCarriers } = useAccountCarrierConnections({
    accountId,
    usageFilter,
    enabled: selectedTab === "carriers"
  });

  // Get system shipments for this organization
  const { query: systemShipmentsQuery, shipments } = useSystemShipments({
    accountId,
    dateAfter: usageFilter.date_after,
    dateBefore: usageFilter.date_before,
    offset: shipmentsPagination.paginationState.offset,
    first: shipmentsPagination.paginationState.pageSize,
    enabled: selectedTab === "shipments",
  });

  // Get system trackers for this organization
  const { query: systemTrackersQuery, trackers } = useSystemTrackers({
    accountId,
    dateAfter: usageFilter.date_after,
    dateBefore: usageFilter.date_before,
    offset: trackersPagination.paginationState.offset,
    first: trackersPagination.paginationState.pageSize,
    enabled: selectedTab === "trackers",
  });

  const accountDetailsLoading = accountDetailsQuery.isLoading;
  const carriersLoading = accountCarriersQuery.isLoading;
  const shipmentsLoading = systemShipmentsQuery.isLoading;
  const trackersLoading = systemTrackersQuery.isLoading;


  // Get filtered carriers
  const filteredCarriers = useFilteredCarriers(carrierSearch, carrierFilter);

  // Check if any data is loading
  const isLoading = accountDetailsLoading;

  // Show loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading organization details...</p>
        </div>
      </div>
    );
  }

  // Show not found state
  if (!accountDetails) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Building2 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Organization Not Found</h2>
          <p className="text-muted-foreground mb-4">
            The organization you're looking for doesn't exist or you don't have access to it.
          </p>
          <Button asChild>
            <Link href="/shippers/accounts">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Organizations
            </Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Button
        variant="ghost"
        size="sm"
        asChild
        className="flex items-center gap-2 w-fit"
      >
        <Link href="/shippers/accounts">
          <ArrowLeft className="h-4 w-4" />
          Back to Organizations
        </Link>
      </Button>

      {/* Organization Header */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gray-600 rounded-lg flex items-center justify-center">
            <Building2 className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-semibold text-gray-900 flex items-center gap-3">
              {accountDetails.name}
              <StatusBadge status={accountDetails.is_active ? "enabled" : "disabled"} />
            </h1>
          </div>
        </div>

        {/* Organization Details Row */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-6 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <span className="font-mono">{accountDetails.slug}</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => copyToClipboard(accountDetails.id)}
              className="flex items-center gap-2 text-gray-700 border-gray-300 hover:bg-gray-50"
            >
              <Copy className="h-4 w-4" />
              Copy ID
            </Button>

          </div>
        </div>

        {/* Tab Navigation with Period Filter */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-gray-200 gap-4">
          <nav className="flex space-x-8 overflow-x-auto">
            <button
              className={cn(
                "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
                selectedTab === "overview"
                  ? "border-purple-500 text-purple-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              )}
              onClick={() => setSelectedTab("overview")}
            >
              Overview
            </button>
            <button
              className={cn(
                "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
                selectedTab === "carriers"
                  ? "border-purple-500 text-purple-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              )}
              onClick={() => setSelectedTab("carriers")}
            >
              Carriers
            </button>
            <button
              className={cn(
                "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
                selectedTab === "shipments"
                  ? "border-purple-500 text-purple-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              )}
              onClick={() => setSelectedTab("shipments")}
            >
              Shipments
            </button>
            <button
              className={cn(
                "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
                selectedTab === "trackers"
                  ? "border-purple-500 text-purple-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              )}
              onClick={() => setSelectedTab("trackers")}
            >
              Trackers
            </button>
          </nav>

          <div className="flex items-center gap-2 py-4">
            <Select value={dateRange} onValueChange={handleDateRangeChange}>
              <SelectTrigger className="w-full sm:w-[140px] h-8 text-sm">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="7d">Last 7 days</SelectItem>
                <SelectItem value="30d">Last 30 days</SelectItem>
                <SelectItem value="90d">Last 90 days</SelectItem>
                <SelectItem value="1y">Last year</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      <div className="space-y-6">

        {selectedTab === "overview" && (
          <div className="space-y-8 mt-6">
            {/* Primary Metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="border shadow-none">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <Users className="h-4 w-4 text-gray-500" />
                  </div>
                  <p className="text-sm text-gray-600">Members</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {(accountDetails.usage?.members || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>

              <Card className="border shadow-none">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <Package className="h-4 w-4 text-gray-500" />
                  </div>
                  <p className="text-sm text-gray-600">Total Shipments</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {(accountDetails.usage?.total_shipments || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>

              <Card className="border shadow-none">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <MapPin className="h-4 w-4 text-gray-500" />
                  </div>
                  <p className="text-sm text-gray-600">Trackers</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {(accountDetails.usage?.total_trackers || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>

              <Card className="border shadow-none">
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">Total Spend</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    ${(accountDetails.usage?.total_shipping_spend || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Secondary Metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="border shadow-none">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <Activity className="h-4 w-4 text-gray-500" />
                  </div>
                  <p className="text-sm text-gray-600">API Requests</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {(accountDetails.usage?.total_requests || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>

              <Card className="border shadow-none">
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">Order Volume</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {(accountDetails.usage?.order_volume || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>

              <Card className="border shadow-none">
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">Unfulfilled Orders</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {(accountDetails.usage?.unfulfilled_orders || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>

              <Card className="border shadow-none">
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">Addons Charges</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    ${(accountDetails.usage?.total_addons_charges || 0).toLocaleString()}
                  </p>
                </CardContent>
              </Card>
            </div>

            <div>
              <h2 className="text-lg font-medium text-gray-900 mb-4">Organization Information</h2>
              <div className="border-b">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 py-4">
                  <div>
                    <label className="text-sm font-medium text-gray-600">Organization Name</label>
                    <p className="text-sm text-gray-900 mt-1">{accountDetails.name}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">Slug</label>
                    <p className="text-sm text-gray-900 mt-1">{accountDetails.slug}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">Organization ID</label>
                    <p className="text-sm font-mono text-gray-900 mt-1">{accountDetails.id}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">Status</label>
                    <div className="mt-1">
                      <StatusBadge status={accountDetails.is_active ? "active" : "inactive"} />
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">Created</label>
                    <p className="text-sm text-gray-900 mt-1">
                      {new Date(accountDetails.created).toLocaleDateString("en-US", {
                        month: "long",
                        day: "numeric",
                        year: "numeric"
                      })}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">Last Modified</label>
                    <p className="text-sm text-gray-900 mt-1">
                      {new Date(accountDetails.modified).toLocaleDateString("en-US", {
                        month: "long",
                        day: "numeric",
                        year: "numeric"
                      })}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Members Table */}
            <div>
              <h2 className="text-lg font-medium text-gray-900 mb-4">Organization Members</h2>
              <div className="border rounded-lg">
                <Table>
                  <TableHeader className="bg-gray-50">
                    <TableRow>
                      <TableHead className="w-[300px]">Member</TableHead>
                      <TableHead className="w-[200px]">Role</TableHead>
                      <TableHead className="w-[150px]">Status</TableHead>
                      <TableHead className="w-[200px]">Last Active</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {accountDetails.members && accountDetails.members.length > 0 ? (
                      accountDetails.members.map((member) => (
                        <TableRow key={member.user_id} className="hover:bg-gray-50">
                          <TableCell>
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                                <Users className="h-4 w-4 text-purple-600" />
                              </div>
                              <div>
                                <div className="font-medium text-gray-900">
                                  {member.full_name || member.email}
                                </div>
                                <div className="text-sm text-gray-500">{member.email}</div>
                              </div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-2">
                              {member.is_owner && (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                                  Owner
                                </span>
                              )}
                              {member.is_admin && !member.is_owner && (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                  Admin
                                </span>
                              )}
                              {!member.is_admin && !member.is_owner && (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                                  Member
                                </span>
                              )}
                            </div>
                          </TableCell>
                          <TableCell>
                            <StatusBadge status="active" />
                          </TableCell>
                          <TableCell>
                            <div className="text-sm text-gray-500">
                              {member.last_login
                                ? new Date(member.last_login).toLocaleDateString("en-US", {
                                  month: "short",
                                  day: "numeric",
                                  year: "numeric"
                                })
                                : "Never"}
                            </div>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={4} className="text-center py-12">
                          <Users className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                          <h3 className="text-lg font-medium text-gray-500 mb-2">
                            No members found
                          </h3>
                          <p className="text-sm text-gray-400">
                            This organization doesn't have any members yet.
                          </p>
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </div>
            </div>
          </div>
        )}

        {selectedTab === "carriers" && (
          <div className="space-y-6 mt-3">
            {/* Carriers Header */}
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-medium text-gray-900">Carrier Connections</h2>
                <p className="text-sm text-gray-600 mt-1">
                  {accountCarriersQuery.data?.carrier_connections?.edges?.length || 0} total connections
                </p>
              </div>
            </div>

            {/* Filters */}
            <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex-1 relative">
                <div className="flex h-9 w-full items-center rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2">
                  <Search className="h-4 w-4 text-muted-foreground mr-2 flex-shrink-0" />
                  <input
                    placeholder="Search carriers..."
                    value={carrierSearch}
                    onChange={(e) => setCarrierSearch(e.target.value)}
                    className="flex-1 bg-transparent border-0 px-0 py-0 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-0 disabled:cursor-not-allowed disabled:opacity-50"
                    autoComplete="off"
                  />
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4 text-gray-500" />
                <Select value={carrierFilter} onValueChange={setCarrierFilter}>
                  <SelectTrigger className="w-[120px] h-9">
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

            {carriersLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
              </div>
            ) : filteredCarriers.length > 0 ? (
              <div className="space-y-3">
                {filteredCarriers.map(({ node: carrier }) => (
                  <div
                    key={carrier.id}
                    className="group relative flex items-center justify-between p-3 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all duration-200 bg-white"
                  >
                    {/* Main Content */}
                    <div className="flex items-center space-x-3 flex-1">
                      {/* Carrier Logo */}
                      <div className="flex-none">
                        <CarrierImage
                          carrier_name={carrier.carrier_name}
                          width={40}
                          height={40}
                          className="rounded-lg"
                        />
                      </div>

                      {/* Carrier Details - Reduced to 2 rows */}
                      <div className="flex-1 min-w-0">
                        {/* Row 1: Name and Status */}
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="font-medium text-gray-900 truncate text-sm">
                            {carrier.display_name || carrier.carrier_name}
                          </h3>
                          <div className="flex items-center gap-1.5">
                            <StatusBadge status={carrier.active ? "active" : "inactive"} />
                            {carrier.test_mode && (
                              <StatusBadge status="test" />
                            )}
                          </div>
                        </div>

                        {/* Row 2: Carrier ID and Capabilities */}
                        <div className="flex items-center gap-2">
                          <div className="flex items-center gap-1.5">
                            <span className="text-xs text-gray-600 font-mono">
                              {carrier.carrier_id}
                            </span>
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-3 w-3 p-0 hover:bg-gray-100 opacity-0 group-hover:opacity-100 transition-opacity"
                              onClick={() => copyToClipboard(carrier.carrier_id)}
                            >
                              <Copy className="h-2.5 w-2.5" />
                            </Button>
                          </div>
                          <span className="text-gray-400">•</span>
                          <div className="flex flex-wrap gap-1">
                            {carrier.capabilities && carrier.capabilities.length > 0 ? (
                              <>
                                {carrier.capabilities.slice(0, 2).map((capability) => (
                                  <span
                                    key={capability}
                                    className="text-[10px] px-1.5 py-0.5 bg-gray-100 text-gray-700 rounded border-0"
                                  >
                                    {capability}
                                  </span>
                                ))}
                                {carrier.capabilities.length > 2 && (
                                  <span
                                    className="text-[10px] px-1.5 py-0.5 border border-gray-300 text-gray-600 rounded"
                                  >
                                    +{carrier.capabilities.length - 2}
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

                    {/* Right Side - Usage Stats */}
                    <div className="flex items-center space-x-4 text-right">
                      {/* Usage Stats */}
                      <div className="space-y-0.5">
                        <div className="text-xs text-gray-500">{
                          dateRange === "7d" ? "Last 7 days" :
                            dateRange === "30d" ? "Last 30 days" :
                              dateRange === "90d" ? "Last 90 days" :
                                "Last year"
                        }</div>
                        <div className="flex items-center space-x-3">
                          <div className="text-center">
                            <div className="text-sm font-medium text-gray-900">
                              {carrier.usage?.total_shipments || 0}
                            </div>
                            <div className="text-[10px] text-gray-500">Shipments</div>
                          </div>
                          <div className="text-center">
                            <div className="text-sm font-medium text-gray-900">
                              ${(carrier.usage?.total_shipping_spend || 0).toLocaleString()}
                            </div>
                            <div className="text-[10px] text-gray-500">Spend</div>
                          </div>
                          <div className="text-center">
                            <div className="text-sm font-medium text-gray-900">
                              {carrier.usage?.total_trackers || 0}
                            </div>
                            <div className="text-[10px] text-gray-500">Trackers</div>
                          </div>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex items-center opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyToClipboard(carrier.id)}
                          className="h-6 w-6 p-0 hover:bg-gray-100"
                        >
                          <Copy className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>

                    {/* Connection Line Indicator */}
                    <div className={`absolute left-0 top-0 bottom-0 w-1 rounded-l-lg ${carrier.active
                      ? carrier.test_mode
                        ? "bg-orange-400"
                        : "bg-green-400"
                      : "bg-gray-300"
                      }`} />
                  </div>
                ))}
              </div>
            ) : accountCarriersQuery.data?.carrier_connections?.edges?.length === 0 ? (
              <div className="text-center py-12">
                <Truck className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <h3 className="text-lg font-medium text-gray-500 mb-2">
                  No carrier connections
                </h3>
                <p className="text-sm text-gray-400">
                  This organization hasn't set up any carrier connections yet.
                </p>
              </div>
            ) : (
              <div className="text-center py-12">
                <Truck className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <h3 className="text-lg font-medium text-gray-500 mb-2">
                  No carriers match your filters
                </h3>
                <p className="text-sm text-gray-400">
                  Try adjusting your search or filter criteria.
                </p>
                <Button
                  variant="outline"
                  className="mt-4"
                  onClick={() => {
                    setCarrierSearch("");
                    setCarrierFilter("all");
                  }}
                >
                  Clear filters
                </Button>
              </div>
            )}
          </div>
        )}

        {selectedTab === "shipments" && (
          <div className="space-y-6 mt-6">
            {shipmentsLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
              </div>
            ) : (shipments?.edges?.length ?? 0) > 0 ? (
              <div className="border-b">
                <Table>
                  <TableHeader className="bg-gray-50">
                    <TableRow>
                      <TableHead className="w-[350px]">Shipping Service</TableHead>
                      <TableHead className="w-[120px]">Status</TableHead>
                      <TableHead className="w-[250px]">Recipient</TableHead>
                      <TableHead className="w-[120px]">Total</TableHead>
                      <TableHead className="w-[120px]">Date</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {shipments?.edges?.map(({ node: shipment }) => (
                      <TableRow key={shipment.id} className="hover:bg-gray-50">
                        <TableCell>
                          <div className="flex items-center gap-3">
                            <CarrierImage
                              carrier_name={shipment.selected_rate?.carrier_name || shipment.meta?.carrier || "unknown"}
                              width={32}
                              height={32}
                              className="rounded"
                            />
                            <div className="min-w-0 flex-1">
                              <div className="flex items-center gap-2">
                                <span className="font-medium text-blue-600 text-sm">
                                  {shipment.tracking_number || "-"}
                                </span>
                              </div>
                              <div className="text-xs text-gray-500 truncate">
                                {shipment.selected_rate?.service || shipment.service || "No service"}
                              </div>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <StatusBadge status={shipment.status} />
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">
                            <div className="font-medium text-gray-900 truncate">
                              {shipment.recipient?.company_name ||
                                shipment.recipient?.person_name ||
                                "No recipient"}
                            </div>
                            <div className="text-xs text-gray-500 truncate">
                              {shipment.recipient?.city && shipment.recipient?.state_code
                                ? `${shipment.recipient.city}, ${shipment.recipient.state_code}`
                                : shipment.recipient?.city || "No address"}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm font-medium text-gray-900">
                            {shipment.selected_rate?.total_charge
                              ? `${shipment.selected_rate.total_charge} ${shipment.selected_rate.currency || "USD"}`
                              : "-"}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-xs text-gray-500">
                            {new Date(shipment.created_at).toLocaleDateString("en-US", {
                              month: "short",
                              day: "numeric",
                              year: "numeric"
                            })}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>

            ) : (
              <div className="text-center py-12">
                <Package className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <h3 className="text-lg font-medium text-gray-500 mb-2">
                  No shipments found
                </h3>
                <p className="text-sm text-gray-400">
                  No shipments found for the selected time period.
                </p>
              </div>
            )}
          </div>
        )}


        {selectedTab === "trackers" && (
          <div className="space-y-6 mt-6">
            {trackersLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
              </div>
            ) : (trackers?.edges?.length ?? 0) > 0 ? (
              <div className="border-b">
                <Table>
                  <TableHeader className="bg-gray-50">
                    <TableRow>
                      <TableHead className="w-[350px]">Tracking Service</TableHead>
                      <TableHead className="w-[120px]">Status</TableHead>
                      <TableHead className="w-[200px]">Last Event</TableHead>
                      <TableHead className="w-[120px]">Created</TableHead>
                      <TableHead className="w-[120px]">Last Updated</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {trackers?.edges?.map(({ node: tracker }) => {
                      const typedTracker = tracker as unknown as SystemTrackerNode;
                      return (
                        <TableRow key={typedTracker.id} className="hover:bg-gray-50">
                          <TableCell>
                            <div className="flex items-center gap-3">
                              <CarrierImage
                                carrier_name={typedTracker.meta?.carrier || typedTracker.carrier_name || "unknown"}
                                width={32}
                                height={32}
                                className="rounded"
                              />
                              <div className="min-w-0 flex-1">
                                <div className="flex items-center gap-2">
                                  <button
                                    onClick={() => copyToClipboard(typedTracker.tracking_number)}
                                    className="font-medium text-blue-600 text-sm hover:text-blue-700 transition-colors"
                                    title="Click to copy"
                                  >
                                    {typedTracker.tracking_number}
                                  </button>
                                </div>
                                <div className="text-xs text-gray-500 truncate">
                                  {typedTracker.info?.shipment_service ||
                                    typedTracker.shipment?.meta?.service_name ||
                                    typedTracker.shipment?.service ||
                                    "Service unknown"}
                                </div>
                              </div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <StatusBadge status={typedTracker.status} />
                          </TableCell>
                          <TableCell>
                            <div className="text-sm text-gray-900">
                              <div className="truncate">
                                {typedTracker.events && typedTracker.events.length > 0
                                  ? typedTracker.events[0].description || "No description"
                                  : "No events"}
                              </div>
                              <div className="text-xs text-gray-500">
                                {typedTracker.events && typedTracker.events.length > 0 && typedTracker.events[0].date
                                  ? `${typedTracker.events[0].date} ${typedTracker.events[0].time || ""}`.trim()
                                  : ""}
                              </div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="text-xs text-gray-500">
                              {new Date(typedTracker.created_at).toLocaleDateString("en-US", {
                                month: "short",
                                day: "numeric",
                                year: "numeric"
                              })}
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="text-xs text-gray-500">
                              {new Date(typedTracker.updated_at).toLocaleDateString("en-US", {
                                month: "short",
                                day: "numeric",
                                year: "numeric"
                              })}
                            </div>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </div>

            ) : (
              <div className="text-center py-12">
                <MapPin className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <h3 className="text-lg font-medium text-gray-500 mb-2">
                  No trackers found
                </h3>
                <p className="text-sm text-gray-400">
                  No tracking information found for the selected time period.
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default function Page(pageProps: { params: Promise<{ id?: string }> }) {
  const Component = (): JSX.Element => {
    const params = React.use(pageProps.params);
    const accountId = params.id;

    if (!accountId) {
      return (
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <Building2 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">Invalid Organization ID</h2>
            <p className="text-muted-foreground mb-4">
              Please provide a valid organization ID in the URL.
            </p>
          </div>
        </div>
      );
    }

    return <ShippersAccountDetail accountId={accountId} />;
  };

  return <Component />;
}
