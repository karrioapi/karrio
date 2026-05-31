// hooks/resources.ts — GraphQL resource reads (orders + saved templates) and
// ALL write mutations. UNIT E aligns field selections to the dashboard GET_*
// queries and keeps mutations on GraphQL. See STUDIO_GRAPHQL_REBUILD.md.
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { graphql, restMutate } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import { graphqlEdges, keyExtra } from "~/lib/karrio/hooks/_shared";
import type {
  AddressTemplate,
  Order,
  ParcelTemplate,
  ProductTemplate,
  RateSheet,
  ShippingRule,
  Workflow,
} from "~/lib/karrio/types";

// === Orders (GraphQL) =======================================================
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

// === Address templates (GraphQL) ============================================
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

// === Parcel templates (GraphQL) =============================================
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

// === Product templates / commodities (GraphQL) ==============================
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

// === Shipping rules (GraphQL, EE-only → graceful []) ========================
const SHIPPING_RULES_QUERY = `query { shipping_rules { edges { node {
  id name priority is_active description action_type
} } } }`;

export function useShippingRules() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["shipping-rules", keyExtra(ctx)],
    queryFn: async (): Promise<ShippingRule[]> => {
      try {
        return await graphqlEdges<ShippingRule>(ctx, SHIPPING_RULES_QUERY, "shipping_rules");
      } catch {
        return [];
      }
    },
    enabled: Boolean(ctx.token),
  });
}

// === Workflows (GraphQL, EE-only → graceful []) =============================
const WORKFLOWS_QUERY = `query { workflows { edges { node {
  id name description is_active trigger action_count
} } } }`;

export function useWorkflows() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["workflows", keyExtra(ctx)],
    queryFn: async (): Promise<Workflow[]> => {
      try {
        return await graphqlEdges<Workflow>(ctx, WORKFLOWS_QUERY, "workflows");
      } catch {
        return [];
      }
    },
    enabled: Boolean(ctx.token),
  });
}

// === Rate sheets (GraphQL) ==================================================
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

// === Mutations: address / parcel / product (GraphQL) ========================
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

// === Mutations: webhooks / connections (REST today; UNIT E may move to GQL) ==
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
