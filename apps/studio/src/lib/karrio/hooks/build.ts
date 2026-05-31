// hooks/build.ts — Build-mode read hooks. UNIT B migrates api_keys + webhooks
// to the tenant GraphQL schema, and renders honest "not available" states for
// apps / plugins / mcp (no OSS source — see STUDIO_GRAPHQL_REBUILD.md).
import { useQuery } from "@tanstack/react-query";
import { restGet } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import { keyExtra } from "~/lib/karrio/hooks/_shared";
import type { ApiKey, App, McpInfo, Paginated, Plugin, Webhook } from "~/lib/karrio/types";

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

export function useWebhooks() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["webhooks", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Webhook>>(ctx, "/v1/webhooks"),
    enabled: Boolean(ctx.token),
  });
}

export function useApiKeys() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["api-keys", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<ApiKey>>(ctx, "/v1/api_keys"),
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
