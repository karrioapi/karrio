// hooks/govern.ts — Govern-mode read hooks (UNIT C). Sourced from Karrio's
// canonical GraphQL: team + admin overview from the ADMIN schema
// (/admin/graphql), usage + audit from the tenant schema. `tenants` has no OSS
// source (no `accounts`) → empty/EE state. See STUDIO_GRAPHQL_REBUILD.md.
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { adminGraphql, graphql } from "~/lib/karrio/client";
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

// --- Team mutations (ADMIN GraphQL create/update/remove user) ---------------
// Role is encoded onto the Django flags the admin schema exposes:
//   owner  → is_superuser   admin → is_staff   member → neither.
type Role = "owner" | "admin" | "member";
const roleFlags = (role: Role) => ({
  is_superuser: role === "owner",
  is_staff: role === "owner" || role === "admin",
});

const CREATE_USER = `mutation($input: CreateUserMutationInput!) {
  create_user(input: $input) { user { id email } errors { field messages } }
}`;
const UPDATE_USER = `mutation($input: UpdateUserMutationInput!) {
  update_user(input: $input) { user { id email } errors { field messages } }
}`;
const REMOVE_USER = `mutation($input: DeleteUserMutationInput!) {
  remove_user(input: $input) { id }
}`;

export type InviteUserInput = { email: string; full_name?: string; role: Role; redirect_url?: string };

// create_user requires password1/password2; for an invite we generate a random
// one-time password (the user resets via the email flow / redirect_url). Uses
// the Web Crypto CSPRNG — never Math.random — since this is a credential.
function randomPassword(): string {
  const charset = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789";
  const bytes = new Uint8Array(20);
  crypto.getRandomValues(bytes);
  const body = Array.from(bytes, (b) => charset[b % charset.length]).join("");
  // Prefix guarantees the Django validators (length, not-all-numeric, mixed) pass.
  return `St!${body}`;
}

export function useInviteUser() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: InviteUserInput) => {
      const password = randomPassword();
      return adminGraphql(ctx, CREATE_USER, {
        input: {
          email: vars.email,
          full_name: vars.full_name || undefined,
          password1: password,
          password2: password,
          redirect_url: vars.redirect_url || (typeof window !== "undefined" ? window.location.origin : undefined),
          ...roleFlags(vars.role),
        },
      });
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["team"] }),
  });
}

export type UpdateUserInput = { id: string; role?: Role; is_active?: boolean; full_name?: string };

export function useUpdateUser() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: UpdateUserInput) =>
      adminGraphql(ctx, UPDATE_USER, {
        input: {
          id: Number(vars.id),
          ...(vars.full_name !== undefined ? { full_name: vars.full_name } : {}),
          ...(vars.is_active !== undefined ? { is_active: vars.is_active } : {}),
          ...(vars.role ? roleFlags(vars.role) : {}),
        },
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["team"] }),
  });
}

export function useRemoveUser() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => adminGraphql(ctx, REMOVE_USER, { input: { id: Number(id) } }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["team"] }),
  });
}

// --- Admin overview (ADMIN GraphQL `worker_health`) -------------------------
const ADMIN_OVERVIEW_QUERY = `query {
  worker_health { is_available }
  users { edges { node { id } } }
  system_carrier_connections { edges { node { id active } } }
}`;

type AdminOverviewRaw = {
  worker_health?: { is_available?: boolean };
  users?: { edges: Array<{ node: { id: string } }> };
  system_carrier_connections?: { edges: Array<{ node: { id: string; active?: boolean } }> };
};

export function useAdminInfo() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["admin-info", keyExtra(ctx)],
    queryFn: async (): Promise<AdminInfo> => {
      const data = await adminGraphql<AdminOverviewRaw>(ctx, ADMIN_OVERVIEW_QUERY);
      const available = data.worker_health?.is_available;
      const conns = data.system_carrier_connections?.edges ?? [];
      return {
        license: "Open Source",
        users: data.users?.edges?.length ?? 0,
        system_connections: conns.length,
        worker_available: available,
        runtimes: [
          { name: "Background worker", memory: available ? "available" : available === false ? "unavailable" : "—" },
        ],
        resources: [],
      };
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Tenants: no OSS source (no `accounts`) → honest empty/EE state ----------
export function useTenants() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["tenants", keyExtra(ctx)],
    queryFn: async (): Promise<Paginated<Tenant>> => ({ count: 0, next: null, previous: null, results: [] }),
    enabled: Boolean(ctx.token),
    staleTime: Infinity,
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
  shipment_count { date count }
  shipping_spend { date count }
  order_volumes { date count }
  api_requests { date count }
  tracker_count { date count }
} }`;

type Point = { date: string; count: number };
type RawUsage = {
  total_shipments?: number;
  total_trackers?: number;
  total_requests?: number;
  total_shipping_spend?: number;
  order_volume?: number;
  shipment_count?: Point[];
  shipping_spend?: Point[];
  order_volumes?: Point[];
  api_requests?: Point[];
  tracker_count?: Point[];
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
        series: [
          { key: "shipment_count", label: "Shipments", format: "number", points: u.shipment_count ?? [] },
          { key: "shipping_spend", label: "Shipping spend", format: "currency", points: u.shipping_spend ?? [] },
          { key: "api_requests", label: "API requests", format: "number", points: u.api_requests ?? [] },
          { key: "order_volumes", label: "Orders", format: "number", points: u.order_volumes ?? [] },
        ],
      };
    },
    enabled: Boolean(ctx.token),
  });
}
