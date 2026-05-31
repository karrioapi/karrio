// hooks/govern.ts — Govern-mode read hooks (UNIT C). Sourced from Karrio's
// canonical GraphQL: team + admin overview from the ADMIN schema
// (/admin/graphql), usage + audit from the tenant schema. `tenants` has no OSS
// source (no `accounts`) → empty/EE state. See STUDIO_GRAPHQL_REBUILD.md.
import { useQuery } from "@tanstack/react-query";
import { adminGraphql, graphql, restGet } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import { graphqlEdges, keyExtra } from "~/lib/karrio/hooks/_shared";
import type {
  AdminInfo,
  AuditEvent,
  Paginated,
  TeamMember,
  Tenant,
  UsageSummary,
} from "~/lib/karrio/types";

// --- Team & roles (ADMIN GraphQL `users`) -----------------------------------
const ADMIN_USERS_QUERY = `query { users { edges { node {
  id email full_name is_active is_staff is_superuser last_login
} } } }`;

type RawUser = {
  id: number | string;
  email: string;
  full_name?: string;
  is_active?: boolean;
  is_staff?: boolean;
  is_superuser?: boolean;
  last_login?: string;
};

export function useTeam() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["team", keyExtra(ctx)],
    queryFn: async (): Promise<Paginated<TeamMember>> => {
      const raws = await graphqlEdges<RawUser>(ctx, ADMIN_USERS_QUERY, "users", undefined, "/admin/graphql");
      const results: TeamMember[] = raws.map((u) => ({
        id: String(u.id),
        name: u.full_name || undefined,
        email: u.email,
        role: u.is_superuser ? "owner" : u.is_staff ? "admin" : "member",
        status: u.is_active ? "active" : "inactive",
      }));
      return { count: results.length, next: null, previous: null, results };
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Admin overview (ADMIN GraphQL `worker_health`) -------------------------
const WORKER_HEALTH_QUERY = `query { worker_health { is_available } }`;

export function useAdminInfo() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["admin-info", keyExtra(ctx)],
    queryFn: async (): Promise<AdminInfo> => {
      const data = await adminGraphql<{ worker_health?: { is_available?: boolean } }>(
        ctx,
        WORKER_HEALTH_QUERY,
      );
      const health = data.worker_health;
      return {
        license: "Open Source",
        runtimes: health
          ? [{ name: "Background worker", memory: health.is_available ? "available" : "unavailable" }]
          : [],
        resources: [],
      };
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Tenants ------------------------------------------------------------------
// FOLLOW-UP (Unit C, EBE-98): no OSS source (no `accounts` in /admin/graphql —
// it's EE-only). Still calls the provisional REST path; needs an honest EE
// empty state, tracked separately with the screen UX change.
export function useTenants() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["tenants", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Tenant>>(ctx, "/v1/admin/tenants"),
    enabled: Boolean(ctx.token),
  });
}

// --- Audit log (tenant GraphQL `events`) ------------------------------------
const EVENTS_QUERY = `query { events { edges { node {
  id type created_at created_by { email }
} } } }`;

type RawEvent = { id: string; type?: string; created_at?: string; created_by?: { email?: string } };

export function useAuditLog() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["audit", keyExtra(ctx)],
    queryFn: async (): Promise<Paginated<AuditEvent>> => {
      const raws = await graphqlEdges<RawEvent>(ctx, EVENTS_QUERY, "events");
      const results: AuditEvent[] = raws.map((e) => ({
        id: e.id,
        type: e.type,
        description: e.type,
        actor: e.created_by?.email,
        at: e.created_at,
      }));
      return { count: results.length, next: null, previous: null, results };
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Usage (tenant GraphQL `system_usage`) ----------------------------------
const SYSTEM_USAGE_QUERY = `query { system_usage {
  total_shipments total_trackers total_requests total_shipping_spend order_volume
} }`;

type RawUsage = {
  total_shipments?: number;
  total_trackers?: number;
  total_requests?: number;
  total_shipping_spend?: number;
  order_volume?: number;
};

const num = (n?: number) => (n == null ? "—" : Math.round(n).toLocaleString());

export function useUsage() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["usage", keyExtra(ctx)],
    queryFn: async (): Promise<UsageSummary> => {
      const u = (await graphql<{ system_usage?: RawUsage }>(ctx, SYSTEM_USAGE_QUERY)).system_usage ?? {};
      return {
        plan: "Open Source",
        period: "All time",
        metrics: [
          { label: "Shipments", value: num(u.total_shipments) },
          { label: "Trackers", value: num(u.total_trackers) },
          { label: "Orders", value: num(u.order_volume) },
          { label: "API requests", value: num(u.total_requests) },
          { label: "Shipping spend", value: u.total_shipping_spend != null ? `$${u.total_shipping_spend.toLocaleString()}` : "—" },
        ],
      };
    },
    enabled: Boolean(ctx.token),
  });
}
