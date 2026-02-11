/**
 * Embed-compatible replacement for @karrio/hooks/karrio.
 *
 * Provides useKarrio(), useAuthenticatedQuery(), useAuthenticatedMutation(),
 * ClientProvider, and APIClientsContext – all backed by the KarrioEmbedProvider
 * (token-based auth instead of next-auth sessions).
 */
import { useQuery, useMutation, UseQueryOptions, UseMutationOptions } from "@tanstack/react-query";
import { useKarrioEmbed } from "../providers/karrio-embed-provider";
import React from "react";

// ---------- Context (for compatibility with code that reads APIClientsContext) ----------

type APIClientsContextProps = {
  graphql: { request: <T = any>(query: string, variables?: Record<string, any>) => Promise<T> };
  webhooks: {
    create: (args: { webhookData: any }) => Promise<any>;
    update: (args: { id: string; patchedWebhookData: any }) => Promise<any>;
    remove: (args: { id: string }) => Promise<any>;
    test: (args: { id: string; webhookTestRequest: { payload: any } }) => Promise<any>;
  };
  isAuthenticated: boolean;
  pageData: Record<string, any>;
  axios: any;
  [key: string]: any;
};

export const APIClientsContext = React.createContext<APIClientsContextProps>({} as any);

// ---------- ClientProvider (no-op wrapper for embed) ----------

export const ClientProvider = ({ children }: { children?: React.ReactNode }) => {
  return <>{children}</>;
};

// ---------- useKarrio ----------

export function useKarrio(): APIClientsContextProps {
  const { host, token, headers, graphqlRequest } = useKarrioEmbed();

  return React.useMemo(() => {
    // REST helper
    const restRequest = async (method: string, path: string, body?: any) => {
      const response = await fetch(`${host}${path}`, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
      });
      const json = await response.json();
      if (!response.ok) {
        const err: any = new Error(json?.detail || json?.message || "Request failed");
        err.response = { status: response.status, data: json };
        throw err;
      }
      // Mimic AxiosResponse shape so handleFailure/consumers work
      return { data: json, status: response.status };
    };

    return {
      graphql: { request: graphqlRequest },
      webhooks: {
        create: ({ webhookData }: { webhookData: any }) =>
          restRequest("POST", "/v1/webhooks", webhookData),
        update: ({ id, patchedWebhookData }: { id: string; patchedWebhookData: any }) =>
          restRequest("PATCH", `/v1/webhooks/${id}`, patchedWebhookData),
        remove: ({ id }: { id: string }) =>
          restRequest("DELETE", `/v1/webhooks/${id}`),
        test: ({ id, webhookTestRequest }: { id: string; webhookTestRequest: { payload: any } }) =>
          restRequest("POST", `/v1/webhooks/${id}/test`, webhookTestRequest),
      },
      documents: {
        generateDocument: ({ documentData }: { documentData: any }) =>
          restRequest("POST", "/v1/documents/generate", documentData),
      },
      // Minimal axios-like interface for hooks that use karrio.axios.post (e.g. resource-token)
      axios: {
        post: async (path: string, body?: any) => restRequest("POST", path, body),
        get: async (path: string) => restRequest("GET", path),
      },
      isAuthenticated: true,
      pageData: {},
    };
  }, [host, token, headers, graphqlRequest]);
}

// ---------- useAuthenticatedQuery ----------

export function useAuthenticatedQuery<TQueryFnData = unknown, TError = unknown, TData = TQueryFnData>(
  options: Omit<UseQueryOptions<TQueryFnData, TError, TData>, "enabled"> & {
    enabled?: boolean;
    requireAuth?: boolean;
  },
) {
  const { enabled = true, requireAuth: _requireAuth, ...queryOptions } = options;

  return useQuery({
    ...queryOptions,
    enabled,
    retry: (failureCount, error) => {
      if (
        (error as any)?.response?.errors?.[0]?.code === "authentication_required" ||
        (error as any)?.message?.includes("authentication")
      ) {
        return false;
      }
      return failureCount < 1;
    },
  });
}

// ---------- useAuthenticatedMutation ----------

export function useAuthenticatedMutation<
  TData = unknown,
  TError = unknown,
  TVariables = void,
  TContext = unknown,
>(options: UseMutationOptions<TData, TError, TVariables, TContext>) {
  return useMutation(options);
}
