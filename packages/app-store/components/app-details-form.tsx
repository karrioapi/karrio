"use client";
import { SheetHeader, SheetTitle, SheetDescription } from "@karrio/ui/components/ui/sheet";
import { ExternalLink, Globe, Mail, Plus, Trash2, Check, Settings } from "lucide-react";
import { useLoader } from "@karrio/ui/core/components/loader";
import { Button } from "@karrio/ui/components/ui/button";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useAppMutations } from "@karrio/hooks";
import { AppConfigureSheet } from "./app-configure-sheet";
import React from "react";

interface PhysicalApp {
  id: string;
  manifest: any;
  isInstalled: boolean;
  installation?: any;
}

interface AppDetailsFormProps {
  app: PhysicalApp;
  onClose: () => void;
  onSave: () => void;
  onLaunch?: (app: PhysicalApp) => void;
  onConfigure?: (app: PhysicalApp) => void;
}

export function AppDetailsForm({ app, onClose, onSave, onLaunch, onConfigure }: AppDetailsFormProps) {
  const { setLoading } = useLoader();
  const { toast } = useToast();
  const { installApp, uninstallApp } = useAppMutations();
  const [configureSheetOpen, setConfigureSheetOpen] = React.useState(false);

  const handleInstall = async () => {
    try {
      setLoading(true);
      const result = await installApp.mutateAsync({
        app_id: app.id,
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
        onSave(); // Refresh the parent data
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

  const handleUninstall = async () => {
    if (!confirm(`Are you sure you want to uninstall ${app.manifest.name}? This action cannot be undone and will remove all app data.`)) {
      return;
    }

    try {
      setLoading(true);
      const result = await uninstallApp.mutateAsync({
        app_id: app.id,
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
          description: "The app has been removed from your workspace",
        });
        onSave(); // Refresh the parent data
      }
    } catch (error: any) {
      toast({
        title: "Error uninstalling app",
        description: error.message || "An unexpected error occurred",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleLaunch = () => {
    if (onLaunch) {
      onLaunch(app);
      onClose(); // Close the details sheet when launching
    }
  };

  const handleConfigure = () => {
    if (onConfigure) {
      onConfigure(app);
      onClose(); // Close details sheet when opening configure
    } else {
      setConfigureSheetOpen(true);
    }
  };

  return (
    <div className="h-full flex flex-col">
      <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
        <div className="flex items-center justify-between">
          <SheetTitle className="text-lg font-semibold">
            App Details
          </SheetTitle>
        </div>
        <SheetDescription className="sr-only">
          View detailed information about the selected app including description, features, and installation options.
        </SheetDescription>
      </SheetHeader>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-6 pb-32">
        {/* App Header */}
        <div className="space-y-4">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-xl font-semibold flex-shrink-0">
              {app.manifest.name?.charAt(0) || 'A'}
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-xl font-semibold text-slate-900 mb-1">
                {app.manifest.name}
              </h2>
              <p className="text-sm text-slate-600 mb-2">
                by {app.manifest.developer?.name || 'Unknown Developer'}
              </p>
              {app.isInstalled && (
                <Badge variant="default" className="text-xs">
                  <Check className="w-3 h-3 mr-1" />
                  Installed
                </Badge>
              )}
            </div>
          </div>
        </div>

        {/* Description */}
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-2">Description</h3>
            <p className="text-sm text-slate-700 leading-relaxed">
              {app.manifest.description || 'No description available.'}
            </p>
          </div>
        </div>

        {/* App Information */}
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-4">App Information</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-slate-50 rounded-md border">
                <div>
                  <Label className="text-xs text-slate-700">Version</Label>
                  <p className="text-xs text-slate-500">{app.manifest.version || '1.0.0'}</p>
                </div>
                <Badge variant="outline" className="text-xs">
                  v{app.manifest.version || '1.0.0'}
                </Badge>
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-50 rounded-md border">
                <div>
                  <Label className="text-xs text-slate-700">Category</Label>
                  <p className="text-xs text-slate-500">{app.manifest.category || 'General'}</p>
                </div>
                <Badge variant="outline" className="text-xs">
                  {app.manifest.category || 'General'}
                </Badge>
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-50 rounded-md border">
                <div>
                  <Label className="text-xs text-slate-700">Type</Label>
                  <p className="text-xs text-slate-500">{app.manifest.type || 'Integration'}</p>
                </div>
                <Badge variant="outline" className="text-xs">
                  {app.manifest.type || 'Integration'}
                </Badge>
              </div>
            </div>
          </div>
        </div>

        {/* Features */}
        {app.manifest.features && app.manifest.features.length > 0 && (
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-slate-900 mb-2">Features</h3>
              <div className="flex flex-wrap gap-2">
                {app.manifest.features.map((feature: string) => (
                  <Badge key={feature} variant="secondary" className="text-xs">
                    {feature}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Pricing */}
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-2">Pricing</h3>
            <div className="p-3 bg-slate-50 rounded-md border">
              <p className="text-sm font-medium text-slate-900">
                {app.manifest.pricing || 'Free'}
              </p>
            </div>
          </div>
        </div>

        {/* Contact Information */}
        {(app.manifest.developer?.website || app.manifest.developer?.email) && (
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-slate-900 mb-2">Contact</h3>
              <div className="space-y-2">
                {app.manifest.developer?.website && (
                  <div className="flex items-center gap-2 text-sm text-slate-600">
                    <Globe className="w-4 h-4" />
                    <a
                      href={app.manifest.developer.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-slate-900 hover:underline"
                    >
                      {app.manifest.developer.website}
                    </a>
                  </div>
                )}
                {app.manifest.developer?.email && (
                  <div className="flex items-center gap-2 text-sm text-slate-600">
                    <Mail className="w-4 h-4" />
                    <a
                      href={`mailto:${app.manifest.developer.email}`}
                      className="hover:text-slate-900 hover:underline"
                    >
                      {app.manifest.developer.email}
                    </a>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Disclaimer */}
        <div className="space-y-4">
          <div className="p-3 bg-slate-50 rounded-md border">
            <p className="text-xs text-slate-500 leading-relaxed">
              Every app published on the Karrio App Store is open source and thoroughly tested via
              peer reviews. Nevertheless, Karrio, Inc. does not endorse or certify these apps unless
              they are published by Karrio. If you encounter inappropriate content or behaviour
              please report it.
            </p>
            <button className="text-xs text-red-600 hover:text-red-700 mt-2 flex items-center gap-1">
              🚩 Report app
            </button>
          </div>
        </div>
      </div>

      {/* Floating Action Buttons */}
      <div className="sticky bottom-0 z-10 bg-white border-t px-4 py-4">
        <div className="flex items-center justify-between">
          <div>
            {app.isInstalled && (
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleConfigure}
                  className="text-slate-600 border-slate-200 hover:bg-slate-50"
                >
                  <Settings className="h-4 w-4 mr-1" />
                  Configure
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleUninstall}
                  className="text-red-600 border-red-200 hover:bg-red-50"
                >
                  <Trash2 className="h-4 w-4 mr-1" />
                  Uninstall
                </Button>
              </div>
            )}
          </div>
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={onClose}
            >
              Close
            </Button>
            {app.isInstalled ? (
              <Button
                onClick={handleLaunch}
                size="sm"
              >
                <ExternalLink className="h-4 w-4 mr-1" />
                Launch
              </Button>
            ) : (
              <Button
                onClick={handleInstall}
                size="sm"
              >
                <Plus className="h-4 w-4 mr-1" />
                Install App
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Configure Sheet */}
      <AppConfigureSheet
        open={configureSheetOpen}
        onOpenChange={setConfigureSheetOpen}
        app={app}
      />
    </div>
  );
}
