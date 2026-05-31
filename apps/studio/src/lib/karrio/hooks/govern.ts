// hooks/govern.ts — Govern-mode read hooks. UNIT C migrates these to the ADMIN
// GraphQL schema (/admin/graphql): team→users, admin→worker_health/configs,
// usage→system_usage; audit→tenant `events`; tenants has no OSS source
// (no `accounts`) → EE empty state. See STUDIO_GRAPHQL_REBUILD.md.
import { useQuery } from "@tanstack/react-query";
import { restGet } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import { keyExtra } from "~/lib/karrio/hooks/_shared";
import type {
  AdminInfo,
  AuditEvent,
  Paginated,
  TeamMember,
  Tenant,
  UsageSummary,
} from "~/lib/karrio/types";

export function useAdminInfo() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["admin-info", keyExtra(ctx)],
    queryFn: () => restGet<AdminInfo>(ctx, "/v1/admin"),
    enabled: Boolean(ctx.token),
  });
}

export function useTenants() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["tenants", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Tenant>>(ctx, "/v1/admin/tenants"),
    enabled: Boolean(ctx.token),
  });
}

export function useTeam() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["team", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<TeamMember>>(ctx, "/v1/admin/users"),
    enabled: Boolean(ctx.token),
  });
}

export function useAuditLog() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["audit", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<AuditEvent>>(ctx, "/v1/events"),
    enabled: Boolean(ctx.token),
  });
}

export function useUsage() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["usage", keyExtra(ctx)],
    queryFn: () => restGet<UsageSummary>(ctx, "/v1/usage"),
    enabled: Boolean(ctx.token),
  });
}
