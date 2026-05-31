// types.ts — local Karrio API types (decoupled; no @karrio/types dependency).
// Only the fields Studio screens consume are modeled; extend as screens grow.

export type Paginated<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export type Address = {
  city?: string;
  state_code?: string;
  country_code?: string;
  person_name?: string;
  company_name?: string;
  address_line1?: string;
  address_line2?: string;
  postal_code?: string;
  email?: string;
  phone_number?: string;
  residential?: boolean;
};

export type Charge = { name?: string; amount?: number; currency?: string };

export type Parcel = {
  id?: string;
  weight?: number;
  weight_unit?: string;
  width?: number;
  height?: number;
  length?: number;
  dimension_unit?: string;
  packaging_type?: string;
  reference_number?: string;
};

export type Rate = {
  carrier_name?: string;
  carrier_id?: string;
  service?: string;
  total_charge?: number;
  currency?: string;
  transit_days?: number;
  extra_charges?: Charge[];
};

export type Shipment = {
  id: string;
  status: string;
  carrier_name?: string;
  carrier_id?: string;
  tracking_number?: string;
  service?: string;
  selected_rate?: Rate | null;
  parcels?: Parcel[];
  recipient?: Address;
  shipper?: Address;
  reference?: string;
  created_at?: string;
  meta?: Record<string, unknown>;
};

export type Tracker = {
  id: string;
  tracking_number: string;
  carrier_name?: string;
  status: string;
  estimated_delivery?: string;
  events?: Array<{ description?: string; location?: string; date?: string; time?: string }>;
  meta?: Record<string, unknown>;
};

export type Order = {
  id: string;
  order_id?: string;
  status: string;
  source?: string;
  created_at?: string;
  line_items?: Array<{ id: string; title?: string; quantity?: number }>;
  shipping_to?: Address;
};

export type CarrierConnection = {
  id: string;
  carrier_name: string;
  carrier_id: string;
  test_mode?: boolean;
  active?: boolean;
  capabilities?: string[];
};

export type Pickup = {
  id: string;
  confirmation_number?: string;
  carrier_name?: string;
  pickup_date?: string;
  ready_time?: string;
  closing_time?: string;
  status?: string;
  address?: Address;
};

// AddressTemplate: live schema exposes the Address model directly via the
// `addresses` Connection. Fields are flat on the node; label/is_default live
// in the `meta` JSON field. The hook normalises meta into top-level `label`,
// `is_default`, and an `address` sub-object for screen backward-compat.
export type AddressTemplate = {
  id: string;
  /** Populated by hook from meta.label */
  label?: string;
  /** Populated by hook from meta.is_default */
  is_default?: boolean;
  /** Raw meta from the API (contains label, is_default, …) */
  meta?: { label?: string; is_default?: boolean; [key: string]: unknown };
  /** Nested address fields (normalised by hook from flat wire fields) */
  address?: Address;
  // Also exposed flat for direct access:
  person_name?: string;
  company_name?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state_code?: string;
  postal_code?: string;
  country_code?: string;
  email?: string;
  phone_number?: string;
  residential?: boolean;
};

// ParcelTemplate: live schema exposes the Parcel model directly via the
// `parcels` Connection. Fields are flat; label/is_default live in `meta`.
// The hook normalises meta into top-level `label` and `is_default`.
export type ParcelTemplate = {
  id: string;
  /** Populated by hook from meta.label */
  label?: string;
  /** Populated by hook from meta.is_default */
  is_default?: boolean;
  /** Raw meta from the API */
  meta?: { label?: string; is_default?: boolean; [key: string]: unknown };
  packaging_type?: string;
  width?: number;
  height?: number;
  length?: number;
  dimension_unit?: string;
  weight?: number;
  weight_unit?: string;
};

// ProductTemplate: live schema exposes the Commodity model via the `products`
// Connection. label/is_default live in `meta`. The hook normalises them.
export type ProductTemplate = {
  id: string;
  /** Populated by hook from meta.label */
  label?: string;
  /** Populated by hook from meta.is_default */
  is_default?: boolean;
  /** Raw meta from the API */
  meta?: { label?: string; is_default?: boolean; [key: string]: unknown };
  title?: string;
  sku?: string;
  hs_code?: string;
  weight?: number;
  weight_unit?: string;
  value_amount?: number;
  value_currency?: string;
  origin_country?: string;
};

export type ShippingRule = {
  id: string;
  name: string;
  priority?: number;
  is_active?: boolean;
  description?: string;
  action_type?: string;
};

export type DocumentTemplate = {
  id: string;
  name: string;
  slug?: string;
  related_object?: string;
  description?: string;
  active?: boolean;
};

export type App = {
  id: string;
  name: string;
  vendor?: string;
  description?: string;
  installed?: boolean;
  status?: string;
  category?: string;
  badge?: string;
};

export type Plugin = {
  id: string;
  name: string;
  vendor?: string;
  description?: string;
  installed?: boolean;
  status?: string;
  version?: string;
  tags?: string[];
  badge?: string;
};

export type Webhook = {
  id: string;
  url: string;
  description?: string;
  enabled?: boolean;
  events?: string[];
};

export type ApiKey = {
  id: string;
  label?: string;
  key: string;
  test_mode?: boolean;
  created?: string;
};

export type McpTool = { name: string; description?: string; requests?: number; p99?: string };
export type McpClient = { id: string; name: string; connected?: boolean; last_seen?: string; calls?: number };
export type McpInvocation = { id: string; tool: string; client?: string; duration_ms?: number; at?: string };
export type McpInfo = {
  status?: string;
  url?: string;
  version?: string;
  stats?: { tools?: number; clients?: number; calls_24h?: string; p99?: string };
  tools?: McpTool[];
  clients?: McpClient[];
  invocations?: McpInvocation[];
};

export type Tenant = {
  id: string;
  name: string;
  slug?: string;
  status?: string;
  members?: number;
  created?: string;
};

export type TeamMember = {
  id: string;
  name?: string;
  email: string;
  role?: string;
  status?: string;
};

export type AuditEvent = {
  id: string;
  type?: string;
  actor?: string;
  description?: string;
  at?: string;
};

export type AdminInfo = {
  version?: string;
  tenants?: number;
  license?: string;
  resources?: { label: string; used: number; total: number }[];
  runtimes?: { name: string; memory?: string; calls?: number; p99?: string }[];
};

// --- Parity resources (manifests, batches, workflows, rate sheets, usage) ----
export type Manifest = {
  id: string;
  carrier_name?: string;
  reference?: string;
  shipment_count?: number;
  created_at?: string;
  manifest_url?: string;
};

export type BatchOperation = {
  id: string;
  status?: string;
  resource_type?: string;
  total?: number;
  created_at?: string;
};

export type Workflow = {
  id: string;
  name: string;
  description?: string;
  is_active?: boolean;
  trigger?: string;
  action_count?: number;
};

// RateSheet: live OSS schema fields are id, name, slug, carrier_name.
// `services_count` and `is_system` do not exist on the OSS RateSheetType and
// will always be undefined when fetched from OSS; screens degrade gracefully.
export type RateSheet = {
  id: string;
  name: string;
  slug?: string;
  carrier_name?: string;
  /** OSS: always undefined — not exposed by the OSS GraphQL schema */
  services_count?: number;
  /** OSS: always undefined — not exposed by the OSS GraphQL schema */
  is_system?: boolean;
};

export type UsageRecord = {
  label: string;
  value: string;
  delta?: string;
};

export type UsagePoint = { date: string; count: number };
export type UsageSeries = {
  key: string;
  label: string;
  format?: "number" | "currency";
  points: UsagePoint[];
};
export type UsageSummary = {
  plan?: string;
  period?: string;
  metrics?: UsageRecord[];
  series?: UsageSeries[];
};
