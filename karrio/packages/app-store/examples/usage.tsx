"use client";
import React from "react";
import { AppContainer } from "@karrio/app-store";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";

/**
 * Example: Embedding the Greeter app in a dashboard
 */
export function DashboardWithGreeter() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Main content */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Shipments Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <p>Your shipment statistics and recent activity...</p>
            </CardContent>
          </Card>
        </div>

        {/* Embedded app */}
        <div>
          <AppContainer
            appId="greeter"
            viewport="dashboard"
            context={{
              workspace: {
                id: "ws_123",
                name: "Acme Shipping Co."
              },
              user: {
                id: "u_456",
                name: "John Doe",
                email: "john@acme.com"
              },
              page: {
                route: "/dashboard",
                params: {},
              },
            }}
            className="h-full"
          />
        </div>
      </div>
    </div>
  );
}

/**
 * Example: App marketplace page
 */
export function AppMarketplace() {
  // This would typically use useAppStore() hook
  const featuredApps = [
    {
      id: "greeter",
      name: "Greeter",
      description: "A simple greeting app for testing",
      category: "utility",
      features: ["automation"],
      installed: false,
    },
    {
      id: "shipstation",
      name: "ShipStation",
      description: "Connect your ShipStation account",
      category: "shipping",
      features: ["shipments", "orders"],
      installed: true,
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">App Marketplace</h1>
        <p className="text-gray-600">Discover apps to extend your Karrio experience</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {featuredApps.map((app) => (
          <Card key={app.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-base">{app.name}</CardTitle>
                  <p className="text-sm text-gray-600">{app.description}</p>
                </div>
                {app.installed && (
                  <Badge variant="default" className="text-xs">
                    Installed
                  </Badge>
                )}
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-1 mb-4">
                {app.features.map((feature) => (
                  <Badge key={feature} variant="secondary" className="text-xs">
                    {feature}
                  </Badge>
                ))}
              </div>

              {/* Preview the app */}
              {app.id === "greeter" && (
                <div className="border rounded-lg p-3 bg-gray-50">
                  <p className="text-xs text-gray-600 mb-2">Preview:</p>
                  <AppContainer
                    appId="greeter"
                    viewport="dashboard"
                    context={{
                      workspace: { id: "demo", name: "Demo Workspace" },
                      user: { id: "demo", name: "Demo User", email: "demo@example.com" },
                    }}
                    className="scale-75 origin-top-left"
                  />
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

/**
 * Example: Shipment detail page with embedded apps
 */
export function ShipmentDetailWithApps() {
  const shipmentId = "shp_123";

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Shipment #{shipmentId}</h1>
        <p className="text-gray-600">Track and manage your shipment</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main shipment info */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Shipment Details</CardTitle>
            </CardHeader>
            <CardContent>
              <p>Shipment information, tracking, etc...</p>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar with apps */}
        <div className="space-y-4">
          {/* Apps that support the "shipments" viewport */}
          <AppContainer
            appId="greeter"
            viewport="shipments"
            context={{
              workspace: { id: "ws_123", name: "Acme Shipping" },
              user: { id: "u_456", name: "John Doe", email: "john@acme.com" },
              page: { route: `/shipments/${shipmentId}`, params: { id: shipmentId } },
              data: {
                shipment: {
                  id: shipmentId,
                  status: "in_transit",
                  tracking_number: "1Z999AA1234567890"
                }
              },
            }}
          />
        </div>
      </div>
    </div>
  );
}

/**
 * Example: Error handling and fallbacks
 */
export function AppWithErrorHandling() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">App Error Handling Examples</h2>

      {/* App that doesn't exist */}
      <div>
        <h3 className="font-medium mb-2">Non-existent App:</h3>
        <AppContainer
          appId="non-existent-app"
          viewport="dashboard"
          context={{
            workspace: { id: "demo", name: "Demo" },
          }}
        />
      </div>

      {/* App with unsupported viewport */}
      <div>
        <h3 className="font-medium mb-2">Unsupported Viewport:</h3>
        <AppContainer
          appId="greeter"
          viewport={"unsupported-viewport" as any}
          context={{
            workspace: { id: "demo", name: "Demo" },
          }}
        />
      </div>
    </div>
  );
}

/**
 * Example: Building a custom app wrapper
 */
interface CustomAppWrapperProps {
  appId: string;
  title?: string;
  subtitle?: string;
  children?: React.ReactNode;
}

export function CustomAppWrapper({
  appId,
  title,
  subtitle,
  children
}: CustomAppWrapperProps) {
  return (
    <Card>
      {(title || subtitle) && (
        <CardHeader>
          {title && <CardTitle>{title}</CardTitle>}
          {subtitle && <p className="text-sm text-gray-600">{subtitle}</p>}
        </CardHeader>
      )}
      <CardContent>
        <AppContainer
          appId={appId}
          viewport="dashboard"
          context={{
            workspace: { id: "custom", name: "Custom Workspace" },
          }}
        />
        {children}
      </CardContent>
    </Card>
  );
}

/**
 * Example usage of custom wrapper
 */
export function DashboardWithCustomWrapper() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Custom App Integration</h1>

      <CustomAppWrapper
        appId="greeter"
        title="Welcome Widget"
        subtitle="A personalized greeting for your team"
      >
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            💡 This app is wrapped in a custom container with additional content.
          </p>
        </div>
      </CustomAppWrapper>
    </div>
  );
}
