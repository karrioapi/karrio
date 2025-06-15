import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  GET_OAUTH_APPS,
  GET_OAUTH_APP,
  GET_APP_INSTALLATIONS,
  GET_APP_INSTALLATION_BY_APP_ID,
  INSTALL_APP,
  UNINSTALL_APP,
  UPDATE_APP_INSTALLATION,
  CREATE_OAUTH_APP,
  UPDATE_OAUTH_APP,
  DELETE_OAUTH_APP,
} from "@karrio/types/graphql/ee/queries";
import {
  GetOAuthApps,
  GetOAuthApp,
  GetAppInstallations,
  GetAppInstallationByAppId,
  InstallApp,
  UninstallApp,
  UpdateAppInstallation,
  CreateOAuthApp,
  UpdateOAuthApp,
  DeleteOAuthApp,
  OAuthAppFilter,
  AppInstallationFilter,
  CreateOAuthAppMutationInput,
  UpdateOAuthAppMutationInput,
  DeleteOAuthAppMutationInput,
  InstallAppMutationInput,
  UninstallAppMutationInput,
  UpdateAppInstallationMutationInput,
} from "@karrio/types/graphql/ee/types";
import { gqlstr } from "@karrio/lib";
import { useKarrio } from "./karrio";

// OAuth Apps queries (for developers page)
export function useOAuthApps(filter?: OAuthAppFilter) {
  const karrio = useKarrio();
  const query = useQuery({
    staleTime: 5000,
    refetchOnWindowFocus: false,
    queryKey: ["oauth-apps", filter],
    queryFn: () => karrio.graphql.request<GetOAuthApps>(gqlstr(GET_OAUTH_APPS), { variables: { filter } }),
  });

  return {
    query,
    get: (id: string) => {
      return query.data?.oauth_apps?.edges?.find((edge: any) => edge.node.id === id)?.node;
    },
  };
}

export function useOAuthApp(id: string) {
  const karrio = useKarrio();
  const query = useQuery({
    staleTime: 5000,
    refetchOnWindowFocus: false,
    queryKey: ["oauth-app", id],
    queryFn: () => karrio.graphql.request<GetOAuthApp>(gqlstr(GET_OAUTH_APP), { variables: { id } }),
    enabled: !!id,
  });

  return {
    query,
  };
}

// App Installations queries (for app store)
export function useAppInstallations(filter?: AppInstallationFilter) {
  const karrio = useKarrio();
  const query = useQuery({
    staleTime: 5000,
    refetchOnWindowFocus: false,
    queryKey: ["app-installations", filter],
    queryFn: () => karrio.graphql.request<GetAppInstallations>(gqlstr(GET_APP_INSTALLATIONS), { variables: { filter } }),
  });

  return {
    query,
    get: (id: string) => {
      return query.data?.app_installations?.edges?.find((edge: any) => edge.node.id === id)?.node;
    },
  };
}

export function useAppInstallationByAppId(appId: string, enabled = true) {
  const karrio = useKarrio();
  const query = useQuery({
    staleTime: 5000,
    refetchOnWindowFocus: false,
    queryKey: ["app-installation-by-app-id", appId],
    queryFn: () => karrio.graphql.request<GetAppInstallationByAppId>(gqlstr(GET_APP_INSTALLATION_BY_APP_ID), { variables: { app_id: appId } }),
    enabled: enabled && !!appId,
  });

  return {
    query,
  };
}

// Legacy compatibility functions (for gradual migration)
export function useApps(filter?: any) {
  // For marketplace apps, we now use app installations
  return useAppInstallations(filter);
}

export function usePrivateApps(filter?: OAuthAppFilter) {
  // Private apps are now OAuth apps
  return useOAuthApps(filter);
}

export function useInstalledApps(filter?: AppInstallationFilter) {
  const karrio = useKarrio();
  const query = useQuery({
    staleTime: 5000,
    refetchOnWindowFocus: false,
    queryKey: ["installed-apps", filter],
    queryFn: async () => {
      const response = await karrio.graphql.request<GetAppInstallations>(gqlstr(GET_APP_INSTALLATIONS), {
        variables: { filter: { ...filter, is_active: true } }
      });
      return {
        app_installations: response.app_installations
      };
    },
  });

  return {
    query,
    get: (appId: string) => {
      return query.data?.app_installations?.edges?.find((edge: any) => edge.node.app_id === appId)?.node;
    },
  };
}

export function useApp(appId: string, enabled = true) {
  // Check if it's an installation by app_id
  const { query } = useAppInstallationByAppId(enabled && appId ? appId : "", enabled);

  return {
    query: {
      ...query,
      data: query.data ? { app: query.data.app_installation_by_app_id } : undefined,
    },
  };
}

// Hook for checking app installation status and data
export function useAppInstallation(appId: string, enabled = true) {
  const { query } = useAppInstallationByAppId(appId, enabled);

  const installation = query.data?.app_installation_by_app_id;
  const isInstalled = !!installation;

  return {
    isInstalled,
    installation,
    app: installation ? { id: installation.app_id, installation } : null,
    isLoading: query.isLoading,
    error: query.error,
    query,
  };
}

// Mutations
export function useAppMutations() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateAppsCache = () => {
    queryClient.invalidateQueries(["oauth-apps"]);
    queryClient.invalidateQueries(["app-installations"]);
    queryClient.invalidateQueries(["installed-apps"]);
    queryClient.invalidateQueries(["app-installation-by-app-id"]);
  };

  const installApp = useMutation({
    mutationFn: (data: InstallAppMutationInput) =>
      karrio.graphql.request<InstallApp>(gqlstr(INSTALL_APP), { variables: { data } }),
    onSuccess: () => invalidateAppsCache(),
  });

  const uninstallApp = useMutation({
    mutationFn: (data: UninstallAppMutationInput) =>
      karrio.graphql.request<UninstallApp>(gqlstr(UNINSTALL_APP), { variables: { data } }),
    onSuccess: () => invalidateAppsCache(),
  });

  const updateAppInstallation = useMutation({
    mutationFn: (data: UpdateAppInstallationMutationInput) =>
      karrio.graphql.request<UpdateAppInstallation>(gqlstr(UPDATE_APP_INSTALLATION), { variables: { data } }),
    onSuccess: () => invalidateAppsCache(),
  });

  const createOAuthApp = useMutation({
    mutationFn: (data: CreateOAuthAppMutationInput) =>
      karrio.graphql.request<CreateOAuthApp>(gqlstr(CREATE_OAUTH_APP), { variables: { data } }),
    onSuccess: () => invalidateAppsCache(),
  });

  const updateOAuthApp = useMutation({
    mutationFn: (data: UpdateOAuthAppMutationInput) => {
      const updateData = { ...data };
      return karrio.graphql.request<UpdateOAuthApp>(gqlstr(UPDATE_OAUTH_APP), { variables: { data: updateData } });
    },
    onSuccess: () => invalidateAppsCache(),
  });

  const deleteOAuthApp = useMutation({
    mutationFn: (data: DeleteOAuthAppMutationInput) =>
      karrio.graphql.request<DeleteOAuthApp>(gqlstr(DELETE_OAUTH_APP), { variables: { data } }),
    onSuccess: () => invalidateAppsCache(),
  });

  // Legacy compatibility
  const createApp = createOAuthApp;
  const updateApp = updateOAuthApp;
  const deleteApp = deleteOAuthApp;

  return {
    installApp,
    uninstallApp,
    updateAppInstallation,
    createOAuthApp,
    updateOAuthApp,
    deleteOAuthApp,
    // Legacy compatibility
    createApp,
    updateApp,
    deleteApp,
  };
}

// Main app store hook
export function useAppStore() {
  const oauthApps = useOAuthApps();
  const installedApps = useInstalledApps();
  const appInstallations = useAppInstallations();

  return {
    oauth: oauthApps,
    installed: installedApps,
    installations: appInstallations,
    // Legacy compatibility
    marketplace: appInstallations,
    private: oauthApps,
  };
}
