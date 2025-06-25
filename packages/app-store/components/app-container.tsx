"use client";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import React, { useState, useEffect, Suspense } from "react";
import { useSyncedSession } from "@karrio/hooks/session";
import { createKarrioClient } from "@karrio/app-store";
import { Loader2, AlertTriangle } from "lucide-react";
import { useAppInstallation, useAppStore } from "@karrio/hooks";
import { getAppStore } from "@karrio/app-store";
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
import { AppErrorBoundary } from "./app-error-boundary";

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

  // Fetch app installation data for all apps (builtin and non-builtin)
  const shouldFetchInstallation = state.status === "ready";
  const { isInstalled, installation, app, isLoading, error } = useAppInstallation(
    appId,
    shouldFetchInstallation
  );

  // Debug logging for app installation data
  React.useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('App Installation Debug:', {
        appId,
        appType: state.module?.default.type,
        hasInstallation: !!installation,
        installationMetafieldsCount: installation?.metafields?.length || 0,
        installationMetafields: installation?.metafields,
        isLoading,
        error: error,
        isInstalled,
      });
    }
  }, [appId, state.module?.default.type, installation, isLoading, error, isInstalled]);

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
  }, [appId, viewport, installation?.updated_at]);

  // Show loading while app installation data is being fetched
  if (shouldFetchInstallation && isLoading) {
    return <AppLoadingState />;
  }

  // Show error if failed to fetch app installation data
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

  // Show not installed state for non-builtin apps that require installation
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
    // Use the installation data directly (works for both builtin and non-builtin apps)
    const finalInstallation = installation;

    return (
      <AppRenderer
        appId={appId}
        module={state.module}
        appData={app}
        installation={finalInstallation}
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
  const { query: sessionQuery } = useSyncedSession();
  const session = sessionQuery.data;

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

  // Create enhanced app instance with proper installation structure
  const appInstance: AppInstance = {
    id: appId,
    manifest: module.default as AppManifest,
    installation: {
      ...installation,
      // Ensure metafields are properly accessible
      metafields: installation?.metafields || [],
      config: installation?.metafields?.reduce((acc: Record<string, any>, field: any) => {
        acc[field.key] = field.value;
        return acc;
      }, {}) || installation?.metadata || {},
      // Ensure API key is accessible
      api_key: installation?.api_key,
    },
    isInstalled: !!installation,
    isEnabled: installation ? installation.enabled !== false : false,
    ...normalizeAppMetadata(appData),
  };

  // Create enhanced app context with session data and org info
  const appContext: AppContext & {
    org?: { id: string; name: string };
  } = {
    workspace: {
      id: session?.orgId || context.workspace?.id || "default",
      name: context.workspace?.name || "Default Workspace",
    },
    user: session?.user ? {
      id: session.user.id || 'unknown',
      email: session.user.email || '',
      name: session.user.name || session.user.email || '',
    } : context.user,
    org: session?.orgId ? {
      id: session.orgId,
      name: 'Default Organization',
    } : undefined,
    page: context.page || {
      route: typeof window !== 'undefined' ? window.location.pathname : '',
      params: {},
    },
    data: context.data,
  };

  // Create Karrio client if API key is available
  const karrio = appInstance.installation?.api_key ? createKarrioClient(appInstance.installation.api_key) : undefined;

  // Debug logging for authentication context in development
  React.useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('AppContainer Authentication Debug:', {
        appId,
        appType: module.default?.type,
        hasInstallation: !!appInstance.installation,
        hasApiKey: !!appInstance.installation?.api_key,
        hasKarrioClient: !!karrio,
        metafieldsCount: appInstance.installation?.metafields?.length || 0,
        configKeys: Object.keys((appInstance.installation as any)?.config || {}),
        installationId: appInstance.installation?.id,
        rawMetafields: appInstance.installation?.metafields,
      });
    }
  }, [appId, appInstance.installation, karrio, module]);

  // Set global context for JWT authentication if user and workspace are available
  React.useEffect(() => {
    if (typeof window !== 'undefined' && appContext.user?.id && appContext.workspace?.id) {
      (window as any).__KARRIO_USER_ID__ = appContext.user.id;
      (window as any).__KARRIO_ORG_ID__ = appContext.workspace.id;
    }
  }, [appContext.user?.id, appContext.workspace?.id]);

  // Handle app actions
  const handleAction = (action: any) => {
    console.log(`App ${appId} action:`, action);
    // TODO: Implement action handling (events, navigation, etc.)
  };

  // Create enhanced props for the component
  const componentProps = {
    app: appInstance,
    context: appContext,
    karrio,
    onAction: handleAction,
  };

  return (
    <div className={`karrio-app-container ${className}`} data-app-id={appId}>
      <AppErrorBoundary
        context={`App Component (${appId})`}
        showDetails={process.env.NODE_ENV === 'development'}
      >
        <Suspense fallback={<AppLoadingState />}>
          <Component {...componentProps} />
        </Suspense>
      </AppErrorBoundary>
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
