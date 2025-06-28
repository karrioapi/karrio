"use client";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@karrio/ui/components/ui/dialog";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@karrio/ui/components/ui/tabs";
import { Plus, Shield, AlertTriangle, Info, Settings, Trash2 } from "lucide-react";
import { AppDetailsForm, AppSheet, AppConfigureSheet } from "@karrio/app-store";
import { Alert, AlertDescription, AlertTitle } from "@karrio/ui/components/ui/alert";
import { Sheet, SheetContent } from "@karrio/ui/components/ui/sheet";
import { getAppStore, getAppManifest } from "@karrio/app-store";
import { useLoader } from "@karrio/ui/core/components/loader";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { useAppStore, useAppMutations } from "@karrio/hooks";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { bundleContexts } from "@karrio/hooks/utils";
import { Spinner } from "@karrio/ui/core/components";
import { useState, useEffect } from "react";

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
    const [appToInstall, setAppToInstall] = useState<PhysicalApp | null>(null);
    const [showInstallConfirmation, setShowInstallConfirmation] = useState(false);
    const [appToUninstall, setAppToUninstall] = useState<PhysicalApp | null>(null);
    const [showUninstallConfirmation, setShowUninstallConfirmation] = useState(false);
    const [appToConfigure, setAppToConfigure] = useState<PhysicalApp | null>(null);
    const [showConfigureSheet, setShowConfigureSheet] = useState(false);
    const [activeTab, setActiveTab] = useState("all");

    // Get installed apps data
    const { installed } = useAppStore();
    const { installApp, uninstallApp } = useAppMutations();

    // Add CSS for app sidebar and floating sheets
    useEffect(() => {
      const style = document.createElement('style');
      style.textContent = `
        /* App sidebar styles - only for launched apps */
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

        /* Hide sheet overlay for floating sheets */
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

    // Handle body class for sidebar - only for app launch, not config/details
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
    }, [installed.query.data]);

    const handleInstallApp = (appId: string) => {
      const app = physicalApps.find(a => a.id === appId);
      if (!app) return;

      // Check if already installed
      if (app.isInstalled) {
        toast({
          title: "App already installed",
          description: `${app.manifest.name} is already installed in your workspace`,
          variant: "default",
        });
        return;
      }

      setAppToInstall(app);
      setShowInstallConfirmation(true);
    };

    const confirmInstallApp = async () => {
      if (!appToInstall) return;

      try {
        setLoading(true);
        setShowInstallConfirmation(false);

        // Get access scopes from app manifest
        const accessScopes = appToInstall.manifest.oauth?.scopes || ['read', 'write'];

        const result = await installApp.mutateAsync({
          app_id: appToInstall.id,
          access_scopes: accessScopes,
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
            description: `${appToInstall.manifest.name} has been installed to your workspace`,
          });
          // Force refetch of installed apps to get updated data
          await installed.query.refetch();
        }
      } catch (error: any) {
        toast({
          title: "Error installing app",
          description: error.message || "An unexpected error occurred",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
        setAppToInstall(null);
      }
    };

    const cancelInstallApp = () => {
      setShowInstallConfirmation(false);
      setAppToInstall(null);
    };

    const handleUninstallApp = (app: PhysicalApp) => {
      if (!app.installation?.id) return;

      setAppToUninstall(app);
      setShowUninstallConfirmation(true);
    };

    const confirmUninstallApp = async () => {
      if (!appToUninstall?.installation?.id) return;

      try {
        setLoading(true);
        setShowUninstallConfirmation(false);

        const result = await uninstallApp.mutateAsync({
          app_id: appToUninstall.id,
        });

        if (result.uninstall_app?.errors?.length) {
          const error = result.uninstall_app.errors[0];
          toast({
            title: "Error uninstalling app",
            description: error.messages?.join(", "),
            variant: "destructive",
          });
        } else {
          toast({
            title: "App uninstalled successfully",
            description: `${appToUninstall.manifest.name} has been uninstalled from your workspace`,
          });
          // Force refetch of installed apps to get updated data
          await installed.query.refetch();
        }
      } catch (error: any) {
        toast({
          title: "Error uninstalling app",
          description: error.message || "An unexpected error occurred",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
        setAppToUninstall(null);
      }
    };

    const cancelUninstallApp = () => {
      setShowUninstallConfirmation(false);
      setAppToUninstall(null);
    };

    const handleConfigureApp = (app: PhysicalApp) => {
      setAppToConfigure(app);
      setShowConfigureSheet(true);
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
    const installedApps = physicalApps.filter(app => app.isInstalled);

    const renderAppCard = (app: PhysicalApp, cardType: 'all' | 'installed') => (
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
            {cardType === 'all' && (
              <>
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
                  disabled={app.isInstalled}
                  onClick={() => handleInstallApp(app.id)}
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Install
                </Button>
              </>
            )}
            {cardType === 'installed' && (
              <>
                <Button
                  size="sm"
                  variant="outline"
                  className="flex-1 text-sm h-9"
                  onClick={() => handleConfigureApp(app)}
                >
                  <Settings className="w-4 h-4 mr-2" />
                  Configure
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  className="flex-1 text-sm h-9"
                  onClick={() => handleUninstallApp(app)}
                >
                  <Trash2 className="w-4 h-4 mr-2" />
                  Uninstall
                </Button>
              </>
            )}
          </div>
        </CardContent>
      </Card>
    );

    return (
      <>
        {/* Header */}
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <div className="title is-4">
            <span>App store</span>
            <span className="tag is-warning is-size-7 has-text-weight-bold mx-2">
              PREVIEW
            </span>
            <p className="text-sm text-muted-foreground pt-4">
              Discover and install apps to extend your Karrio experience
            </p>
          </div>
        </header>

        <div className="py-4">
          {/* Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-6">
              <TabsTrigger value="all">All Apps</TabsTrigger>
              <TabsTrigger value="installed">Installed ({installedApps.length})</TabsTrigger>
            </TabsList>

            <TabsContent value="all" className="mt-0">
              {!loadingApps && (
                <div className="tailwind-only">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {physicalApps.map((app) => renderAppCard(app, 'all'))}
                    {physicalApps.length === 0 && (
                      <div className="col-span-full text-center py-12 text-muted-foreground">
                        No apps available in the store
                      </div>
                    )}
                  </div>
                </div>
              )}
            </TabsContent>

            <TabsContent value="installed" className="mt-0">
              {!loadingApps && (
                <div className="tailwind-only">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {installedApps.map((app) => renderAppCard(app, 'installed'))}
                    {installedApps.length === 0 && (
                      <div className="col-span-full text-center py-12 text-muted-foreground">
                        <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                          <Plus className="w-8 h-8 text-slate-400" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-900 mb-2">No apps installed</h3>
                        <p className="text-sm text-slate-500 mb-4">
                          Install apps from the "All Apps" tab to get started
                        </p>
                        <Button
                          variant="outline"
                          onClick={() => setActiveTab("all")}
                        >
                          Browse Apps
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </TabsContent>
          </Tabs>

          {loadingApps && <div className="flex justify-center py-8"><Spinner /></div>}

          {/* App Launch Sidebar */}
          {showAppSheet && launchedApp && (
            <div className={`app-sidebar ${showAppSheet ? 'open' : ''}`}>
              <AppSheet
                app={launchedApp}
                onClose={() => {
                  setShowAppSheet(false);
                  setLaunchedApp(null);
                }}
              />
            </div>
          )}

          {/* App Details Sheet - Floating */}
          <Sheet open={!!selectedAppId} onOpenChange={(open) => { if (!open) setSelectedAppId(null) }}>
            <SheetContent className="w-[400px] max-w-[400px] p-0 shadow-lg">
              {selectedApp && (
                <AppDetailsForm
                  app={selectedApp}
                  onClose={() => setSelectedAppId(null)}
                />
              )}
            </SheetContent>
          </Sheet>

          {/* App Configure Sheet - Floating */}
          <Sheet open={showConfigureSheet} onOpenChange={setShowConfigureSheet}>
            <SheetContent className="w-[400px] max-w-[400px] p-0 shadow-lg">
              {appToConfigure && (
                <AppConfigureSheet
                  app={appToConfigure}
                  onOpenChange={(open) => {
                    setShowConfigureSheet(open);
                    if (!open) {
                      // Refresh the installed apps data when configuration is closed
                      installed.query.refetch();
                      // If the app is currently launched, refresh it too
                      if (launchedApp && launchedApp.id === appToConfigure.id) {
                        // Force re-render by clearing and setting the launched app
                        setLaunchedApp(null);
                        setTimeout(() => {
                          setLaunchedApp(appToConfigure);
                        }, 100);
                      }
                    }
                  }}
                />
              )}
            </SheetContent>
          </Sheet>

          {/* Install Confirmation Modal */}
          <Dialog open={showInstallConfirmation} onOpenChange={setShowInstallConfirmation}>
            <DialogContent className="sm:max-w-[500px] p-4 pb-8" aria-describedby="install-dialog-description">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5 text-blue-600" />
                  Install {appToInstall?.manifest.name}
                </DialogTitle>
                <DialogDescription id="install-dialog-description">
                  Review the permissions this app requires to function properly in your workspace.
                </DialogDescription>
              </DialogHeader>

              {appToInstall && (
                <div className="space-y-4">
                  {/* App Info */}
                  <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-sm font-semibold flex-shrink-0">
                      {appToInstall.manifest.name?.charAt(0) || 'A'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-sm">{appToInstall.manifest.name}</h4>
                      <p className="text-xs text-muted-foreground">
                        by {appToInstall.manifest.developer?.name || 'Unknown Developer'}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                        {appToInstall.manifest.description}
                      </p>
                    </div>
                  </div>

                  {/* Permissions Section */}
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="h-4 w-4 text-amber-500" />
                      <h4 className="font-medium text-sm">Required Permissions</h4>
                    </div>

                    {/* Access Scopes */}
                    {appToInstall.manifest.oauth?.scopes && appToInstall.manifest.oauth.scopes.length > 0 && (
                      <div className="space-y-2">
                        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                          API Access Scopes
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {appToInstall.manifest.oauth.scopes.map((scope: string) => (
                            <Badge key={scope} variant="secondary" className="text-xs">
                              {scope}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Features/Resources */}
                    {appToInstall.manifest.features && appToInstall.manifest.features.length > 0 && (
                      <div className="space-y-2">
                        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                          Features Access
                        </p>
                        <div className="space-y-1">
                          {appToInstall.manifest.features.map((feature: string) => (
                            <div key={feature} className="flex items-center gap-2 text-sm">
                              <div className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                              <span className="capitalize">{feature.replace('_', ' ')}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Webhooks */}
                    {appToInstall.manifest.webhooks?.events && appToInstall.manifest.webhooks.events.length > 0 && (
                      <div className="space-y-2">
                        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                          Event Subscriptions
                        </p>
                        <div className="space-y-1">
                          {appToInstall.manifest.webhooks.events.map((event: string) => (
                            <div key={event} className="flex items-center gap-2 text-sm">
                              <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
                              <span>{event.replace('.', ' ').replace('_', ' ')}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Security Notice */}
                  <Alert>
                    <Info className="h-4 w-4" />
                    <AlertDescription className="text-xs">
                      This app will have access to the specified data and features in your workspace.
                      You can review and modify these permissions in your app settings after installation.
                    </AlertDescription>
                  </Alert>
                </div>
              )}

              <DialogFooter className="gap-2">
                <Button variant="outline" onClick={cancelInstallApp}>
                  Cancel
                </Button>
                <Button onClick={confirmInstallApp} disabled={!appToInstall}>
                  <Shield className="w-4 h-4 mr-2" />
                  Install App
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>

          {/* Uninstall Confirmation Modal */}
          <Dialog open={showUninstallConfirmation} onOpenChange={setShowUninstallConfirmation}>
            <DialogContent className="sm:max-w-[500px] p-4 pb-8" aria-describedby="uninstall-dialog-description">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-red-600" />
                  Uninstall {appToUninstall?.manifest.name}
                </DialogTitle>
                <DialogDescription id="uninstall-dialog-description">
                  Are you sure you want to uninstall this app? This action cannot be undone.
                </DialogDescription>
              </DialogHeader>

              {appToUninstall && (
                <div className="space-y-4">
                  {/* App Info */}
                  <div className="flex items-start gap-3 p-3 bg-red-50 rounded-lg border border-red-200">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-sm font-semibold flex-shrink-0">
                      {appToUninstall.manifest.name?.charAt(0) || 'A'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-sm">{appToUninstall.manifest.name}</h4>
                      <p className="text-xs text-muted-foreground">
                        by {appToUninstall.manifest.developer?.name || 'Unknown Developer'}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                        {appToUninstall.manifest.description}
                      </p>
                    </div>
                  </div>

                  {/* Warning */}
                  <Alert variant="destructive">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertTitle>Warning</AlertTitle>
                    <AlertDescription className="text-sm">
                      Uninstalling this app will:
                      <ul className="list-disc list-inside mt-2 space-y-1">
                        <li>Remove all app configuration and settings</li>
                        <li>Revoke API access permissions</li>
                        <li>Stop all active integrations and webhooks</li>
                        <li>Remove the app from your workspace permanently</li>
                      </ul>
                    </AlertDescription>
                  </Alert>

                  {/* Data retention notice */}
                  <div className="p-3 bg-amber-50 rounded-lg border border-amber-200">
                    <div className="flex items-start gap-2">
                      <Info className="h-4 w-4 text-amber-600 mt-0.5" />
                      <div>
                        <p className="text-sm font-medium text-amber-800">Data Retention</p>
                        <p className="text-xs text-amber-700 mt-1">
                          Your Karrio data will remain intact. Only app-specific configurations and integrations will be removed.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <DialogFooter className="gap-2">
                <Button variant="outline" onClick={cancelUninstallApp}>
                  Cancel
                </Button>
                <Button variant="destructive" onClick={confirmUninstallApp} disabled={!appToUninstall}>
                  <Trash2 className="w-4 h-4 mr-2" />
                  Uninstall App
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
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
