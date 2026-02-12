import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React, { createContext, useContext, useMemo } from "react";

interface EmbedConfig {
  host: string;
  token: string;
  admin?: boolean;
}

interface EmbedContext extends EmbedConfig {
  headers: Record<string, string>;
  graphqlRequest: <T = any>(query: string, variables?: Record<string, any>) => Promise<T>;
}

const KarrioEmbedContext = createContext<EmbedContext>({} as EmbedContext);

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export function KarrioEmbedProvider({
  host,
  token,
  admin = false,
  children,
}: EmbedConfig & { children: React.ReactNode }) {
  const headers = useMemo(
    () => ({
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    }),
    [token],
  );

  const graphqlEndpoint = admin ? `${host}/admin/graphql` : `${host}/graphql`;

  const graphqlRequest = useMemo(
    () =>
      async <T = any>(query: string, variables?: Record<string, any>): Promise<T> => {
        const response = await fetch(graphqlEndpoint, {
          method: "POST",
          headers,
          body: JSON.stringify({ query, variables }),
        });
        const json = await response.json();
        if (json.errors) {
          throw new Error(json.errors[0]?.message || "GraphQL error");
        }
        return json.data as T;
      },
    [graphqlEndpoint, headers],
  );

  const value = useMemo(
    () => ({ host, token, admin, headers, graphqlRequest }),
    [host, token, admin, headers, graphqlRequest],
  );

  return (
    <QueryClientProvider client={queryClient}>
      <KarrioEmbedContext.Provider value={value}>
        {children}
      </KarrioEmbedContext.Provider>
    </QueryClientProvider>
  );
}

export function useKarrioEmbed() {
  return useContext(KarrioEmbedContext);
}
