"use client";
import React, { useState, useEffect, Suspense } from "react";
import {
  SheetHeader,
  SheetTitle,
} from "@karrio/ui/components/ui/sheet";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import type { AppManifest, AppConfigurationContext } from "../types";
import { GetAppInstallation_app_installation, MetafieldTypeEnum } from "@karrio/types/graphql/ee/types";
import { useSyncedSession } from "@karrio/hooks/session";
import { Button } from "@karrio/ui/components/ui/button";
import { createKarrioClient } from "@karrio/app-store";
import { AlertCircle, X, Loader2 } from "lucide-react";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useAppMutations } from "@karrio/hooks";
import { AppErrorBoundary } from "./app-error-boundary";

interface AppConfigureSheetProps {
  onOpenChange: (open: boolean) => void;
  app: {
    id: string;
    manifest: AppManifest;
    installation?: Partial<GetAppInstallation_app_installation>;
  };
}

// Dynamic configuration component loader
async function loadAppConfigurationComponent(app: AppConfigureSheetProps['app']) {
  try {
    // Use app slug for directory path, fallback to id extraction
    let appSlug = app.id;

    // If the app has manifest with slug, use that
    if ((app.manifest as any)?.slug) {
      appSlug = (app.manifest as any).slug;
    } else {
      // Extract slug from app ID (e.g., "karrio.app.shipping-tasks" -> "shipping-tasks")
      const parts = app.id.split('.');
      if (parts.length > 2 && parts[0] === 'karrio' && parts[1] === 'app') {
        appSlug = parts.slice(2).join('-');
      }
    }

    // Try to dynamically import the configuration component
    const module = await import(`../apps/${appSlug}/configuration`);
    return module.default;
  } catch (error) {
    console.warn(`Failed to load configuration component for app ${app.id}:`, error);
    // Configuration component doesn't exist, return null
    return null;
  }
}

function ConfigurationLoader({
  app,
  context
}: {
  app: AppConfigureSheetProps['app'];
  context: AppConfigurationContext;
}) {
  const [ConfigurationComponent, setConfigurationComponent] = useState<React.ComponentType<any> | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    const loadComponent = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const component = await loadAppConfigurationComponent(app);

        if (mounted) {
          setConfigurationComponent(() => component);
          setIsLoading(false);
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to load configuration');
          setIsLoading(false);
        }
      }
    };

    loadComponent();

    return () => {
      mounted = false;
    };
  }, [app.id]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-2" />
          <p className="text-sm text-slate-600">Loading configuration...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
          <p className="text-sm text-red-600">Failed to load configuration: {error}</p>
        </div>
      </div>
    );
  }

  if (ConfigurationComponent) {
    return (
      <AppErrorBoundary
        context="App Configuration Component"
        showDetails={process.env.NODE_ENV === 'development'}
      >
        <ConfigurationComponent {...context} />
      </AppErrorBoundary>
    );
  }

  return null;
}

export function AppConfigurationSheet({ app, onOpenChange }: AppConfigureSheetProps) {
  const [hasCustomConfiguration, setHasCustomConfiguration] = useState<boolean | null>(null);
  const [configValues, setConfigValues] = useState<Record<string, any>>({});
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();
  const { updateAppInstallation } = useAppMutations();
  const { query: sessionQuery } = useSyncedSession();
  const session = sessionQuery.data;

  // Check if custom configuration component exists
  useEffect(() => {
    const checkCustomConfiguration = async () => {
      const component = await loadAppConfigurationComponent(app);
      setHasCustomConfiguration(!!component);
    };

    checkCustomConfiguration();
  }, [app.id]);

  // Initialize form values from existing installation metafields or defaults
  useEffect(() => {
    if (!app.manifest.metafields) return;

    const initialValues: Record<string, any> = {};

    app.manifest.metafields.forEach((field) => {
      // Check if there's an existing value from installation
      const existingValue = app.installation?.metafields?.find(
        (mf) => mf.key === field.key
      )?.value;

      if (existingValue !== undefined) {
        // Parse the existing value based on field type
        if (field.type === "boolean") {
          initialValues[field.key] = existingValue === "true" || existingValue === "1" || Boolean(existingValue);
        } else if (field.type === "number") {
          initialValues[field.key] = parseFloat(existingValue) || 0;
        } else {
          initialValues[field.key] = existingValue;
        }
      } else if (field.default_value !== undefined) {
        initialValues[field.key] = field.default_value;
      } else {
        // Set appropriate empty values based on type
        if (field.type === "boolean") {
          initialValues[field.key] = false;
        } else if (field.type === "number") {
          initialValues[field.key] = 0;
        } else {
          initialValues[field.key] = "";
        }
      }
    });

    setConfigValues(initialValues);
  }, [app.manifest.metafields, app.installation?.metafields]);

  const handleValueChange = (key: string, value: any) => {
    setConfigValues(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSave = async () => {
    if (!app.installation?.id) {
      toast({
        title: "Error",
        description: "App installation not found",
        variant: "destructive",
      });
      return;
    }

    try {
      setIsLoading(true);

      // Convert form values to metafields format - preserve existing IDs to avoid duplicates
      const metafields = app.manifest.metafields?.map((field) => {
        // Map all frontend types to backend enum values (only text, number, boolean supported)
        let backendType: MetafieldTypeEnum = MetafieldTypeEnum.text;
        if (field.type === "number") {
          backendType = MetafieldTypeEnum.number;
        } else if (field.type === "boolean") {
          backendType = MetafieldTypeEnum.boolean;
        } else {
          // All other types (password, url, multiselect, select, etc.) are stored as text
          backendType = MetafieldTypeEnum.text;
        }

        // Find existing metafield to preserve ID and avoid duplicates
        const existingMetafield = app.installation?.metafields?.find(
          (mf) => mf.key === field.key
        );

        return {
          ...(existingMetafield?.id ? { id: existingMetafield.id } : {}),
          key: field.key,
          value: String(configValues[field.key] || ""),
          type: backendType,
          is_required: field.is_required || false,
        };
      }) || [];

      const result = await updateAppInstallation.mutateAsync({
        id: app.installation.id,
        metafields: metafields,
      });

      if (result.update_app_installation?.errors?.length) {
        const error = result.update_app_installation.errors[0];
        toast({
          title: "Error saving configuration",
          description: error.messages?.join(", "),
          variant: "destructive",
        });
      } else {
        toast({
          title: "Configuration saved",
          description: `${app.manifest.name} has been configured successfully`,
        });
        onOpenChange(false);
      }
    } catch (error: any) {
      toast({
        title: "Error saving configuration",
        description: error.message || "An unexpected error occurred",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Create configuration context for embedded components
  const configurationContext: AppConfigurationContext = {
    app: {
      id: app.id,
      manifest: app.manifest as any, // Pass through the actual manifest
      installation: app.installation,
      config: app.installation?.metafields?.reduce((acc, field) => {
        acc[field.key] = field.value;
        return acc;
      }, {} as Record<string, any>) || {},
      isInstalled: !!app.installation,
      isEnabled: !!app.installation,
    },
    context: {
      workspace: { id: session?.orgId || 'unknown', name: 'Workspace' },
      user: session?.user as any,
      org: session?.orgId ? { id: session.orgId, name: 'Organization' } : undefined,
    },
    karrio: app.installation?.api_key ? createKarrioClient(app.installation.api_key) : undefined,
    onConfigChange: handleValueChange,
    onSave: handleSave,
    onCancel: () => onOpenChange(false),
  };

  // Render read-only metafields summary
  const renderMetafieldsSummary = () => {
    if (!app.installation?.metafields || app.installation.metafields.length === 0) {
      return (
        <div className="flex items-center justify-center py-8">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-sm text-slate-700 leading-relaxed">
              This app has no configuration settings.
            </p>
          </div>
        </div>
      );
    }

    return (
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-slate-900 mb-4">Current Configuration</h3>
        <div className="space-y-3">
          {app.installation.metafields.map((field) => {
            const schemaField = app.manifest.metafields?.find(f => f.key === field.key);
            const displayValue = field.type === 'password' || schemaField?.sensitive
              ? '••••••••'
              : field.value || 'Not set';

            return (
              <div key={field.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-md border">
                <div>
                  <Label className="text-xs font-medium text-slate-700">
                    {schemaField?.label || field.key}
                  </Label>
                  <p className="text-sm text-slate-600 mt-1">
                    {displayValue}
                  </p>
                </div>
                {field.is_required && (
                  <Badge variant="outline" className="text-xs">
                    Required
                  </Badge>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  if (!app.manifest.metafields || app.manifest.metafields.length === 0) {
    return (
      <div className="h-full flex flex-col">
        <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
          <div className="flex items-center justify-between">
            <SheetTitle className="text-lg font-semibold">
              {app.manifest.name} Configuration
            </SheetTitle>
            <div>
              <Button variant="ghost" size="sm" onClick={() => onOpenChange(false)} className="p-0 rounded-full">
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </SheetHeader>
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-6">
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
                  by {app.manifest.developer?.name || 'Karrio'}
                </p>
                <p className="text-sm text-slate-700 leading-relaxed">
                  Configure the settings for this app installation.
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-center py-8">
              <div className="text-center">
                <AlertCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-sm text-slate-700 leading-relaxed">
                  This app has no configurable settings.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <AppErrorBoundary
      context="App Configuration Sheet"
      showDetails={process.env.NODE_ENV === 'development'}
    >
      <div className="h-full flex flex-col">
        <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
          <div className="flex items-center justify-between">
            <SheetTitle className="text-lg font-semibold">
              {app.manifest.name} Configuration
            </SheetTitle>
            <div>
              <Button variant="ghost" size="sm" onClick={() => onOpenChange(false)} className="p-0 rounded-full">
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </SheetHeader>
        <div className="flex-1 overflow-y-auto">
          {/* Configuration Content */}
          <div className="max-w-4xl mx-auto space-y-6 h-full">
            {hasCustomConfiguration === null ? (
              // Loading state
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin" />
              </div>
            ) : hasCustomConfiguration ? (
              // Custom configuration component
              <Suspense fallback={
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin" />
                </div>
              }>
                <ConfigurationLoader
                  app={app}
                  context={configurationContext}
                />
              </Suspense>
            ) : (
              // Default metafields summary (read-only)
              <AppErrorBoundary
                context="Metafields Summary"
                showDetails={process.env.NODE_ENV === 'development'}
              >
                {renderMetafieldsSummary()}
              </AppErrorBoundary>
            )}
          </div>
        </div>
      </div>
    </AppErrorBoundary>
  );
}
