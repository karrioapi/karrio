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
