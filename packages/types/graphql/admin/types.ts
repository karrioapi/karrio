

/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetUsers
// ====================================================

export interface GetUsers_users_edges_node {
  id: number;
  email: string;
  full_name: string;
  is_staff: boolean;
  is_active: boolean;
  is_superuser: boolean | null;
  last_login: any | null;
  date_joined: any;
  permissions: string[] | null;
}

export interface GetUsers_users_edges {
  node: GetUsers_users_edges_node;
}

export interface GetUsers_users_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetUsers_users {
  edges: GetUsers_users_edges[];
  page_info: GetUsers_users_page_info;
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
// GraphQL query operation: GetUser
// ====================================================

export interface GetUser_user {
  id: number;
  email: string;
  full_name: string;
  is_staff: boolean;
  is_active: boolean;
  is_superuser: boolean | null;
  last_login: any | null;
  date_joined: any;
  permissions: string[] | null;
}

export interface GetUser {
  user: GetUser_user | null;
}

export interface GetUserVariables {
  email: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetPermissionGroups
// ====================================================

export interface GetPermissionGroups_permission_groups_edges_node {
  id: number;
  name: string;
}

export interface GetPermissionGroups_permission_groups_edges {
  node: GetPermissionGroups_permission_groups_edges_node;
}

export interface GetPermissionGroups_permission_groups {
  edges: GetPermissionGroups_permission_groups_edges[];
}

export interface GetPermissionGroups {
  permission_groups: GetPermissionGroups_permission_groups;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConfigs
// ====================================================

export interface GetConfigs_configs {
  APP_NAME: string | null;
  APP_WEBSITE: string | null;
  EMAIL_USE_TLS: boolean | null;
  EMAIL_HOST_USER: string | null;
  EMAIL_HOST_PASSWORD: string | null;
  EMAIL_HOST: string | null;
  EMAIL_PORT: number | null;
  EMAIL_FROM_ADDRESS: string | null;
  GOOGLE_CLOUD_API_KEY: string | null;
  CANADAPOST_ADDRESS_COMPLETE_API_KEY: string | null;
  ORDER_DATA_RETENTION: number | null;
  TRACKER_DATA_RETENTION: number | null;
  SHIPMENT_DATA_RETENTION: number | null;
  API_LOGS_DATA_RETENTION: number | null;
  AUDIT_LOGGING: boolean | null;
  ALLOW_SIGNUP: boolean | null;
  ALLOW_ADMIN_APPROVED_SIGNUP: boolean | null;
  ALLOW_MULTI_ACCOUNT: boolean | null;
  ADMIN_DASHBOARD: boolean | null;
  MULTI_ORGANIZATIONS: boolean | null;
  ORDERS_MANAGEMENT: boolean | null;
  APPS_MANAGEMENT: boolean | null;
  DOCUMENTS_MANAGEMENT: boolean | null;
  DATA_IMPORT_EXPORT: boolean | null;
  WORKFLOW_MANAGEMENT: boolean | null;
  SHIPPING_RULES: boolean | null;
  PERSIST_SDK_TRACING: boolean | null;
}

export interface GetConfigs {
  configs: GetConfigs_configs;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetAdminSystemUsage
// ====================================================

export interface GetAdminSystemUsage_usage_api_requests {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetAdminSystemUsage_usage_api_errors {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetAdminSystemUsage_usage_shipment_count {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetAdminSystemUsage_usage_tracker_count {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetAdminSystemUsage_usage_order_volumes {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetAdminSystemUsage_usage_shipping_spend {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetAdminSystemUsage_usage_addons_charges {
  date: string | null;
  amount: number | null;
}

export interface GetAdminSystemUsage_usage {
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  total_shipping_spend: number | null;
  total_errors: number | null;
  order_volume: number | null;
  organization_count: number | null;
  user_count: number | null;
  total_addons_charges: number | null;
  api_requests: GetAdminSystemUsage_usage_api_requests[] | null;
  api_errors: GetAdminSystemUsage_usage_api_errors[] | null;
  shipment_count: GetAdminSystemUsage_usage_shipment_count[] | null;
  tracker_count: GetAdminSystemUsage_usage_tracker_count[] | null;
  order_volumes: GetAdminSystemUsage_usage_order_volumes[] | null;
  shipping_spend: GetAdminSystemUsage_usage_shipping_spend[] | null;
  addons_charges: GetAdminSystemUsage_usage_addons_charges[] | null;
}

export interface GetAdminSystemUsage {
  usage: GetAdminSystemUsage_usage;
}

export interface GetAdminSystemUsageVariables {
  filter?: UsageFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSystemConnections
// ====================================================

export interface GetSystemConnections_system_carrier_connections_edges_node_rate_sheet {
  id: string;
}

export interface GetSystemConnections_system_carrier_connections_edges_node_usage {
  total_trackers: number | null;
  total_shipments: number | null;
  total_shipping_spend: number | null;
  total_addons_charges: number | null;
}

export interface GetSystemConnections_system_carrier_connections_edges_node {
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  active: boolean;
  capabilities: string[];
  credentials: any;
  config: any | null;
  metadata: any | null;
  test_mode: boolean;
  rate_sheet: GetSystemConnections_system_carrier_connections_edges_node_rate_sheet | null;
  usage: GetSystemConnections_system_carrier_connections_edges_node_usage;
}

export interface GetSystemConnections_system_carrier_connections_edges {
  node: GetSystemConnections_system_carrier_connections_edges_node;
}

export interface GetSystemConnections_system_carrier_connections_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetSystemConnections_system_carrier_connections {
  edges: GetSystemConnections_system_carrier_connections_edges[];
  page_info: GetSystemConnections_system_carrier_connections_page_info;
}

export interface GetSystemConnections {
  system_carrier_connections: GetSystemConnections_system_carrier_connections;
}

export interface GetSystemConnectionsVariables {
  filter?: CarrierFilter | null;
  usageFilter?: UsageFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSystemConnection
// ====================================================

export interface GetSystemConnection_system_carrier_connection_rate_sheet {
  id: string;
}

export interface GetSystemConnection_system_carrier_connection {
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  active: boolean;
  capabilities: string[];
  credentials: any;
  config: any | null;
  metadata: any | null;
  test_mode: boolean;
  rate_sheet: GetSystemConnection_system_carrier_connection_rate_sheet | null;
}

export interface GetSystemConnection {
  system_carrier_connection: GetSystemConnection_system_carrier_connection | null;
}

export interface GetSystemConnectionVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetRateSheets
// ====================================================

export interface GetRateSheets_rate_sheets_edges_node_zones {
  id: string;
  label: string | null;
  country_codes: string[] | null;
  postal_codes: string[] | null;
  cities: string[] | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface GetRateSheets_rate_sheets_edges_node_surcharges {
  id: string;
  name: string;
  amount: number;
  surcharge_type: string;
  cost: number | null;
  active: boolean;
}

export interface GetRateSheets_rate_sheets_edges_node_service_rates {
  service_id: string;
  zone_id: string;
  rate: number;
  cost: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface GetRateSheets_rate_sheets_edges_node_services_features {
  first_mile: string | null;
  last_mile: string | null;
  form_factor: string | null;
  b2c: boolean | null;
  b2b: boolean | null;
  shipment_type: string | null;
  age_check: string | null;
  signature: boolean | null;
  tracked: boolean | null;
  insurance: boolean | null;
  express: boolean | null;
  dangerous_goods: boolean | null;
  saturday_delivery: boolean | null;
  sunday_delivery: boolean | null;
  multicollo: boolean | null;
  neighbor_delivery: boolean | null;
}

export interface GetRateSheets_rate_sheets_edges_node_services {
  id: string;
  service_name: string | null;
  service_code: string | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  dimension_unit: DimensionUnitEnum | null;
  max_weight: number | null;
  weight_unit: WeightUnitEnum | null;
  active: boolean | null;
  dim_factor: number | null;
  use_volumetric: boolean | null;
  zone_ids: string[];
  surcharge_ids: string[];
  features: GetRateSheets_rate_sheets_edges_node_services_features;
}

export interface GetRateSheets_rate_sheets_edges_node_carriers {
  id: string;
  carrier_name: string;
  active: boolean;
}

export interface GetRateSheets_rate_sheets_edges_node {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  origin_countries: string[] | null;
  metadata: any | null;
  zones: GetRateSheets_rate_sheets_edges_node_zones[] | null;
  surcharges: GetRateSheets_rate_sheets_edges_node_surcharges[] | null;
  service_rates: GetRateSheets_rate_sheets_edges_node_service_rates[] | null;
  services: GetRateSheets_rate_sheets_edges_node_services[];
  carriers: GetRateSheets_rate_sheets_edges_node_carriers[];
}

export interface GetRateSheets_rate_sheets_edges {
  node: GetRateSheets_rate_sheets_edges_node;
}

export interface GetRateSheets_rate_sheets_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetRateSheets_rate_sheets {
  edges: GetRateSheets_rate_sheets_edges[];
  page_info: GetRateSheets_rate_sheets_page_info;
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
// GraphQL query operation: GetRateSheet
// ====================================================

export interface GetRateSheet_rate_sheet_zones {
  id: string;
  label: string | null;
  country_codes: string[] | null;
  postal_codes: string[] | null;
  cities: string[] | null;
  transit_days: number | null;
  transit_time: number | null;
  radius: number | null;
  latitude: number | null;
  longitude: number | null;
}

export interface GetRateSheet_rate_sheet_surcharges {
  id: string;
  name: string;
  amount: number;
  surcharge_type: string;
  cost: number | null;
  active: boolean;
}

export interface GetRateSheet_rate_sheet_service_rates {
  service_id: string;
  zone_id: string;
  rate: number;
  cost: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface GetRateSheet_rate_sheet_services_features {
  first_mile: string | null;
  last_mile: string | null;
  form_factor: string | null;
  b2c: boolean | null;
  b2b: boolean | null;
  shipment_type: string | null;
  age_check: string | null;
  signature: boolean | null;
  tracked: boolean | null;
  insurance: boolean | null;
  express: boolean | null;
  dangerous_goods: boolean | null;
  saturday_delivery: boolean | null;
  sunday_delivery: boolean | null;
  multicollo: boolean | null;
  neighbor_delivery: boolean | null;
}

export interface GetRateSheet_rate_sheet_services {
  id: string;
  object_type: string;
  service_name: string | null;
  service_code: string | null;
  carrier_service_code: string | null;
  description: string | null;
  active: boolean | null;
  currency: CurrencyCodeEnum | null;
  transit_days: number | null;
  transit_time: number | null;
  max_width: number | null;
  max_height: number | null;
  max_length: number | null;
  dimension_unit: DimensionUnitEnum | null;
  max_weight: number | null;
  weight_unit: WeightUnitEnum | null;
  dim_factor: number | null;
  use_volumetric: boolean | null;
  domicile: boolean | null;
  international: boolean | null;
  zone_ids: string[];
  surcharge_ids: string[];
  features: GetRateSheet_rate_sheet_services_features;
}

export interface GetRateSheet_rate_sheet_carriers {
  id: string;
  carrier_name: string;
  active: boolean;
  carrier_id: string;
  display_name: string;
  capabilities: string[];
  test_mode: boolean;
}

export interface GetRateSheet_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  origin_countries: string[] | null;
  metadata: any | null;
  zones: GetRateSheet_rate_sheet_zones[] | null;
  surcharges: GetRateSheet_rate_sheet_surcharges[] | null;
  service_rates: GetRateSheet_rate_sheet_service_rates[] | null;
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
// GraphQL query operation: GetMarkups
// ====================================================

export interface GetMarkups_markups_edges_node_usage {
  total_shipments: number | null;
  total_addons_charges: number | null;
}

export interface GetMarkups_markups_edges_node {
  id: string;
  name: string;
  active: boolean;
  amount: number;
  markup_type: string;
  is_visible: boolean;
  carrier_codes: string[];
  service_codes: string[];
  connection_ids: string[];
  organization_ids: string[];
  metadata: any | null;
  usage: GetMarkups_markups_edges_node_usage;
}

export interface GetMarkups_markups_edges {
  node: GetMarkups_markups_edges_node;
}

export interface GetMarkups_markups_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetMarkups_markups {
  edges: GetMarkups_markups_edges[];
  page_info: GetMarkups_markups_page_info;
}

export interface GetMarkups {
  markups: GetMarkups_markups;
}

export interface GetMarkupsVariables {
  filter?: MarkupFilter | null;
  usageFilter?: UsageFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetMarkup
// ====================================================

export interface GetMarkup_markup_usage {
  total_shipments: number | null;
  total_addons_charges: number | null;
}

export interface GetMarkup_markup {
  id: string;
  name: string;
  active: boolean;
  amount: number;
  markup_type: string;
  is_visible: boolean;
  carrier_codes: string[];
  service_codes: string[];
  connection_ids: string[];
  organization_ids: string[];
  metadata: any | null;
  usage: GetMarkup_markup_usage;
}

export interface GetMarkup {
  markup: GetMarkup_markup | null;
}

export interface GetMarkupVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetOrganizationDetails
// ====================================================

export interface GetOrganizationDetails_account_members {
  email: string;
  is_admin: boolean;
  roles: UserRole[] | null;
  is_owner: boolean | null;
  full_name: string | null;
  last_login: any | null;
  user_id: string | null;
}

export interface GetOrganizationDetails_account_usage_api_requests {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetOrganizationDetails_account_usage_api_errors {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetOrganizationDetails_account_usage_shipping_spend {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetOrganizationDetails_account_usage_shipment_count {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetOrganizationDetails_account_usage_tracker_count {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetOrganizationDetails_account_usage_order_volumes {
  date: string | null;
  count: number | null;
  label: string | null;
}

export interface GetOrganizationDetails_account_usage {
  members: number | null;
  total_requests: number | null;
  total_errors: number | null;
  order_volume: number | null;
  total_shipments: number | null;
  total_shipping_spend: number | null;
  unfulfilled_orders: number | null;
  total_trackers: number | null;
  total_addons_charges: number | null;
  api_requests: GetOrganizationDetails_account_usage_api_requests[] | null;
  api_errors: GetOrganizationDetails_account_usage_api_errors[] | null;
  shipping_spend: GetOrganizationDetails_account_usage_shipping_spend[] | null;
  shipment_count: GetOrganizationDetails_account_usage_shipment_count[] | null;
  tracker_count: GetOrganizationDetails_account_usage_tracker_count[] | null;
  order_volumes: GetOrganizationDetails_account_usage_order_volumes[] | null;
}

export interface GetOrganizationDetails_account {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  created: any;
  modified: any;
  members: GetOrganizationDetails_account_members[];
  usage: GetOrganizationDetails_account_usage;
}

export interface GetOrganizationDetails {
  account: GetOrganizationDetails_account | null;
}

export interface GetOrganizationDetailsVariables {
  id: string;
  usageFilter?: OrgUsageFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetOrganizations
// ====================================================

export interface GetOrganizations_accounts_edges_node_usage {
  members: number | null;
  total_shipments: number | null;
  total_trackers: number | null;
  total_requests: number | null;
  total_shipping_spend: number | null;
  total_addons_charges: number | null;
  total_errors: number | null;
  order_volume: number | null;
  unfulfilled_orders: number | null;
}

export interface GetOrganizations_accounts_edges_node {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  created: any;
  modified: any;
  usage: GetOrganizations_accounts_edges_node_usage;
}

export interface GetOrganizations_accounts_edges {
  node: GetOrganizations_accounts_edges_node;
  cursor: string;
}

export interface GetOrganizations_accounts_page_info {
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetOrganizations_accounts {
  edges: GetOrganizations_accounts_edges[];
  page_info: GetOrganizations_accounts_page_info;
}

export interface GetOrganizations {
  accounts: GetOrganizations_accounts;
}

export interface GetOrganizationsVariables {
  filter?: AccountFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetCarrierConnections
// ====================================================

export interface GetCarrierConnections_carrier_connections_edges_node_usage {
  total_shipments: number | null;
  total_trackers: number | null;
  total_shipping_spend: number | null;
  total_addons_charges: number | null;
}

export interface GetCarrierConnections_carrier_connections_edges_node {
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  active: boolean;
  capabilities: string[];
  config: any | null;
  test_mode: boolean;
  usage: GetCarrierConnections_carrier_connections_edges_node_usage;
}

export interface GetCarrierConnections_carrier_connections_edges {
  node: GetCarrierConnections_carrier_connections_edges_node;
}

export interface GetCarrierConnections_carrier_connections_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetCarrierConnections_carrier_connections {
  edges: GetCarrierConnections_carrier_connections_edges[];
  page_info: GetCarrierConnections_carrier_connections_page_info;
}

export interface GetCarrierConnections {
  carrier_connections: GetCarrierConnections_carrier_connections;
}

export interface GetCarrierConnectionsVariables {
  filter?: AccountCarrierConnectionFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetCarrierConnection
// ====================================================

export interface GetCarrierConnection_carrier_connection_usage {
  total_shipments: number | null;
  total_trackers: number | null;
  total_shipping_spend: number | null;
  total_addons_charges: number | null;
}

export interface GetCarrierConnection_carrier_connection {
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  active: boolean;
  capabilities: string[];
  config: any | null;
  test_mode: boolean;
  usage: GetCarrierConnection_carrier_connection_usage;
}

export interface GetCarrierConnection {
  carrier_connection: GetCarrierConnection_carrier_connection | null;
}

export interface GetCarrierConnectionVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetShipments
// ====================================================

export interface GetShipments_shipments_edges_node_selected_rate {
  id: string;
  service: string;
  total_charge: number;
  currency: CurrencyCodeEnum;
}

export interface GetShipments_shipments_edges_node {
  id: string;
  tracking_number: string | null;
  status: ShipmentStatusEnum;
  carrier_name: string | null;
  service: string | null;
  created_at: any;
  updated_at: any;
  selected_rate: GetShipments_shipments_edges_node_selected_rate | null;
}

export interface GetShipments_shipments_edges {
  node: GetShipments_shipments_edges_node;
}

export interface GetShipments_shipments_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetShipments_shipments {
  edges: GetShipments_shipments_edges[];
  page_info: GetShipments_shipments_page_info;
}

export interface GetShipments {
  shipments: GetShipments_shipments;
}

export interface GetShipmentsVariables {
  filter?: SystemShipmentFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTrackers
// ====================================================

export interface GetTrackers_trackers_edges_node {
  id: string;
  tracking_number: string;
  status: TrackerStatusEnum;
  carrier_name: string | null;
  carrier_id: string | null;
  created_at: any;
  updated_at: any;
}

export interface GetTrackers_trackers_edges {
  node: GetTrackers_trackers_edges_node;
}

export interface GetTrackers_trackers_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetTrackers_trackers {
  edges: GetTrackers_trackers_edges[];
  page_info: GetTrackers_trackers_page_info;
}

export interface GetTrackers {
  trackers: GetTrackers_trackers;
}

export interface GetTrackersVariables {
  filter?: SystemTrackerFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetOrders
// ====================================================

export interface GetOrders_orders_edges_node {
  id: string;
  order_id: string;
  status: OrderStatus;
  created_at: any;
  updated_at: any;
}

export interface GetOrders_orders_edges {
  node: GetOrders_orders_edges_node;
}

export interface GetOrders_orders_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetOrders_orders {
  edges: GetOrders_orders_edges[];
  page_info: GetOrders_orders_page_info;
}

export interface GetOrders {
  orders: GetOrders_orders;
}

export interface GetOrdersVariables {
  filter?: SystemOrderFilter | null;
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
  id: number;
  email: string;
  full_name: string;
  is_staff: boolean;
  is_active: boolean;
  last_login: any | null;
  date_joined: any;
  permissions: string[] | null;
}

export interface CreateUser_create_user {
  errors: CreateUser_create_user_errors[] | null;
  user: CreateUser_create_user_user | null;
}

export interface CreateUser {
  create_user: CreateUser_create_user;
}

export interface CreateUserVariables {
  input: CreateUserMutationInput;
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

export interface UpdateUser_update_user_user {
  id: number;
  email: string;
  full_name: string;
  is_staff: boolean;
  is_active: boolean;
  last_login: any | null;
  date_joined: any;
  permissions: string[] | null;
}

export interface UpdateUser_update_user {
  errors: UpdateUser_update_user_errors[] | null;
  user: UpdateUser_update_user_user | null;
}

export interface UpdateUser {
  update_user: UpdateUser_update_user;
}

export interface UpdateUserVariables {
  input: UpdateUserMutationInput;
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
  errors: RemoveUser_remove_user_errors[] | null;
  id: number;
}

export interface RemoveUser {
  remove_user: RemoveUser_remove_user;
}

export interface RemoveUserVariables {
  input: DeleteUserMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateConfigs
// ====================================================

export interface UpdateConfigs_update_configs_errors {
  field: string;
  messages: string[];
}

export interface UpdateConfigs_update_configs_configs {
  ALLOW_SIGNUP: boolean | null;
  ALLOW_ADMIN_APPROVED_SIGNUP: boolean | null;
  ALLOW_MULTI_ACCOUNT: boolean | null;
  ADMIN_DASHBOARD: boolean | null;
  AUDIT_LOGGING: boolean | null;
  ORDERS_MANAGEMENT: boolean | null;
  APPS_MANAGEMENT: boolean | null;
  MULTI_ORGANIZATIONS: boolean | null;
  PERSIST_SDK_TRACING: boolean | null;
}

export interface UpdateConfigs_update_configs {
  errors: UpdateConfigs_update_configs_errors[] | null;
  configs: UpdateConfigs_update_configs_configs | null;
}

export interface UpdateConfigs {
  update_configs: UpdateConfigs_update_configs;
}

export interface UpdateConfigsVariables {
  input: InstanceConfigMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateSystemConnection
// ====================================================

export interface CreateSystemConnection_create_system_carrier_connection_errors {
  field: string;
  messages: string[];
}

export interface CreateSystemConnection_create_system_carrier_connection_connection {
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  active: boolean;
  capabilities: string[];
  credentials: any;
  config: any | null;
  metadata: any | null;
  test_mode: boolean;
}

export interface CreateSystemConnection_create_system_carrier_connection {
  errors: CreateSystemConnection_create_system_carrier_connection_errors[] | null;
  connection: CreateSystemConnection_create_system_carrier_connection_connection | null;
}

export interface CreateSystemConnection {
  create_system_carrier_connection: CreateSystemConnection_create_system_carrier_connection;
}

export interface CreateSystemConnectionVariables {
  input: CreateConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateSystemConnection
// ====================================================

export interface UpdateSystemConnection_update_system_carrier_connection_errors {
  field: string;
  messages: string[];
}

export interface UpdateSystemConnection_update_system_carrier_connection_connection {
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  active: boolean;
  capabilities: string[];
  credentials: any;
  config: any | null;
  metadata: any | null;
  test_mode: boolean;
}

export interface UpdateSystemConnection_update_system_carrier_connection {
  errors: UpdateSystemConnection_update_system_carrier_connection_errors[] | null;
  connection: UpdateSystemConnection_update_system_carrier_connection_connection | null;
}

export interface UpdateSystemConnection {
  update_system_carrier_connection: UpdateSystemConnection_update_system_carrier_connection;
}

export interface UpdateSystemConnectionVariables {
  input: UpdateConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteSystemConnection
// ====================================================

export interface DeleteSystemConnection_delete_system_carrier_connection_errors {
  field: string;
  messages: string[];
}

export interface DeleteSystemConnection_delete_system_carrier_connection {
  errors: DeleteSystemConnection_delete_system_carrier_connection_errors[] | null;
  id: string;
}

export interface DeleteSystemConnection {
  delete_system_carrier_connection: DeleteSystemConnection_delete_system_carrier_connection;
}

export interface DeleteSystemConnectionVariables {
  input: DeleteConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateRateSheet
// ====================================================

export interface CreateRateSheet_create_rate_sheet_errors {
  field: string;
  messages: string[];
}

export interface CreateRateSheet_create_rate_sheet_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface CreateRateSheet_create_rate_sheet {
  errors: CreateRateSheet_create_rate_sheet_errors[] | null;
  rate_sheet: CreateRateSheet_create_rate_sheet_rate_sheet | null;
}

export interface CreateRateSheet {
  create_rate_sheet: CreateRateSheet_create_rate_sheet;
}

export interface CreateRateSheetVariables {
  input: CreateRateSheetMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateRateSheet
// ====================================================

export interface UpdateRateSheet_update_rate_sheet_errors {
  field: string;
  messages: string[];
}

export interface UpdateRateSheet_update_rate_sheet_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface UpdateRateSheet_update_rate_sheet {
  errors: UpdateRateSheet_update_rate_sheet_errors[] | null;
  rate_sheet: UpdateRateSheet_update_rate_sheet_rate_sheet | null;
}

export interface UpdateRateSheet {
  update_rate_sheet: UpdateRateSheet_update_rate_sheet;
}

export interface UpdateRateSheetVariables {
  input: UpdateRateSheetMutationInput;
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
  errors: DeleteRateSheet_delete_rate_sheet_errors[] | null;
  id: string;
}

export interface DeleteRateSheet {
  delete_rate_sheet: DeleteRateSheet_delete_rate_sheet;
}

export interface DeleteRateSheetVariables {
  input: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteRateSheetService
// ====================================================

export interface DeleteRateSheetService_delete_rate_sheet_service_errors {
  field: string;
  messages: string[];
}

export interface DeleteRateSheetService_delete_rate_sheet_service {
  errors: DeleteRateSheetService_delete_rate_sheet_service_errors[] | null;
}

export interface DeleteRateSheetService {
  delete_rate_sheet_service: DeleteRateSheetService_delete_rate_sheet_service;
}

export interface DeleteRateSheetServiceVariables {
  input: DeleteRateSheetServiceMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: AddSharedZone
// ====================================================

export interface AddSharedZone_add_shared_zone_rate_sheet_zones {
  id: string;
  label: string | null;
  country_codes: string[] | null;
  postal_codes: string[] | null;
  cities: string[] | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface AddSharedZone_add_shared_zone_rate_sheet {
  id: string;
  zones: AddSharedZone_add_shared_zone_rate_sheet_zones[] | null;
}

export interface AddSharedZone_add_shared_zone_errors {
  field: string;
  messages: string[];
}

export interface AddSharedZone_add_shared_zone {
  rate_sheet: AddSharedZone_add_shared_zone_rate_sheet | null;
  errors: AddSharedZone_add_shared_zone_errors[] | null;
}

export interface AddSharedZone {
  add_shared_zone: AddSharedZone_add_shared_zone;
}

export interface AddSharedZoneVariables {
  input: AddSharedZoneMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateSharedZone
// ====================================================

export interface UpdateSharedZone_update_shared_zone_rate_sheet_zones {
  id: string;
  label: string | null;
  country_codes: string[] | null;
  postal_codes: string[] | null;
  cities: string[] | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface UpdateSharedZone_update_shared_zone_rate_sheet {
  id: string;
  zones: UpdateSharedZone_update_shared_zone_rate_sheet_zones[] | null;
}

export interface UpdateSharedZone_update_shared_zone_errors {
  field: string;
  messages: string[];
}

export interface UpdateSharedZone_update_shared_zone {
  rate_sheet: UpdateSharedZone_update_shared_zone_rate_sheet | null;
  errors: UpdateSharedZone_update_shared_zone_errors[] | null;
}

export interface UpdateSharedZone {
  update_shared_zone: UpdateSharedZone_update_shared_zone;
}

export interface UpdateSharedZoneVariables {
  input: UpdateSharedZoneMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteSharedZone
// ====================================================

export interface DeleteSharedZone_delete_shared_zone_rate_sheet_zones {
  id: string;
  label: string | null;
}

export interface DeleteSharedZone_delete_shared_zone_rate_sheet {
  id: string;
  zones: DeleteSharedZone_delete_shared_zone_rate_sheet_zones[] | null;
}

export interface DeleteSharedZone_delete_shared_zone_errors {
  field: string;
  messages: string[];
}

export interface DeleteSharedZone_delete_shared_zone {
  rate_sheet: DeleteSharedZone_delete_shared_zone_rate_sheet | null;
  errors: DeleteSharedZone_delete_shared_zone_errors[] | null;
}

export interface DeleteSharedZone {
  delete_shared_zone: DeleteSharedZone_delete_shared_zone;
}

export interface DeleteSharedZoneVariables {
  input: DeleteSharedZoneMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: AddSharedSurcharge
// ====================================================

export interface AddSharedSurcharge_add_shared_surcharge_rate_sheet_surcharges {
  id: string;
  name: string;
  amount: number;
  surcharge_type: string;
  cost: number | null;
  active: boolean;
}

export interface AddSharedSurcharge_add_shared_surcharge_rate_sheet {
  id: string;
  surcharges: AddSharedSurcharge_add_shared_surcharge_rate_sheet_surcharges[] | null;
}

export interface AddSharedSurcharge_add_shared_surcharge_errors {
  field: string;
  messages: string[];
}

export interface AddSharedSurcharge_add_shared_surcharge {
  rate_sheet: AddSharedSurcharge_add_shared_surcharge_rate_sheet | null;
  errors: AddSharedSurcharge_add_shared_surcharge_errors[] | null;
}

export interface AddSharedSurcharge {
  add_shared_surcharge: AddSharedSurcharge_add_shared_surcharge;
}

export interface AddSharedSurchargeVariables {
  input: AddSharedSurchargeMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateSharedSurcharge
// ====================================================

export interface UpdateSharedSurcharge_update_shared_surcharge_rate_sheet_surcharges {
  id: string;
  name: string;
  amount: number;
  surcharge_type: string;
  cost: number | null;
  active: boolean;
}

export interface UpdateSharedSurcharge_update_shared_surcharge_rate_sheet {
  id: string;
  surcharges: UpdateSharedSurcharge_update_shared_surcharge_rate_sheet_surcharges[] | null;
}

export interface UpdateSharedSurcharge_update_shared_surcharge_errors {
  field: string;
  messages: string[];
}

export interface UpdateSharedSurcharge_update_shared_surcharge {
  rate_sheet: UpdateSharedSurcharge_update_shared_surcharge_rate_sheet | null;
  errors: UpdateSharedSurcharge_update_shared_surcharge_errors[] | null;
}

export interface UpdateSharedSurcharge {
  update_shared_surcharge: UpdateSharedSurcharge_update_shared_surcharge;
}

export interface UpdateSharedSurchargeVariables {
  input: UpdateSharedSurchargeMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteSharedSurcharge
// ====================================================

export interface DeleteSharedSurcharge_delete_shared_surcharge_rate_sheet_surcharges {
  id: string;
  name: string;
}

export interface DeleteSharedSurcharge_delete_shared_surcharge_rate_sheet {
  id: string;
  surcharges: DeleteSharedSurcharge_delete_shared_surcharge_rate_sheet_surcharges[] | null;
}

export interface DeleteSharedSurcharge_delete_shared_surcharge_errors {
  field: string;
  messages: string[];
}

export interface DeleteSharedSurcharge_delete_shared_surcharge {
  rate_sheet: DeleteSharedSurcharge_delete_shared_surcharge_rate_sheet | null;
  errors: DeleteSharedSurcharge_delete_shared_surcharge_errors[] | null;
}

export interface DeleteSharedSurcharge {
  delete_shared_surcharge: DeleteSharedSurcharge_delete_shared_surcharge;
}

export interface DeleteSharedSurchargeVariables {
  input: DeleteSharedSurchargeMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: BatchUpdateSurcharges
// ====================================================

export interface BatchUpdateSurcharges_batch_update_surcharges_rate_sheet_surcharges {
  id: string;
  name: string;
  amount: number;
  surcharge_type: string;
  cost: number | null;
  active: boolean;
}

export interface BatchUpdateSurcharges_batch_update_surcharges_rate_sheet {
  id: string;
  surcharges: BatchUpdateSurcharges_batch_update_surcharges_rate_sheet_surcharges[] | null;
}

export interface BatchUpdateSurcharges_batch_update_surcharges_errors {
  field: string;
  messages: string[];
}

export interface BatchUpdateSurcharges_batch_update_surcharges {
  rate_sheet: BatchUpdateSurcharges_batch_update_surcharges_rate_sheet | null;
  errors: BatchUpdateSurcharges_batch_update_surcharges_errors[] | null;
}

export interface BatchUpdateSurcharges {
  batch_update_surcharges: BatchUpdateSurcharges_batch_update_surcharges;
}

export interface BatchUpdateSurchargesVariables {
  input: BatchUpdateSurchargesMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateServiceRate
// ====================================================

export interface UpdateServiceRate_update_service_rate_rate_sheet_service_rates {
  service_id: string;
  zone_id: string;
  rate: number;
  cost: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface UpdateServiceRate_update_service_rate_rate_sheet {
  id: string;
  service_rates: UpdateServiceRate_update_service_rate_rate_sheet_service_rates[] | null;
}

export interface UpdateServiceRate_update_service_rate_errors {
  field: string;
  messages: string[];
}

export interface UpdateServiceRate_update_service_rate {
  rate_sheet: UpdateServiceRate_update_service_rate_rate_sheet | null;
  errors: UpdateServiceRate_update_service_rate_errors[] | null;
}

export interface UpdateServiceRate {
  update_service_rate: UpdateServiceRate_update_service_rate;
}

export interface UpdateServiceRateVariables {
  input: UpdateServiceRateMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: BatchUpdateServiceRates
// ====================================================

export interface BatchUpdateServiceRates_batch_update_service_rates_rate_sheet_service_rates {
  service_id: string;
  zone_id: string;
  rate: number;
  cost: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface BatchUpdateServiceRates_batch_update_service_rates_rate_sheet {
  id: string;
  service_rates: BatchUpdateServiceRates_batch_update_service_rates_rate_sheet_service_rates[] | null;
}

export interface BatchUpdateServiceRates_batch_update_service_rates_errors {
  field: string;
  messages: string[];
}

export interface BatchUpdateServiceRates_batch_update_service_rates {
  rate_sheet: BatchUpdateServiceRates_batch_update_service_rates_rate_sheet | null;
  errors: BatchUpdateServiceRates_batch_update_service_rates_errors[] | null;
}

export interface BatchUpdateServiceRates {
  batch_update_service_rates: BatchUpdateServiceRates_batch_update_service_rates;
}

export interface BatchUpdateServiceRatesVariables {
  input: BatchUpdateServiceRatesMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: AddWeightRange
// ====================================================

export interface AddWeightRange_add_weight_range_rate_sheet_service_rates {
  service_id: string;
  zone_id: string;
  rate: number;
  cost: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface AddWeightRange_add_weight_range_rate_sheet {
  id: string;
  service_rates: AddWeightRange_add_weight_range_rate_sheet_service_rates[] | null;
}

export interface AddWeightRange_add_weight_range_errors {
  field: string;
  messages: string[];
}

export interface AddWeightRange_add_weight_range {
  rate_sheet: AddWeightRange_add_weight_range_rate_sheet | null;
  errors: AddWeightRange_add_weight_range_errors[] | null;
}

export interface AddWeightRange {
  add_weight_range: AddWeightRange_add_weight_range;
}

export interface AddWeightRangeVariables {
  input: AddWeightRangeMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: RemoveWeightRange
// ====================================================

export interface RemoveWeightRange_remove_weight_range_rate_sheet_service_rates {
  service_id: string;
  zone_id: string;
  rate: number;
  cost: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface RemoveWeightRange_remove_weight_range_rate_sheet {
  id: string;
  service_rates: RemoveWeightRange_remove_weight_range_rate_sheet_service_rates[] | null;
}

export interface RemoveWeightRange_remove_weight_range_errors {
  field: string;
  messages: string[];
}

export interface RemoveWeightRange_remove_weight_range {
  rate_sheet: RemoveWeightRange_remove_weight_range_rate_sheet | null;
  errors: RemoveWeightRange_remove_weight_range_errors[] | null;
}

export interface RemoveWeightRange {
  remove_weight_range: RemoveWeightRange_remove_weight_range;
}

export interface RemoveWeightRangeVariables {
  input: RemoveWeightRangeMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteServiceRate
// ====================================================

export interface DeleteServiceRate_delete_service_rate_rate_sheet_service_rates {
  service_id: string;
  zone_id: string;
  rate: number;
  cost: number | null;
  min_weight: number | null;
  max_weight: number | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface DeleteServiceRate_delete_service_rate_rate_sheet {
  id: string;
  service_rates: DeleteServiceRate_delete_service_rate_rate_sheet_service_rates[] | null;
}

export interface DeleteServiceRate_delete_service_rate_errors {
  field: string;
  messages: string[];
}

export interface DeleteServiceRate_delete_service_rate {
  rate_sheet: DeleteServiceRate_delete_service_rate_rate_sheet | null;
  errors: DeleteServiceRate_delete_service_rate_errors[] | null;
}

export interface DeleteServiceRate {
  delete_service_rate: DeleteServiceRate_delete_service_rate;
}

export interface DeleteServiceRateVariables {
  input: DeleteServiceRateMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateServiceZoneIds
// ====================================================

export interface UpdateServiceZoneIds_update_service_zone_ids_rate_sheet_services {
  id: string;
  zone_ids: string[];
}

export interface UpdateServiceZoneIds_update_service_zone_ids_rate_sheet {
  id: string;
  services: UpdateServiceZoneIds_update_service_zone_ids_rate_sheet_services[];
}

export interface UpdateServiceZoneIds_update_service_zone_ids_errors {
  field: string;
  messages: string[];
}

export interface UpdateServiceZoneIds_update_service_zone_ids {
  rate_sheet: UpdateServiceZoneIds_update_service_zone_ids_rate_sheet | null;
  errors: UpdateServiceZoneIds_update_service_zone_ids_errors[] | null;
}

export interface UpdateServiceZoneIds {
  update_service_zone_ids: UpdateServiceZoneIds_update_service_zone_ids;
}

export interface UpdateServiceZoneIdsVariables {
  input: UpdateServiceZoneIdsMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateServiceSurchargeIds
// ====================================================

export interface UpdateServiceSurchargeIds_update_service_surcharge_ids_rate_sheet_services {
  id: string;
  surcharge_ids: string[];
}

export interface UpdateServiceSurchargeIds_update_service_surcharge_ids_rate_sheet {
  id: string;
  services: UpdateServiceSurchargeIds_update_service_surcharge_ids_rate_sheet_services[];
}

export interface UpdateServiceSurchargeIds_update_service_surcharge_ids_errors {
  field: string;
  messages: string[];
}

export interface UpdateServiceSurchargeIds_update_service_surcharge_ids {
  rate_sheet: UpdateServiceSurchargeIds_update_service_surcharge_ids_rate_sheet | null;
  errors: UpdateServiceSurchargeIds_update_service_surcharge_ids_errors[] | null;
}

export interface UpdateServiceSurchargeIds {
  update_service_surcharge_ids: UpdateServiceSurchargeIds_update_service_surcharge_ids;
}

export interface UpdateServiceSurchargeIdsVariables {
  input: UpdateServiceSurchargeIdsMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateMarkup
// ====================================================

export interface CreateMarkup_create_markup_errors {
  field: string;
  messages: string[];
}

export interface CreateMarkup_create_markup_markup {
  id: string;
  name: string;
  active: boolean;
  amount: number;
  markup_type: string;
  is_visible: boolean;
  carrier_codes: string[];
  service_codes: string[];
  connection_ids: string[];
  metadata: any | null;
}

export interface CreateMarkup_create_markup {
  errors: CreateMarkup_create_markup_errors[] | null;
  markup: CreateMarkup_create_markup_markup | null;
}

export interface CreateMarkup {
  create_markup: CreateMarkup_create_markup;
}

export interface CreateMarkupVariables {
  input: CreateMarkupMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateMarkup
// ====================================================

export interface UpdateMarkup_update_markup_errors {
  field: string;
  messages: string[];
}

export interface UpdateMarkup_update_markup_markup {
  id: string;
  name: string;
  active: boolean;
  amount: number;
  markup_type: string;
  is_visible: boolean;
  carrier_codes: string[];
  service_codes: string[];
  connection_ids: string[];
  metadata: any | null;
}

export interface UpdateMarkup_update_markup {
  errors: UpdateMarkup_update_markup_errors[] | null;
  markup: UpdateMarkup_update_markup_markup | null;
}

export interface UpdateMarkup {
  update_markup: UpdateMarkup_update_markup;
}

export interface UpdateMarkupVariables {
  input: UpdateMarkupMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteMarkup
// ====================================================

export interface DeleteMarkup_delete_markup_errors {
  field: string;
  messages: string[];
}

export interface DeleteMarkup_delete_markup {
  errors: DeleteMarkup_delete_markup_errors[] | null;
  id: string;
}

export interface DeleteMarkup {
  delete_markup: DeleteMarkup_delete_markup;
}

export interface DeleteMarkupVariables {
  input: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateOrganizationAccount
// ====================================================

export interface CreateOrganizationAccount_create_organization_account_account {
  id: string;
}

export interface CreateOrganizationAccount_create_organization_account_errors {
  field: string;
  messages: string[];
}

export interface CreateOrganizationAccount_create_organization_account {
  account: CreateOrganizationAccount_create_organization_account_account | null;
  errors: CreateOrganizationAccount_create_organization_account_errors[] | null;
}

export interface CreateOrganizationAccount {
  create_organization_account: CreateOrganizationAccount_create_organization_account;
}

export interface CreateOrganizationAccountVariables {
  input: CreateOrganizationAccountMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateOrganizationAccount
// ====================================================

export interface UpdateOrganizationAccount_update_organization_account_account {
  id: string;
}

export interface UpdateOrganizationAccount_update_organization_account_errors {
  field: string;
  messages: string[];
}

export interface UpdateOrganizationAccount_update_organization_account {
  account: UpdateOrganizationAccount_update_organization_account_account | null;
  errors: UpdateOrganizationAccount_update_organization_account_errors[] | null;
}

export interface UpdateOrganizationAccount {
  update_organization_account: UpdateOrganizationAccount_update_organization_account;
}

export interface UpdateOrganizationAccountVariables {
  input: UpdateOrganizationAccountMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DisableOrganizationAccount
// ====================================================

export interface DisableOrganizationAccount_disable_organization_account_account {
  id: string;
}

export interface DisableOrganizationAccount_disable_organization_account_errors {
  field: string;
  messages: string[];
}

export interface DisableOrganizationAccount_disable_organization_account {
  account: DisableOrganizationAccount_disable_organization_account_account | null;
  errors: DisableOrganizationAccount_disable_organization_account_errors[] | null;
}

export interface DisableOrganizationAccount {
  disable_organization_account: DisableOrganizationAccount_disable_organization_account;
}

export interface DisableOrganizationAccountVariables {
  input: DisableOrganizationAccountMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteOrganizationAccount
// ====================================================

export interface DeleteOrganizationAccount_delete_organization_account_errors {
  field: string;
  messages: string[];
}

export interface DeleteOrganizationAccount_delete_organization_account {
  account_id: string;
  errors: DeleteOrganizationAccount_delete_organization_account_errors[] | null;
}

export interface DeleteOrganizationAccount {
  delete_organization_account: DeleteOrganizationAccount_delete_organization_account;
}

export interface DeleteOrganizationAccountVariables {
  input: DeleteOrganizationAccountMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: InviteOrganizationUser
// ====================================================

export interface InviteOrganizationUser_invite_organization_user_account {
  id: string;
}

export interface InviteOrganizationUser_invite_organization_user_errors {
  field: string;
  messages: string[];
}

export interface InviteOrganizationUser_invite_organization_user {
  account: InviteOrganizationUser_invite_organization_user_account | null;
  errors: InviteOrganizationUser_invite_organization_user_errors[] | null;
}

export interface InviteOrganizationUser {
  invite_organization_user: InviteOrganizationUser_invite_organization_user;
}

export interface InviteOrganizationUserVariables {
  input: InviteOrganizationUserMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSystemShipments
// ====================================================

export interface GetSystemShipments_shipments_edges_node_recipient {
  company_name: string | null;
  person_name: string | null;
  address_line1: string | null;
  city: string | null;
  state_code: string | null;
  postal_code: string | null;
  country_code: CountryCodeEnum | null;
}

export interface GetSystemShipments_shipments_edges_node_shipper {
  company_name: string | null;
  person_name: string | null;
  address_line1: string | null;
  city: string | null;
  state_code: string | null;
  postal_code: string | null;
  country_code: CountryCodeEnum | null;
}

export interface GetSystemShipments_shipments_edges_node_selected_rate {
  carrier_name: string;
  carrier_id: string;
  service: string;
  total_charge: number;
  currency: CurrencyCodeEnum;
}

export interface GetSystemShipments_shipments_edges_node_parcels {
  id: string | null;
  weight: number | null;
  width: number | null;
  height: number | null;
  length: number | null;
  packaging_type: string | null;
}

export interface GetSystemShipments_shipments_edges_node_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface GetSystemShipments_shipments_edges_node_tracker_events {
  code: string | null;
  date: string | null;
  description: string | null;
  location: string | null;
  time: string | null;
}

export interface GetSystemShipments_shipments_edges_node_tracker {
  id: string;
  tracking_number: string;
  events: GetSystemShipments_shipments_edges_node_tracker_events[];
}

export interface GetSystemShipments_shipments_edges_node {
  id: string;
  tracking_number: string | null;
  recipient: GetSystemShipments_shipments_edges_node_recipient;
  shipper: GetSystemShipments_shipments_edges_node_shipper;
  status: ShipmentStatusEnum;
  service: string | null;
  carrier_name: string | null;
  carrier_id: string | null;
  created_at: any;
  updated_at: any;
  test_mode: boolean;
  meta: any | null;
  options: any;
  selected_rate: GetSystemShipments_shipments_edges_node_selected_rate | null;
  parcels: GetSystemShipments_shipments_edges_node_parcels[];
  messages: GetSystemShipments_shipments_edges_node_messages[];
  tracker: GetSystemShipments_shipments_edges_node_tracker | null;
}

export interface GetSystemShipments_shipments_edges {
  node: GetSystemShipments_shipments_edges_node;
}

export interface GetSystemShipments_shipments_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetSystemShipments_shipments {
  edges: GetSystemShipments_shipments_edges[];
  page_info: GetSystemShipments_shipments_page_info;
}

export interface GetSystemShipments {
  shipments: GetSystemShipments_shipments;
}

export interface GetSystemShipmentsVariables {
  filter?: SystemShipmentFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSystemTrackers
// ====================================================

export interface GetSystemTrackers_trackers_edges_node_info {
  customer_name: string | null;
  expected_delivery: string | null;
  note: string | null;
  order_date: string | null;
  order_id: string | null;
  package_weight: string | null;
  shipment_package_count: string | null;
  shipment_pickup_date: string | null;
  shipment_delivery_date: string | null;
  shipment_service: string | null;
  shipment_origin_country: string | null;
  shipment_origin_postal_code: string | null;
  shipment_destination_country: string | null;
  shipment_destination_postal_code: string | null;
}

export interface GetSystemTrackers_trackers_edges_node_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface GetSystemTrackers_trackers_edges_node_events {
  code: string | null;
  date: string | null;
  description: string | null;
  location: string | null;
  time: string | null;
}

export interface GetSystemTrackers_trackers_edges_node_shipment {
  id: string;
  service: string | null;
  status: ShipmentStatusEnum;
  meta: any | null;
}

export interface GetSystemTrackers_trackers_edges_node {
  id: string;
  tracking_number: string;
  carrier_name: string | null;
  carrier_id: string | null;
  status: TrackerStatusEnum;
  delivered: boolean | null;
  test_mode: boolean;
  created_at: any;
  updated_at: any;
  info: GetSystemTrackers_trackers_edges_node_info | null;
  meta: any | null;
  messages: GetSystemTrackers_trackers_edges_node_messages[];
  events: GetSystemTrackers_trackers_edges_node_events[];
  shipment: GetSystemTrackers_trackers_edges_node_shipment | null;
}

export interface GetSystemTrackers_trackers_edges {
  node: GetSystemTrackers_trackers_edges_node;
}

export interface GetSystemTrackers_trackers_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetSystemTrackers_trackers {
  edges: GetSystemTrackers_trackers_edges[];
  page_info: GetSystemTrackers_trackers_page_info;
}

export interface GetSystemTrackers {
  trackers: GetSystemTrackers_trackers;
}

export interface GetSystemTrackersVariables {
  filter?: SystemTrackerFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetAccountCarrierConnections
// ====================================================

export interface GetAccountCarrierConnections_carrier_connections_edges_node_usage {
  total_shipments: number | null;
  total_trackers: number | null;
  total_shipping_spend: number | null;
  total_addons_charges: number | null;
}

export interface GetAccountCarrierConnections_carrier_connections_edges_node {
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  active: boolean;
  test_mode: boolean;
  capabilities: string[];
  config: any | null;
  created_at: any | null;
  updated_at: any | null;
  usage: GetAccountCarrierConnections_carrier_connections_edges_node_usage;
}

export interface GetAccountCarrierConnections_carrier_connections_edges {
  node: GetAccountCarrierConnections_carrier_connections_edges_node;
}

export interface GetAccountCarrierConnections_carrier_connections_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetAccountCarrierConnections_carrier_connections {
  edges: GetAccountCarrierConnections_carrier_connections_edges[];
  page_info: GetAccountCarrierConnections_carrier_connections_page_info;
}

export interface GetAccountCarrierConnections {
  carrier_connections: GetAccountCarrierConnections_carrier_connections;
}

export interface GetAccountCarrierConnectionsVariables {
  filter?: AccountCarrierConnectionFilter | null;
  usageFilter?: UsageFilter | null;
}

/* tslint:disable */
// This file was automatically generated and should not be edited.

//==============================================================
// START Enums and Input Objects
//==============================================================

export enum CarrierNameEnum {
  aramex = "aramex",
  asendia = "asendia",
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
  dpd_meta = "dpd_meta",
  dtdc = "dtdc",
  easypost = "easypost",
  easyship = "easyship",
  eshipper = "eshipper",
  fedex = "fedex",
  freightcom = "freightcom",
  generic = "generic",
  geodis = "geodis",
  gls = "gls",
  hay_post = "hay_post",
  hermes = "hermes",
  landmark = "landmark",
  laposte = "laposte",
  locate2u = "locate2u",
  mydhl = "mydhl",
  nationex = "nationex",
  parcelone = "parcelone",
  postat = "postat",
  purolator = "purolator",
  roadie = "roadie",
  royalmail = "royalmail",
  sapient = "sapient",
  seko = "seko",
  sendle = "sendle",
  shipengine = "shipengine",
  spring = "spring",
  teleship = "teleship",
  tge = "tge",
  tnt = "tnt",
  ups = "ups",
  usps = "usps",
  usps_international = "usps_international",
  veho = "veho",
  zoom2u = "zoom2u",
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
  RON = "RON",
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

export enum DimensionUnitEnum {
  CM = "CM",
  IN = "IN",
}

export enum WeightUnitEnum {
  G = "G",
  KG = "KG",
  LB = "LB",
  OZ = "OZ",
}

export enum MarkupTypeEnum {
  AMOUNT = "AMOUNT",
  PERCENTAGE = "PERCENTAGE",
}

export enum UserRole {
  admin = "admin",
  developer = "developer",
  member = "member",
}

export enum ShipmentStatusEnum {
  cancelled = "cancelled",
  delivered = "delivered",
  delivery_failed = "delivery_failed",
  draft = "draft",
  in_transit = "in_transit",
  needs_attention = "needs_attention",
  out_for_delivery = "out_for_delivery",
  purchased = "purchased",
  shipped = "shipped",
}

export enum TrackerStatusEnum {
  cancelled = "cancelled",
  delivered = "delivered",
  delivery_delayed = "delivery_delayed",
  delivery_failed = "delivery_failed",
  in_transit = "in_transit",
  on_hold = "on_hold",
  out_for_delivery = "out_for_delivery",
  pending = "pending",
  picked_up = "picked_up",
  ready_for_pickup = "ready_for_pickup",
  return_to_sender = "return_to_sender",
  unknown = "unknown",
}

export enum OrderStatus {
  cancelled = "cancelled",
  delivered = "delivered",
  fulfilled = "fulfilled",
  partial = "partial",
  unfulfilled = "unfulfilled",
}

export enum CountryCodeEnum {
  AC = "AC",
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
  BL = "BL",
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
  EH = "EH",
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
  IM = "IM",
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
  MF = "MF",
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
  SX = "SX",
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
export interface UsageFilter {
  date_after?: string | null;
  date_before?: string | null;
  omit?: string[] | null;
  surcharge_id?: string | null;
}

// null
export interface CarrierFilter {
  offset?: number | null;
  first?: number | null;
  active?: boolean | null;
  metadata_key?: string | null;
  metadata_value?: string | null;
  carrier_name?: string[] | null;
}

// null
export interface RateSheetFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
}

// null
export interface MarkupFilter {
  offset?: number | null;
  first?: number | null;
  id?: string | null;
  name?: string | null;
  active?: boolean | null;
  markup_type?: MarkupTypeEnum | null;
  account_id?: string | null;
}

// null
export interface OrgUsageFilter {
  date_after?: string | null;
  date_before?: string | null;
  omit?: string[] | null;
  surcharge_id?: string | null;
  id: string;
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
export interface AccountCarrierConnectionFilter {
  offset?: number | null;
  first?: number | null;
  active?: boolean | null;
  metadata_key?: string | null;
  metadata_value?: string | null;
  carrier_name?: string[] | null;
  account_id?: string | null;
}

// null
export interface SystemShipmentFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
  address?: string | null;
  id?: string[] | null;
  created_after?: string | null;
  created_before?: string | null;
  carrier_name?: string[] | null;
  reference?: string | null;
  service?: string[] | null;
  status?: ShipmentStatusEnum[] | null;
  option_key?: string | null;
  option_value?: any | null;
  metadata_key?: string | null;
  metadata_value?: any | null;
  meta_key?: string | null;
  meta_value?: any | null;
  has_tracker?: boolean | null;
  has_manifest?: boolean | null;
  account_id?: string | null;
}

// null
export interface SystemTrackerFilter {
  offset?: number | null;
  first?: number | null;
  tracking_number?: string | null;
  created_after?: string | null;
  created_before?: string | null;
  carrier_name?: string[] | null;
  status?: string[] | null;
  account_id?: string | null;
}

// null
export interface SystemOrderFilter {
  offset?: number | null;
  first?: number | null;
  id?: string[] | null;
  keyword?: string | null;
  source?: string[] | null;
  order_id?: string[] | null;
  ontion_key?: string[] | null;
  address?: string[] | null;
  ontion_value?: string[] | null;
  metadata_key?: string[] | null;
  metadata_value?: string[] | null;
  status?: OrderStatus[] | null;
  account_id?: string | null;
}

// null
export interface CreateUserMutationInput {
  email: string;
  password1: string;
  password2: string;
  redirect_url?: string | null;
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
export interface InstanceConfigMutationInput {
  APP_NAME?: string | null;
  APP_WEBSITE?: string | null;
  EMAIL_USE_TLS?: boolean | null;
  EMAIL_HOST_USER?: string | null;
  EMAIL_HOST_PASSWORD?: string | null;
  EMAIL_HOST?: string | null;
  EMAIL_PORT?: number | null;
  EMAIL_FROM_ADDRESS?: string | null;
  GOOGLE_CLOUD_API_KEY?: string | null;
  CANADAPOST_ADDRESS_COMPLETE_API_KEY?: string | null;
  ORDER_DATA_RETENTION?: number | null;
  TRACKER_DATA_RETENTION?: number | null;
  SHIPMENT_DATA_RETENTION?: number | null;
  API_LOGS_DATA_RETENTION?: number | null;
  AUDIT_LOGGING?: boolean | null;
  ALLOW_SIGNUP?: boolean | null;
  ALLOW_ADMIN_APPROVED_SIGNUP?: boolean | null;
  ALLOW_MULTI_ACCOUNT?: boolean | null;
  ADMIN_DASHBOARD?: boolean | null;
  MULTI_ORGANIZATIONS?: boolean | null;
  ORDERS_MANAGEMENT?: boolean | null;
  APPS_MANAGEMENT?: boolean | null;
  DOCUMENTS_MANAGEMENT?: boolean | null;
  DATA_IMPORT_EXPORT?: boolean | null;
  WORKFLOW_MANAGEMENT?: boolean | null;
  SHIPPING_RULES?: boolean | null;
  PERSIST_SDK_TRACING?: boolean | null;
  ENABLE_ALL_PLUGINS_BY_DEFAULT?: boolean | null;
  ADDRESSCOMPLETE_ENABLED?: boolean | null;
  ALLIED_EXPRESS_ENABLED?: boolean | null;
  ALLIED_EXPRESS_LOCAL_ENABLED?: boolean | null;
  AMAZON_SHIPPING_ENABLED?: boolean | null;
  ARAMEX_ENABLED?: boolean | null;
  ASENDIA_ENABLED?: boolean | null;
  ASENDIA_US_ENABLED?: boolean | null;
  AUSTRALIAPOST_ENABLED?: boolean | null;
  BOXKNIGHT_ENABLED?: boolean | null;
  BPOST_ENABLED?: boolean | null;
  CANADAPOST_ENABLED?: boolean | null;
  CANPAR_ENABLED?: boolean | null;
  CHRONOPOST_ENABLED?: boolean | null;
  COLISSIMO_ENABLED?: boolean | null;
  DHL_EXPRESS_ENABLED?: boolean | null;
  DHL_PARCEL_DE_ENABLED?: boolean | null;
  DHL_POLAND_ENABLED?: boolean | null;
  DHL_UNIVERSAL_ENABLED?: boolean | null;
  DICOM_ENABLED?: boolean | null;
  DPD_ENABLED?: boolean | null;
  DPD_META_ENABLED?: boolean | null;
  DTDC_ENABLED?: boolean | null;
  EASYPOST_ENABLED?: boolean | null;
  EASYSHIP_ENABLED?: boolean | null;
  ESHIPPER_ENABLED?: boolean | null;
  FEDEX_ENABLED?: boolean | null;
  FREIGHTCOM_ENABLED?: boolean | null;
  GENERIC_ENABLED?: boolean | null;
  GEODIS_ENABLED?: boolean | null;
  GLS_ENABLED?: boolean | null;
  GOOGLEGEOCODING_ENABLED?: boolean | null;
  HAY_POST_ENABLED?: boolean | null;
  HERMES_ENABLED?: boolean | null;
  LANDMARK_ENABLED?: boolean | null;
  LAPOSTE_ENABLED?: boolean | null;
  LOCATE2U_ENABLED?: boolean | null;
  MYDHL_ENABLED?: boolean | null;
  NATIONEX_ENABLED?: boolean | null;
  PARCELONE_ENABLED?: boolean | null;
  POSTAT_ENABLED?: boolean | null;
  PUROLATOR_ENABLED?: boolean | null;
  ROADIE_ENABLED?: boolean | null;
  ROYALMAIL_ENABLED?: boolean | null;
  SAPIENT_ENABLED?: boolean | null;
  SEKO_ENABLED?: boolean | null;
  SENDLE_ENABLED?: boolean | null;
  SHIPENGINE_ENABLED?: boolean | null;
  SPRING_ENABLED?: boolean | null;
  TELESHIP_ENABLED?: boolean | null;
  TGE_ENABLED?: boolean | null;
  TNT_ENABLED?: boolean | null;
  UPS_ENABLED?: boolean | null;
  USPS_ENABLED?: boolean | null;
  USPS_INTERNATIONAL_ENABLED?: boolean | null;
  VEHO_ENABLED?: boolean | null;
  ZOOM2U_ENABLED?: boolean | null;
  DHL_PARCEL_DE_USERNAME?: string | null;
  DHL_PARCEL_DE_PASSWORD?: string | null;
  DHL_PARCEL_DE_CLIENT_ID?: string | null;
  DHL_PARCEL_DE_CLIENT_SECRET?: string | null;
  DHL_PARCEL_DE_SANDBOX_USERNAME?: string | null;
  DHL_PARCEL_DE_SANDBOX_PASSWORD?: string | null;
  DHL_PARCEL_DE_SANDBOX_CLIENT_ID?: string | null;
  DHL_PARCEL_DE_SANDBOX_CLIENT_SECRET?: string | null;
  TELESHIP_OAUTH_CLIENT_ID?: string | null;
  TELESHIP_OAUTH_CLIENT_SECRET?: string | null;
  TELESHIP_SANDBOX_OAUTH_CLIENT_ID?: string | null;
  TELESHIP_SANDBOX_OAUTH_CLIENT_SECRET?: string | null;
}

// null
export interface CreateConnectionMutationInput {
  carrier_name: CarrierNameEnum;
  carrier_id: string;
  credentials: any;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  capabilities?: string[] | null;
}

// null
export interface UpdateConnectionMutationInput {
  id: string;
  active?: boolean | null;
  carrier_id?: string | null;
  credentials?: any | null;
  config?: any | null;
  metadata?: any | null;
  capabilities?: string[] | null;
}

// null
export interface DeleteConnectionMutationInput {
  id: string;
}

// null
export interface CreateRateSheetMutationInput {
  name: string;
  carrier_name: CarrierNameEnum;
  services?: CreateServiceLevelInput[] | null;
  zones?: SharedZoneInput[] | null;
  surcharges?: SharedSurchargeInput[] | null;
  service_rates?: ServiceRateInput[] | null;
  carriers?: string[] | null;
  origin_countries?: string[] | null;
  metadata?: any | null;
}

// null
export interface CreateServiceLevelInput {
  service_name: string;
  service_code: string;
  currency: CurrencyCodeEnum;
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
  max_volume?: number | null;
  cost?: number | null;
  dim_factor?: number | null;
  use_volumetric?: boolean | null;
  domicile?: boolean | null;
  international?: boolean | null;
  features?: ServiceLevelFeaturesInput | null;
  zone_ids?: string[] | null;
  surcharge_ids?: string[] | null;
  metadata?: any | null;
}

// null
export interface ServiceLevelFeaturesInput {
  first_mile?: string | null;
  last_mile?: string | null;
  form_factor?: string | null;
  b2c?: boolean | null;
  b2b?: boolean | null;
  shipment_type?: string | null;
  age_check?: string | null;
  signature?: boolean | null;
  tracked?: boolean | null;
  insurance?: boolean | null;
  express?: boolean | null;
  dangerous_goods?: boolean | null;
  saturday_delivery?: boolean | null;
  sunday_delivery?: boolean | null;
  multicollo?: boolean | null;
  neighbor_delivery?: boolean | null;
}

// null
export interface SharedZoneInput {
  label: string;
  id?: string | null;
  country_codes?: string[] | null;
  postal_codes?: string[] | null;
  cities?: string[] | null;
  transit_days?: number | null;
  transit_time?: number | null;
  radius?: number | null;
  latitude?: number | null;
  longitude?: number | null;
  min_weight?: number | null;
  max_weight?: number | null;
  weight_unit?: WeightUnitEnum | null;
}

// null
export interface SharedSurchargeInput {
  name: string;
  amount: number;
  id?: string | null;
  surcharge_type?: string | null;
  cost?: number | null;
  active?: boolean | null;
}

// null
export interface ServiceRateInput {
  service_id: string;
  zone_id: string;
  rate: number;
  cost?: number | null;
  min_weight?: number | null;
  max_weight?: number | null;
  transit_days?: number | null;
  transit_time?: number | null;
}

// null
export interface UpdateRateSheetMutationInput {
  id: string;
  name?: string | null;
  services?: UpdateServiceLevelInput[] | null;
  zones?: SharedZoneInput[] | null;
  surcharges?: SharedSurchargeInput[] | null;
  service_rates?: ServiceRateInput[] | null;
  carriers?: string[] | null;
  origin_countries?: string[] | null;
  remove_missing_services?: boolean | null;
  metadata?: any | null;
}

// null
export interface UpdateServiceLevelInput {
  id?: string | null;
  service_name?: string | null;
  service_code?: string | null;
  currency?: CurrencyCodeEnum | null;
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
  max_volume?: number | null;
  cost?: number | null;
  dim_factor?: number | null;
  use_volumetric?: boolean | null;
  domicile?: boolean | null;
  international?: boolean | null;
  features?: ServiceLevelFeaturesInput | null;
  zone_ids?: string[] | null;
  surcharge_ids?: string[] | null;
  metadata?: any | null;
}

// null
export interface DeleteMutationInput {
  id: string;
}

// null
export interface DeleteRateSheetServiceMutationInput {
  rate_sheet_id: string;
  service_id: string;
}

// null
export interface AddSharedZoneMutationInput {
  rate_sheet_id: string;
  zone: SharedZoneInput;
}

// null
export interface UpdateSharedZoneMutationInput {
  rate_sheet_id: string;
  zone_id: string;
  zone: SharedZoneInput;
}

// null
export interface DeleteSharedZoneMutationInput {
  rate_sheet_id: string;
  zone_id: string;
}

// null
export interface AddSharedSurchargeMutationInput {
  rate_sheet_id: string;
  surcharge: SharedSurchargeInput;
}

// null
export interface UpdateSharedSurchargeMutationInput {
  rate_sheet_id: string;
  surcharge_id: string;
  surcharge: SharedSurchargeInput;
}

// null
export interface DeleteSharedSurchargeMutationInput {
  rate_sheet_id: string;
  surcharge_id: string;
}

// null
export interface BatchUpdateSurchargesMutationInput {
  rate_sheet_id: string;
  surcharges: SharedSurchargeInput[];
}

// null
export interface UpdateServiceRateMutationInput {
  rate_sheet_id: string;
  service_id: string;
  zone_id: string;
  rate: number;
  cost?: number | null;
  min_weight?: number | null;
  max_weight?: number | null;
  transit_days?: number | null;
  transit_time?: number | null;
}

// null
export interface BatchUpdateServiceRatesMutationInput {
  rate_sheet_id: string;
  rates: ServiceRateInput[];
}

// null
export interface AddWeightRangeMutationInput {
  rate_sheet_id: string;
  min_weight: number;
  max_weight: number;
}

// null
export interface RemoveWeightRangeMutationInput {
  rate_sheet_id: string;
  min_weight: number;
  max_weight: number;
}

// null
export interface DeleteServiceRateMutationInput {
  rate_sheet_id: string;
  service_id: string;
  zone_id: string;
  min_weight?: number | null;
  max_weight?: number | null;
}

// null
export interface UpdateServiceZoneIdsMutationInput {
  rate_sheet_id: string;
  service_id: string;
  zone_ids: string[];
}

// null
export interface UpdateServiceSurchargeIdsMutationInput {
  rate_sheet_id: string;
  service_id: string;
  surcharge_ids: string[];
}

// null
export interface CreateMarkupMutationInput {
  name: string;
  amount: number;
  markup_type: MarkupTypeEnum;
  active?: boolean | null;
  is_visible?: boolean | null;
  carrier_codes?: string[] | null;
  service_codes?: string[] | null;
  connection_ids?: string[] | null;
  organizations?: string[] | null;
  metadata?: any | null;
}

// null
export interface UpdateMarkupMutationInput {
  id: string;
  name?: string | null;
  amount?: number | null;
  markup_type?: MarkupTypeEnum | null;
  active?: boolean | null;
  is_visible?: boolean | null;
  carrier_codes?: string[] | null;
  service_codes?: string[] | null;
  connection_ids?: string[] | null;
  organizations?: string[] | null;
  metadata?: any | null;
}

// null
export interface CreateOrganizationAccountMutationInput {
  name: string;
  slug?: string | null;
  is_active?: boolean | null;
}

// null
export interface UpdateOrganizationAccountMutationInput {
  id: string;
  name?: string | null;
  slug?: string | null;
  is_active?: boolean | null;
}

// null
export interface DisableOrganizationAccountMutationInput {
  id: string;
}

// null
export interface DeleteOrganizationAccountMutationInput {
  id: string;
}

// null
export interface InviteOrganizationUserMutationInput {
  email: string;
  roles: UserRole[];
  is_owner: boolean;
}

//==============================================================
// END Enums and Input Objects
//==============================================================