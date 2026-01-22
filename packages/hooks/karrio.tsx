"use client";

import {
  SessionType,
  KarrioClient,
  Metadata,
  UserType,
  GetWorkspaceConfig_workspace_config,
} from "@karrio/types";
import { useQuery, useMutation, UseQueryOptions, UseMutationOptions } from "@tanstack/react-query";
import { get_organizations_organizations } from "@karrio/types/graphql/ee";
import { getCookie, KARRIO_API, logger, url$ } from "@karrio/lib";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useSyncedSession } from "@karrio/hooks/session";
import React from "react";

logger.debug("API clients initialized for Server: " + KARRIO_API);

type ClientProviderProps = {
  children?: React.ReactNode;
};

interface ExtendedSessionType {
  accessToken?: string;
  testMode?: boolean;
  orgId?: string;
  error?: string;
}

type APIClientsContextProps = KarrioClient & {
  isAuthenticated: boolean;
  pageData?: {
    orgId?: string;
    user?: UserType;
    pathname?: string;
    metadata?: Metadata;
    organizations?: get_organizations_organizations[];
    workspace_config?: GetWorkspaceConfig_workspace_config;
  };
};

const defaultClient = new KarrioClient({ basePath: url$`${KARRIO_API || ""}` });

export const APIClientsContext = React.createContext<APIClientsContextProps>({
  ...defaultClient,
  isAuthenticated: false,
  pageData: {},
});

export const ClientProvider = ({
  children,
  ...pageData
}: ClientProviderProps): JSX.Element => {
  const { getHost } = useAPIMetadata();
  const { query: sessionQuery, isAuthenticated } = useSyncedSession();
  const session = sessionQuery.data as ExtendedSessionType;

  const host = getHost?.() || KARRIO_API || "";

  // Use a ref to always have the latest session for the interceptor
  const sessionRef = React.useRef<ExtendedSessionType | undefined>(session);
  React.useEffect(() => {
    sessionRef.current = session;
  }, [session]);

  // Memoize client setup to avoid recreating on every render
  // but use sessionRef in interceptor to always get latest session
  const client = React.useMemo(() => {
    const karrioClient = new KarrioClient({ basePath: url$`${host}` });
    karrioClient.axios.interceptors.request.use((config: any = { headers: {} }) => {
      const currentSession = sessionRef.current;
      const cookieOrgId = getCookie("orgId");
      const testHeader: any = !!currentSession?.testMode
        ? { "x-test-mode": currentSession.testMode }
        : {};
      const authHeader: any = !!currentSession?.accessToken
        ? { authorization: `Bearer ${currentSession.accessToken}` }
        : {};
      const orgHeader: any = !!currentSession?.orgId
        ? { "x-org-id": currentSession.orgId }
        : {};

      config.headers = {
        ...config.headers,
        ...authHeader,
        ...orgHeader,
        ...testHeader,
      };

      return config;
    });
    return karrioClient;
  }, [host]);

  return (
    <APIClientsContext.Provider
      value={{
        ...client,
        isAuthenticated,
        pageData,
      }}
    >
      {children}
    </APIClientsContext.Provider>
  );
};

export function useKarrio() {
  return React.useContext(APIClientsContext);
}

// Utility hook for authentication-aware queries
export function useAuthenticatedQuery<TQueryFnData = unknown, TError = unknown, TData = TQueryFnData>(
  options: Omit<UseQueryOptions<TQueryFnData, TError, TData>, 'enabled'> & {
    enabled?: boolean;
    requireAuth?: boolean;
  }
) {
  const { isAuthenticated } = useKarrio();
  const { query: sessionQuery } = useSyncedSession();
  const { requireAuth = true, enabled = true, ...queryOptions } = options;

  // Wait for session to be fully loaded with data before enabling authenticated queries
  // isAuthenticated already checks for accessToken presence, so this ensures data is ready
  const sessionReady = isAuthenticated && !!(sessionQuery.data as any)?.accessToken;
  const shouldEnable = requireAuth ? (enabled && sessionReady) : enabled;

  // Scope query keys by orgId and testMode to avoid cross-org cache bleed
  const baseKey = (queryOptions as any).queryKey;
  // Ensure we append scope info to the existing array key instead of nesting it
  const keyArray = Array.isArray(baseKey)
    ? baseKey
    : baseKey != null
      ? [baseKey]
      : baseKey;
  const scopedKey = keyArray
    ? [
      ...keyArray,
      {
        orgId: (sessionQuery.data as any)?.orgId,
        testMode: (sessionQuery.data as any)?.testMode,
      },
    ]
    : baseKey;

  return useQuery({
    ...queryOptions,
    queryKey: scopedKey,
    enabled: shouldEnable,
    retry: (failureCount, error) => {
      // Don't retry if it's an authentication error
      if (
        (error as any)?.response?.errors?.[0]?.code === "authentication_required" ||
        (error as any)?.errors?.[0]?.extensions?.code === "UNAUTHENTICATED" ||
        (error as any)?.message?.includes("authentication")
      ) {
        return false;
      }
      return failureCount < 1;
    },
  });
}

// Utility hook for authentication-aware mutations
export function useAuthenticatedMutation<TData = unknown, TError = unknown, TVariables = void, TContext = unknown>(
  options: UseMutationOptions<TData, TError, TVariables, TContext>
) {
  return useMutation(options);
}
