"use client";

import React, { useState } from "react";
import { useDeveloperTools, DeveloperView } from "@karrio/developers/context/developer-tools-context";
import { Drawer, DrawerPortal, DrawerHeader, DrawerTitle, DrawerDescription } from "@karrio/ui/components/ui/drawer";
import { Drawer as DrawerPrimitive } from "vaul";
import { X, Activity, Key, Webhook, Calendar, FileText, Settings, Terminal, Menu } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@karrio/ui/components/ui/tabs";
import { Button } from "@karrio/ui/components/ui/button";
import { cn } from "@karrio/ui/lib/utils";

// Import view components
import { WebhooksView } from "@karrio/developers/components/views/webhooks-view";
import { ActivityView } from "@karrio/developers/components/views/activity-view";
import { ApiKeysView } from "@karrio/developers/components/views/api-keys-view";
import { EventsView } from "@karrio/developers/components/views/events-view";
import { LogsView } from "@karrio/developers/components/views/logs-view";
import { AppsView } from "@karrio/developers/components/views/apps-view";

// Custom DrawerContent without overlay
const CustomDrawerContent = React.forwardRef<
  React.ElementRef<typeof DrawerPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DrawerPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DrawerPortal>
    <DrawerPrimitive.Content
      ref={ref}
      className={cn(
        "fixed inset-0 z-50 flex h-full flex-col rounded-none border bg-background",
        "w-full max-w-full", // Full screen on mobile, no margins
        className
      )}
      {...props}
    >
      <div className="mx-auto mt-2 h-1 w-[100px] rounded-full bg-muted lg:hidden" />
      {children}
    </DrawerPrimitive.Content>
  </DrawerPortal>
));

const VIEW_CONFIG = {
  activity: {
    label: "Activity",
    icon: Activity,
    component: ActivityView,
  },
  "api-keys": {
    label: "API Keys",
    icon: Key,
    component: ApiKeysView,
  },
  logs: {
    label: "Logs",
    icon: FileText,
    component: LogsView,
  },
  events: {
    label: "Events",
    icon: Calendar,
    component: EventsView,
  },
  apps: {
    label: "Apps",
    icon: Settings,
    component: AppsView,
  },
  webhooks: {
    label: "Webhooks",
    icon: Webhook,
    component: WebhooksView,
  },
};

export function DeveloperToolsDrawer() {
  const { isOpen, currentView, closeDeveloperTools, setCurrentView } = useDeveloperTools();
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  const handleTabChange = (value: string) => {
    setCurrentView(value as DeveloperView);
    // Close mobile sidebar when selecting a tab
    setIsMobileSidebarOpen(false);
  };

  return (
    <Drawer open={isOpen} onOpenChange={(open) => {
      if (!open) {
        closeDeveloperTools();
        setIsMobileSidebarOpen(false);
      }
    }}>
      <CustomDrawerContent className="h-full max-h-full flex flex-col overflow-hidden">
        {/* Header */}
        <DrawerHeader className="flex-shrink-0 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-2 sm:px-4 py-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 sm:gap-3">
              {/* Mobile menu button */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
                className="h-10 w-10 p-0 lg:hidden"
              >
                <Menu className="h-6 w-6" />
              </Button>
              <Terminal className="h-6 w-6 sm:h-7 sm:w-7 text-muted-foreground" />
              <DrawerTitle className="text-base sm:text-lg font-semibold">Developer Tools</DrawerTitle>
              <DrawerDescription className="sr-only">Developer tools drawer</DrawerDescription>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={closeDeveloperTools}
              className="h-10 w-10 p-0"
            >
              <X className="h-6 w-6" />
            </Button>
          </div>
        </DrawerHeader>

        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden relative">
          <Tabs
            value={currentView}
            onValueChange={handleTabChange}
            orientation="vertical"
            className="flex h-full w-full"
          >
            {/* Mobile Sidebar Overlay */}
            {isMobileSidebarOpen && (
              <div
                className="absolute inset-0 bg-black/20 z-20 lg:hidden"
                onClick={() => setIsMobileSidebarOpen(false)}
              />
            )}

            {/* Sidebar Navigation */}
            <div className={cn(
              "flex-shrink-0 border-r bg-background transition-transform duration-200 ease-in-out z-30",
              // Mobile: slide in from left, hidden by default
              "absolute lg:relative inset-y-0 left-0",
              "w-52 sm:w-56 lg:w-52",
              isMobileSidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
            )}>
              <TabsList className="flex flex-col h-full w-full justify-start bg-transparent p-2 space-y-1">
                {Object.entries(VIEW_CONFIG).map(([viewKey, config]) => {
                  const Icon = config.icon;
                  return (
                    <TabsTrigger
                      key={viewKey}
                      value={viewKey}
                      className={cn(
                        "w-full justify-start gap-3 px-3 py-3 text-sm font-medium transition-all",
                        "data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm",
                        "hover:bg-muted/50"
                      )}
                    >
                      <Icon className="h-5 w-5 flex-shrink-0" />
                      <span className="truncate">{config.label}</span>
                    </TabsTrigger>
                  );
                })}
              </TabsList>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 overflow-hidden lg:ml-0">
              {Object.entries(VIEW_CONFIG).map(([viewKey, config]) => {
                const Component = config.component;
                return (
                  <TabsContent
                    key={viewKey}
                    value={viewKey}
                    className="h-full m-0 p-0 overflow-hidden data-[state=active]:flex data-[state=active]:flex-col"
                  >
                    <div className="flex-1 overflow-auto">
                      <Component />
                    </div>
                  </TabsContent>
                );
              })}
            </div>
          </Tabs>
        </div>
      </CustomDrawerContent>
    </Drawer>
  );
}
