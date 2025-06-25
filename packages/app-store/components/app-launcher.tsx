"use client";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
// Sheet component removed - using custom sidebar instead
import { Loader2, LayoutGrid, AppWindow } from "lucide-react";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useInstalledApps } from "@karrio/hooks";
import { AppSheet } from "@karrio/app-store";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getAppManifest } from "../utils";
import { getAppStore } from "../index";

interface InstalledPhysicalApp {
  id: string;
  manifest: any;
  installation: any;
}

export const AppLauncher = (): JSX.Element => {
  const { toast } = useToast();
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [installedApps, setInstalledApps] = useState<InstalledPhysicalApp[]>([]);
  const [loadingApps, setLoadingApps] = useState(true);
  const [launchedApp, setLaunchedApp] = useState<any>(null);
  const [showAppSheet, setShowAppSheet] = useState(false);

  // Get installed apps data using the new hook
  const { query: installedAppsQuery } = useInstalledApps();

  // Load installed physical apps
  useEffect(() => {
    async function loadInstalledPhysicalApps() {
      try {
        // Get app installations from the new query structure
        const appInstallations = installedAppsQuery.data?.app_installations?.edges?.map(edge => edge.node) || [];
        const appStore = getAppStore();
        const appIds = Object.keys(appStore.apps);

        const apps: InstalledPhysicalApp[] = [];

        for (const installation of appInstallations) {
          try {
            // Check if this app is registered in our app store
            if (appIds.includes(installation.app_id)) {
              const manifest = await getAppManifest(installation.app_id, appStore.apps[installation.app_id]);
              if (manifest) {
                apps.push({
                  id: installation.app_id,
                  manifest,
                  installation,
                });
              }
            }
          } catch (error) {
            console.error(`Failed to load manifest for app ${installation.app_id}:`, error);
          }
        }

        setInstalledApps(apps);
      } catch (error) {
        console.error('Failed to load installed physical apps:', error);
      } finally {
        setLoadingApps(false);
      }
    }

    if (open) {
      loadInstalledPhysicalApps();
    }
  }, [open, installedAppsQuery.data]);

  const handleLaunchApp = (app: InstalledPhysicalApp) => {
    if (!app.manifest.ui?.viewports?.includes('dashboard')) {
      toast({
        title: "App not available",
        description: "This app doesn't support dashboard view",
        variant: "destructive",
      });
      return;
    }

    // Launch in embedded sheet
    setLaunchedApp(app);
    setShowAppSheet(true);
    setOpen(false); // Close the dropdown
  };

  // Add CSS for proper app sidebar behavior
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      /* App sidebar styles */
      .app-sidebar {
        position: fixed;
        top: 0;
        right: 0;
        height: 100vh;
        width: 100vw;
        background: white;
        border-left: 1px solid hsl(var(--border));
        z-index: 50;
        transform: translateX(100%);
        transition: transform 0.3s ease-out;
      }

      .app-sidebar.open {
        transform: translateX(0);
      }

      /* Desktop: sidebar behavior */
      @media (min-width: 768px) {
        .app-sidebar {
          width: 400px;
        }

        .app-sidebar.open {
          transform: translateX(0);
        }

        /* Push main content on desktop */
        body[data-app-sidebar-open="true"] .main-layout {
          margin-right: 400px;
          transition: margin-right 0.3s ease-out;
        }

        /* Responsive grid adjustments for desktop */
        body[data-app-sidebar-open="true"] .lg\\:grid-cols-4 {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        body[data-app-sidebar-open="true"] .lg\\:grid-cols-3 {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        body[data-app-sidebar-open="true"] .grid-cols-4 {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        body[data-app-sidebar-open="true"] .grid-cols-3 {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }
      }

      /* Mobile: full screen overlay */
      @media (max-width: 767px) {
        .app-sidebar {
          width: 100vw;
        }

        /* No content pushing on mobile */
        body[data-app-sidebar-open="true"] .main-layout {
          margin-right: 0;
        }
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
  }, []);

  // Handle body class for sidebar
  useEffect(() => {
    if (showAppSheet) {
      document.body.setAttribute('data-app-sidebar-open', 'true');
    } else {
      document.body.removeAttribute('data-app-sidebar-open');
    }

    return () => {
      document.body.removeAttribute('data-app-sidebar-open');
    };
  }, [showAppSheet]);

  return (
    <>
      <DropdownMenu open={open} onOpenChange={setOpen}>
        <DropdownMenuTrigger asChild>
          <div className="nav-item is-flex m-0">
            <button className="button is-default mr-2" style={{ borderRadius: "50%" }}>
              <span className="icon">
                <AppWindow className="w-4 h-4" />
              </span>
            </button>
          </div>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          className="w-80 p-4"
          align="end"
          side="bottom"
          sideOffset={8}
        >
          <div className="mb-3">
            <h3 className="text-sm font-semibold text-slate-900">Installed apps</h3>
            <p className="text-xs text-slate-500">Launch your installed applications</p>
          </div>

          {loadingApps || installedAppsQuery.isLoading ? (
            <div className="flex justify-center items-center py-8">
              <Loader2 className="w-6 h-6 animate-spin" />
            </div>
          ) : installedApps.length > 0 ? (
            <div className="grid grid-cols-3 gap-3">
              {installedApps.map((app) => (
                <div
                  key={app.id}
                  className="flex flex-col items-center p-3 rounded-lg hover:bg-slate-50 cursor-pointer transition-colors"
                  onClick={() => handleLaunchApp(app)}
                >
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-sm font-semibold mb-2">
                    {app.manifest.name.charAt(0)}
                  </div>
                  <span className="text-xs text-center text-slate-700 font-medium leading-tight">
                    {app.manifest.name}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-6 text-slate-500">
              <LayoutGrid className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p className="text-xs">No apps installed</p>
              <p className="text-xs opacity-75">Visit the App Store to install apps</p>
            </div>
          )}

          <div className="mt-4 pt-3 border-t border-slate-100">
            <button
              className="text-xs text-blue-600 hover:text-blue-700 font-medium"
              onClick={() => {
                router.push('/app-store');
                setOpen(false);
              }}
            >
              Explore the App Marketplace →
            </button>
          </div>
        </DropdownMenuContent>
      </DropdownMenu>

      {/* App Launch Sidebar */}
      {showAppSheet && launchedApp && (
        <div className={`app-sidebar ${showAppSheet ? 'open' : ''}`}>
          <AppSheet
            app={{
              id: launchedApp.id,
              manifest: launchedApp.manifest,
              isInstalled: true,
              installation: launchedApp.installation,
            }}
            onClose={() => {
              setShowAppSheet(false);
              setLaunchedApp(null);
            }}
          />
        </div>
      )}
    </>
  );
};
