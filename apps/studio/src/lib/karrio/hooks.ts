// hooks.ts — TanStack Query data hooks over the decoupled Karrio client.
// These replace @karrio/hooks (which is NextAuth/Next-coupled). Each hook reads
// the KarrioCtx (base URL + token + org + test-mode) from the SessionProvider.
import { useQuery } from "@tanstack/react-query";
import { restGet, graphql, type KarrioCtx } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import type {
  AddressTemplate,
  CarrierConnection,
  DocumentTemplate,
  Order,
  Paginated,
  ParcelTemplate,
  Pickup,
  ProductTemplate,
  Shipment,
  ShippingRule,
  Tracker,
} from "~/lib/karrio/types";

const keyExtra = (ctx: KarrioCtx) => ({ org: ctx.orgId, test: ctx.testMode });

export function useShipments(params?: Record<string, string | number | undefined>) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["shipments", params, keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Shipment>>(ctx, "/v1/shipments", params),
    enabled: Boolean(ctx.token),
  });
}

export function useShipment(id: string) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["shipment", id, keyExtra(ctx)],
    queryFn: () => restGet<Shipment>(ctx, `/v1/shipments/${id}`),
    enabled: Boolean(ctx.token && id),
  });
}

export function useTrackers(params?: Record<string, string | number | undefined>) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["trackers", params, keyExtra(ctx)],
    queryFn: async () => {
      const data = await restGet<Paginated<Tracker>>(ctx, "/v1/trackers", params);
      // Karrio stores the carrier under meta on tracking records; surface it.
      data.results = data.results.map((t) => ({
        ...t,
        carrier_name: t.carrier_name || (t.meta as { carrier_name?: string } | undefined)?.carrier_name,
      }));
      return data;
    },
    enabled: Boolean(ctx.token),
  });
}

export function useCarrierConnections() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["carrier-connections", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<CarrierConnection>>(ctx, "/v1/connections"),
    enabled: Boolean(ctx.token),
  });
}

const ORDERS_QUERY = `query Orders($filter: OrderFilter) {
  orders(filter: $filter) {
    edges { node { id order_id status source created_at
      line_items { id title quantity }
      shipping_to { city country_code person_name }
    } }
  }
}`;

type OrdersResponse = { orders: { edges: Array<{ node: Order }> } };

export function useOrders(filter?: Record<string, unknown>) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["orders", filter, keyExtra(ctx)],
    queryFn: async () => {
      const data = await graphql<OrdersResponse>(ctx, ORDERS_QUERY, { filter });
      return data.orders.edges.map((e) => e.node);
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Generic GraphQL edge helper -------------------------------------------
async function graphqlEdges<T>(
  ctx: KarrioCtx,
  query: string,
  field: string,
  variables?: Record<string, unknown>,
): Promise<T[]> {
  const data = await graphql<Record<string, { edges: Array<{ node: T }> }>>(ctx, query, variables);
  return (data[field]?.edges ?? []).map((e) => e.node);
}

// --- Connections (REST) ------------------------------------------------------
// (useCarrierConnections defined above)

// --- Pickups (REST) ----------------------------------------------------------
export function usePickups() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["pickups", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Pickup>>(ctx, "/v1/pickups"),
    enabled: Boolean(ctx.token),
  });
}

// --- Address templates (GraphQL) ---------------------------------------------
// Live schema exposes saved addresses as `addresses` (Connection[AddressTemplateType]).
// Fields are flat on the node; label/is_default live in the `meta` JSON field.
// The hook normalises meta into top-level label/is_default and an `address` sub-object
// for backward compat with the screens that use a.label, a.is_default, a.address.*.
const ADDRESS_TEMPLATES_QUERY = `query { addresses { edges { node {
  id meta
  person_name company_name address_line1 address_line2
  city state_code postal_code country_code email phone_number residential
} } } }`;

type RawAddress = {
  id: string;
  meta?: { label?: string; is_default?: boolean; [key: string]: unknown };
  person_name?: string; company_name?: string; address_line1?: string; address_line2?: string;
  city?: string; state_code?: string; postal_code?: string; country_code?: string;
  email?: string; phone_number?: string; residential?: boolean;
};

function normaliseAddress(raw: RawAddress): AddressTemplate {
  const { meta, person_name, company_name, address_line1, address_line2,
    city, state_code, postal_code, country_code, email, phone_number, residential, ...rest } = raw;
  return {
    ...rest,
    meta,
    label: meta?.label,
    is_default: meta?.is_default,
    person_name, company_name, address_line1, address_line2,
    city, state_code, postal_code, country_code, email, phone_number, residential,
    address: { person_name, company_name, address_line1, address_line2,
      city, state_code, postal_code, country_code, email, phone_number, residential },
  };
}

export function useAddresses() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["address-templates", keyExtra(ctx)],
    queryFn: async () => {
      const raws = await graphqlEdges<RawAddress>(ctx, ADDRESS_TEMPLATES_QUERY, "addresses");
      return raws.map(normaliseAddress);
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Parcel templates (GraphQL) ----------------------------------------------
// Live schema exposes saved parcels as `parcels` (Connection[ParcelTemplateType]).
// Fields are flat on the node; label/is_default live in the `meta` JSON field.
// The hook normalises meta into top-level label/is_default for screen compat.
const PARCEL_TEMPLATES_QUERY = `query { parcels { edges { node {
  id meta packaging_type width height length dimension_unit weight weight_unit
} } } }`;

type RawParcel = {
  id: string;
  meta?: { label?: string; is_default?: boolean; [key: string]: unknown };
  packaging_type?: string; width?: number; height?: number; length?: number;
  dimension_unit?: string; weight?: number; weight_unit?: string;
};

function normaliseParcel(raw: RawParcel): ParcelTemplate {
  return { ...raw, label: raw.meta?.label, is_default: raw.meta?.is_default };
}

export function useParcels() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["parcel-templates", keyExtra(ctx)],
    queryFn: async () => {
      const raws = await graphqlEdges<RawParcel>(ctx, PARCEL_TEMPLATES_QUERY, "parcels");
      return raws.map(normaliseParcel);
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Product templates / commodities (GraphQL) -------------------------------
// Live schema exposes saved commodities as `products` (Connection[ProductTemplateType]).
// label/is_default live in `meta`; there is no direct label/is_default field on the node.
// The hook normalises meta into top-level label/is_default for screen compat.
const PRODUCTS_QUERY = `query { products { edges { node {
  id meta title sku hs_code weight weight_unit value_amount value_currency origin_country
} } } }`;

type RawProduct = {
  id: string;
  meta?: { label?: string; is_default?: boolean; [key: string]: unknown };
  title?: string; sku?: string; hs_code?: string; weight?: number; weight_unit?: string;
  value_amount?: number; value_currency?: string; origin_country?: string;
};

function normaliseProduct(raw: RawProduct): ProductTemplate {
  return { ...raw, label: raw.meta?.label, is_default: raw.meta?.is_default };
}

export function useProducts() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["products", keyExtra(ctx)],
    queryFn: async () => {
      const raws = await graphqlEdges<RawProduct>(ctx, PRODUCTS_QUERY, "products");
      return raws.map(normaliseProduct);
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Shipping rules (GraphQL) ------------------------------------------------
// `shipping_rules` is NOT exposed by the OSS Karrio GraphQL schema.
// Return an empty list so UI screens degrade gracefully on single-tenant OSS.
export function useShippingRules() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["shipping-rules", keyExtra(ctx)],
    queryFn: (): Promise<ShippingRule[]> => Promise.resolve([]),
    enabled: Boolean(ctx.token),
  });
}

// --- Document templates (REST) -----------------------------------------------
export function useDocumentTemplates() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["document-templates", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<DocumentTemplate>>(ctx, "/v1/documents/templates"),
    enabled: Boolean(ctx.token),
  });
}

// === Build mode ============================================================
// NOTE: app-store / plugin-registry / MCP endpoints are provisional pending the
// Build-mode backend integration (EPIC D/F); shapes are intercepted in tests.
import type { App, ApiKey, McpInfo, Plugin, Webhook } from "~/lib/karrio/types";

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

// === Govern mode ===========================================================
import type { AdminInfo, AuditEvent, TeamMember, Tenant } from "~/lib/karrio/types";

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

// === Mutations =============================================================
import { useMutation, useQueryClient } from "@tanstack/react-query";

// Address template create/update/delete.
// Live schema mutations: create_address / update_address / delete_address.
// Input is flat with a `meta` JSON field carrying label/is_default.
const CREATE_ADDRESS = `mutation($input: CreateAddressInput!) {
  create_address(input: $input) {
    address { id meta person_name company_name address_line1 city state_code postal_code country_code }
    errors { field messages }
  }
}`;
const UPDATE_ADDRESS = `mutation($input: UpdateAddressInput!) {
  update_address(input: $input) {
    address { id meta person_name company_name address_line1 city state_code postal_code country_code }
    errors { field messages }
  }
}`;
const DELETE_ADDRESS = `mutation($input: DeleteMutationInput!) { delete_address(input: $input) { id } }`;

export function useSaveAddress() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: { id?: string; data: Record<string, unknown> }) =>
      graphql(ctx, vars.id ? UPDATE_ADDRESS : CREATE_ADDRESS, {
        input: vars.id ? { id: vars.id, ...vars.data } : vars.data,
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["address-templates"] }),
  });
}

export function useDeleteAddress() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => graphql(ctx, DELETE_ADDRESS, { input: { id } }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["address-templates"] }),
  });
}

// Parcel template create/update/delete.
// Live schema mutations: create_parcel / update_parcel / delete_parcel.
// Input is flat with a `meta` JSON field carrying label/is_default.
const CREATE_PARCEL = `mutation($input: CreateParcelInput!) {
  create_parcel(input: $input) {
    parcel { id meta weight weight_unit width height length dimension_unit packaging_type }
    errors { field messages }
  }
}`;
const UPDATE_PARCEL = `mutation($input: UpdateParcelInput!) {
  update_parcel(input: $input) {
    parcel { id meta weight weight_unit width height length dimension_unit packaging_type }
    errors { field messages }
  }
}`;
const DELETE_PARCEL = `mutation($input: DeleteMutationInput!) { delete_parcel(input: $input) { id } }`;

export function useSaveParcel() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: { id?: string; data: Record<string, unknown> }) =>
      graphql(ctx, vars.id ? UPDATE_PARCEL : CREATE_PARCEL, {
        input: vars.id ? { id: vars.id, ...vars.data } : vars.data,
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["parcel-templates"] }),
  });
}

export function useDeleteParcel() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => graphql(ctx, DELETE_PARCEL, { input: { id } }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["parcel-templates"] }),
  });
}

// Product / commodity template create/update/delete.
// Live schema mutations: create_product / update_product / delete_product.
// Input is flat with a `meta` JSON field carrying label/is_default.
const CREATE_PRODUCT = `mutation($input: CreateProductInput!) {
  create_product(input: $input) {
    product { id meta title sku hs_code weight weight_unit value_amount value_currency origin_country }
    errors { field messages }
  }
}`;
const UPDATE_PRODUCT = `mutation($input: UpdateProductInput!) {
  update_product(input: $input) {
    product { id meta title sku hs_code weight weight_unit value_amount value_currency origin_country }
    errors { field messages }
  }
}`;
const DELETE_PRODUCT = `mutation($input: DeleteMutationInput!) { delete_product(input: $input) { id } }`;

export function useSaveProduct() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: { id?: string; data: Record<string, unknown> }) =>
      graphql(ctx, vars.id ? UPDATE_PRODUCT : CREATE_PRODUCT, {
        input: vars.id ? { id: vars.id, ...vars.data } : vars.data,
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["products"] }),
  });
}

export function useDeleteProduct() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => graphql(ctx, DELETE_PRODUCT, { input: { id } }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["products"] }),
  });
}

// === REST mutations (connections, webhooks) =================================
import { restMutate } from "~/lib/karrio/client";

export function useSaveWebhook() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: { id?: string; data: Record<string, unknown> }) =>
      vars.id
        ? restMutate(ctx, "PATCH", `/v1/webhooks/${vars.id}`, vars.data)
        : restMutate(ctx, "POST", "/v1/webhooks", vars.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["webhooks"] }),
  });
}

export function useDeleteWebhook() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => restMutate(ctx, "DELETE", `/v1/webhooks/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["webhooks"] }),
  });
}

export function useSaveConnection() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: { id?: string; data: Record<string, unknown> }) =>
      vars.id
        ? restMutate(ctx, "PATCH", `/v1/connections/${vars.id}`, vars.data)
        : restMutate(ctx, "POST", "/v1/connections", vars.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["carrier-connections"] }),
  });
}

export function useDeleteConnection() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => restMutate(ctx, "DELETE", `/v1/connections/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["carrier-connections"] }),
  });
}

// === Parity resources ======================================================
import type {
  BatchOperation,
  Manifest,
  RateSheet,
  UsageSummary,
  Workflow,
} from "~/lib/karrio/types";

export function useManifests() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["manifests", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Manifest>>(ctx, "/v1/manifests"),
    enabled: Boolean(ctx.token),
  });
}

export function useBatches() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["batches", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<BatchOperation>>(ctx, "/v1/batches/operations"),
    enabled: Boolean(ctx.token),
  });
}

// `workflows` is NOT exposed by the OSS Karrio GraphQL schema (EE/platform only).
// Return an empty list so the Workflows screen degrades gracefully on OSS.
export function useWorkflows() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["workflows", keyExtra(ctx)],
    queryFn: (): Promise<Workflow[]> => Promise.resolve([]),
    enabled: Boolean(ctx.token),
  });
}

// RateSheetType fields on OSS: id, name, slug, carrier_name.
// `services_count` and `is_system` do not exist on the OSS type.
const RATE_SHEETS_QUERY = `query { rate_sheets { edges { node {
  id name slug carrier_name
} } } }`;

export function useRateSheets() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["rate-sheets", keyExtra(ctx)],
    queryFn: () => graphqlEdges<RateSheet>(ctx, RATE_SHEETS_QUERY, "rate_sheets"),
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
