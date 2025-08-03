"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { ResponsiveContainer, Tooltip, PieChart, Pie, Cell } from "recharts";
import { useOrganizationAccounts } from "@karrio/hooks/admin-accounts";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Button } from "@karrio/ui/components/ui/button";
import { useUser } from "@karrio/hooks/user";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import {
  Package,
  MapPin,
  DollarSign,
  ShoppingCart,
  Users,
  Building2,
  Activity,
  AlertTriangle,
  BarChart3,
  ArrowRight,
  CheckCircle,
  XCircle,
} from "lucide-react";

export default function ShippersOverview() {
  const {
    query: { data: { user } = {}, isLoading: userLoading },
  } = useUser();

  const { query, accounts: accountsData } = useOrganizationAccounts();
  const isLoading = query.isLoading;

  // Don't render until user is loaded
  if (userLoading || isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading system overview...</p>
        </div>
      </div>
    );
  }

  const accounts = accountsData?.edges || [];

  // Calculate system-wide statistics
  const systemStats = accounts.reduce((acc, { node }) => {
    const usage = node.usage || {};
    return {
      totalOrganizations: acc.totalOrganizations + 1,
      activeOrganizations: acc.activeOrganizations + (node.is_active ? 1 : 0),
      totalMembers: acc.totalMembers + (usage.members || 0),
      totalShipments: acc.totalShipments + (usage.total_shipments || 0),
      totalTrackers: acc.totalTrackers + (usage.total_trackers || 0),
      totalRequests: acc.totalRequests + (usage.total_requests || 0),
      totalSpend: acc.totalSpend + (usage.total_shipping_spend || 0),
      totalErrors: acc.totalErrors + (usage.total_errors || 0),
      orderVolume: acc.orderVolume + (usage.order_volume || 0),
      unfulfilled: acc.unfulfilled + (usage.unfulfilled_orders || 0),
    };
  }, {
    totalOrganizations: 0,
    activeOrganizations: 0,
    totalMembers: 0,
    totalShipments: 0,
    totalTrackers: 0,
    totalRequests: 0,
    totalSpend: 0,
    totalErrors: 0,
    orderVolume: 0,
    unfulfilled: 0,
  });

  const systemHealthMetrics = [
    {
      title: "Active Organizations",
      value: systemStats.activeOrganizations,
      total: systemStats.totalOrganizations,
      percentage: systemStats.totalOrganizations > 0 ? Math.round((systemStats.activeOrganizations / systemStats.totalOrganizations) * 100) : 0,
      icon: Building2,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
      trend: "+12%"
    },
    {
      title: "Total Members",
      value: systemStats.totalMembers,
      icon: Users,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
      trend: "+8%"
    },
    {
      title: "API Requests",
      value: systemStats.totalRequests.toLocaleString(),
      icon: Activity,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
      trend: "+15%"
    },
    {
      title: "System Health",
      value: systemStats.totalRequests > 0 ? Math.round(((systemStats.totalRequests - systemStats.totalErrors) / systemStats.totalRequests) * 100) : 100,
      suffix: "%",
      icon: CheckCircle,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
      trend: "+2%"
    }
  ];

  const operationalMetrics = [
    {
      title: "Total Shipments",
      value: systemStats.totalShipments.toLocaleString(),
      icon: Package,
      color: "text-purple-600",
      bgColor: "bg-purple-50"
    },
    {
      title: "Total Trackers",
      value: systemStats.totalTrackers.toLocaleString(),
      icon: MapPin,
      color: "text-purple-600",
      bgColor: "bg-purple-50"
    },
    {
      title: "Shipping Spend",
      value: `$${systemStats.totalSpend.toLocaleString()}`,
      icon: DollarSign,
      color: "text-purple-600",
      bgColor: "bg-purple-50"
    },
    {
      title: "Order Volume",
      value: `$${systemStats.orderVolume.toLocaleString()}`,
      icon: ShoppingCart,
      color: "text-purple-600",
      bgColor: "bg-purple-50"
    }
  ];

  // Top organizations by shipments
  const topOrganizations = accounts
    .map(({ node }) => ({
      name: node.name,
      shipments: node.usage?.total_shipments || 0,
      spend: node.usage?.total_shipping_spend || 0,
      members: node.usage?.members || 0,
      isActive: node.is_active
    }))
    .sort((a, b) => b.shipments - a.shipments)
    .slice(0, 5);

  // Organization status distribution
  const statusDistribution = [
    { name: 'Active', value: systemStats.activeOrganizations, color: '#10b981' },
    { name: 'Inactive', value: systemStats.totalOrganizations - systemStats.activeOrganizations, color: '#ef4444' }
  ];

  return (
    <div className="space-y-8">
      <header className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">System Overview</h1>
          <p className="text-muted-foreground">
            Monitor your platform's health and organizational metrics
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Select defaultValue="30">
            <SelectTrigger className="w-[140px]">
              <SelectValue placeholder="Time range" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7">Last 7 days</SelectItem>
              <SelectItem value="15">Last 15 days</SelectItem>
              <SelectItem value="30">Last 30 days</SelectItem>
              <SelectItem value="90">Last 90 days</SelectItem>
            </SelectContent>
          </Select>
          <Button asChild>
            <AppLink href="/shippers/accounts">
              View All Organizations
              <ArrowRight className="h-4 w-4 ml-2" />
            </AppLink>
          </Button>
        </div>
      </header>

      {/* System Health Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        {systemHealthMetrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <Card key={index} className="border-2 shadow-none">
              <CardContent className="p-4">
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-3 rounded-lg ${metric.bgColor}`}>
                    <Icon className={`h-6 w-6 ${metric.color}`} />
                  </div>
                  <div className="text-xs font-medium text-purple-600 bg-purple-50 px-2 py-1 rounded-full">
                    {metric.trend}
                  </div>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    {metric.title}
                  </p>
                  <p className="text-2xl font-bold">
                    {metric.value.toLocaleString()}{metric.suffix}
                    {metric.total && (
                      <span className="text-sm text-muted-foreground font-normal ml-1">
                        / {metric.total}
                      </span>
                    )}
                  </p>
                  {metric.percentage !== undefined && (
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div
                        className="bg-purple-600 h-2 rounded-full"
                        style={{ width: `${metric.percentage}%` }}
                      ></div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Alerts and Issues */}
      {systemStats.totalErrors > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <Card className="border-red-200 bg-red-50">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-red-100">
                    <AlertTriangle className="h-6 w-6 text-red-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-red-900">
                      {systemStats.totalErrors.toLocaleString()} system errors
                    </h3>
                    <p className="text-sm text-red-700">
                      API errors across all organizations need attention
                    </p>
                  </div>
                </div>
                <Button size="sm" variant="outline" className="border-red-300 text-red-700 hover:bg-red-100">
                  View Logs
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Operational Metrics and Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Operational Metrics */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-lg font-semibold">Operational Metrics</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {operationalMetrics.map((metric, index) => {
              const Icon = metric.icon;
              return (
                <Card key={index} className="border-2 shadow-none">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className={`p-2 rounded-lg ${metric.bgColor}`}>
                        <Icon className={`h-5 w-5 ${metric.color}`} />
                      </div>
                      <BarChart3 className="h-4 w-4 text-purple-600" />
                    </div>
                    <div className="space-y-1">
                      <p className="text-sm font-medium text-muted-foreground">
                        {metric.title}
                      </p>
                      <p className="text-xl font-bold">
                        {metric.value}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Organization Status Distribution */}
        <Card className="border-2 shadow-none">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg">Organization Status</CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <div className="h-[200px] flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={statusDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    dataKey="value"
                  >
                    {statusDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-4 space-y-2">
              {statusDistribution.map((item, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: item.color }}
                    ></div>
                    <span className="text-sm">{item.name}</span>
                  </div>
                  <span className="text-sm font-medium">{item.value}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Top Organizations */}
      <Card className="border-2 shadow-none">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Top Organizations by Shipments</CardTitle>
        </CardHeader>
        <CardContent className="p-4 pt-0">
          <div className="space-y-4">
            {topOrganizations.map((org, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                    <span className="text-sm font-medium text-purple-600">
                      {index + 1}
                    </span>
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="font-medium">{org.name}</p>
                      {org.isActive ? (
                        <CheckCircle className="h-4 w-4 text-purple-600" />
                      ) : (
                        <XCircle className="h-4 w-4 text-red-600" />
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {org.members} members
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-medium">{org.shipments.toLocaleString()} shipments</p>
                  <p className="text-sm text-muted-foreground">
                    ${org.spend.toLocaleString()} spend
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
