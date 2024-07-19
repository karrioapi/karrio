

/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSystemUsage
// ====================================================

export interface GetSystemUsage_system_usage_api_errors {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetSystemUsage_system_usage_api_requests {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetSystemUsage_system_usage_order_volumes {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetSystemUsage_system_usage_shipment_count {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetSystemUsage_system_usage_tracker_count {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetSystemUsage_system_usage_shipping_spend {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetSystemUsage_system_usage {
  total_errors: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  organization_count: number | null;
  total_shipping_spend: number | null;
  api_errors: GetSystemUsage_system_usage_api_errors[] | null;
  api_requests: GetSystemUsage_system_usage_api_requests[] | null;
  order_volumes: GetSystemUsage_system_usage_order_volumes[] | null;
  shipment_count: GetSystemUsage_system_usage_shipment_count[] | null;
  tracker_count: GetSystemUsage_system_usage_tracker_count[] | null;
  shipping_spend: GetSystemUsage_system_usage_shipping_spend[] | null;
}

export interface GetSystemUsage {
  system_usage: GetSystemUsage_system_usage;
}

export interface GetSystemUsageVariables {
  filter?: UsageFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetAccounts
// ====================================================

export interface GetAccounts_accounts_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetAccounts_accounts_edges_node_usage_api_errors {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetAccounts_accounts_edges_node_usage_api_requests {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetAccounts_accounts_edges_node_usage_order_volumes {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetAccounts_accounts_edges_node_usage_shipment_count {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetAccounts_accounts_edges_node_usage_tracker_count {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetAccounts_accounts_edges_node_usage_shipping_spend {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface GetAccounts_accounts_edges_node_usage {
  members: number | null;
  order_volume: number | null;
  total_errors: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  total_shipping_spend: number | null;
  api_errors: GetAccounts_accounts_edges_node_usage_api_errors[] | null;
  api_requests: GetAccounts_accounts_edges_node_usage_api_requests[] | null;
  order_volumes: GetAccounts_accounts_edges_node_usage_order_volumes[] | null;
  shipment_count: GetAccounts_accounts_edges_node_usage_shipment_count[] | null;
  tracker_count: GetAccounts_accounts_edges_node_usage_tracker_count[] | null;
  shipping_spend: GetAccounts_accounts_edges_node_usage_shipping_spend[] | null;
}

export interface GetAccounts_accounts_edges_node {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  created: any;
  modified: any;
  usage: GetAccounts_accounts_edges_node_usage;
}

export interface GetAccounts_accounts_edges {
  node: GetAccounts_accounts_edges_node;
}

export interface GetAccounts_accounts {
  page_info: GetAccounts_accounts_page_info;
  edges: GetAccounts_accounts_edges[];
}

export interface GetAccounts {
  accounts: GetAccounts_accounts;
}

export interface GetAccountsVariables {
  filter?: AccountFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetUsers
// ====================================================

export interface GetUsers_users_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetUsers_users_edges_node {
  id: number;
  email: string;
  full_name: string;
  is_staff: boolean;
  is_active: boolean;
  is_superuser: boolean | null;
  date_joined: any;
  last_login: any | null;
  permissions: string[] | null;
}

export interface GetUsers_users_edges {
  node: GetUsers_users_edges_node;
}

export interface GetUsers_users {
  page_info: GetUsers_users_page_info;
  edges: GetUsers_users_edges[];
}

export interface GetUsers {
  users: GetUsers_users;
}

export interface GetUsersVariables {
  filter?: UserFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSurcharges
// ====================================================

export interface GetSurcharges_surcharges_carrier_accounts {
  id: string;
  active: boolean;
  carrier_id: string;
  test_mode: boolean;
  capabilities: string[];
  carrier_name: string;
  display_name: string;
}

export interface GetSurcharges_surcharges {
  object_type: string;
  id: string;
  name: string;
  active: boolean;
  amount: number;
  carriers: string[];
  services: string[];
  surcharge_type: string;
  carrier_accounts: GetSurcharges_surcharges_carrier_accounts[];
}

export interface GetSurcharges {
  surcharges: GetSurcharges_surcharges[];
}

export interface GetSurchargesVariables {
  filter?: SurchargeFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSurcharge
// ====================================================

export interface GetSurcharge_surcharge_carrier_accounts {
  id: string;
  active: boolean;
  carrier_id: string;
  test_mode: boolean;
  capabilities: string[];
  carrier_name: string;
  display_name: string;
}

export interface GetSurcharge_surcharge {
  object_type: string;
  id: string;
  name: string;
  active: boolean;
  amount: number;
  carriers: string[];
  services: string[];
  surcharge_type: string;
  carrier_accounts: GetSurcharge_surcharge_carrier_accounts[];
}

export interface GetSurcharge {
  surcharge: GetSurcharge_surcharge | null;
}

export interface GetSurchargeVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSystemConnections
// ====================================================

export interface GetSystemConnections_system_connections_AlliedExpressSettingsType {
  __typename: "AlliedExpressSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  username: string | null;
  password: string | null;
  account: string | null;
  service_type: string | null;
}

export interface GetSystemConnections_system_connections_AlliedExpressLocalSettingsType {
  __typename: "AlliedExpressLocalSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  username: string | null;
  password: string | null;
  account: string | null;
  service_type: string | null;
}

export interface GetSystemConnections_system_connections_AmazonShippingSettingsType {
  __typename: "AmazonShippingSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  seller_id: string | null;
  developer_id: string | null;
  mws_auth_token: string | null;
  aws_region: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_AramexSettingsType {
  __typename: "AramexSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  username: string | null;
  password: string | null;
  account_pin: string | null;
  account_entity: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_AsendiaUSSettingsType {
  __typename: "AsendiaUSSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  username: string | null;
  password: string | null;
  account_number: string | null;
  api_key: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_AustraliaPostSettingsType {
  __typename: "AustraliaPostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  api_key: string | null;
  password: string | null;
  account_number: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_BoxKnightSettingsType {
  __typename: "BoxKnightSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  username: string | null;
  password: string | null;
  config: any | null;
  metadata: any | null;
}

export interface GetSystemConnections_system_connections_BelgianPostSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnections_system_connections_BelgianPostSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnections_system_connections_BelgianPostSettingsType_services_zones[];
}

export interface GetSystemConnections_system_connections_BelgianPostSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnections_system_connections_BelgianPostSettingsType {
  __typename: "BelgianPostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  account_id: string | null;
  passphrase: string | null;
  services: GetSystemConnections_system_connections_BelgianPostSettingsType_services[] | null;
  rate_sheet: GetSystemConnections_system_connections_BelgianPostSettingsType_rate_sheet | null;
}

export interface GetSystemConnections_system_connections_CanadaPostSettingsType {
  __typename: "CanadaPostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  username: string | null;
  password: string | null;
  customer_number: string | null;
  contract_id: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_CanparSettingsType {
  __typename: "CanparSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_ChronopostSettingsType {
  __typename: "ChronopostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  password: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_ColissimoSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnections_system_connections_ColissimoSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnections_system_connections_ColissimoSettingsType_services_zones[];
}

export interface GetSystemConnections_system_connections_ColissimoSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnections_system_connections_ColissimoSettingsType {
  __typename: "ColissimoSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  password: string | null;
  contract_number: string | null;
  laposte_api_key: string | null;
  services: GetSystemConnections_system_connections_ColissimoSettingsType_services[] | null;
  rate_sheet: GetSystemConnections_system_connections_ColissimoSettingsType_rate_sheet | null;
}

export interface GetSystemConnections_system_connections_DHLParcelDESettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnections_system_connections_DHLParcelDESettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnections_system_connections_DHLParcelDESettingsType_services_zones[];
}

export interface GetSystemConnections_system_connections_DHLParcelDESettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnections_system_connections_DHLParcelDESettingsType {
  __typename: "DHLParcelDESettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  customer_number: string | null;
  dhl_api_key: string | null;
  tracking_consumer_key: string | null;
  tracking_consumer_secret: string | null;
  config: any | null;
  services: GetSystemConnections_system_connections_DHLParcelDESettingsType_services[] | null;
  rate_sheet: GetSystemConnections_system_connections_DHLParcelDESettingsType_rate_sheet | null;
}

export interface GetSystemConnections_system_connections_DHLExpressSettingsType {
  __typename: "DHLExpressSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  site_id: string | null;
  password: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_DHLPolandSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnections_system_connections_DHLPolandSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnections_system_connections_DHLPolandSettingsType_services_zones[];
}

export interface GetSystemConnections_system_connections_DHLPolandSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnections_system_connections_DHLPolandSettingsType {
  __typename: "DHLPolandSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  username: string | null;
  password: string | null;
  account_number: string | null;
  services: GetSystemConnections_system_connections_DHLPolandSettingsType_services[] | null;
  rate_sheet: GetSystemConnections_system_connections_DHLPolandSettingsType_rate_sheet | null;
}

export interface GetSystemConnections_system_connections_DHLUniversalSettingsType {
  __typename: "DHLUniversalSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  consumer_key: string | null;
  consumer_secret: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_DicomSettingsType {
  __typename: "DicomSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  billing_account: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_DPDSettingsType_services_zones {
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
  label: string | null;
  latitude: number | null;
  longitude: number | null;
  max_weight: number | null;
  min_weight: number | null;
  radius: number | null;
  rate: number | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface GetSystemConnections_system_connections_DPDSettingsType_services {
  active: boolean | null;
  currency: CurrencyCodeEnum | null;
  description: string | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  id: string;
  international: boolean | null;
  max_height: number | null;
  max_length: number | null;
  max_weight: number | null;
  max_width: number | null;
  service_code: string | null;
  service_name: string | null;
  carrier_service_code: string | null;
  transit_days: number | null;
  transit_time: number | null;
  weight_unit: WeightUnitEnum | null;
  zones: GetSystemConnections_system_connections_DPDSettingsType_services_zones[];
}

export interface GetSystemConnections_system_connections_DPDSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnections_system_connections_DPDSettingsType {
  __typename: "DPDSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  config: any | null;
  capabilities: string[];
  delis_id: string | null;
  password: string | null;
  depot: string | null;
  account_country_code: string | null;
  services: GetSystemConnections_system_connections_DPDSettingsType_services[] | null;
  rate_sheet: GetSystemConnections_system_connections_DPDSettingsType_rate_sheet | null;
}

export interface GetSystemConnections_system_connections_DPDHLSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnections_system_connections_DPDHLSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnections_system_connections_DPDHLSettingsType_services_zones[];
}

export interface GetSystemConnections_system_connections_DPDHLSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnections_system_connections_DPDHLSettingsType {
  __typename: "DPDHLSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  app_id: string | null;
  app_token: string | null;
  zt_id: string | null;
  zt_password: string | null;
  account_number: string | null;
  config: any | null;
  services: GetSystemConnections_system_connections_DPDHLSettingsType_services[] | null;
  rate_sheet: GetSystemConnections_system_connections_DPDHLSettingsType_rate_sheet | null;
}

export interface GetSystemConnections_system_connections_EShipperSettingsType {
  __typename: "EShipperSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  principal: string | null;
  credential: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_EasyPostSettingsType {
  __typename: "EasyPostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_FedexSettingsType {
  __typename: "FedexSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  account_number: string | null;
  api_key: string | null;
  secret_key: string | null;
  track_api_key: string | null;
  track_secret_key: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_FedexWSSettingsType {
  __typename: "FedexWSSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  account_number: string | null;
  password: string | null;
  meter_number: string | null;
  user_key: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_FreightcomSettingsType {
  __typename: "FreightcomSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_GenericSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnections_system_connections_GenericSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnections_system_connections_GenericSettingsType_services_zones[];
}

export interface GetSystemConnections_system_connections_GenericSettingsType_label_template {
  id: string;
  slug: string | null;
  template: string | null;
  template_type: LabelTemplateTypeEnum | null;
  shipment_sample: any | null;
  width: number | null;
  height: number | null;
}

export interface GetSystemConnections_system_connections_GenericSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnections_system_connections_GenericSettingsType {
  __typename: "GenericSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  custom_carrier_name: string | null;
  account_number: string | null;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  config: any | null;
  capabilities: string[];
  account_country_code: string | null;
  services: GetSystemConnections_system_connections_GenericSettingsType_services[] | null;
  label_template: GetSystemConnections_system_connections_GenericSettingsType_label_template | null;
  rate_sheet: GetSystemConnections_system_connections_GenericSettingsType_rate_sheet | null;
}

export interface GetSystemConnections_system_connections_GEODISSettingsType {
  __typename: "GEODISSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  identifier: string | null;
  language: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_LaPosteSettingsType {
  __typename: "LaPosteSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  lang: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_Locate2uSettingsType {
  __typename: "Locate2uSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  account_country_code: string | null;
  client_id: string | null;
  client_secret: string | null;
}

export interface GetSystemConnections_system_connections_NationexSettingsType {
  __typename: "NationexSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  customer_id: string | null;
  billing_account: string | null;
  language: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_PurolatorSettingsType {
  __typename: "PurolatorSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  account_number: string | null;
  user_token: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_RoadieSettingsType {
  __typename: "RoadieSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_RoyalMailSettingsType {
  __typename: "RoyalMailSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  client_id: string | null;
  client_secret: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_SendleSettingsType {
  __typename: "SendleSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  sendle_id: string | null;
  api_key: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_TGESettingsType {
  __typename: "TGESettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  config: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  api_key: string | null;
  toll_username: string | null;
  toll_password: string | null;
  my_toll_token: string | null;
  my_toll_identity: string | null;
  account_code: string | null;
}

export interface GetSystemConnections_system_connections_TNTSettingsType {
  __typename: "TNTSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_UPSSettingsType {
  __typename: "UPSSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  client_id: string | null;
  client_secret: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_USPSSettingsType {
  __typename: "USPSSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  mailer_id: string | null;
  customer_registration_id: string | null;
  logistics_manager_mailer_id: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_USPSInternationalSettingsType {
  __typename: "USPSInternationalSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  mailer_id: string | null;
  customer_registration_id: string | null;
  logistics_manager_mailer_id: string | null;
  config: any | null;
}

export interface GetSystemConnections_system_connections_Zoom2uSettingsType {
  __typename: "Zoom2uSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  account_country_code: string | null;
  api_key: string | null;
}

export type GetSystemConnections_system_connections = GetSystemConnections_system_connections_AlliedExpressSettingsType | GetSystemConnections_system_connections_AlliedExpressLocalSettingsType | GetSystemConnections_system_connections_AmazonShippingSettingsType | GetSystemConnections_system_connections_AramexSettingsType | GetSystemConnections_system_connections_AsendiaUSSettingsType | GetSystemConnections_system_connections_AustraliaPostSettingsType | GetSystemConnections_system_connections_BoxKnightSettingsType | GetSystemConnections_system_connections_BelgianPostSettingsType | GetSystemConnections_system_connections_CanadaPostSettingsType | GetSystemConnections_system_connections_CanparSettingsType | GetSystemConnections_system_connections_ChronopostSettingsType | GetSystemConnections_system_connections_ColissimoSettingsType | GetSystemConnections_system_connections_DHLParcelDESettingsType | GetSystemConnections_system_connections_DHLExpressSettingsType | GetSystemConnections_system_connections_DHLPolandSettingsType | GetSystemConnections_system_connections_DHLUniversalSettingsType | GetSystemConnections_system_connections_DicomSettingsType | GetSystemConnections_system_connections_DPDSettingsType | GetSystemConnections_system_connections_DPDHLSettingsType | GetSystemConnections_system_connections_EShipperSettingsType | GetSystemConnections_system_connections_EasyPostSettingsType | GetSystemConnections_system_connections_FedexSettingsType | GetSystemConnections_system_connections_FedexWSSettingsType | GetSystemConnections_system_connections_FreightcomSettingsType | GetSystemConnections_system_connections_GenericSettingsType | GetSystemConnections_system_connections_GEODISSettingsType | GetSystemConnections_system_connections_LaPosteSettingsType | GetSystemConnections_system_connections_Locate2uSettingsType | GetSystemConnections_system_connections_NationexSettingsType | GetSystemConnections_system_connections_PurolatorSettingsType | GetSystemConnections_system_connections_RoadieSettingsType | GetSystemConnections_system_connections_RoyalMailSettingsType | GetSystemConnections_system_connections_SendleSettingsType | GetSystemConnections_system_connections_TGESettingsType | GetSystemConnections_system_connections_TNTSettingsType | GetSystemConnections_system_connections_UPSSettingsType | GetSystemConnections_system_connections_USPSSettingsType | GetSystemConnections_system_connections_USPSInternationalSettingsType | GetSystemConnections_system_connections_Zoom2uSettingsType;

export interface GetSystemConnections {
  system_connections: GetSystemConnections_system_connections[];
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSystemConnection
// ====================================================

export interface GetSystemConnection_system_connection_AlliedExpressSettingsType {
  __typename: "AlliedExpressSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  username: string | null;
  password: string | null;
  account: string | null;
  service_type: string | null;
}

export interface GetSystemConnection_system_connection_AlliedExpressLocalSettingsType {
  __typename: "AlliedExpressLocalSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  username: string | null;
  password: string | null;
  account: string | null;
  service_type: string | null;
}

export interface GetSystemConnection_system_connection_AmazonShippingSettingsType {
  __typename: "AmazonShippingSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  seller_id: string | null;
  developer_id: string | null;
  mws_auth_token: string | null;
  aws_region: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_AramexSettingsType {
  __typename: "AramexSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  username: string | null;
  password: string | null;
  account_pin: string | null;
  account_entity: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_AsendiaUSSettingsType {
  __typename: "AsendiaUSSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  username: string | null;
  password: string | null;
  account_number: string | null;
  api_key: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_AustraliaPostSettingsType {
  __typename: "AustraliaPostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  api_key: string | null;
  password: string | null;
  account_number: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_BoxKnightSettingsType {
  __typename: "BoxKnightSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  username: string | null;
  password: string | null;
  config: any | null;
  metadata: any | null;
}

export interface GetSystemConnection_system_connection_BelgianPostSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnection_system_connection_BelgianPostSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnection_system_connection_BelgianPostSettingsType_services_zones[];
}

export interface GetSystemConnection_system_connection_BelgianPostSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnection_system_connection_BelgianPostSettingsType {
  __typename: "BelgianPostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  account_id: string | null;
  passphrase: string | null;
  services: GetSystemConnection_system_connection_BelgianPostSettingsType_services[] | null;
  rate_sheet: GetSystemConnection_system_connection_BelgianPostSettingsType_rate_sheet | null;
}

export interface GetSystemConnection_system_connection_CanadaPostSettingsType {
  __typename: "CanadaPostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  username: string | null;
  password: string | null;
  customer_number: string | null;
  contract_id: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_CanparSettingsType {
  __typename: "CanparSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_ChronopostSettingsType {
  __typename: "ChronopostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  password: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_ColissimoSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnection_system_connection_ColissimoSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnection_system_connection_ColissimoSettingsType_services_zones[];
}

export interface GetSystemConnection_system_connection_ColissimoSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnection_system_connection_ColissimoSettingsType {
  __typename: "ColissimoSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  password: string | null;
  contract_number: string | null;
  laposte_api_key: string | null;
  services: GetSystemConnection_system_connection_ColissimoSettingsType_services[] | null;
  rate_sheet: GetSystemConnection_system_connection_ColissimoSettingsType_rate_sheet | null;
}

export interface GetSystemConnection_system_connection_DHLParcelDESettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnection_system_connection_DHLParcelDESettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnection_system_connection_DHLParcelDESettingsType_services_zones[];
}

export interface GetSystemConnection_system_connection_DHLParcelDESettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnection_system_connection_DHLParcelDESettingsType {
  __typename: "DHLParcelDESettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  customer_number: string | null;
  dhl_api_key: string | null;
  tracking_consumer_key: string | null;
  tracking_consumer_secret: string | null;
  config: any | null;
  services: GetSystemConnection_system_connection_DHLParcelDESettingsType_services[] | null;
  rate_sheet: GetSystemConnection_system_connection_DHLParcelDESettingsType_rate_sheet | null;
}

export interface GetSystemConnection_system_connection_DHLExpressSettingsType {
  __typename: "DHLExpressSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  site_id: string | null;
  password: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_DHLPolandSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnection_system_connection_DHLPolandSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnection_system_connection_DHLPolandSettingsType_services_zones[];
}

export interface GetSystemConnection_system_connection_DHLPolandSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnection_system_connection_DHLPolandSettingsType {
  __typename: "DHLPolandSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  username: string | null;
  password: string | null;
  account_number: string | null;
  services: GetSystemConnection_system_connection_DHLPolandSettingsType_services[] | null;
  rate_sheet: GetSystemConnection_system_connection_DHLPolandSettingsType_rate_sheet | null;
}

export interface GetSystemConnection_system_connection_DHLUniversalSettingsType {
  __typename: "DHLUniversalSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  consumer_key: string | null;
  consumer_secret: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_DicomSettingsType {
  __typename: "DicomSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  billing_account: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_DPDSettingsType_services_zones {
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
  label: string | null;
  latitude: number | null;
  longitude: number | null;
  max_weight: number | null;
  min_weight: number | null;
  radius: number | null;
  rate: number | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface GetSystemConnection_system_connection_DPDSettingsType_services {
  active: boolean | null;
  currency: CurrencyCodeEnum | null;
  description: string | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  id: string;
  international: boolean | null;
  max_height: number | null;
  max_length: number | null;
  max_weight: number | null;
  max_width: number | null;
  service_code: string | null;
  service_name: string | null;
  carrier_service_code: string | null;
  transit_days: number | null;
  transit_time: number | null;
  weight_unit: WeightUnitEnum | null;
  zones: GetSystemConnection_system_connection_DPDSettingsType_services_zones[];
}

export interface GetSystemConnection_system_connection_DPDSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnection_system_connection_DPDSettingsType {
  __typename: "DPDSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  config: any | null;
  capabilities: string[];
  delis_id: string | null;
  password: string | null;
  depot: string | null;
  account_country_code: string | null;
  services: GetSystemConnection_system_connection_DPDSettingsType_services[] | null;
  rate_sheet: GetSystemConnection_system_connection_DPDSettingsType_rate_sheet | null;
}

export interface GetSystemConnection_system_connection_DPDHLSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnection_system_connection_DPDHLSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnection_system_connection_DPDHLSettingsType_services_zones[];
}

export interface GetSystemConnection_system_connection_DPDHLSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnection_system_connection_DPDHLSettingsType {
  __typename: "DPDHLSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  app_id: string | null;
  app_token: string | null;
  zt_id: string | null;
  zt_password: string | null;
  account_number: string | null;
  config: any | null;
  services: GetSystemConnection_system_connection_DPDHLSettingsType_services[] | null;
  rate_sheet: GetSystemConnection_system_connection_DPDHLSettingsType_rate_sheet | null;
}

export interface GetSystemConnection_system_connection_EShipperSettingsType {
  __typename: "EShipperSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  principal: string | null;
  credential: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_EasyPostSettingsType {
  __typename: "EasyPostSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_FedexSettingsType {
  __typename: "FedexSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  account_number: string | null;
  api_key: string | null;
  secret_key: string | null;
  track_api_key: string | null;
  track_secret_key: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_FedexWSSettingsType {
  __typename: "FedexWSSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  account_number: string | null;
  password: string | null;
  meter_number: string | null;
  user_key: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_FreightcomSettingsType {
  __typename: "FreightcomSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_GenericSettingsType_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
}

export interface GetSystemConnection_system_connection_GenericSettingsType_services {
  id: string;
  active: boolean | null;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_weight: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  weight_unit: WeightUnitEnum | null;
  dimension_unit: DimensionUnitEnum | null;
  domicile: boolean | null;
  international: boolean | null;
  zones: GetSystemConnection_system_connection_GenericSettingsType_services_zones[];
}

export interface GetSystemConnection_system_connection_GenericSettingsType_label_template {
  id: string;
  slug: string | null;
  template: string | null;
  template_type: LabelTemplateTypeEnum | null;
  shipment_sample: any | null;
  width: number | null;
  height: number | null;
}

export interface GetSystemConnection_system_connection_GenericSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnection_system_connection_GenericSettingsType {
  __typename: "GenericSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  custom_carrier_name: string | null;
  account_number: string | null;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  config: any | null;
  capabilities: string[];
  account_country_code: string | null;
  services: GetSystemConnection_system_connection_GenericSettingsType_services[] | null;
  label_template: GetSystemConnection_system_connection_GenericSettingsType_label_template | null;
  rate_sheet: GetSystemConnection_system_connection_GenericSettingsType_rate_sheet | null;
}

export interface GetSystemConnection_system_connection_GEODISSettingsType {
  __typename: "GEODISSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  identifier: string | null;
  language: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_LaPosteSettingsType {
  __typename: "LaPosteSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  lang: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_Locate2uSettingsType {
  __typename: "Locate2uSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  account_country_code: string | null;
  client_id: string | null;
  client_secret: string | null;
}

export interface GetSystemConnection_system_connection_NationexSettingsType {
  __typename: "NationexSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  customer_id: string | null;
  billing_account: string | null;
  language: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_PurolatorSettingsType {
  __typename: "PurolatorSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  account_number: string | null;
  user_token: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_RoadieSettingsType {
  __typename: "RoadieSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  api_key: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_RoyalMailSettingsType {
  __typename: "RoyalMailSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  client_id: string | null;
  client_secret: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_SendleSettingsType {
  __typename: "SendleSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  sendle_id: string | null;
  api_key: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_TGESettingsType {
  __typename: "TGESettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  config: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  api_key: string | null;
  toll_username: string | null;
  toll_password: string | null;
  my_toll_token: string | null;
  my_toll_identity: string | null;
  account_code: string | null;
}

export interface GetSystemConnection_system_connection_TNTSettingsType {
  __typename: "TNTSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_UPSSettingsType {
  __typename: "UPSSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  client_id: string | null;
  client_secret: string | null;
  account_number: string | null;
  account_country_code: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_USPSSettingsType {
  __typename: "USPSSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  mailer_id: string | null;
  customer_registration_id: string | null;
  logistics_manager_mailer_id: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_USPSInternationalSettingsType {
  __typename: "USPSInternationalSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  metadata: any | null;
  capabilities: string[];
  username: string | null;
  password: string | null;
  mailer_id: string | null;
  customer_registration_id: string | null;
  logistics_manager_mailer_id: string | null;
  config: any | null;
}

export interface GetSystemConnection_system_connection_Zoom2uSettingsType {
  __typename: "Zoom2uSettingsType";
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  metadata: any | null;
  config: any | null;
  account_country_code: string | null;
  api_key: string | null;
}

export type GetSystemConnection_system_connection = GetSystemConnection_system_connection_AlliedExpressSettingsType | GetSystemConnection_system_connection_AlliedExpressLocalSettingsType | GetSystemConnection_system_connection_AmazonShippingSettingsType | GetSystemConnection_system_connection_AramexSettingsType | GetSystemConnection_system_connection_AsendiaUSSettingsType | GetSystemConnection_system_connection_AustraliaPostSettingsType | GetSystemConnection_system_connection_BoxKnightSettingsType | GetSystemConnection_system_connection_BelgianPostSettingsType | GetSystemConnection_system_connection_CanadaPostSettingsType | GetSystemConnection_system_connection_CanparSettingsType | GetSystemConnection_system_connection_ChronopostSettingsType | GetSystemConnection_system_connection_ColissimoSettingsType | GetSystemConnection_system_connection_DHLParcelDESettingsType | GetSystemConnection_system_connection_DHLExpressSettingsType | GetSystemConnection_system_connection_DHLPolandSettingsType | GetSystemConnection_system_connection_DHLUniversalSettingsType | GetSystemConnection_system_connection_DicomSettingsType | GetSystemConnection_system_connection_DPDSettingsType | GetSystemConnection_system_connection_DPDHLSettingsType | GetSystemConnection_system_connection_EShipperSettingsType | GetSystemConnection_system_connection_EasyPostSettingsType | GetSystemConnection_system_connection_FedexSettingsType | GetSystemConnection_system_connection_FedexWSSettingsType | GetSystemConnection_system_connection_FreightcomSettingsType | GetSystemConnection_system_connection_GenericSettingsType | GetSystemConnection_system_connection_GEODISSettingsType | GetSystemConnection_system_connection_LaPosteSettingsType | GetSystemConnection_system_connection_Locate2uSettingsType | GetSystemConnection_system_connection_NationexSettingsType | GetSystemConnection_system_connection_PurolatorSettingsType | GetSystemConnection_system_connection_RoadieSettingsType | GetSystemConnection_system_connection_RoyalMailSettingsType | GetSystemConnection_system_connection_SendleSettingsType | GetSystemConnection_system_connection_TGESettingsType | GetSystemConnection_system_connection_TNTSettingsType | GetSystemConnection_system_connection_UPSSettingsType | GetSystemConnection_system_connection_USPSSettingsType | GetSystemConnection_system_connection_USPSInternationalSettingsType | GetSystemConnection_system_connection_Zoom2uSettingsType;

export interface GetSystemConnection {
  system_connection: GetSystemConnection_system_connection | null;
}

export interface GetSystemConnectionVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetRateSheet
// ====================================================

export interface GetRateSheet_rate_sheet_services_zones {
  object_type: string;
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
}

export interface GetRateSheet_rate_sheet_services {
  id: string;
  object_type: string;
  service_name: string | null;
  service_code: string | null;
  description: string | null;
  active: boolean | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  dimension_unit: DimensionUnitEnum | null;
  zones: GetRateSheet_rate_sheet_services_zones[];
}

export interface GetRateSheet_rate_sheet_carriers {
  id: string;
  active: boolean;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  capabilities: string[];
  test_mode: boolean;
}

export interface GetRateSheet_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  services: GetRateSheet_rate_sheet_services[];
  carriers: GetRateSheet_rate_sheet_carriers[];
}

export interface GetRateSheet {
  rate_sheet: GetRateSheet_rate_sheet | null;
}

export interface GetRateSheetVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetRateSheets
// ====================================================

export interface GetRateSheets_rate_sheets_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetRateSheets_rate_sheets_edges_node_services_zones {
  label: string | null;
  rate: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
}

export interface GetRateSheets_rate_sheets_edges_node_services {
  id: string;
  service_name: string | null;
  service_code: string | null;
  description: string | null;
  active: boolean | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  dimension_unit: DimensionUnitEnum | null;
  zones: GetRateSheets_rate_sheets_edges_node_services_zones[];
}

export interface GetRateSheets_rate_sheets_edges_node_carriers {
  id: string;
  active: boolean;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  capabilities: string[];
  test_mode: boolean;
}

export interface GetRateSheets_rate_sheets_edges_node {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  services: GetRateSheets_rate_sheets_edges_node_services[];
  carriers: GetRateSheets_rate_sheets_edges_node_carriers[];
}

export interface GetRateSheets_rate_sheets_edges {
  node: GetRateSheets_rate_sheets_edges_node;
}

export interface GetRateSheets_rate_sheets {
  page_info: GetRateSheets_rate_sheets_page_info;
  edges: GetRateSheets_rate_sheets_edges[];
}

export interface GetRateSheets {
  rate_sheets: GetRateSheets_rate_sheets;
}

export interface GetRateSheetsVariables {
  filter?: RateSheetFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetPermissionGroups
// ====================================================

export interface GetPermissionGroups_permission_groups_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetPermissionGroups_permission_groups_edges_node {
  id: number;
  name: string;
  permissions: string[] | null;
}

export interface GetPermissionGroups_permission_groups_edges {
  node: GetPermissionGroups_permission_groups_edges_node;
}

export interface GetPermissionGroups_permission_groups {
  page_info: GetPermissionGroups_permission_groups_page_info;
  edges: GetPermissionGroups_permission_groups_edges[];
}

export interface GetPermissionGroups {
  permission_groups: GetPermissionGroups_permission_groups;
}

export interface GetPermissionGroupsVariables {
  filter?: PermissionGroupFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateUser
// ====================================================

export interface CreateUser_create_user_errors {
  field: string;
  messages: string[];
}

export interface CreateUser_create_user_user {
  email: string;
  full_name: string;
  is_staff: boolean;
  is_active: boolean;
  is_superuser: boolean | null;
  date_joined: any;
  last_login: any | null;
}

export interface CreateUser_create_user {
  errors: CreateUser_create_user_errors[] | null;
  user: CreateUser_create_user_user | null;
}

export interface CreateUser {
  create_user: CreateUser_create_user;
}

export interface CreateUserVariables {
  data: CreateUserMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateUser
// ====================================================

export interface UpdateUser_update_user_errors {
  field: string;
  messages: string[];
}

export interface UpdateUser_update_user {
  errors: UpdateUser_update_user_errors[] | null;
}

export interface UpdateUser {
  update_user: UpdateUser_update_user;
}

export interface UpdateUserVariables {
  data: UpdateUserMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: RemoveUser
// ====================================================

export interface RemoveUser_remove_user_errors {
  field: string;
  messages: string[];
}

export interface RemoveUser_remove_user {
  id: number;
  errors: RemoveUser_remove_user_errors[] | null;
}

export interface RemoveUser {
  remove_user: RemoveUser_remove_user;
}

export interface RemoveUserVariables {
  data: DeleteUserMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateSurcharge
// ====================================================

export interface CreateSurcharge_create_surcharge_errors {
  field: string;
  messages: string[];
}

export interface CreateSurcharge_create_surcharge {
  errors: CreateSurcharge_create_surcharge_errors[] | null;
}

export interface CreateSurcharge {
  create_surcharge: CreateSurcharge_create_surcharge;
}

export interface CreateSurchargeVariables {
  data: CreateSurchargeMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateSurcharge
// ====================================================

export interface UpdateSurcharge_update_surcharge_errors {
  field: string;
  messages: string[];
}

export interface UpdateSurcharge_update_surcharge {
  errors: UpdateSurcharge_update_surcharge_errors[] | null;
}

export interface UpdateSurcharge {
  update_surcharge: UpdateSurcharge_update_surcharge;
}

export interface UpdateSurchargeVariables {
  data: UpdateSurchargeMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteSurcharge
// ====================================================

export interface DeleteSurcharge_delete_surcharge_errors {
  field: string;
  messages: string[];
}

export interface DeleteSurcharge_delete_surcharge {
  id: string;
  errors: DeleteSurcharge_delete_surcharge_errors[] | null;
}

export interface DeleteSurcharge {
  delete_surcharge: DeleteSurcharge_delete_surcharge;
}

export interface DeleteSurchargeVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateCarrierConnection
// ====================================================

export interface CreateCarrierConnection_create_carrier_connection_errors {
  field: string;
  messages: string[];
}

export interface CreateCarrierConnection_create_carrier_connection {
  errors: CreateCarrierConnection_create_carrier_connection_errors[] | null;
}

export interface CreateCarrierConnection {
  create_carrier_connection: CreateCarrierConnection_create_carrier_connection;
}

export interface CreateCarrierConnectionVariables {
  data: CreateConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateCarrierConnection
// ====================================================

export interface UpdateCarrierConnection_update_carrier_connection_errors {
  field: string;
  messages: string[];
}

export interface UpdateCarrierConnection_update_carrier_connection {
  errors: UpdateCarrierConnection_update_carrier_connection_errors[] | null;
}

export interface UpdateCarrierConnection {
  update_carrier_connection: UpdateCarrierConnection_update_carrier_connection;
}

export interface UpdateCarrierConnectionVariables {
  data: UpdateConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteCarrierConnection
// ====================================================

export interface DeleteCarrierConnection_delete_carrier_connection_errors {
  field: string;
  messages: string[];
}

export interface DeleteCarrierConnection_delete_carrier_connection {
  id: string;
  errors: DeleteCarrierConnection_delete_carrier_connection_errors[] | null;
}

export interface DeleteCarrierConnection {
  delete_carrier_connection: DeleteCarrierConnection_delete_carrier_connection;
}

export interface DeleteCarrierConnectionVariables {
  data: DeleteConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateOrganizationAccount
// ====================================================

export interface UpdateOrganizationAccount_update_organization_account_errors {
  field: string;
  messages: string[];
}

export interface UpdateOrganizationAccount_update_organization_account {
  errors: UpdateOrganizationAccount_update_organization_account_errors[] | null;
}

export interface UpdateOrganizationAccount {
  update_organization_account: UpdateOrganizationAccount_update_organization_account;
}

export interface UpdateOrganizationAccountVariables {
  data: UpdateOrganizationAccountMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateRateSheet
// ====================================================

export interface CreateRateSheet_create_rate_sheet_rate_sheet {
  id: string;
}

export interface CreateRateSheet_create_rate_sheet_errors {
  field: string;
  messages: string[];
}

export interface CreateRateSheet_create_rate_sheet {
  rate_sheet: CreateRateSheet_create_rate_sheet_rate_sheet | null;
  errors: CreateRateSheet_create_rate_sheet_errors[] | null;
}

export interface CreateRateSheet {
  create_rate_sheet: CreateRateSheet_create_rate_sheet;
}

export interface CreateRateSheetVariables {
  data: CreateRateSheetMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateRateSheet
// ====================================================

export interface UpdateRateSheet_update_rate_sheet_rate_sheet {
  id: string;
}

export interface UpdateRateSheet_update_rate_sheet_errors {
  field: string;
  messages: string[];
}

export interface UpdateRateSheet_update_rate_sheet {
  rate_sheet: UpdateRateSheet_update_rate_sheet_rate_sheet | null;
  errors: UpdateRateSheet_update_rate_sheet_errors[] | null;
}

export interface UpdateRateSheet {
  update_rate_sheet: UpdateRateSheet_update_rate_sheet;
}

export interface UpdateRateSheetVariables {
  data: UpdateRateSheetMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteRateSheet
// ====================================================

export interface DeleteRateSheet_delete_rate_sheet_errors {
  field: string;
  messages: string[];
}

export interface DeleteRateSheet_delete_rate_sheet {
  id: string;
  errors: DeleteRateSheet_delete_rate_sheet_errors[] | null;
}

export interface DeleteRateSheet {
  delete_rate_sheet: DeleteRateSheet_delete_rate_sheet;
}

export interface DeleteRateSheetVariables {
  data: DeleteMutationInput;
}

/* tslint:disable */
// This file was automatically generated and should not be edited.

//==============================================================
// START Enums and Input Objects
//==============================================================

export enum SurchargeTypeEnum {
  AMOUNT = "AMOUNT",
  PERCENTAGE = "PERCENTAGE",
}

export enum CurrencyCodeEnum {
  AED = "AED",
  AMD = "AMD",
  ANG = "ANG",
  AOA = "AOA",
  ARS = "ARS",
  AUD = "AUD",
  AWG = "AWG",
  AZN = "AZN",
  BAM = "BAM",
  BBD = "BBD",
  BDT = "BDT",
  BGN = "BGN",
  BHD = "BHD",
  BIF = "BIF",
  BMD = "BMD",
  BND = "BND",
  BOB = "BOB",
  BRL = "BRL",
  BSD = "BSD",
  BTN = "BTN",
  BWP = "BWP",
  BYN = "BYN",
  BZD = "BZD",
  CAD = "CAD",
  CDF = "CDF",
  CHF = "CHF",
  CLP = "CLP",
  CNY = "CNY",
  COP = "COP",
  CRC = "CRC",
  CUC = "CUC",
  CVE = "CVE",
  CZK = "CZK",
  DJF = "DJF",
  DKK = "DKK",
  DOP = "DOP",
  DZD = "DZD",
  EGP = "EGP",
  ERN = "ERN",
  ETB = "ETB",
  EUR = "EUR",
  FJD = "FJD",
  GBP = "GBP",
  GEL = "GEL",
  GHS = "GHS",
  GMD = "GMD",
  GNF = "GNF",
  GTQ = "GTQ",
  GYD = "GYD",
  HKD = "HKD",
  HNL = "HNL",
  HRK = "HRK",
  HTG = "HTG",
  HUF = "HUF",
  IDR = "IDR",
  ILS = "ILS",
  INR = "INR",
  IRR = "IRR",
  ISK = "ISK",
  JMD = "JMD",
  JOD = "JOD",
  JPY = "JPY",
  KES = "KES",
  KGS = "KGS",
  KHR = "KHR",
  KMF = "KMF",
  KPW = "KPW",
  KRW = "KRW",
  KWD = "KWD",
  KYD = "KYD",
  KZT = "KZT",
  LAK = "LAK",
  LKR = "LKR",
  LRD = "LRD",
  LSL = "LSL",
  LYD = "LYD",
  MAD = "MAD",
  MDL = "MDL",
  MGA = "MGA",
  MKD = "MKD",
  MMK = "MMK",
  MNT = "MNT",
  MOP = "MOP",
  MRO = "MRO",
  MUR = "MUR",
  MVR = "MVR",
  MWK = "MWK",
  MXN = "MXN",
  MYR = "MYR",
  MZN = "MZN",
  NAD = "NAD",
  NGN = "NGN",
  NIO = "NIO",
  NOK = "NOK",
  NPR = "NPR",
  NZD = "NZD",
  OMR = "OMR",
  PEN = "PEN",
  PGK = "PGK",
  PHP = "PHP",
  PKR = "PKR",
  PLN = "PLN",
  PYG = "PYG",
  QAR = "QAR",
  RSD = "RSD",
  RUB = "RUB",
  RWF = "RWF",
  SAR = "SAR",
  SBD = "SBD",
  SCR = "SCR",
  SDG = "SDG",
  SEK = "SEK",
  SGD = "SGD",
  SHP = "SHP",
  SLL = "SLL",
  SOS = "SOS",
  SRD = "SRD",
  SSP = "SSP",
  STD = "STD",
  SYP = "SYP",
  SZL = "SZL",
  THB = "THB",
  TJS = "TJS",
  TND = "TND",
  TOP = "TOP",
  TRY = "TRY",
  TTD = "TTD",
  TWD = "TWD",
  TZS = "TZS",
  UAH = "UAH",
  USD = "USD",
  UYU = "UYU",
  UZS = "UZS",
  VEF = "VEF",
  VND = "VND",
  VUV = "VUV",
  WST = "WST",
  XAF = "XAF",
  XCD = "XCD",
  XOF = "XOF",
  XPF = "XPF",
  YER = "YER",
  ZAR = "ZAR",
}

export enum WeightUnitEnum {
  G = "G",
  KG = "KG",
  LB = "LB",
  OZ = "OZ",
}

export enum DimensionUnitEnum {
  CM = "CM",
  IN = "IN",
}

export enum CountryCodeEnum {
  AD = "AD",
  AE = "AE",
  AF = "AF",
  AG = "AG",
  AI = "AI",
  AL = "AL",
  AM = "AM",
  AN = "AN",
  AO = "AO",
  AR = "AR",
  AS = "AS",
  AT = "AT",
  AU = "AU",
  AW = "AW",
  AZ = "AZ",
  BA = "BA",
  BB = "BB",
  BD = "BD",
  BE = "BE",
  BF = "BF",
  BG = "BG",
  BH = "BH",
  BI = "BI",
  BJ = "BJ",
  BM = "BM",
  BN = "BN",
  BO = "BO",
  BR = "BR",
  BS = "BS",
  BT = "BT",
  BW = "BW",
  BY = "BY",
  BZ = "BZ",
  CA = "CA",
  CD = "CD",
  CF = "CF",
  CG = "CG",
  CH = "CH",
  CI = "CI",
  CK = "CK",
  CL = "CL",
  CM = "CM",
  CN = "CN",
  CO = "CO",
  CR = "CR",
  CU = "CU",
  CV = "CV",
  CY = "CY",
  CZ = "CZ",
  DE = "DE",
  DJ = "DJ",
  DK = "DK",
  DM = "DM",
  DO = "DO",
  DZ = "DZ",
  EC = "EC",
  EE = "EE",
  EG = "EG",
  ER = "ER",
  ES = "ES",
  ET = "ET",
  FI = "FI",
  FJ = "FJ",
  FK = "FK",
  FM = "FM",
  FO = "FO",
  FR = "FR",
  GA = "GA",
  GB = "GB",
  GD = "GD",
  GE = "GE",
  GF = "GF",
  GG = "GG",
  GH = "GH",
  GI = "GI",
  GL = "GL",
  GM = "GM",
  GN = "GN",
  GP = "GP",
  GQ = "GQ",
  GR = "GR",
  GT = "GT",
  GU = "GU",
  GW = "GW",
  GY = "GY",
  HK = "HK",
  HN = "HN",
  HR = "HR",
  HT = "HT",
  HU = "HU",
  IC = "IC",
  ID = "ID",
  IE = "IE",
  IL = "IL",
  IN = "IN",
  IQ = "IQ",
  IR = "IR",
  IS = "IS",
  IT = "IT",
  JE = "JE",
  JM = "JM",
  JO = "JO",
  JP = "JP",
  KE = "KE",
  KG = "KG",
  KH = "KH",
  KI = "KI",
  KM = "KM",
  KN = "KN",
  KP = "KP",
  KR = "KR",
  KV = "KV",
  KW = "KW",
  KY = "KY",
  KZ = "KZ",
  LA = "LA",
  LB = "LB",
  LC = "LC",
  LI = "LI",
  LK = "LK",
  LR = "LR",
  LS = "LS",
  LT = "LT",
  LU = "LU",
  LV = "LV",
  LY = "LY",
  MA = "MA",
  MC = "MC",
  MD = "MD",
  ME = "ME",
  MG = "MG",
  MH = "MH",
  MK = "MK",
  ML = "ML",
  MM = "MM",
  MN = "MN",
  MO = "MO",
  MP = "MP",
  MQ = "MQ",
  MR = "MR",
  MS = "MS",
  MT = "MT",
  MU = "MU",
  MV = "MV",
  MW = "MW",
  MX = "MX",
  MY = "MY",
  MZ = "MZ",
  NA = "NA",
  NC = "NC",
  NE = "NE",
  NG = "NG",
  NI = "NI",
  NL = "NL",
  NO = "NO",
  NP = "NP",
  NR = "NR",
  NU = "NU",
  NZ = "NZ",
  OM = "OM",
  PA = "PA",
  PE = "PE",
  PF = "PF",
  PG = "PG",
  PH = "PH",
  PK = "PK",
  PL = "PL",
  PR = "PR",
  PT = "PT",
  PW = "PW",
  PY = "PY",
  QA = "QA",
  RE = "RE",
  RO = "RO",
  RS = "RS",
  RU = "RU",
  RW = "RW",
  SA = "SA",
  SB = "SB",
  SC = "SC",
  SD = "SD",
  SE = "SE",
  SG = "SG",
  SH = "SH",
  SI = "SI",
  SK = "SK",
  SL = "SL",
  SM = "SM",
  SN = "SN",
  SO = "SO",
  SR = "SR",
  SS = "SS",
  ST = "ST",
  SV = "SV",
  SY = "SY",
  SZ = "SZ",
  TC = "TC",
  TD = "TD",
  TG = "TG",
  TH = "TH",
  TJ = "TJ",
  TL = "TL",
  TN = "TN",
  TO = "TO",
  TR = "TR",
  TT = "TT",
  TV = "TV",
  TW = "TW",
  TZ = "TZ",
  UA = "UA",
  UG = "UG",
  US = "US",
  UY = "UY",
  UZ = "UZ",
  VA = "VA",
  VC = "VC",
  VE = "VE",
  VG = "VG",
  VI = "VI",
  VN = "VN",
  VU = "VU",
  WS = "WS",
  XB = "XB",
  XC = "XC",
  XE = "XE",
  XM = "XM",
  XN = "XN",
  XS = "XS",
  XY = "XY",
  YE = "YE",
  YT = "YT",
  ZA = "ZA",
  ZM = "ZM",
  ZW = "ZW",
}

export enum CarrierNameEnum {
  allied_express = "allied_express",
  allied_express_local = "allied_express_local",
  amazon_shipping = "amazon_shipping",
  aramex = "aramex",
  asendia_us = "asendia_us",
  australiapost = "australiapost",
  boxknight = "boxknight",
  bpost = "bpost",
  canadapost = "canadapost",
  canpar = "canpar",
  chronopost = "chronopost",
  colissimo = "colissimo",
  dhl_express = "dhl_express",
  dhl_parcel_de = "dhl_parcel_de",
  dhl_poland = "dhl_poland",
  dhl_universal = "dhl_universal",
  dicom = "dicom",
  dpd = "dpd",
  dpdhl = "dpdhl",
  easypost = "easypost",
  eshipper = "eshipper",
  fedex = "fedex",
  fedex_ws = "fedex_ws",
  freightcom = "freightcom",
  generic = "generic",
  geodis = "geodis",
  laposte = "laposte",
  locate2u = "locate2u",
  nationex = "nationex",
  purolator = "purolator",
  roadie = "roadie",
  royalmail = "royalmail",
  sendle = "sendle",
  tge = "tge",
  tnt = "tnt",
  ups = "ups",
  usps = "usps",
  usps_international = "usps_international",
  zoom2u = "zoom2u",
}

export enum LabelTemplateTypeEnum {
  SVG = "SVG",
  ZPL = "ZPL",
}

// null
export interface UsageFilter {
  date_after?: string | null;
  date_before?: string | null;
  omit?: string[] | null;
}

// null
export interface AccountFilter {
  offset?: number | null;
  first?: number | null;
  id?: string | null;
  name?: string | null;
  slug?: string | null;
  is_active?: boolean | null;
  order_by?: string | null;
}

// null
export interface UserFilter {
  offset?: number | null;
  first?: number | null;
  id?: string | null;
  email?: string | null;
  is_staff?: boolean | null;
  is_active?: boolean | null;
  is_superuser?: boolean | null;
  order_by?: string | null;
}

// null
export interface SurchargeFilter {
  id?: string | null;
  name?: string | null;
  active?: boolean | null;
  surcharge_type?: SurchargeTypeEnum | null;
}

// null
export interface RateSheetFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
}

// null
export interface PermissionGroupFilter {
  offset?: number | null;
  first?: number | null;
}

// null
export interface CreateUserMutationInput {
  email: string;
  password1: string;
  password2: string;
  redirect_url: string;
  full_name?: string | null;
  is_staff?: boolean | null;
  is_active?: boolean | null;
  is_superuser?: boolean | null;
  organization_id?: string | null;
  permissions?: string[] | null;
}

// null
export interface UpdateUserMutationInput {
  id: number;
  email?: string | null;
  full_name?: string | null;
  is_staff?: boolean | null;
  is_active?: boolean | null;
  is_superuser?: boolean | null;
  permissions?: string[] | null;
}

// null
export interface DeleteUserMutationInput {
  id: number;
}

// null
export interface CreateSurchargeMutationInput {
  name: string;
  amount: number;
  surcharge_type: SurchargeTypeEnum;
  active?: boolean | null;
  carriers?: string[] | null;
  services?: string[] | null;
  organizations?: string[] | null;
  carrier_accounts?: string[] | null;
}

// null
export interface UpdateSurchargeMutationInput {
  name?: string | null;
  amount?: number | null;
  surcharge_type?: SurchargeTypeEnum | null;
  active?: boolean | null;
  carriers?: string[] | null;
  services?: string[] | null;
  organizations?: string[] | null;
  carrier_accounts?: string[] | null;
  id: string;
}

// null
export interface DeleteMutationInput {
  id: string;
}

// null
export interface CreateConnectionMutationInput {
  allied_express?: AlliedExpressSettingsInput | null;
  allied_express_local?: AlliedExpressLocalSettingsInput | null;
  amazon_shipping?: AmazonShippingSettingsInput | null;
  aramex?: AramexSettingsInput | null;
  asendia_us?: AsendiaUSSettingsInput | null;
  australiapost?: AustraliaPostSettingsInput | null;
  boxknight?: BoxKnightSettingsInput | null;
  bpost?: BelgianPostSettingsInput | null;
  canadapost?: CanadaPostSettingsInput | null;
  canpar?: CanparSettingsInput | null;
  chronopost?: ChronopostSettingsInput | null;
  colissimo?: ColissimoSettingsInput | null;
  dhl_express?: DHLExpressSettingsInput | null;
  dhl_parcel_de?: DHLParcelDESettingsInput | null;
  dhl_poland?: DHLPolandSettingsInput | null;
  dhl_universal?: DHLUniversalSettingsInput | null;
  dicom?: DicomSettingsInput | null;
  dpd?: DPDSettingsInput | null;
  dpdhl?: DPDHLSettingsInput | null;
  easypost?: EasyPostSettingsInput | null;
  eshipper?: EShipperSettingsInput | null;
  fedex?: FedexSettingsInput | null;
  fedex_ws?: FedexWSSettingsInput | null;
  freightcom?: FreightcomSettingsInput | null;
  generic?: GenericSettingsInput | null;
  geodis?: GEODISSettingsInput | null;
  laposte?: LaPosteSettingsInput | null;
  locate2u?: Locate2uSettingsInput | null;
  nationex?: NationexSettingsInput | null;
  purolator?: PurolatorSettingsInput | null;
  roadie?: RoadieSettingsInput | null;
  royalmail?: RoyalMailSettingsInput | null;
  sendle?: SendleSettingsInput | null;
  tge?: TGESettingsInput | null;
  tnt?: TNTSettingsInput | null;
  ups?: UPSSettingsInput | null;
  usps?: USPSSettingsInput | null;
  usps_international?: USPSInternationalSettingsInput | null;
  zoom2u?: Zoom2uSettingsInput | null;
}

// null
export interface AlliedExpressSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  account?: string | null;
  service_type?: string | null;
  carrier_id: string;
}

// null
export interface AlliedExpressLocalSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  account?: string | null;
  service_type?: string | null;
  carrier_id: string;
}

// null
export interface AmazonShippingSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  seller_id: string;
  developer_id: string;
  mws_auth_token: string;
  aws_region: string;
  carrier_id: string;
}

// null
export interface AramexSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  account_pin: string;
  account_entity: string;
  account_number: string;
  carrier_id: string;
}

// null
export interface AsendiaUSSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  api_key: string;
  account_number: string;
  carrier_id: string;
}

// null
export interface AustraliaPostSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key: string;
  password: string;
  account_number: string;
  carrier_id: string;
}

// null
export interface BoxKnightSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  carrier_id: string;
}

// null
export interface BelgianPostSettingsInput {
  services?: CreateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  account_id: string;
  passphrase: string;
  carrier_id: string;
}

// null
export interface CreateServiceLevelInput {
  service_name: string;
  service_code: string;
  currency: CurrencyCodeEnum;
  zones: ServiceZoneInput[];
  carrier_service_code?: string | null;
  description?: string | null;
  active?: boolean | null;
  transit_days?: number | null;
  transit_time?: number | null;
  max_width?: number | null;
  max_height?: number | null;
  max_length?: number | null;
  dimension_unit?: DimensionUnitEnum | null;
  min_weight?: number | null;
  max_weight?: number | null;
  weight_unit?: WeightUnitEnum | null;
  domicile?: boolean | null;
  international?: boolean | null;
  metadata?: any | null;
}

// null
export interface ServiceZoneInput {
  rate: number;
  label?: string | null;
  min_weight?: number | null;
  max_weight?: number | null;
  transit_days?: number | null;
  transit_time?: number | null;
  radius?: number | null;
  latitude?: number | null;
  longitude?: number | null;
  cities?: string[] | null;
  postal_codes?: string[] | null;
  country_codes?: string[] | null;
}

// null
export interface CanadaPostSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  customer_number?: string | null;
  contract_id?: string | null;
  carrier_id: string;
}

// null
export interface CanparSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  carrier_id: string;
}

// null
export interface ChronopostSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  account_number: string;
  password: string;
  carrier_id: string;
}

// null
export interface ColissimoSettingsInput {
  services?: CreateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  password: string;
  contract_number: string;
  laposte_api_key: string;
  carrier_id: string;
}

// null
export interface DHLExpressSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  site_id: string;
  password: string;
  account_number: string;
  carrier_id: string;
}

// null
export interface DHLParcelDESettingsInput {
  services?: CreateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  dhl_api_key: string;
  customer_number: string;
  tracking_consumer_key?: string | null;
  tracking_consumer_secret?: string | null;
  carrier_id: string;
}

// null
export interface DHLPolandSettingsInput {
  services?: CreateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  account_number: string;
  carrier_id: string;
}

// null
export interface DHLUniversalSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  consumer_key: string;
  consumer_secret: string;
  carrier_id: string;
}

// null
export interface DicomSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  billing_account?: string | null;
  carrier_id: string;
}

// null
export interface DPDSettingsInput {
  account_country_code?: string | null;
  services?: CreateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  delis_id: string;
  password: string;
  depot?: string | null;
  carrier_id: string;
}

// null
export interface DPDHLSettingsInput {
  services?: CreateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  app_id?: string | null;
  app_token?: string | null;
  zt_id?: string | null;
  zt_password?: string | null;
  account_number?: string | null;
  carrier_id: string;
}

// null
export interface EasyPostSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key: string;
  carrier_id: string;
}

// null
export interface EShipperSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  principal: string;
  credential: string;
  carrier_id: string;
}

// null
export interface FedexSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key?: string | null;
  secret_key?: string | null;
  account_number?: string | null;
  track_api_key?: string | null;
  track_secret_key?: string | null;
  carrier_id: string;
}

// null
export interface FedexWSSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  password: string;
  meter_number: string;
  account_number: string;
  user_key: string;
  carrier_id: string;
}

// null
export interface FreightcomSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  carrier_id: string;
}

// null
export interface GenericSettingsInput {
  account_country_code?: string | null;
  label_template?: LabelTemplateInput | null;
  services?: CreateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  display_name: string;
  custom_carrier_name: string;
  carrier_id: string;
  account_number?: string | null;
}

// null
export interface LabelTemplateInput {
  slug: string;
  template: string;
  template_type: LabelTemplateTypeEnum;
  width?: number | null;
  height?: number | null;
  shipment_sample?: any | null;
  id?: string | null;
}

// null
export interface GEODISSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key: string;
  identifier: string;
  code_client: string;
  language?: string | null;
  carrier_id: string;
}

// null
export interface LaPosteSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key: string;
  lang?: string | null;
  carrier_id: string;
}

// null
export interface Locate2uSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  client_id: string;
  client_secret: string;
  carrier_id: string;
}

// null
export interface NationexSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key: string;
  customer_id: string;
  billing_account?: string | null;
  language?: string | null;
  carrier_id: string;
}

// null
export interface PurolatorSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  account_number: string;
  user_token?: string | null;
  carrier_id: string;
}

// null
export interface RoadieSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key: string;
  carrier_id: string;
}

// null
export interface RoyalMailSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  client_id: string;
  client_secret: string;
  carrier_id: string;
}

// null
export interface SendleSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  sendle_id: string;
  api_key: string;
  carrier_id: string;
}

// null
export interface TGESettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  api_key: string;
  toll_username: string;
  toll_password: string;
  my_toll_token: string;
  my_toll_identity: string;
  account_code: string;
  carrier_id: string;
}

// null
export interface TNTSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  account_number: string;
  carrier_id: string;
}

// null
export interface UPSSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  client_id: string;
  client_secret: string;
  account_number?: string | null;
  carrier_id: string;
}

// null
export interface USPSSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  mailer_id?: string | null;
  customer_registration_id?: string | null;
  logistics_manager_mailer_id?: string | null;
  carrier_id: string;
}

// null
export interface USPSInternationalSettingsInput {
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username: string;
  password: string;
  mailer_id?: string | null;
  customer_registration_id?: string | null;
  logistics_manager_mailer_id?: string | null;
  carrier_id: string;
}

// null
export interface Zoom2uSettingsInput {
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key: string;
  carrier_id: string;
}

// null
export interface UpdateConnectionMutationInput {
  allied_express?: UpdateAlliedExpressSettingsInput | null;
  allied_express_local?: UpdateAlliedExpressLocalSettingsInput | null;
  amazon_shipping?: UpdateAmazonShippingSettingsInput | null;
  aramex?: UpdateAramexSettingsInput | null;
  asendia_us?: UpdateAsendiaUSSettingsInput | null;
  australiapost?: UpdateAustraliaPostSettingsInput | null;
  boxknight?: UpdateBoxKnightSettingsInput | null;
  bpost?: UpdateBelgianPostSettingsInput | null;
  canadapost?: UpdateCanadaPostSettingsInput | null;
  canpar?: UpdateCanparSettingsInput | null;
  chronopost?: UpdateChronopostSettingsInput | null;
  colissimo?: UpdateColissimoSettingsInput | null;
  dhl_express?: UpdateDHLExpressSettingsInput | null;
  dhl_parcel_de?: UpdateDHLParcelDESettingsInput | null;
  dhl_poland?: UpdateDHLPolandSettingsInput | null;
  dhl_universal?: UpdateDHLUniversalSettingsInput | null;
  dicom?: UpdateDicomSettingsInput | null;
  dpd?: UpdateDPDSettingsInput | null;
  dpdhl?: UpdateDPDHLSettingsInput | null;
  easypost?: UpdateEasyPostSettingsInput | null;
  eshipper?: UpdateEShipperSettingsInput | null;
  fedex?: UpdateFedexSettingsInput | null;
  fedex_ws?: UpdateFedexWSSettingsInput | null;
  freightcom?: UpdateFreightcomSettingsInput | null;
  generic?: UpdateGenericSettingsInput | null;
  geodis?: UpdateGEODISSettingsInput | null;
  laposte?: UpdateLaPosteSettingsInput | null;
  locate2u?: UpdateLocate2uSettingsInput | null;
  nationex?: UpdateNationexSettingsInput | null;
  purolator?: UpdatePurolatorSettingsInput | null;
  roadie?: UpdateRoadieSettingsInput | null;
  royalmail?: UpdateRoyalMailSettingsInput | null;
  sendle?: UpdateSendleSettingsInput | null;
  tge?: UpdateTGESettingsInput | null;
  tnt?: UpdateTNTSettingsInput | null;
  ups?: UpdateUPSSettingsInput | null;
  usps?: UpdateUSPSSettingsInput | null;
  usps_international?: UpdateUSPSInternationalSettingsInput | null;
  zoom2u?: UpdateZoom2uSettingsInput | null;
}

// null
export interface UpdateAlliedExpressSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  account?: string | null;
  service_type?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateAlliedExpressLocalSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  account?: string | null;
  service_type?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateAmazonShippingSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  seller_id?: string | null;
  developer_id?: string | null;
  mws_auth_token?: string | null;
  aws_region?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateAramexSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  account_pin?: string | null;
  account_entity?: string | null;
  account_number?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateAsendiaUSSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  api_key?: string | null;
  account_number?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateAustraliaPostSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key?: string | null;
  password?: string | null;
  account_number?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateBoxKnightSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateBelgianPostSettingsInput {
  id: string;
  services?: UpdateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  account_id?: string | null;
  passphrase?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateServiceLevelInput {
  service_name?: string | null;
  service_code?: string | null;
  currency?: CurrencyCodeEnum | null;
  zones?: UpdateServiceZoneInput[] | null;
  carrier_service_code?: string | null;
  description?: string | null;
  active?: boolean | null;
  transit_days?: number | null;
  transit_time?: number | null;
  max_width?: number | null;
  max_height?: number | null;
  max_length?: number | null;
  dimension_unit?: DimensionUnitEnum | null;
  min_weight?: number | null;
  max_weight?: number | null;
  weight_unit?: WeightUnitEnum | null;
  domicile?: boolean | null;
  international?: boolean | null;
  metadata?: any | null;
  id?: string | null;
}

// null
export interface UpdateServiceZoneInput {
  rate?: number | null;
  label?: string | null;
  min_weight?: number | null;
  max_weight?: number | null;
  transit_days?: number | null;
  transit_time?: number | null;
  radius?: number | null;
  latitude?: number | null;
  longitude?: number | null;
  cities?: string[] | null;
  postal_codes?: string[] | null;
  country_codes?: string[] | null;
}

// null
export interface UpdateCanadaPostSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  customer_number?: string | null;
  contract_id?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateCanparSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateChronopostSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  account_number?: string | null;
  password?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateColissimoSettingsInput {
  id: string;
  services?: UpdateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  password?: string | null;
  contract_number?: string | null;
  laposte_api_key?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateDHLExpressSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  site_id?: string | null;
  password?: string | null;
  account_number?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateDHLParcelDESettingsInput {
  id: string;
  services?: UpdateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  dhl_api_key?: string | null;
  customer_number?: string | null;
  tracking_consumer_key?: string | null;
  tracking_consumer_secret?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateDHLPolandSettingsInput {
  id: string;
  services?: UpdateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  account_number?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateDHLUniversalSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  consumer_key?: string | null;
  consumer_secret?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateDicomSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  billing_account?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateDPDSettingsInput {
  id: string;
  account_country_code?: string | null;
  services?: UpdateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  delis_id?: string | null;
  password?: string | null;
  depot?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateDPDHLSettingsInput {
  id: string;
  services?: UpdateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  app_id?: string | null;
  app_token?: string | null;
  zt_id?: string | null;
  zt_password?: string | null;
  account_number?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateEasyPostSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateEShipperSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  principal?: string | null;
  credential?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateFedexSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key?: string | null;
  secret_key?: string | null;
  account_number?: string | null;
  track_api_key?: string | null;
  track_secret_key?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateFedexWSSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  password?: string | null;
  meter_number?: string | null;
  account_number?: string | null;
  user_key?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateFreightcomSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateGenericSettingsInput {
  id: string;
  account_country_code?: string | null;
  label_template?: LabelTemplateInput | null;
  services?: UpdateServiceLevelInput[] | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  display_name?: string | null;
  custom_carrier_name?: string | null;
  carrier_id?: string | null;
  account_number?: string | null;
}

// null
export interface UpdateGEODISSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key?: string | null;
  identifier?: string | null;
  code_client?: string | null;
  language?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateLaPosteSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key?: string | null;
  lang?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateLocate2uSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  client_id?: string | null;
  client_secret?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateNationexSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key?: string | null;
  customer_id?: string | null;
  billing_account?: string | null;
  language?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdatePurolatorSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  account_number?: string | null;
  user_token?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateRoadieSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateRoyalMailSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  client_id?: string | null;
  client_secret?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateSendleSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  sendle_id?: string | null;
  api_key?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateTGESettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  api_key?: string | null;
  toll_username?: string | null;
  toll_password?: string | null;
  my_toll_token?: string | null;
  my_toll_identity?: string | null;
  account_code?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateTNTSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  account_number?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateUPSSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  client_id?: string | null;
  client_secret?: string | null;
  account_number?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateUSPSSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  mailer_id?: string | null;
  customer_registration_id?: string | null;
  logistics_manager_mailer_id?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateUSPSInternationalSettingsInput {
  id: string;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  username?: string | null;
  password?: string | null;
  mailer_id?: string | null;
  customer_registration_id?: string | null;
  logistics_manager_mailer_id?: string | null;
  carrier_id?: string | null;
}

// null
export interface UpdateZoom2uSettingsInput {
  id: string;
  account_country_code?: string | null;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  api_key?: string | null;
  carrier_id?: string | null;
}

// null
export interface DeleteConnectionMutationInput {
  id: string;
}

// null
export interface UpdateOrganizationAccountMutationInput {
  id: string;
  name?: string | null;
  slug?: string | null;
  is_active?: boolean | null;
}

// null
export interface CreateRateSheetMutationInput {
  name: string;
  carrier_name: CarrierNameEnum;
  services?: CreateServiceLevelInput[] | null;
  carriers?: string[] | null;
}

// null
export interface UpdateRateSheetMutationInput {
  id: string;
  name?: string | null;
  services?: UpdateServiceLevelInput[] | null;
  carriers?: string[] | null;
}

//==============================================================
// END Enums and Input Objects
//==============================================================