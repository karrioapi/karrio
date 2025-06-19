"use client";

import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis } from "recharts";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { SelectField } from "@karrio/ui/core/components";
import { Button } from "@karrio/ui/components/ui/button";
import { useAppMode } from "@karrio/hooks/app-mode";
import { useAPIUsage } from "@karrio/hooks/usage";
import { useUser } from "@karrio/hooks/user";
import { useRouter } from "next/navigation";
import { p } from "@karrio/lib";
import moment from "moment";
import {
  Package,
  MapPin,
  DollarSign,
  ShoppingCart,
  Truck,
  FileText,
  Eye,
  Settings,
  ArrowRight,
  BarChart3
} from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const { basePath } = useAppMode();
  const {
    query: { data: { user } = {}, isLoading: userLoading, error: userError },
  } = useUser();
  const {
    query: { data: { usage } = {}, isLoading: usageLoading, error: usageError },
    setFilter,
    filter,
    USAGE_FILTERS,
    DAYS_LIST,
    currentFilter,
  } = useAPIUsage();

  // Don't render until user is loaded
  if (userLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Handle authentication errors
  if (userError || usageError) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <p className="text-red-600 mb-2">Authentication required</p>
          <p className="text-muted-foreground">Please refresh the page or sign in again.</p>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      title: "Total Shipments",
      value: usage?.total_shipments || 0,
      icon: Package,
      color: "text-primary",
      bgColor: "bg-primary/10",
      data: usage?.shipment_count,
      dataKey: "count"
    },
    {
      title: "Total Trackers",
      value: usage?.total_trackers || 0,
      icon: MapPin,
      color: "text-primary",
      bgColor: "bg-primary/10",
      data: usage?.tracker_count,
      dataKey: "count"
    },
    {
      title: "Order Volume",
      value: `$${usage?.order_volume || 0}`,
      icon: ShoppingCart,
      color: "text-primary",
      bgColor: "bg-primary/10",
      data: usage?.order_volumes,
      dataKey: "count"
    },
    {
      title: "Shipping Spend",
      value: `$${usage?.total_shipping_spend || 0}`,
      icon: DollarSign,
      color: "text-primary",
      bgColor: "bg-primary/10",
      data: usage?.shipping_spend,
      dataKey: "count"
    }
  ];

  const actionCards = [
    {
      title: "Add shipping location address",
      description: "Add one or multiple warehouse locations.",
      icon: MapPin,
      href: "/settings/addresses",
      color: "text-primary",
      bgColor: "bg-primary/10"
    },
    {
      title: "Set up carrier accounts",
      description: "Connect your carrier accounts to start shipping.",
      icon: Truck,
      href: "/connections",
      color: "text-primary",
      bgColor: "bg-primary/10"
    },
    {
      title: "Print a test label",
      description: "Generate a test label for a sample shipment.",
      icon: FileText,
      href: "/test/create_label?shipment_id=new",
      color: "text-primary",
      bgColor: "bg-primary/10",
      external: true
    },
    {
      title: "Add a tracking number",
      description: "Add one or multiple shipments to track.",
      icon: MapPin,
      href: "/trackers?modal=new",
      color: "text-primary",
      bgColor: "bg-primary/10"
    },
    {
      title: "Set up an API connection",
      description: "Retrieve your API key to connect via API.",
      icon: Settings,
      href: "/developers/apikeys",
      color: "text-primary",
      bgColor: "bg-primary/10"
    },
    {
      title: "Review your API requests",
      description: "Audit your API requests logs and system health.",
      icon: Eye,
      href: "/developers/logs",
      color: "text-primary",
      bgColor: "bg-primary/10"
    }
  ];

  const renderChart = (data: any[] | null | undefined, dataKey: string = "count") => {
    if (!data || data.length === 0) return null;

    const chartData = DAYS_LIST[currentFilter() || "15 days"].map(
      (day) => ({
        name: day,
        [dataKey]: data.find(
          ({ date }) => moment(date).format("MMM D") === day,
        )?.[dataKey] || 0,
      }),
    );

    return (
      <ResponsiveContainer width="100%" height={120}>
        <BarChart data={chartData}>
          <Tooltip
            contentStyle={{
              background: 'hsl(var(--card))',
              border: '1px solid hsl(var(--border))',
              borderRadius: '6px',
              fontSize: '12px'
            }}
          />
          <Bar dataKey={dataKey} fill="#79e5dd" radius={[2, 2, 0, 0]} />
          <XAxis
            dataKey="name"
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 10, fill: 'hsl(var(--muted-foreground))' }}
            interval="preserveStartEnd"
          />
        </BarChart>
      </ResponsiveContainer>
    );
  };

  return (
    <>
      <header className="pb-0 pt-4 is-flex is-justify-content-space-between">
        <span className="title is-4">
          {`Welcome${!!user?.full_name ? ", " + user.full_name : ""}`}
        </span>
        <div></div>
      </header>

      <div className="mt-6 space-y-8">
        {/* Usage Filter */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg sm:text-xl font-semibold">Usage Overview</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Track your shipping activity and performance metrics
            </p>
          </div>
          <div className="w-full sm:w-48 sm:ml-auto">
            <SelectField
              className="is-small text-right"
              fieldClass="py-0"
              value={JSON.stringify(filter)}
              onChange={(e) => setFilter(JSON.parse(e.target.value))}
              disabled={usageLoading}
            >
              {Object.entries(USAGE_FILTERS).map(([key, value]) => (
                <option key={key} value={JSON.stringify(value)}>
                  {key}
                </option>
              ))}
            </SelectField>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          {usageLoading ? (
            // Loading skeleton for stats cards
            Array.from({ length: 4 }).map((_, index) => (
              <Card key={index} className="transition-all">
                <CardContent className="p-3">
                  <div className="flex items-center justify-between mb-3">
                    <div className="w-10 h-10 bg-gray-200 rounded-lg animate-pulse"></div>
                    <div className="w-4 h-4 bg-gray-200 rounded animate-pulse"></div>
                  </div>
                  <div className="space-y-1 mb-3">
                    <div className="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
                    <div className="w-16 h-8 bg-gray-200 rounded animate-pulse"></div>
                  </div>
                  <div className="h-[120px] bg-gray-100 rounded animate-pulse"></div>
                </CardContent>
              </Card>
            ))
          ) : (
            statCards.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <Card key={index} className="transition-all">
                  <CardContent className="p-3">
                    <div className="flex items-center justify-between mb-3">
                      <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                        <Icon className={`h-5 w-5 ${stat.color}`} />
                      </div>
                      <BarChart3 className="h-4 w-4 text-muted-foreground" />
                    </div>

                    <div className="space-y-1 mb-3">
                      <p className="text-sm font-medium text-muted-foreground">
                        {stat.title}
                      </p>
                      <p className="text-2xl font-bold">
                        {stat.value}
                      </p>
                    </div>

                    {/* Mini Chart */}
                    <div className={`h-[120px] ${stat.color}`}>
                      {renderChart(stat.data, stat.dataKey)}
                    </div>
                  </CardContent>
                </Card>
              );
            })
          )}
        </div>

        {/* Unfulfilled Orders Alert */}
        {!!usage?.unfulfilled_orders && usage.unfulfilled_orders > 0 && (
          <Card className="border-orange-200 bg-orange-50">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-orange-100">
                    <ShoppingCart className="h-5 w-5 text-orange-600" />
                  </div>
                  <div>
                    <h3 className="font-medium text-orange-900">
                      {usage.unfulfilled_orders} order{usage.unfulfilled_orders > 1 ? "s" : ""} to fulfill
                    </h3>
                    <p className="text-sm text-orange-700">
                      You have pending orders waiting to be fulfilled
                    </p>
                  </div>
                </div>
                <Button asChild size="sm" className="bg-orange-600 hover:bg-orange-700">
                  <AppLink href="/orders?status=unfulfilled,partial">
                    View Orders
                    <ArrowRight className="h-4 w-4 ml-2" />
                  </AppLink>
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Quick Actions */}
        <div className="space-y-4">
          <div>
            <h2 className="text-lg sm:text-xl font-semibold">Quick Actions</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Common tasks to help you get started and manage your shipping
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
            {actionCards.map((action, index) => {
              const Icon = action.icon;
              const href = action.external ? action.href : p`${basePath}${action.href}`;

              return (
                <Card
                  key={index}
                  className="cursor-pointer transition-all hover:scale-[1.02] group"
                  onClick={() => router.push(href)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      <div className={`p-2 rounded-lg ${action.bgColor} group-hover:scale-110 transition-transform`}>
                        <Icon className={`h-5 w-5 ${action.color}`} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-sm leading-5 mb-1">
                          {action.title}
                        </h3>
                        <p className="text-xs text-muted-foreground leading-4">
                          {action.description}
                        </p>
                      </div>
                      <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-foreground group-hover:translate-x-1 transition-all" />
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </div>
    </>
  );
}
