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

// --- Apps / Plugins / MCP -----------------------------------------------------
// FOLLOW-UP (Unit B, EBE-97): the OSS Karrio schema has no source for these
// (no oauth_apps/app_installations, plugin registry, or mcp endpoint). They
// still call the provisional REST paths and need an honest "not available"
// state — tracked separately so it ships with the screen UX change.
export function useApps() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["apps", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<App>>(ctx, "/v1/apps"),
    enabled: Boolean(ctx.token),
  });
}

export function usePlugins() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["plugins", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Plugin>>(ctx, "/v1/plugins"),
    enabled: Boolean(ctx.token),
  });
}

export function useMcp() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["mcp", keyExtra(ctx)],
    queryFn: () => restGet<McpInfo>(ctx, "/v1/mcp"),
    enabled: Boolean(ctx.token),
  });
}
