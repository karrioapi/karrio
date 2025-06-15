"use client";
import React, { useState, useEffect, Suspense } from "react";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Loader2, AlertTriangle } from "lucide-react";
import { useAppInstallation } from "@karrio/hooks";
import {
  AppContainerProps,
  AppInstance,
  AppContext,
  AppModule,
  AppManifest,
  AppError,
  AppStatus
} from "@karrio/app-store/types";
import {
  loadAppModule,
  normalizeAppMetadata,
  appSupportsViewport,
  createAppError
} from "../utils";
import { getAppStore } from "@karrio/app-store";

interface AppContainerState {
  status: AppStatus;
  module: AppModule | null;
  error: AppError | null;
}

/**
 * AppContainer - Loads and renders Karrio apps with proper error handling and loading states
 */
export function AppContainer({
  appId,
  viewport = "dashboard",
  context = {},
  className = "",
}: AppContainerProps) {
  const [state, setState] = useState<AppContainerState>({
    status: "loading",
    module: null,
    error: null,
  });

  // Only fetch app installation data for non-builtin apps
  const shouldFetchInstallation = state.module?.default.type !== "builtin";
  const { isInstalled, installation, app, isLoading, error } = useAppInstallation(
    appId,
    shouldFetchInstallation
  );

  // Load app module when component mounts
  useEffect(() => {
    let isMounted = true;

    async function loadApp() {
      try {
        setState(prev => ({ ...prev, status: "loading", error: null }));

        const appStore = getAppStore();
        const appImportFunc = appStore.apps[appId];

        if (!appImportFunc) {
          throw createAppError(
            "APP_NOT_FOUND",
            `App ${appId} not found in app store`,
            { appId }
          );
        }

        const module = await loadAppModule(appId, appImportFunc);

        // Validate that app supports the requested viewport
        if (!appSupportsViewport(module.default, viewport)) {
          throw createAppError(
            "VIEWPORT_NOT_SUPPORTED",
            `App ${appId} does not support viewport ${viewport}`,
            { appId, viewport, supportedViewports: module.default.ui?.viewports }
          );
        }

        if (isMounted) {
          setState({
            status: "ready",
            module,
            error: null,
          });
        }
      } catch (error) {
        console.error(`Failed to load app ${appId}:`, error);

        if (isMounted) {
          setState({
            status: "error",
            module: null,
            error: error as AppError,
          });
        }
      }
    }

    loadApp();

    return () => {
      isMounted = false;
    };
  }, [appId, viewport]);

  // Show loading while app installation data is being fetched (only for non-builtin apps)
  if (shouldFetchInstallation && isLoading) {
    return <AppLoadingState />;
  }

  // Show error if failed to fetch app installation data (only for non-builtin apps)
  if (shouldFetchInstallation && error) {
    return (
      <AppErrorState
        error={createAppError(
          "APP_DATA_ERROR",
          "Failed to load app installation data",
          { error }
        )}
      />
    );
  }

  // Show not installed state for apps that require installation
  if (shouldFetchInstallation && !isInstalled && state.module?.default.type !== "builtin") {
    return <AppNotInstalledState appId={appId} manifest={state.module?.default} />;
  }

  // Show loading state while app module is loading
  if (state.status === "loading") {
    return <AppLoadingState />;
  }

  // Show error state
  if (state.status === "error" || state.error) {
    return <AppErrorState error={state.error!} />;
  }

  // Render the app
  if (state.status === "ready" && state.module) {
    return (
      <AppRenderer
        appId={appId}
        module={state.module}
        appData={app}
        installation={installation}
        context={context}
        viewport={viewport}
        className={className}
      />
    );
  }

  return <AppLoadingState />;
}

/**
 * AppRenderer - Renders the actual app component
 */
interface AppRendererProps {
  appId: string;
  module: AppModule;
  appData: any;
  installation: any;
  context: Partial<AppContext>;
  viewport: string;
  className: string;
}

function AppRenderer({
  appId,
  module,
  appData,
  installation,
  context,
  viewport,
  className,
}: AppRendererProps) {
  const { Component } = module;

  if (!Component) {
    return (
      <AppErrorState
        error={createAppError(
          "NO_COMPONENT",
          `App ${appId} does not export a Component`,
          { appId }
        )}
      />
    );
  }

  // Create app instance
  const appInstance: AppInstance = {
    id: appId,
    manifest: module.default,
    installation,
    config: installation?.metadata || {},
    isInstalled: !!installation,
    isEnabled: installation ? installation.enabled !== false : false,
    ...normalizeAppMetadata(appData),
  };

  // Create app context
  const appContext: AppContext = {
    workspace: {
      id: context.workspace?.id || "default",
      name: context.workspace?.name || "Default Workspace",
    },
    user: context.user,
    page: context.page || {
      route: window.location.pathname,
      params: {},
    },
    data: context.data,
  };

  // Handle app actions
  const handleAction = (action: any) => {
    console.log(`App ${appId} action:`, action);
    // TODO: Implement action handling (events, navigation, etc.)
  };

  return (
    <div className={`karrio-app-container ${className}`} data-app-id={appId}>
      <Suspense fallback={<AppLoadingState />}>
        <Component
          app={appInstance}
          context={appContext}
          onAction={handleAction}
        />
      </Suspense>
    </div>
  );
}

/**
 * Loading state component
 */
function AppLoadingState() {
  return (
    <Card className="w-full">
      <CardContent className="flex items-center justify-center py-8">
        <div className="flex items-center gap-2 text-muted-foreground">
          <Loader2 className="h-4 w-4 animate-spin" />
          <span className="text-sm">Loading app...</span>
        </div>
      </CardContent>
    </Card>
  );
}

/**
 * Error state component
 */
interface AppErrorStateProps {
  error: AppError;
}

function AppErrorState({ error }: AppErrorStateProps) {
  return (
    <Alert variant="destructive">
      <AlertTriangle className="h-4 w-4" />
      <AlertDescription>
        <div>
          <strong>App Error ({error.code}):</strong> {error.message}
          {error.details && (
            <details className="mt-2">
              <summary className="cursor-pointer text-sm">View details</summary>
              <pre className="mt-1 text-xs bg-gray-100 p-2 rounded overflow-auto">
                {JSON.stringify(error.details, null, 2)}
              </pre>
            </details>
          )}
        </div>
      </AlertDescription>
    </Alert>
  );
}

/**
 * Not installed state component
 */
interface AppNotInstalledStateProps {
  appId: string;
  manifest?: AppManifest;
}

function AppNotInstalledState({ appId, manifest }: AppNotInstalledStateProps) {
  return (
    <Card className="w-full">
      <CardContent className="flex items-center justify-center py-8">
        <div className="text-center text-muted-foreground">
          <AlertTriangle className="h-8 w-8 mx-auto mb-2" />
          <p className="text-sm">
            {manifest ? `${manifest.name} is not installed` : `App ${appId} is not installed`}
          </p>
          <p className="text-xs mt-1">
            Install this app from the marketplace to use it.
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
