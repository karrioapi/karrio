"use client";

import React, { useState } from "react";
import { useDeveloperTools, DeveloperView } from "@karrio/developers/context/developer-tools-context";
import { Drawer, DrawerPortal, DrawerHeader, DrawerTitle, DrawerDescription } from "@karrio/ui/components/ui/drawer";
import { Drawer as DrawerPrimitive } from "vaul";
import { X, Activity, Key, Webhook, Calendar, FileText, Settings, Terminal, Menu, Code2, Database } from "lucide-react";
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
import { PlaygroundView } from "@karrio/developers/components/views/playground-view";
import { GraphiQLView } from "@karrio/developers/components/views/graphiql-view";

// Custom DrawerContent with responsive positioning
const CustomDrawerContent = React.forwardRef<
  React.ElementRef<typeof DrawerPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DrawerPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DrawerPortal>
    <DrawerPrimitive.Content
      ref={ref}
      className={cn(
        "fixed z-50 flex flex-col border-t bg-[#0f0c24]",
        // Mobile: full screen with rounded top corners
        "inset-0 h-full w-full lg:inset-auto",
        // Desktop: positioned below navbar (navbar is h-14 = 56px)
        "lg:top-14 lg:left-0 lg:right-0 lg:bottom-0 lg:h-[calc(100vh-3.5rem)]",
        // Force dark mode for this drawer only (scoped)
        "dark",
        className
      )}
      {...props}
    >
      <div className="mx-auto mt-2 h-1 w-[100px] rounded-full bg-purple-900/40 lg:hidden" />
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
  playground: {
    label: "Playground",
    icon: Code2,
    component: PlaygroundView,
  },
  graphiql: {
    label: "GraphiQL",
    icon: Database,
    component: GraphiQLView,
  },
};

export function DeveloperToolsDrawer() {
  const { isOpen, currentView, closeDeveloperTools, setCurrentView } = useDeveloperTools();
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  // Emit state changes for floating button
  React.useEffect(() => {
    const event = new CustomEvent('developer-tools-state-change', {
      detail: { isOpen }
    });
    window.dispatchEvent(event);
  }, [isOpen]);

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
        <DrawerHeader className="relative z-50 flex-shrink-0 border-b border-neutral-800 !bg-[#0b0a1a] px-2 sm:px-4 py-2 text-white">
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
              <Terminal className="h-6 w-6 sm:h-7 sm:w-7 text-white" />
              <DrawerTitle className="text-base sm:text-lg font-semibold text-white">Developer Tools</DrawerTitle>
              <DrawerDescription className="sr-only">Developer tools drawer</DrawerDescription>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={closeDeveloperTools}
              className="h-10 w-10 p-0 text-neutral-300 hover:text-white hover:bg-neutral-800/40"
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
                className="absolute inset-0 bg-blue-900/30 z-5 lg:hidden"
                onClick={() => setIsMobileSidebarOpen(false)}
              />
            )}

            {/* Sidebar Navigation */}
            <div className={cn(
              "flex-shrink-0 border-r border-neutral-800 bg-[#0b0a1a] transition-transform duration-200 ease-in-out z-10",
              // Mobile: slide in from left, hidden by default
              "absolute lg:relative inset-y-0 left-0",
              "w-52 sm:w-56 lg:w-52",
              isMobileSidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
            )}>
              <TabsList className="flex flex-col h-full w-full justify-start !bg-transparent !p-2 !rounded-none !h-auto space-y-1">
                {Object.entries(VIEW_CONFIG).map(([viewKey, config]) => {
                  const Icon = config.icon;
                  return (
                    <TabsTrigger
                      key={viewKey}
                      value={viewKey}
                      className={cn(
                        "w-full justify-start gap-3 px-3 py-3 text-sm font-medium transition-all rounded-md",
                        "text-white hover:bg-purple-900/10",
                        "data-[state=active]:bg-purple-900/20 data-[state=active]:text-white data-[state=active]:shadow-sm border border-transparent data-[state=active]:border-neutral-700"
                      )}
                    >
                      <Icon className="h-5 w-5 flex-shrink-0 text-primary" />
                      <span className="truncate">{config.label}</span>
                    </TabsTrigger>
                  );
                })}
              </TabsList>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 overflow-hidden lg:ml-0 bg-[#0f0c24]">
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
