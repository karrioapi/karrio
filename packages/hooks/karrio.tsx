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
  const client = setupRestClient(host, session);

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
  const { requireAuth = true, enabled = true, ...queryOptions } = options;

  return useQuery({
    ...queryOptions,
    enabled: requireAuth ? (enabled && isAuthenticated) : enabled,
    retry: (failureCount, error) => {
      // Don't retry if it's an authentication error
      if ((error as any)?.response?.errors?.[0]?.code === "authentication_required") {
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

function requestInterceptor(session?: ExtendedSessionType) {
  return (config: any = { headers: {} }) => {
    const testHeader: any = !!session?.testMode
      ? { "x-test-mode": session.testMode }
      : {};
    const authHeader: any = !!session?.accessToken
      ? { authorization: `Bearer ${session.accessToken}` }
      : {};
    const orgHeader: any = !!session?.orgId
      ? { "x-org-id": session.orgId }
      : {};

    config.headers = {
      ...config.headers,
      ...authHeader,
      ...orgHeader,
      ...testHeader,
    };

    return config;
  };
}

function setupRestClient(host: string, session?: ExtendedSessionType): KarrioClient {
  const client = new KarrioClient({ basePath: url$`${host}` });
  client.axios.interceptors.request.use(requestInterceptor(session));
  return client;
}
