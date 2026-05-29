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
    queryFn: () => restGet<Paginated<Tracker>>(ctx, "/v1/trackers", params),
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
const ADDRESS_TEMPLATES_QUERY = `query { address_templates { edges { node {
  id label is_default
  address { person_name company_name address_line1 city state_code postal_code country_code email phone_number residential }
} } } }`;

export function useAddresses() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["address-templates", keyExtra(ctx)],
    queryFn: () => graphqlEdges<AddressTemplate>(ctx, ADDRESS_TEMPLATES_QUERY, "address_templates"),
    enabled: Boolean(ctx.token),
  });
}

// --- Parcel templates (GraphQL) ----------------------------------------------
const PARCEL_TEMPLATES_QUERY = `query { parcel_templates { edges { node {
  id label is_default packaging_type width height length dimension_unit weight weight_unit
} } } }`;

export function useParcels() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["parcel-templates", keyExtra(ctx)],
    queryFn: () => graphqlEdges<ParcelTemplate>(ctx, PARCEL_TEMPLATES_QUERY, "parcel_templates"),
    enabled: Boolean(ctx.token),
  });
}

// --- Product templates / commodities (GraphQL) -------------------------------
const PRODUCTS_QUERY = `query { products { edges { node {
  id label title sku hs_code weight weight_unit value_amount value_currency origin_country is_default
} } } }`;

export function useProducts() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["products", keyExtra(ctx)],
    queryFn: () => graphqlEdges<ProductTemplate>(ctx, PRODUCTS_QUERY, "products"),
    enabled: Boolean(ctx.token),
  });
}

// --- Shipping rules (GraphQL) ------------------------------------------------
const SHIPPING_RULES_QUERY = `query { shipping_rules { edges { node {
  id name priority is_active description action_type
} } } }`;

export function useShippingRules() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["shipping-rules", keyExtra(ctx)],
    queryFn: () => graphqlEdges<ShippingRule>(ctx, SHIPPING_RULES_QUERY, "shipping_rules"),
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

// Address template create/update/delete (GraphQL; mutation shapes provisional
// pending live-schema validation — intercepted in tests).
const CREATE_ADDRESS = `mutation($data: PartialAddressMutationInput!) {
  create_address_template(input: { label: $data.label, is_default: $data.is_default, address: $data.address }) {
    template { id } errors { field messages }
  }
}`;
const UPDATE_ADDRESS = `mutation($id: String!, $data: PartialAddressMutationInput!) {
  update_address_template(input: { id: $id, label: $data.label, address: $data.address }) {
    template { id } errors { field messages }
  }
}`;
const DELETE_ADDRESS = `mutation($id: String!) { delete_template(input: { id: $id }) { id } }`;

export function useSaveAddress() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: { id?: string; data: Record<string, unknown> }) =>
      graphql(ctx, vars.id ? UPDATE_ADDRESS : CREATE_ADDRESS, vars.id ? { id: vars.id, data: vars.data } : { data: vars.data }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["address-templates"] }),
  });
}

export function useDeleteAddress() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => graphql(ctx, DELETE_ADDRESS, { id }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["address-templates"] }),
  });
}

// Parcel template create/update/delete (provisional GraphQL shapes; intercepted
// in tests). Mirrors the address mutation pattern.
const CREATE_PARCEL = `mutation($data: PartialParcelMutationInput!) {
  create_parcel_template(input: { label: $data.label, is_default: $data.is_default, parcel: $data.parcel }) {
    template { id } errors { field messages }
  }
}`;
const UPDATE_PARCEL = `mutation($id: String!, $data: PartialParcelMutationInput!) {
  update_parcel_template(input: { id: $id, label: $data.label, parcel: $data.parcel }) {
    template { id } errors { field messages }
  }
}`;
const DELETE_TEMPLATE = `mutation($id: String!) { delete_template(input: { id: $id }) { id } }`;

export function useSaveParcel() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: { id?: string; data: Record<string, unknown> }) =>
      graphql(ctx, vars.id ? UPDATE_PARCEL : CREATE_PARCEL, vars.id ? { id: vars.id, data: vars.data } : { data: vars.data }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["parcel-templates"] }),
  });
}

export function useDeleteParcel() {
  const ctx = useKarrioCtx();
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => graphql(ctx, DELETE_TEMPLATE, { id }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["parcel-templates"] }),
  });
}
