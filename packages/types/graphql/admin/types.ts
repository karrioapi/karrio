

/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_system_usage
// ====================================================

export interface get_system_usage_system_usage_api_errors {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface get_system_usage_system_usage_api_requests {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface get_system_usage_system_usage_order_volumes {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface get_system_usage_system_usage_shipments {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface get_system_usage_system_usage_shipment_spend {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface get_system_usage_system_usage {
  total_errors: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_shipments: number | null;
  organization_count: number | null;
  api_errors: get_system_usage_system_usage_api_errors[];
  api_requests: get_system_usage_system_usage_api_requests[];
  order_volumes: get_system_usage_system_usage_order_volumes[];
  shipments: get_system_usage_system_usage_shipments[];
  shipment_spend: get_system_usage_system_usage_shipment_spend[];
}

export interface get_system_usage {
  system_usage: get_system_usage_system_usage;
}

/* tslint:disable */
// This file was automatically generated and should not be edited.

//==============================================================
// START Enums and Input Objects
//==============================================================

//==============================================================
// END Enums and Input Objects
//==============================================================