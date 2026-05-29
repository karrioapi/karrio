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
  postal_code?: string;
  residential?: boolean;
};

export type Shipment = {
  id: string;
  status: string;
  carrier_name?: string;
  carrier_id?: string;
  tracking_number?: string;
  service?: string;
  selected_rate?: { total_charge?: number; currency?: string } | null;
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

export type AddressTemplate = {
  id: string;
  label?: string;
  is_default?: boolean;
  address?: Address & { email?: string; phone_number?: string; address_line1?: string };
};

export type ParcelTemplate = {
  id: string;
  label?: string;
  is_default?: boolean;
  packaging_type?: string;
  width?: number;
  height?: number;
  length?: number;
  dimension_unit?: string;
  weight?: number;
  weight_unit?: string;
};

export type ProductTemplate = {
  id: string;
  label?: string;
  title?: string;
  sku?: string;
  hs_code?: string;
  weight?: number;
  weight_unit?: string;
  value_amount?: number;
  value_currency?: string;
  origin_country?: string;
  is_default?: boolean;
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
