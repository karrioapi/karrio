"use client";

import React, { useState } from "react";
import { useDeveloperTools, DeveloperView } from "@karrio/developers/context/developer-tools-context";
import { Drawer, DrawerPortal, DrawerHeader, DrawerTitle, DrawerDescription } from "@karrio/ui/components/ui/drawer";
import { Drawer as DrawerPrimitive } from "vaul";
import { X, Activity, Key, Webhook, Calendar, FileText, Settings, Terminal, Menu, Code2, Database, Network, Server, Cpu } from "lucide-react";
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
import { TracingRecordsView } from "@karrio/developers/components/views/tracing-records-view";
import { PlaygroundView } from "@karrio/developers/components/views/playground-view";
import { GraphiQLView } from "@karrio/developers/components/views/graphiql-view";
import { WorkersView } from "@karrio/developers/components/views/workers-view";
import { SystemHealthView } from "@karrio/developers/components/views/system-health-view";

// Custom DrawerContent with responsive positioning
const CustomDrawerContent = React.forwardRef<
  React.ElementRef<typeof DrawerPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DrawerPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DrawerPortal>
    <DrawerPrimitive.Content
      ref={ref}
      className={cn(
        "fixed z-50 grid grid-rows-[1fr,auto] lg:grid-rows-[auto,1fr] border-t bg-background w-full left-0 right-0 top-0 lg:top-[9vh] bottom-0 rounded-t-[10px]",
        // Force dark mode for this drawer only (scoped) and crisp rendering
        "dark antialiased [text-rendering:optimizeLegibility] [backface-visibility:hidden]",
        className
      )}
      style={{ ...(props as any)?.style }}
      onPointerDownCapture={(e) => {
        if (typeof window !== 'undefined' && window.innerWidth < 1024) {
          const strip = (e.currentTarget as HTMLElement).querySelector('#devtools-drag-strip');
          if (strip && (strip === e.target || strip.contains(e.target as Node))) {
            return; // allow drag start from handle
          }
          e.stopPropagation(); // prevent drag start elsewhere so scrolling works
        }
      }}
      onTouchStartCapture={(e) => {
        if (typeof window !== 'undefined' && window.innerWidth < 1024) {
          const strip = (e.currentTarget as HTMLElement).querySelector('#devtools-drag-strip');
          if (strip && (strip === e.target || strip.contains(e.target as Node))) {
            return;
          }
          e.stopPropagation();
        }
      }}
      {...props}
    >
      {/* drag strip handled in parent component */}
      {children}
    </DrawerPrimitive.Content>
  </DrawerPortal>
));

const VIEW_CONFIG: Record<string, { label: string; icon: any; component: React.ComponentType; adminOnly?: boolean }> = {
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
  "tracing-records": {
    label: "Tracing",
    icon: Network,
    component: TracingRecordsView,
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
  "system-health": {
    label: "Health",
    icon: Server,
    component: SystemHealthView,
    adminOnly: true,
  },
  workers: {
    label: "Workers",
    icon: Cpu,
    component: WorkersView,
    adminOnly: true,
  },
};

export function DeveloperToolsDrawer() {
  const { isOpen, currentView, isAdminMode, closeDeveloperTools, setCurrentView } = useDeveloperTools();

  // Filter views based on admin mode
  const visibleViews = React.useMemo(() => {
    return Object.entries(VIEW_CONFIG).filter(
      ([_, config]) => !config.adminOnly || isAdminMode
    );
  }, [isAdminMode]);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const dragInfoRef = React.useRef<{ startY: number; startTime: number; dragging: boolean } | null>(null);


  // Emit state changes for floating button
  React.useEffect(() => {
    const event = new CustomEvent('developer-tools-state-change', {
      detail: { isOpen }
    });
    window.dispatchEvent(event);
  }, [isOpen]);

  // Create a dedicated portal container for DevTools overlays with scoped dark theme
  React.useEffect(() => {
    if (!isOpen || typeof document === 'undefined') return;
    const existing = document.getElementById('devtools-portal');
    if (existing) return;
    const portal = document.createElement('div');
    portal.id = 'devtools-portal';
    portal.className = 'devtools-theme dark';
    portal.style.position = 'fixed';
    portal.style.inset = '0';
    portal.style.zIndex = '9999';
    document.body.appendChild(portal);
    return () => {
      try { document.body.removeChild(portal); } catch (_) { /* ignore */ }
    };
  }, [isOpen]);


  // Revert any transform clearing; use only position-based animations when we re-implement

  const handleTabChange = (value: string) => {
    setCurrentView(value as DeveloperView);
    // Close mobile sidebar when selecting a tab
    setIsMobileSidebarOpen(false);
  };


  // Use CSS sizing (100dvh - offset) to size the main area

  return (
    <Drawer open={isOpen} onOpenChange={(open) => {
      if (!open) {
        closeDeveloperTools();
        setIsMobileSidebarOpen(false);
      }
    }}>
      <CustomDrawerContent className={cn("dark devtools-theme h-full max-h-full lg:overflow-hidden")}>
        <style jsx global>{`
          .devtools-theme.dark {
            --background: 248 44% 11%;
            --card: 248 40% 8%;
            --foreground: 0 0% 100%;
            --muted: 222 47% 11%;
            --muted-foreground: 217 12% 65%;
            --border: 0 0% 15%;
            --input: 248 44% 11%;
            --ring: 258 90% 67%;
            --primary: 258 90% 67%;
            --primary-foreground: 0 0% 100%;
            --popover: 248 40% 8%;
            --popover-foreground: 220 14% 94%;
          }
        `}</style>
        {/* Top drag strip - mobile only; independent from content scrolling */}
        <div
          id="devtools-drag-strip"
          className="absolute top-0 left-0 right-0 h-7 lg:hidden z-[70]"
          onPointerDown={(e) => {
            if (typeof window !== 'undefined' && window.innerWidth < 1024) {
              try { (e.currentTarget as HTMLElement).setPointerCapture((e as any).pointerId); } catch (_) { }
              dragInfoRef.current = { startY: e.pageY, startTime: Date.now(), dragging: true };
              e.stopPropagation();
            }
          }}
          onPointerMove={(e) => {
            const info = dragInfoRef.current;
            if (!info || !info.dragging) return;
            // Optional: we could show feedback; we simply track movement
            e.stopPropagation();
          }}
          onPointerUp={(e) => {
            const info = dragInfoRef.current;
            if (!info) return;
            const deltaY = e.pageY - info.startY;
            const dt = Math.max(1, Date.now() - info.startTime);
            const velocity = deltaY / dt; // px per ms
            dragInfoRef.current = null;
            e.stopPropagation();
            // Thresholds: distance 48px OR fast swipe (>0.6 px/ms ~ 600px/s)
            if (deltaY > 48 || velocity > 0.6) {
              closeDeveloperTools();
            }
          }}
          onTouchStart={(e) => {
            if (typeof window !== 'undefined' && window.innerWidth < 1024) {
              const t = e.touches[0];
              dragInfoRef.current = { startY: t.pageY, startTime: Date.now(), dragging: true };
              e.stopPropagation();
            }
          }}
          onTouchMove={(e) => {
            const info = dragInfoRef.current;
            if (!info || !info.dragging) return;
            e.stopPropagation();
          }}
          onTouchEnd={(e) => {
            const info = dragInfoRef.current;
            if (!info) return;
            const t = (e.changedTouches && e.changedTouches[0]) || ({} as any);
            const deltaY = (t.pageY ?? info.startY) - info.startY;
            const dt = Math.max(1, Date.now() - info.startTime);
            const velocity = deltaY / dt;
            dragInfoRef.current = null;
            e.stopPropagation();
            if (deltaY > 48 || velocity > 0.6) {
              closeDeveloperTools();
            }
          }}
          style={{ WebkitTapHighlightColor: 'transparent' }}
        />
        {/* Header */}
        <DrawerHeader
          className="relative z-50 flex-shrink-0 border-b border-border bg-card px-2 sm:px-4 py-2 lg:py-2 text-foreground row-start-2 lg:row-start-1"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 sm:gap-3">
              {/* Mobile menu button */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
                className="h-10 w-10 p-0 lg:hidden"
                aria-expanded={isMobileSidebarOpen}
                aria-controls="devtools-mobile-nav"
              >
                <Menu className="h-6 w-6" />
              </Button>
              <Terminal className="h-6 w-6 sm:h-7 sm:w-7 text-foreground" />
              <DrawerTitle className="text-base sm:text-lg font-semibold text-foreground">Developer Tools</DrawerTitle>
              <DrawerDescription className="sr-only">Developer tools drawer</DrawerDescription>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={closeDeveloperTools}
              className="h-10 w-10 p-0 text-muted-foreground hover:text-foreground hover:bg-primary/10"
            >
              <X className="h-6 w-6" />
            </Button>
          </div>
        </DrawerHeader>

        {/* Main Content - unified container (desktop and mobile) */}
        <div
          className="row-start-1 lg:row-start-2 min-h-0 h-full box-border flex relative overflow-hidden lg:overflow-hidden"
        >
          <Tabs
            value={currentView}
            onValueChange={handleTabChange}
            orientation="vertical"
            className="flex h-full w-full min-h-0 lg:flex-1"
          >
            {/* Mobile Sidebar Overlay */}
            {isMobileSidebarOpen && (
              <div
                className="absolute inset-0 bg-black/50 backdrop-blur-[1px] z-40 lg:hidden"
                onClick={() => setIsMobileSidebarOpen(false)}
              />
            )}

            {/* Sidebar Navigation */}
            <div id="devtools-mobile-nav" className={cn(
              "flex-shrink-0 border-r border-border bg-card transition-transform duration-200 ease-in-out z-50 lg:z-10",
              // Mobile: slide in from left, hidden by default
              "absolute lg:relative inset-y-0 left-0",
              "w-52 sm:w-56 lg:w-52",
              isMobileSidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
            )}>
              <TabsList className="flex flex-col h-full w-full justify-start !bg-transparent !p-2 !rounded-none !h-auto space-y-1">
                {visibleViews.map(([viewKey, config], index) => {
                  const Icon = config.icon;
                  const isFirstAdmin = config.adminOnly && (index === 0 || !visibleViews[index - 1]?.[1]?.adminOnly);
                  return (
                    <React.Fragment key={viewKey}>
                      {isFirstAdmin && (
                        <div className="pt-2 pb-1 px-3">
                          <div className="border-t border-border" />
                        </div>
                      )}
                      <TabsTrigger
                        value={viewKey}
                        className={cn(
                          "w-full justify-start gap-3 px-3 py-3 text-sm font-medium transition-all rounded-md",
                          "text-foreground hover:bg-primary/10",
                          "data-[state=active]:bg-primary/20 data-[state=active]:text-foreground data-[state=active]:shadow-sm border border-transparent data-[state=active]:border-border"
                        )}
                      >
                        <Icon className="h-5 w-5 flex-shrink-0 text-primary" />
                        <span className="truncate">{config.label}</span>
                      </TabsTrigger>
                    </React.Fragment>
                  );
                })}
              </TabsList>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 lg:ml-0 bg-background min-h-0 pl-0 lg:pl-0 lg:overflow-hidden">
              {visibleViews.map(([viewKey, config]) => {
                const Component = config.component;
                return (
                  <TabsContent
                    key={viewKey}
                    value={viewKey}
                    className="h-full min-h-0 m-0 p-0 data-[state=active]:flex data-[state=active]:flex-col lg:flex-1 lg:min-h-0 lg:overflow-hidden"
                  >
                    <div className="relative h-full min-h-0 lg:flex lg:flex-col lg:flex-1 lg:min-h-0">
                      <div
                        className="absolute inset-0 min-h-0 overflow-auto lg:static lg:flex-1 lg:min-h-0 lg:overflow-auto lg:pb-20"
                        style={{ touchAction: 'pan-y', WebkitOverflowScrolling: 'touch', overscrollBehavior: 'contain' }}
                        data-vaul-no-drag
                      >
                        <Component />
                      </div>
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
