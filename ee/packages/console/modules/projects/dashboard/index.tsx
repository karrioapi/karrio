"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@karrio/insiders/components/ui/card";
import { DashboardHeader } from "@karrio/console/components/dashboard-header";
import { Button } from "@karrio/insiders/components/ui/button";
import { Badge } from "@karrio/insiders/components/ui/badge";
import {
  CopyIcon,
  AlertCircle,
  AlertTriangle,
  BookOpen,
  Code2,
  Boxes,
  PackageSearch,
  Truck,
  Settings,
  ExternalLink,
  Loader2,
} from "lucide-react";
import { Alert, AlertDescription } from "@karrio/insiders/components/ui/alert";
import { toast } from "@karrio/insiders/hooks/use-toast";
import { trpc } from "@karrio/console/trpc/client";
import moment from "moment";
import React, { useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/insiders/components/ui/select";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis } from "recharts";

interface DataPoint {
  name: string;
  total: number;
  failed: number;
}

export default function DashboardPage({
  params,
}: {
  params: { orgId: string; projectId: string };
}) {
  const utils = trpc.useContext();
  const { data: currentProject, isLoading: isProjectLoading } =
    trpc.projects.get.useQuery({
      id: params.projectId,
      organizationId: params.orgId,
    });
  const { data: tenant, isLoading: isTenantLoading } =
    trpc.projects.tenant.get.useQuery(
      { projectId: params.projectId },
      {
        enabled: Boolean(params.projectId),
        refetchInterval: currentProject?.status !== "ACTIVE" ? 30000 : false,
      },
    );
  const checkTenantHealth = trpc.projects.checkTenantHealth.useMutation({
    onSuccess: () => {
      utils.projects.get.invalidate();
    },
  });

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied to clipboard",
      description: "The URL has been copied to your clipboard",
      variant: "default",
    });
  };

  const [dateRange, setDateRange] = useState("15");

  const dateFilter = React.useMemo(
    () => ({
      date_before: moment().toISOString(),
      date_after: moment().subtract(parseInt(dateRange), "days").toISOString(),
    }),
    [dateRange], // Only recalculate when dateRange changes
  );

  const usageStats = trpc.projects.tenant.getUsageStats.useQuery(
    {
      projectId: params.projectId,
      filter: dateFilter,
    },
    {
      enabled: Boolean(params.projectId) && currentProject?.status === "ACTIVE",
    },
  );

  React.useEffect(() => {
    if (tenant && currentProject?.status !== "ACTIVE") {
      utils.projects.get.invalidate();
    }
  }, [tenant]);

  // Handle loading and error states
  if (!params.projectId) {
    return (
      <div className="flex flex-col items-center justify-center h-[50vh]">
        <h2 className="text-xl font-semibold">No Project Selected</h2>
        <p className="text-muted-foreground">
          Please select a project to view its dashboard
        </p>
      </div>
    );
  }

  if (isProjectLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-[50vh]">
        <Loader2 className="h-8 w-8 animate-spin mb-4" />
        <p className="text-muted-foreground">Loading project details...</p>
      </div>
    );
  }

  if (!currentProject) {
    return (
      <div className="flex flex-col items-center justify-center h-[50vh]">
        <h2 className="text-xl font-semibold text-destructive">
          Project Not Found
        </h2>
        <p className="text-muted-foreground">
          The requested project could not be found
        </p>
      </div>
    );
  }

  const isHealthy = currentProject?.status === "ACTIVE";
  const isPending = currentProject?.status === "PENDING";

  return (
    <>
      <DashboardHeader
        title="Project Dashboard"
        description="Monitor your project's health and usage metrics"
      />

      <div className="flex flex-1 flex-col gap-12 p-8 bg-background">
        {/* Project Header */}
        <div className="max-w-6xl mx-auto w-full space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tight">
                {currentProject?.name || "Project Dashboard"}
              </h2>
            </div>
            <Badge
              variant={
                isHealthy ? "default" : isPending ? "secondary" : "destructive"
              }
              className="px-4 py-1 text-sm"
            >
              {currentProject?.status || "PENDING"}
            </Badge>
          </div>

          {isPending && (
            <Alert className="mt-4 border-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              <AlertDescription>
                Your project is being deployed. This may take a few minutes...
              </AlertDescription>
            </Alert>
          )}

          {isHealthy && isTenantLoading && (
            <Alert className="mt-4 border-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              <AlertDescription>
                Initializing tenant services...
              </AlertDescription>
            </Alert>
          )}
        </div>

        {/* Project Stats and API Usage Section */}
        {isHealthy && tenant && (
          <div className="max-w-6xl mx-auto w-full space-y-6 md:space-y-0 md:grid md:grid-cols-12 md:gap-4">
            {/* Left Side - API Usage Graph */}
            <div className="col-span-12 md:col-span-12 lg:col-span-8">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">API Requests</h3>
                  <Select value={dateRange} onValueChange={setDateRange}>
                    <SelectTrigger className="w-[120px]">
                      <SelectValue placeholder="Select days" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="7">7 days</SelectItem>
                      <SelectItem value="15">15 days</SelectItem>
                      <SelectItem value="30">30 days</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="border-t border-border/40 my-0" />

                {/* Legend */}
                <div className="flex items-center gap-6">
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-sm bg-primary/30" />
                    <span className="text-sm font-medium">
                      {usageStats?.data?.total_requests} total
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-sm bg-destructive/30" />
                    <span className="text-sm font-medium">
                      {usageStats?.data?.total_errors} failed
                    </span>
                  </div>
                </div>

                {/* Graph */}
                <div className="h-[300px] w-full relative bg-background/50 rounded-lg p-4 border-2">
                  {!usageStats.data?.api_requests ||
                    usageStats.data.api_requests.length === 0 ? (
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-center text-muted-foreground">
                        <p className="font-medium">
                          No API requests data available
                        </p>
                        <p className="text-sm mt-2">
                          Start making requests to see usage metrics
                        </p>
                      </div>
                    </div>
                  ) : (
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart
                        data={usageStats.data.api_requests
                          .map(
                            (data, idx): DataPoint => ({
                              name: moment(data.date).format("MMM D"),
                              total: data.count || 0,
                              failed:
                                usageStats.data?.api_errors?.[idx]?.count || 0,
                            }),
                          )
                          .reverse()}
                        margin={{ top: 5, right: 5, left: 5, bottom: 25 }}
                      >
                        <Tooltip
                          content={({ active, payload, label }) => {
                            if (active && payload && payload.length) {
                              return (
                                <div className="rounded-lg border-2 bg-background p-3 shadow-lg">
                                  <div className="grid gap-2">
                                    <div className="text-[0.70rem] uppercase text-muted-foreground font-medium">
                                      {label}
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                      <div className="flex flex-col">
                                        <span className="text-[0.70rem] uppercase text-muted-foreground">
                                          Total
                                        </span>
                                        <span className="font-bold text-primary">
                                          {payload[0].value}
                                        </span>
                                      </div>
                                      <div className="flex flex-col">
                                        <span className="text-[0.70rem] uppercase text-muted-foreground">
                                          Failed
                                        </span>
                                        <span className="font-bold text-destructive">
                                          {payload[1].value}
                                        </span>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              );
                            }
                            return null;
                          }}
                        />
                        <Line
                          type="linear"
                          dataKey="total"
                          stroke="#7c3aed"
                          strokeWidth={2.5}
                          dot={false}
                        />
                        <Line
                          type="linear"
                          dataKey="failed"
                          stroke="#ef4444"
                          strokeWidth={2.5}
                          dot={false}
                        />
                        <XAxis
                          dataKey="name"
                          stroke="#888888"
                          fontSize={12}
                          tickLine={false}
                          axisLine={false}
                          ticks={[
                            usageStats.data.api_requests[
                              usageStats.data.api_requests.length - 1
                            ]?.date,
                            usageStats.data.api_requests[0]?.date,
                          ].map((date) => moment(date).format("MMM D"))}
                          interval="preserveStartEnd"
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  )}
                </div>
              </div>
            </div>

            {/* Right Side - Stats */}
            <div className="col-span-12 lg:col-span-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-1 gap-3 h-full">
                <Card className="rounded-lg border-2 shadow-sm">
                  <CardHeader className="p-4 pb-2">
                    <CardTitle>Shipping Spend</CardTitle>
                  </CardHeader>
                  <CardContent className="p-4 pt-2">
                    <div className="text-2xl font-bold text-primary">
                      $
                      {usageStats?.data?.total_shipping_spend?.toFixed(2) ||
                        "0.00"}
                    </div>
                  </CardContent>
                </Card>

                <Card className="rounded-lg border-2 shadow-sm">
                  <CardHeader className="p-4 pb-2">
                    <CardTitle>Shipments</CardTitle>
                  </CardHeader>
                  <CardContent className="p-4 pt-2">
                    <div className="text-2xl font-bold text-primary">
                      {usageStats?.data?.total_shipments || 0}
                    </div>
                  </CardContent>
                </Card>

                <Card className="rounded-lg border-2 shadow-sm">
                  <CardHeader className="p-4 pb-2">
                    <CardTitle>Trackers</CardTitle>
                  </CardHeader>
                  <CardContent className="p-4 pt-2">
                    <div className="text-2xl font-bold text-primary">
                      {usageStats?.data?.total_trackers || 0}
                    </div>
                  </CardContent>
                </Card>

                <Card className="rounded-lg border-2 shadow-sm">
                  <CardHeader className="p-4 pb-2">
                    <CardTitle>Connected Accounts</CardTitle>
                  </CardHeader>
                  <CardContent className="p-4 pt-2">
                    <div className="text-2xl font-bold text-primary">
                      {usageStats?.data?.organization_count || 0}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        )}

        <div className="max-w-6xl mx-auto w-full border-t" />

        {/* Project API Info */}
        <div className="max-w-6xl mx-auto w-full">
          <Card className="rounded-lg border-2 shadow-sm">
            <CardContent className="p-6 space-y-8">
              <div>
                <h3 className="text-lg font-semibold">Project API</h3>
                <p className="text-sm text-muted-foreground">
                  Your API is secured behind a gateway which requires an API Key
                  for every request.
                </p>
              </div>

              {tenant && isHealthy ? (
                <div className="space-y-8">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">API Endpoints</span>
                    </div>
                    {tenant.api_domains?.map((domain, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <code className="flex-1 rounded-lg bg-muted px-3 py-2 font-mono text-sm">
                          {domain}
                        </code>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyToClipboard(domain)}
                        >
                          <CopyIcon className="h-4 w-4 mr-1" />
                          Copy
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => window.open(domain, "_blank")}
                        >
                          <ExternalLink className="h-4 w-4 mr-1" />
                          Open
                        </Button>
                      </div>
                    ))}
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">
                        Dashboard URLs
                      </span>
                    </div>
                    {tenant.app_domains?.map((domain, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <code className="flex-1 rounded-lg bg-muted px-3 py-2 font-mono text-sm">
                          {domain}
                        </code>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyToClipboard(domain)}
                        >
                          <CopyIcon className="h-4 w-4 mr-1" />
                          Copy
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => window.open(domain, "_blank")}
                        >
                          <ExternalLink className="h-4 w-4 mr-1" />
                          Open
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="text-sm text-muted-foreground">
                    Project endpoints will be available once the project is
                    healthy
                  </div>
                  {currentProject?.status === "FAILED" && (
                    <Alert variant="destructive">
                      <AlertTriangle className="h-4 w-4" />
                      <AlertDescription>
                        Tenant deployment failed. Please check the logs or
                        contact support.
                      </AlertDescription>
                    </Alert>
                  )}
                  {currentProject?.status === "UNREACHABLE" && (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>
                        Tenant is currently unreachable. Last successful
                        connection:{" "}
                        {currentProject.lastPing
                          ? new Date(currentProject.lastPing).toLocaleString()
                          : "Never"}
                      </AlertDescription>
                    </Alert>
                  )}
                  {currentProject?.status === "ACTIVE" && (
                    <Button
                      onClick={() => {
                        checkTenantHealth.mutate({
                          projectId: params.projectId,
                        });
                      }}
                      disabled={checkTenantHealth.status === "loading"}
                    >
                      Check Tenant Health
                    </Button>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="max-w-6xl mx-auto w-full border-t" />

        {/* Let's get started */}
        <div className="max-w-6xl mx-auto w-full space-y-8">
          <h2 className="text-2xl font-semibold">Let's get started</h2>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card className="p-6 hover:border-primary/50 transition-colors rounded-lg border-2 shadow-sm">
              <div className="p-2 w-fit rounded-lg bg-primary/10 mb-6">
                <Code2 className="h-4 w-4 text-primary" />
              </div>
              <h3 className="font-semibold mb-3">API Integration</h3>
              <p className="text-sm text-muted-foreground mb-6">
                Start integrating shipping services with our API endpoints.
              </p>
              <Button
                variant="ghost"
                className="w-full justify-start"
                onClick={() => window.open("/docs/api", "_blank")}
              >
                View Documentation <ExternalLink className="ml-2 h-4 w-4" />
              </Button>
            </Card>

            <Card className="p-6 hover:border-primary/50 transition-colors rounded-lg border-2 shadow-sm">
              <div className="p-2 w-fit rounded-lg bg-primary/10 mb-6">
                <Boxes className="h-4 w-4 text-primary" />
              </div>
              <h3 className="font-semibold mb-3">Carrier Setup</h3>
              <p className="text-sm text-muted-foreground mb-6">
                Connect and configure your shipping carrier accounts.
              </p>
              <Button
                variant="ghost"
                className="w-full justify-start"
                onClick={() =>
                  window.open(tenant?.app_domains?.[0] + "/carriers", "_blank")
                }
              >
                Configure Carriers <ExternalLink className="ml-2 h-4 w-4" />
              </Button>
            </Card>

            <Card className="p-6 hover:border-primary/50 transition-colors rounded-lg border-2 shadow-sm">
              <div className="p-2 w-fit rounded-lg bg-primary/10 mb-6">
                <Settings className="h-4 w-4 text-primary" />
              </div>
              <h3 className="font-semibold mb-3">Project Settings</h3>
              <p className="text-sm text-muted-foreground mb-6">
                Configure your project settings and API keys.
              </p>
              <Button
                variant="ghost"
                className="w-full justify-start"
                onClick={() =>
                  window.open(tenant?.app_domains?.[0] + "/settings", "_blank")
                }
              >
                Open Settings <ExternalLink className="ml-2 h-4 w-4" />
              </Button>
            </Card>
          </div>
        </div>

        <div className="max-w-6xl mx-auto w-full border-t" />

        {/* Explore the platform */}
        <div className="max-w-6xl mx-auto w-full space-y-8 pb-8">
          <h2 className="text-2xl font-semibold">Explore the platform</h2>
          <div className="grid gap-8 md:grid-cols-2">
            <div className="space-y-6">
              <div className="flex items-start gap-6">
                <div className="p-2 rounded-lg bg-primary/10">
                  <BookOpen className="h-4 w-4 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Documentation</h3>
                  <p className="text-sm text-muted-foreground">
                    Learn how to integrate Karrio shipping services into your
                    application.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-6">
                <div className="p-2 rounded-lg bg-primary/10">
                  <PackageSearch className="h-4 w-4 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">API Reference</h3>
                  <p className="text-sm text-muted-foreground">
                    Detailed documentation of all Karrio API endpoints and
                    methods.
                  </p>
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div className="flex items-start gap-6">
                <div className="p-2 rounded-lg bg-primary/10">
                  <Truck className="h-4 w-4 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Carrier Integrations</h3>
                  <p className="text-sm text-muted-foreground">
                    Guides on setting up and using different shipping carriers.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-6">
                <div className="p-2 rounded-lg bg-primary/10">
                  <Code2 className="h-4 w-4 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">SDKs</h3>
                  <p className="text-sm text-muted-foreground">
                    Official client libraries for your preferred programming
                    language.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
