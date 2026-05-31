// hooks/build.ts — Build-mode read hooks (UNIT B). api_keys + webhooks come
// from the tenant GraphQL schema; apps / plugins / mcp have NO source in the
// OSS Karrio schema (no oauth_apps/app_installations/plugins/mcp), so they
// resolve to an empty result and the screens render an honest "not available"
// state. See STUDIO_GRAPHQL_REBUILD.md.
import { useQuery } from "@tanstack/react-query";
import { graphql, restGet } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import { keyExtra } from "~/lib/karrio/hooks/_shared";
import type { ApiKey, App, McpInfo, Paginated, Plugin, Webhook } from "~/lib/karrio/types";

// --- API keys (GraphQL `api_keys`) ------------------------------------------
// Live shape: a flat list of { key, label, test_mode, created } (NOT a
// connection). We key rows by `key` (unique) for the screen's row id.
const API_KEYS_QUERY = `query { api_keys { key label test_mode created } }`;

export function useApiKeys() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["api-keys", keyExtra(ctx)],
    queryFn: async (): Promise<Paginated<ApiKey>> => {
      const data = await graphql<{ api_keys: Array<Omit<ApiKey, "id">> }>(ctx, API_KEYS_QUERY);
      const results = (data.api_keys ?? []).map((k) => ({ ...k, id: k.key }));
      return { count: results.length, next: null, previous: null, results };
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Webhooks (REST; full CRUD works today) ---------------------------------
export function useWebhooks() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["webhooks", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Webhook>>(ctx, "/v1/webhooks"),
    enabled: Boolean(ctx.token),
  });
}

// --- Apps / Plugins / MCP: no OSS source → honest empty ---------------------
// The OSS Karrio GraphQL/REST API exposes no app marketplace (oauth_apps/
// app_installations are EE), plugin registry, or MCP server proxy. Resolve to
// empty (no fetch) so the screens render a "not available" notice instead of a
// failed request. Never fabricate rows or a "connected" status.
const empty = <T>(): Paginated<T> => ({ count: 0, next: null, previous: null, results: [] });

export function useApps() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["apps", keyExtra(ctx)],
    queryFn: async (): Promise<Paginated<App>> => empty<App>(),
    enabled: Boolean(ctx.token),
    staleTime: Infinity,
  });
}

export function usePlugins() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["plugins", keyExtra(ctx)],
    queryFn: async (): Promise<Paginated<Plugin>> => empty<Plugin>(),
    enabled: Boolean(ctx.token),
    staleTime: Infinity,
  });
}

export function useMcp() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["mcp", keyExtra(ctx)],
    queryFn: async (): Promise<McpInfo> => ({ status: "not_available", tools: [], clients: [], invocations: [] }),
    enabled: Boolean(ctx.token),
    staleTime: Infinity,
  });
}
