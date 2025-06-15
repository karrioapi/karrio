"use client";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Sheet, SheetContent } from "@karrio/ui/components/ui/sheet";
import { getAppStore, getAppManifest } from "@karrio/app-store";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useAppStore, useAppMutations } from "@karrio/hooks";
import { AppDetailsForm, AppSheet } from "@karrio/app-store";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { Button } from "@karrio/ui/components/ui/button";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { bundleContexts } from "@karrio/hooks/utils";
import { Spinner } from "@karrio/ui/core/components";
import { useState, useEffect } from "react";
import { Plus, Check } from "lucide-react";

const ContextProviders = bundleContexts([ModalProvider]);

interface PhysicalApp {
  id: string;
  manifest: any;
  isInstalled: boolean;
  installation?: any;
}

export default function AppStorePage(pageProps: any) {
  const Component = (): JSX.Element => {
    const { setLoading } = useLoader();
    const { toast } = useToast();
    const [physicalApps, setPhysicalApps] = useState<PhysicalApp[]>([]);
    const [loadingApps, setLoadingApps] = useState(true);
    const [selectedAppId, setSelectedAppId] = useState<string | null>(null);
    const [launchedApp, setLaunchedApp] = useState<PhysicalApp | null>(null);
    const [showAppSheet, setShowAppSheet] = useState(false);

    // Get installed apps data
    const { installed } = useAppStore();
    const { installApp, uninstallApp } = useAppMutations();

    // Add CSS to hide sheet overlay like ShippingRules
    useEffect(() => {
      const style = document.createElement('style');
      style.textContent = `
        [data-radix-dialog-overlay] {
          display: none !important;
        }
        .bg-black\\/80 {
          display: none !important;
        }
      `;
      document.head.appendChild(style);

      return () => {
        document.head.removeChild(style);
      };
    }, []);

    // Load physical apps from app store
    useEffect(() => {
      async function loadPhysicalApps() {
        try {
          const appStore = getAppStore();
          const appIds = Object.keys(appStore.apps);
          const installedApps = installed.query.data?.app_installations?.edges?.map(edge => edge.node) || [];

          const apps: PhysicalApp[] = [];

          for (const appId of appIds) {
            try {
              const manifest = await getAppManifest(appId, appStore.apps[appId]);
              if (manifest) {
                const installedApp = installedApps.find(app => app.app_id === appId);
                apps.push({
                  id: appId,
                  manifest,
                  isInstalled: !!installedApp,
                  installation: installedApp,
                });
              }
            } catch (error) {
              console.error(`Failed to load manifest for app ${appId}:`, error);
            }
          }

          setPhysicalApps(apps);
        } catch (error) {
          console.error('Failed to load physical apps:', error);
          toast({
            title: "Error loading apps",
            description: "Failed to load app store data",
            variant: "destructive",
          });
        } finally {
          setLoadingApps(false);
        }
      }

      loadPhysicalApps();
    }, [installed.query.data]); // Only depend on the actual data, not the derived array

    const handleInstallApp = async (appId: string) => {
      const app = physicalApps.find(a => a.id === appId);
      if (!confirm(`Install ${app?.manifest.name || 'this app'}? This will add new functionality to your workspace.`)) {
        return;
      }

      try {
        setLoading(true);
        const result = await installApp.mutateAsync({
          app_id: appId,
          access_scopes: [],
          metadata: {},
        });

        if (result.install_app?.errors?.length) {
          const error = result.install_app.errors[0];
          toast({
            title: "Error installing app",
            description: error.messages?.join(", "),
            variant: "destructive",
          });
        } else {
          toast({
            title: "App installed successfully",
            description: "The app has been installed to your workspace",
          });
          // Update local state
          setPhysicalApps(prev => prev.map(app =>
            app.id === appId
              ? { ...app, isInstalled: true, installation: result.install_app?.installation }
              : app
          ));
        }
      } catch (error: any) {
        toast({
          title: "Error installing app",
          description: error.message || "An unexpected error occurred",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    const handleLaunchApp = (app: PhysicalApp) => {
      if (!app.manifest.ui?.viewports?.includes('dashboard')) {
        toast({
          title: "App not available",
          description: "This app doesn't support dashboard view",
          variant: "destructive",
        });
        return;
      }

      // Check if app is embedded
      if (app.manifest.type === 'builtin' || app.isInstalled) {
        // Launch in embedded sheet
        setLaunchedApp(app);
        setShowAppSheet(true);
      } else {
        toast({
          title: "App not installed",
          description: "Please install the app first to launch it",
          variant: "destructive",
        });
      }
    };

    const handleFormSave = () => {
      // Simply refetch the installed apps query, which will trigger the useEffect to reload
      installed.query.refetch();
    };

    const selectedApp = physicalApps.find(app => app.id === selectedAppId);

    return (
      <>
        {/* Header */}
        <header className="px-0 pb-0 pt-4 flex justify-between items-center">
          <div>
            <h1 className="title is-4">App Store</h1>
            <p className="text-sm text-muted-foreground">
              Discover and install apps to extend your Karrio experience
            </p>
          </div>
        </header>

        <div className="py-4">
          {/* App Store Info Banner */}
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Plus className="h-4 w-4 text-blue-600" />
              </div>
              <div className="space-y-2">
                <h3 className="text-sm font-semibold text-blue-900">Extend Your Karrio Experience</h3>
                <p className="text-sm text-blue-700">
                  Browse and install apps to add new functionality to your shipping workflow.
                  All apps are thoroughly tested and integrate seamlessly with your workspace.
                </p>
              </div>
            </div>
          </div>

          {!loadingApps && (
            <div className="tailwind-only">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {physicalApps.map((app) => (
                  <Card key={app.id} className="hover:shadow-md transition-shadow">
                    <CardHeader className="pb-4 pt-6 px-6">
                      <div className="flex items-start gap-4">
                        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-lg font-semibold flex-shrink-0">
                          {app.manifest.name?.charAt(0) || 'A'}
                        </div>
                        <div className="flex-1 min-w-0">
                          <CardTitle className="text-base font-semibold leading-tight mb-2">
                            {app.manifest.name}
                          </CardTitle>
                          <CardDescription className="text-sm text-muted-foreground">
                            {app.manifest.developer?.name || 'Unknown Developer'}
                          </CardDescription>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="pt-0 pb-6 px-6">
                      <p className="text-sm text-muted-foreground mb-6 line-clamp-3 leading-relaxed">
                        {app.manifest.description}
                      </p>
                      <div className="flex gap-3">
                        <Button
                          size="sm"
                          variant="outline"
                          className="flex-1 text-sm h-9"
                          onClick={() => setSelectedAppId(app.id)}
                        >
                          Details
                        </Button>
                        <Button
                          size="sm"
                          className="flex-1 text-sm h-9"
                          onClick={() => handleInstallApp(app.id)}
                          disabled={app.isInstalled}
                        >
                          {app.isInstalled ? (
                            <>
                              <Check className="w-4 h-4 mr-2" />
                              Installed
                            </>
                          ) : (
                            <>
                              <Plus className="w-4 h-4 mr-2" />
                              Install
                            </>
                          )}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
                {physicalApps.length === 0 && (
                  <div className="col-span-full text-center py-12 text-muted-foreground">
                    No apps available in the store
                  </div>
                )}
              </div>
            </div>
          )}

          {loadingApps && (
            <div className="flex justify-center py-8">
              <Spinner />
            </div>
          )}

          {/* App Launch Sheet */}
          <Sheet open={showAppSheet} onOpenChange={(open) => {
            if (!open) {
              setShowAppSheet(false);
              setLaunchedApp(null);
            }
          }}>
            <SheetContent className="w-full sm:w-[500px] sm:max-w-[500px] p-0 shadow-none">
              {launchedApp && (
                <AppSheet
                  app={launchedApp}
                  onClose={() => {
                    setShowAppSheet(false);
                    setLaunchedApp(null);
                  }}
                />
              )}
            </SheetContent>
          </Sheet>

          {/* App Details Sheet */}
          <Sheet open={!!selectedAppId} onOpenChange={(open) => {
            if (!open) {
              setSelectedAppId(null);
            }
          }}>
            <SheetContent className="w-full sm:w-[500px] sm:max-w-[500px] p-0 shadow-none">
              {selectedApp && (
                <AppDetailsForm
                  app={selectedApp}
                  onClose={() => setSelectedAppId(null)}
                  onSave={handleFormSave}
                  onLaunch={handleLaunchApp}
                />
              )}
            </SheetContent>
          </Sheet>
        </div>
      </>
    );
  };

  return (
    <>
      <ContextProviders>
        <Component />
      </ContextProviders>
    </>
  );
}
