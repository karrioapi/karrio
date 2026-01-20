

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
// GraphQL query operation: get_addresses
// ====================================================

export interface get_addresses_addresses_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_addresses_addresses_edges_node {
  id: string;
  object_type: string;
  company_name: string | null;
  person_name: string | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  postal_code: string | null;
  residential: boolean | null;
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
  meta: any | null;
}

export interface get_addresses_addresses_edges {
  node: get_addresses_addresses_edges_node;
}

export interface get_addresses_addresses {
  page_info: get_addresses_addresses_page_info;
  edges: get_addresses_addresses_edges[];
}

export interface get_addresses {
  addresses: get_addresses_addresses;
}

export interface get_addressesVariables {
  filter?: AddressFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_default_templates
// ====================================================

export interface get_default_templates_default_templates_default_address {
  id: string;
  object_type: string;
  company_name: string | null;
  person_name: string | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  postal_code: string | null;
  residential: boolean | null;
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
  meta: any | null;
}

export interface get_default_templates_default_templates_default_parcel {
  id: string;
  object_type: string;
  width: number | null;
  height: number | null;
  length: number | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  is_document: boolean | null;
  meta: any | null;
}

export interface get_default_templates_default_templates {
  default_address: get_default_templates_default_templates_default_address | null;
  default_parcel: get_default_templates_default_templates_default_parcel | null;
}

export interface get_default_templates {
  default_templates: get_default_templates_default_templates;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: create_connection
// ====================================================

export interface create_connection_create_carrier_connection_errors {
  field: string;
  messages: string[];
}

export interface create_connection_create_carrier_connection {
  errors: create_connection_create_carrier_connection_errors[] | null;
}

export interface create_connection {
  create_carrier_connection: create_connection_create_carrier_connection;
}

export interface create_connectionVariables {
  data: CreateCarrierConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_connection
// ====================================================

export interface update_connection_update_carrier_connection_errors {
  field: string;
  messages: string[];
}

export interface update_connection_update_carrier_connection {
  errors: update_connection_update_carrier_connection_errors[] | null;
}

export interface update_connection {
  update_carrier_connection: update_connection_update_carrier_connection;
}

export interface update_connectionVariables {
  data: UpdateCarrierConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: delete_connection
// ====================================================

export interface delete_connection_delete_carrier_connection {
  id: string;
}

export interface delete_connection {
  delete_carrier_connection: delete_connection_delete_carrier_connection;
}

export interface delete_connectionVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_log
// ====================================================

export interface get_log_log_records {
  id: string | null;
  key: string | null;
  timestamp: number | null;
  test_mode: boolean | null;
  created_at: any | null;
  meta: any | null;
  record: any | null;
}

export interface get_log_log {
  id: number;
  requested_at: any | null;
  response_ms: number | null;
  path: string | null;
  remote_addr: string | null;
  host: string | null;
  method: string | null;
  query_params: any | null;
  data: any | null;
  response: any | null;
  status_code: number | null;
  records: get_log_log_records[];
}

export interface get_log {
  log: get_log_log | null;
}

export interface get_logVariables {
  id: number;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_logs
// ====================================================

export interface get_logs_logs_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_logs_logs_edges_node_records {
  id: string | null;
  key: string | null;
  timestamp: number | null;
  test_mode: boolean | null;
  created_at: any | null;
  meta: any | null;
  record: any | null;
}

export interface get_logs_logs_edges_node {
  id: number;
  path: string | null;
  host: string | null;
  data: any | null;
  method: string | null;
  response_ms: number | null;
  remote_addr: string | null;
  requested_at: any | null;
  status_code: number | null;
  query_params: any | null;
  response: any | null;
  records: get_logs_logs_edges_node_records[];
}

export interface get_logs_logs_edges {
  node: get_logs_logs_edges_node;
}

export interface get_logs_logs {
  page_info: get_logs_logs_page_info;
  edges: get_logs_logs_edges[];
}

export interface get_logs {
  logs: get_logs_logs;
}

export interface get_logsVariables {
  filter?: LogFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_shipment
// ====================================================

export interface get_shipment_shipment_created_by {
  email: string;
  full_name: string;
}

export interface get_shipment_shipment_recipient {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_shipment_shipper {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_shipment_return_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_shipment_billing_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_shipment_parcels_items {
  id: string | null;
  weight: number | null;
  title: string | null;
  description: string | null;
  quantity: number | null;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  weight_unit: WeightUnitEnum | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
  parent_id: string | null;
}

export interface get_shipment_shipment_parcels {
  id: string | null;
  width: number | null;
  height: number | null;
  length: number | null;
  is_document: boolean | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  freight_class: string | null;
  reference_number: string | null;
  description: string | null;
  items: get_shipment_shipment_parcels_items[] | null;
}

export interface get_shipment_shipment_customs_duty_bill_to {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_shipment_shipment_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
  bill_to: get_shipment_shipment_customs_duty_bill_to | null;
}

export interface get_shipment_shipment_customs_duty_billing_address {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_shipment_shipment_customs_commodities {
  id: string | null;
  sku: string | null;
  hs_code: string | null;
  quantity: number | null;
  description: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
}

export interface get_shipment_shipment_customs {
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  options: any | null;
  duty: get_shipment_shipment_customs_duty | null;
  duty_billing_address: get_shipment_shipment_customs_duty_billing_address | null;
  commodities: get_shipment_shipment_customs_commodities[] | null;
}

export interface get_shipment_shipment_payment {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
}

export interface get_shipment_shipment_selected_rate_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface get_shipment_shipment_selected_rate {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: get_shipment_shipment_selected_rate_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface get_shipment_shipment_rates_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface get_shipment_shipment_rates {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: get_shipment_shipment_rates_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface get_shipment_shipment_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface get_shipment_shipment_selected_rate_carrier {
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  config: any | null;
}

export interface get_shipment_shipment_tracker_events {
  description: string | null;
  location: string | null;
  code: string | null;
  date: string | null;
  time: string | null;
  latitude: number | null;
  longitude: number | null;
}

export interface get_shipment_shipment_tracker_info {
  carrier_tracking_link: string | null;
  customer_name: string | null;
  expected_delivery: string | null;
  note: string | null;
  order_date: string | null;
  order_id: string | null;
  package_weight: string | null;
  package_weight_unit: string | null;
  shipment_package_count: string | null;
  shipment_pickup_date: string | null;
  shipment_service: string | null;
  shipment_delivery_date: string | null;
  shipment_origin_country: string | null;
  shipment_origin_postal_code: string | null;
  shipment_destination_country: string | null;
  shipment_destination_postal_code: string | null;
  shipping_date: string | null;
  signed_by: string | null;
  source: string | null;
}

export interface get_shipment_shipment_tracker_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface get_shipment_shipment_tracker {
  id: string;
  tracking_number: string;
  carrier_id: string;
  carrier_name: string;
  status: TrackerStatusEnum;
  events: get_shipment_shipment_tracker_events[];
  delivered: boolean | null;
  estimated_delivery: any | null;
  meta: any | null;
  metadata: any;
  info: get_shipment_shipment_tracker_info | null;
  messages: get_shipment_shipment_tracker_messages[];
  updated_at: any;
}

export interface get_shipment_shipment {
  id: string;
  carrier_id: string | null;
  carrier_name: string | null;
  created_at: any;
  updated_at: any;
  created_by: get_shipment_shipment_created_by;
  status: ShipmentStatusEnum;
  recipient: get_shipment_shipment_recipient;
  shipper: get_shipment_shipment_shipper;
  return_address: get_shipment_shipment_return_address | null;
  billing_address: get_shipment_shipment_billing_address | null;
  parcels: get_shipment_shipment_parcels[];
  label_type: LabelTypeEnum | null;
  tracking_number: string | null;
  shipment_identifier: string | null;
  label_url: string | null;
  invoice_url: string | null;
  tracking_url: string | null;
  tracker_id: string | null;
  test_mode: boolean;
  service: string | null;
  reference: string | null;
  customs: get_shipment_shipment_customs | null;
  payment: get_shipment_shipment_payment | null;
  selected_rate_id: string | null;
  selected_rate: get_shipment_shipment_selected_rate | null;
  carrier_ids: string[];
  rates: get_shipment_shipment_rates[];
  options: any;
  metadata: any;
  meta: any | null;
  messages: get_shipment_shipment_messages[];
  selected_rate_carrier: get_shipment_shipment_selected_rate_carrier | null;
  tracker: get_shipment_shipment_tracker | null;
}

export interface get_shipment {
  shipment: get_shipment_shipment | null;
}

export interface get_shipmentVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_shipments
// ====================================================

export interface get_shipments_shipments_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_shipments_shipments_edges_node_created_by {
  email: string;
  full_name: string;
}

export interface get_shipments_shipments_edges_node_recipient {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipments_shipments_edges_node_shipper {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipments_shipments_edges_node_return_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipments_shipments_edges_node_billing_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipments_shipments_edges_node_parcels_items {
  id: string | null;
  weight: number | null;
  title: string | null;
  description: string | null;
  quantity: number | null;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  weight_unit: WeightUnitEnum | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
  parent_id: string | null;
}

export interface get_shipments_shipments_edges_node_parcels {
  id: string | null;
  width: number | null;
  height: number | null;
  length: number | null;
  is_document: boolean | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  freight_class: string | null;
  reference_number: string | null;
  description: string | null;
  items: get_shipments_shipments_edges_node_parcels_items[] | null;
}

export interface get_shipments_shipments_edges_node_customs_duty_bill_to {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_shipments_shipments_edges_node_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
  bill_to: get_shipments_shipments_edges_node_customs_duty_bill_to | null;
}

export interface get_shipments_shipments_edges_node_customs_duty_billing_address {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_shipments_shipments_edges_node_customs_commodities {
  id: string | null;
  sku: string | null;
  hs_code: string | null;
  quantity: number | null;
  description: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
}

export interface get_shipments_shipments_edges_node_customs {
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  options: any | null;
  duty: get_shipments_shipments_edges_node_customs_duty | null;
  duty_billing_address: get_shipments_shipments_edges_node_customs_duty_billing_address | null;
  commodities: get_shipments_shipments_edges_node_customs_commodities[] | null;
}

export interface get_shipments_shipments_edges_node_payment {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
}

export interface get_shipments_shipments_edges_node_selected_rate_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface get_shipments_shipments_edges_node_selected_rate {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: get_shipments_shipments_edges_node_selected_rate_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface get_shipments_shipments_edges_node_rates_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface get_shipments_shipments_edges_node_rates {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: get_shipments_shipments_edges_node_rates_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface get_shipments_shipments_edges_node_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface get_shipments_shipments_edges_node_selected_rate_carrier {
  carrier_id: string;
  carrier_name: string;
  config: any | null;
}

export interface get_shipments_shipments_edges_node {
  id: string;
  carrier_id: string | null;
  carrier_name: string | null;
  created_at: any;
  updated_at: any;
  created_by: get_shipments_shipments_edges_node_created_by;
  status: ShipmentStatusEnum;
  recipient: get_shipments_shipments_edges_node_recipient;
  shipper: get_shipments_shipments_edges_node_shipper;
  return_address: get_shipments_shipments_edges_node_return_address | null;
  billing_address: get_shipments_shipments_edges_node_billing_address | null;
  parcels: get_shipments_shipments_edges_node_parcels[];
  label_type: LabelTypeEnum | null;
  tracking_number: string | null;
  shipment_identifier: string | null;
  label_url: string | null;
  invoice_url: string | null;
  tracking_url: string | null;
  tracker_id: string | null;
  test_mode: boolean;
  service: string | null;
  reference: string | null;
  customs: get_shipments_shipments_edges_node_customs | null;
  payment: get_shipments_shipments_edges_node_payment | null;
  selected_rate_id: string | null;
  selected_rate: get_shipments_shipments_edges_node_selected_rate | null;
  carrier_ids: string[];
  rates: get_shipments_shipments_edges_node_rates[];
  options: any;
  metadata: any;
  meta: any | null;
  messages: get_shipments_shipments_edges_node_messages[];
  selected_rate_carrier: get_shipments_shipments_edges_node_selected_rate_carrier | null;
}

export interface get_shipments_shipments_edges {
  node: get_shipments_shipments_edges_node;
}

export interface get_shipments_shipments {
  page_info: get_shipments_shipments_page_info;
  edges: get_shipments_shipments_edges[];
}

export interface get_shipments {
  shipments: get_shipments_shipments;
}

export interface get_shipmentsVariables {
  filter?: ShipmentFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_shipment_data
// ====================================================

export interface get_shipment_data_shipment_recipient {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_data_shipment_shipper {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_data_shipment_return_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_data_shipment_billing_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_data_shipment_parcels_items {
  id: string | null;
  weight: number | null;
  title: string | null;
  description: string | null;
  quantity: number | null;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  weight_unit: WeightUnitEnum | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
  parent_id: string | null;
}

export interface get_shipment_data_shipment_parcels {
  id: string | null;
  width: number | null;
  height: number | null;
  length: number | null;
  is_document: boolean | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  freight_class: string | null;
  reference_number: string | null;
  description: string | null;
  items: get_shipment_data_shipment_parcels_items[] | null;
}

export interface get_shipment_data_shipment_customs_duty_bill_to {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_shipment_data_shipment_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
  bill_to: get_shipment_data_shipment_customs_duty_bill_to | null;
}

export interface get_shipment_data_shipment_customs_duty_billing_address {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_shipment_data_shipment_customs_commodities {
  id: string | null;
  sku: string | null;
  hs_code: string | null;
  quantity: number | null;
  description: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
}

export interface get_shipment_data_shipment_customs {
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  options: any | null;
  duty: get_shipment_data_shipment_customs_duty | null;
  duty_billing_address: get_shipment_data_shipment_customs_duty_billing_address | null;
  commodities: get_shipment_data_shipment_customs_commodities[] | null;
}

export interface get_shipment_data_shipment_payment {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
}

export interface get_shipment_data_shipment_rates_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface get_shipment_data_shipment_rates {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: get_shipment_data_shipment_rates_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface get_shipment_data_shipment_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface get_shipment_data_shipment {
  id: string;
  status: ShipmentStatusEnum;
  recipient: get_shipment_data_shipment_recipient;
  shipper: get_shipment_data_shipment_shipper;
  return_address: get_shipment_data_shipment_return_address | null;
  billing_address: get_shipment_data_shipment_billing_address | null;
  parcels: get_shipment_data_shipment_parcels[];
  label_type: LabelTypeEnum | null;
  service: string | null;
  reference: string | null;
  customs: get_shipment_data_shipment_customs | null;
  payment: get_shipment_data_shipment_payment | null;
  carrier_ids: string[];
  options: any;
  metadata: any;
  rates: get_shipment_data_shipment_rates[];
  messages: get_shipment_data_shipment_messages[];
}

export interface get_shipment_data {
  shipment: get_shipment_data_shipment | null;
}

export interface get_shipment_dataVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: partial_shipment_update
// ====================================================

export interface partial_shipment_update_partial_shipment_update_shipment_recipient {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_shipper {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_return_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_billing_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_parcels_items {
  id: string | null;
  weight: number | null;
  title: string | null;
  description: string | null;
  quantity: number | null;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  weight_unit: WeightUnitEnum | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
  parent_id: string | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_parcels {
  id: string | null;
  width: number | null;
  height: number | null;
  length: number | null;
  is_document: boolean | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  freight_class: string | null;
  reference_number: string | null;
  description: string | null;
  items: partial_shipment_update_partial_shipment_update_shipment_parcels_items[] | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_customs_duty_bill_to {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
  bill_to: partial_shipment_update_partial_shipment_update_shipment_customs_duty_bill_to | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_customs_duty_billing_address {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_customs_commodities {
  id: string | null;
  sku: string | null;
  hs_code: string | null;
  quantity: number | null;
  description: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_customs {
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  options: any | null;
  duty: partial_shipment_update_partial_shipment_update_shipment_customs_duty | null;
  duty_billing_address: partial_shipment_update_partial_shipment_update_shipment_customs_duty_billing_address | null;
  commodities: partial_shipment_update_partial_shipment_update_shipment_customs_commodities[] | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_payment {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_rates_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface partial_shipment_update_partial_shipment_update_shipment_rates {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: partial_shipment_update_partial_shipment_update_shipment_rates_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment {
  id: string;
  status: ShipmentStatusEnum;
  recipient: partial_shipment_update_partial_shipment_update_shipment_recipient;
  shipper: partial_shipment_update_partial_shipment_update_shipment_shipper;
  return_address: partial_shipment_update_partial_shipment_update_shipment_return_address | null;
  billing_address: partial_shipment_update_partial_shipment_update_shipment_billing_address | null;
  parcels: partial_shipment_update_partial_shipment_update_shipment_parcels[];
  label_type: LabelTypeEnum | null;
  service: string | null;
  reference: string | null;
  customs: partial_shipment_update_partial_shipment_update_shipment_customs | null;
  payment: partial_shipment_update_partial_shipment_update_shipment_payment | null;
  carrier_ids: string[];
  options: any;
  metadata: any;
  rates: partial_shipment_update_partial_shipment_update_shipment_rates[];
  messages: partial_shipment_update_partial_shipment_update_shipment_messages[];
}

export interface partial_shipment_update_partial_shipment_update_errors {
  field: string;
  messages: string[];
}

export interface partial_shipment_update_partial_shipment_update {
  shipment: partial_shipment_update_partial_shipment_update_shipment | null;
  errors: partial_shipment_update_partial_shipment_update_errors[] | null;
}

export interface partial_shipment_update {
  partial_shipment_update: partial_shipment_update_partial_shipment_update;
}

export interface partial_shipment_updateVariables {
  data: PartialShipmentMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: change_shipment_status
// ====================================================

export interface change_shipment_status_change_shipment_status_shipment {
  id: string;
}

export interface change_shipment_status_change_shipment_status_errors {
  field: string;
  messages: string[];
}

export interface change_shipment_status_change_shipment_status {
  shipment: change_shipment_status_change_shipment_status_shipment | null;
  errors: change_shipment_status_change_shipment_status_errors[] | null;
}

export interface change_shipment_status {
  change_shipment_status: change_shipment_status_change_shipment_status;
}

export interface change_shipment_statusVariables {
  data: ChangeShipmentStatusMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_tracker
// ====================================================

export interface get_tracker_tracker_events {
  description: string | null;
  location: string | null;
  code: string | null;
  date: string | null;
  time: string | null;
  latitude: number | null;
  longitude: number | null;
}

export interface get_tracker_tracker_info {
  carrier_tracking_link: string | null;
  customer_name: string | null;
  expected_delivery: string | null;
  note: string | null;
  order_date: string | null;
  order_id: string | null;
  package_weight: string | null;
  package_weight_unit: string | null;
  shipment_package_count: string | null;
  shipment_pickup_date: string | null;
  shipment_service: string | null;
  shipment_delivery_date: string | null;
  shipment_origin_country: string | null;
  shipment_origin_postal_code: string | null;
  shipment_destination_country: string | null;
  shipment_destination_postal_code: string | null;
  shipping_date: string | null;
  signed_by: string | null;
  source: string | null;
}

export interface get_tracker_tracker_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface get_tracker_tracker_created_by {
  email: string;
  full_name: string;
}

export interface get_tracker_tracker_tracking_carrier {
  carrier_id: string;
  carrier_name: string;
  config: any | null;
}

export interface get_tracker_tracker_shipment_shipper {
  city: string | null;
  country_code: CountryCodeEnum | null;
}

export interface get_tracker_tracker_shipment_recipient {
  city: string | null;
  country_code: CountryCodeEnum | null;
}

export interface get_tracker_tracker_shipment {
  id: string;
  service: string | null;
  shipper: get_tracker_tracker_shipment_shipper;
  recipient: get_tracker_tracker_shipment_recipient;
  meta: any | null;
  reference: string | null;
}

export interface get_tracker_tracker {
  id: string;
  tracking_number: string;
  carrier_id: string;
  carrier_name: string;
  status: TrackerStatusEnum;
  events: get_tracker_tracker_events[];
  delivered: boolean | null;
  estimated_delivery: any | null;
  meta: any | null;
  metadata: any;
  info: get_tracker_tracker_info | null;
  messages: get_tracker_tracker_messages[];
  created_at: any;
  updated_at: any;
  created_by: get_tracker_tracker_created_by;
  test_mode: boolean;
  tracking_carrier: get_tracker_tracker_tracking_carrier | null;
  shipment: get_tracker_tracker_shipment | null;
}

export interface get_tracker {
  tracker: get_tracker_tracker | null;
}

export interface get_trackerVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_trackers
// ====================================================

export interface get_trackers_trackers_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_trackers_trackers_edges_node_created_by {
  email: string;
  full_name: string;
}

export interface get_trackers_trackers_edges_node_events {
  description: string | null;
  location: string | null;
  code: string | null;
  date: string | null;
  time: string | null;
  latitude: number | null;
  longitude: number | null;
}

export interface get_trackers_trackers_edges_node_info {
  carrier_tracking_link: string | null;
  customer_name: string | null;
  expected_delivery: string | null;
  note: string | null;
  order_date: string | null;
  order_id: string | null;
  package_weight: string | null;
  package_weight_unit: string | null;
  shipment_package_count: string | null;
  shipment_pickup_date: string | null;
  shipment_service: string | null;
  shipment_delivery_date: string | null;
  shipment_origin_country: string | null;
  shipment_origin_postal_code: string | null;
  shipment_destination_country: string | null;
  shipment_destination_postal_code: string | null;
  shipping_date: string | null;
  signed_by: string | null;
  source: string | null;
}

export interface get_trackers_trackers_edges_node_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface get_trackers_trackers_edges_node_tracking_carrier {
  carrier_id: string;
  carrier_name: string;
  config: any | null;
}

export interface get_trackers_trackers_edges_node_shipment_shipper {
  city: string | null;
  country_code: CountryCodeEnum | null;
}

export interface get_trackers_trackers_edges_node_shipment_recipient {
  city: string | null;
  country_code: CountryCodeEnum | null;
}

export interface get_trackers_trackers_edges_node_shipment {
  id: string;
  service: string | null;
  shipper: get_trackers_trackers_edges_node_shipment_shipper;
  recipient: get_trackers_trackers_edges_node_shipment_recipient;
  meta: any | null;
  reference: string | null;
}

export interface get_trackers_trackers_edges_node {
  id: string;
  created_at: any;
  updated_at: any;
  created_by: get_trackers_trackers_edges_node_created_by;
  status: TrackerStatusEnum;
  tracking_number: string;
  events: get_trackers_trackers_edges_node_events[];
  delivered: boolean | null;
  estimated_delivery: any | null;
  test_mode: boolean;
  info: get_trackers_trackers_edges_node_info | null;
  messages: get_trackers_trackers_edges_node_messages[];
  carrier_id: string;
  carrier_name: string;
  meta: any | null;
  metadata: any;
  tracking_carrier: get_trackers_trackers_edges_node_tracking_carrier | null;
  shipment: get_trackers_trackers_edges_node_shipment | null;
}

export interface get_trackers_trackers_edges {
  node: get_trackers_trackers_edges_node;
}

export interface get_trackers_trackers {
  page_info: get_trackers_trackers_page_info;
  edges: get_trackers_trackers_edges[];
}

export interface get_trackers {
  trackers: get_trackers_trackers;
}

export interface get_trackersVariables {
  filter?: TrackerFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_webhook
// ====================================================

export interface get_webhook_webhook_created_by {
  email: string;
  full_name: string;
}

export interface get_webhook_webhook {
  id: string;
  created_by: get_webhook_webhook_created_by | null;
  enabled_events: EventTypes[];
  url: string | null;
  test_mode: boolean | null;
  disabled: boolean | null;
  description: string | null;
  last_event_at: any | null;
  secret: string | null;
}

export interface get_webhook {
  webhook: get_webhook_webhook;
}

export interface get_webhookVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_webhooks
// ====================================================

export interface get_webhooks_webhooks_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_webhooks_webhooks_edges_node_created_by {
  email: string;
  full_name: string;
}

export interface get_webhooks_webhooks_edges_node {
  id: string;
  created_at: any | null;
  updated_at: any | null;
  created_by: get_webhooks_webhooks_edges_node_created_by | null;
  enabled_events: EventTypes[];
  url: string | null;
  test_mode: boolean | null;
  disabled: boolean | null;
  description: string | null;
  last_event_at: any | null;
  secret: string | null;
}

export interface get_webhooks_webhooks_edges {
  node: get_webhooks_webhooks_edges_node;
}

export interface get_webhooks_webhooks {
  page_info: get_webhooks_webhooks_page_info;
  edges: get_webhooks_webhooks_edges[];
}

export interface get_webhooks {
  webhooks: get_webhooks_webhooks;
}

export interface get_webhooksVariables {
  filter?: WebhookFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_parcels
// ====================================================

export interface get_parcels_parcels_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_parcels_parcels_edges_node {
  id: string;
  object_type: string;
  width: number | null;
  height: number | null;
  length: number | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  is_document: boolean | null;
  meta: any | null;
}

export interface get_parcels_parcels_edges {
  node: get_parcels_parcels_edges_node;
}

export interface get_parcels_parcels {
  page_info: get_parcels_parcels_page_info;
  edges: get_parcels_parcels_edges[];
}

export interface get_parcels {
  parcels: get_parcels_parcels;
}

export interface get_parcelsVariables {
  filter?: TemplateFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_system_connections
// ====================================================

export interface get_system_connections_system_connections_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_system_connections_system_connections_edges_node {
  id: string;
  carrier_id: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  carrier_name: string;
  display_name: string;
  enabled: boolean;
  created_at: any | null;
  updated_at: any | null;
}

export interface get_system_connections_system_connections_edges {
  node: get_system_connections_system_connections_edges_node;
}

export interface get_system_connections_system_connections {
  page_info: get_system_connections_system_connections_page_info;
  edges: get_system_connections_system_connections_edges[];
}

export interface get_system_connections {
  system_connections: get_system_connections_system_connections;
}

export interface get_system_connectionsVariables {
  filter?: CarrierFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: mutate_system_connection
// ====================================================

export interface mutate_system_connection_mutate_system_connection_carrier {
  id: string;
  active: boolean;
}

export interface mutate_system_connection_mutate_system_connection {
  carrier: mutate_system_connection_mutate_system_connection_carrier | null;
}

export interface mutate_system_connection {
  mutate_system_connection: mutate_system_connection_mutate_system_connection;
}

export interface mutate_system_connectionVariables {
  data: SystemCarrierMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: delete_address
// ====================================================

export interface delete_address_delete_address {
  id: string;
}

export interface delete_address {
  delete_address: delete_address_delete_address;
}

export interface delete_addressVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: delete_parcel
// ====================================================

export interface delete_parcel_delete_parcel {
  id: string;
}

export interface delete_parcel {
  delete_parcel: delete_parcel_delete_parcel;
}

export interface delete_parcelVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: create_parcel
// ====================================================

export interface create_parcel_create_parcel_parcel {
  id: string;
}

export interface create_parcel_create_parcel_errors {
  field: string;
  messages: string[];
}

export interface create_parcel_create_parcel {
  parcel: create_parcel_create_parcel_parcel | null;
  errors: create_parcel_create_parcel_errors[] | null;
}

export interface create_parcel {
  create_parcel: create_parcel_create_parcel;
}

export interface create_parcelVariables {
  data: CreateParcelInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_parcel
// ====================================================

export interface update_parcel_update_parcel_parcel {
  id: string;
}

export interface update_parcel_update_parcel_errors {
  field: string;
  messages: string[];
}

export interface update_parcel_update_parcel {
  parcel: update_parcel_update_parcel_parcel | null;
  errors: update_parcel_update_parcel_errors[] | null;
}

export interface update_parcel {
  update_parcel: update_parcel_update_parcel;
}

export interface update_parcelVariables {
  data: UpdateParcelInput2;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: create_address
// ====================================================

export interface create_address_create_address_address {
  id: string;
}

export interface create_address_create_address_errors {
  field: string;
  messages: string[];
}

export interface create_address_create_address {
  address: create_address_create_address_address | null;
  errors: create_address_create_address_errors[] | null;
}

export interface create_address {
  create_address: create_address_create_address;
}

export interface create_addressVariables {
  data: CreateAddressInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_address
// ====================================================

export interface update_address_update_address_address {
  id: string;
}

export interface update_address_update_address_errors {
  field: string;
  messages: string[];
}

export interface update_address_update_address {
  address: update_address_update_address_address | null;
  errors: update_address_update_address_errors[] | null;
}

export interface update_address {
  update_address: update_address_update_address;
}

export interface update_addressVariables {
  data: UpdateAddressInput2;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_products
// ====================================================

export interface get_products_products_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_products_products_edges_node {
  id: string;
  object_type: string;
  weight: number;
  weight_unit: WeightUnitEnum | null;
  quantity: number;
  sku: string | null;
  title: string | null;
  hs_code: string | null;
  description: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
  meta: any | null;
  created_at: any | null;
  updated_at: any | null;
}

export interface get_products_products_edges {
  node: get_products_products_edges_node;
}

export interface get_products_products {
  page_info: get_products_products_page_info;
  edges: get_products_products_edges[];
}

export interface get_products {
  products: get_products_products;
}

export interface get_productsVariables {
  filter?: ProductFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: create_product
// ====================================================

export interface create_product_create_product_product {
  id: string;
}

export interface create_product_create_product_errors {
  field: string;
  messages: string[];
}

export interface create_product_create_product {
  product: create_product_create_product_product | null;
  errors: create_product_create_product_errors[] | null;
}

export interface create_product {
  create_product: create_product_create_product;
}

export interface create_productVariables {
  data: CreateProductInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_product
// ====================================================

export interface update_product_update_product_product {
  id: string;
}

export interface update_product_update_product_errors {
  field: string;
  messages: string[];
}

export interface update_product_update_product {
  product: update_product_update_product_product | null;
  errors: update_product_update_product_errors[] | null;
}

export interface update_product {
  update_product: update_product_update_product;
}

export interface update_productVariables {
  data: UpdateProductInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: delete_product
// ====================================================

export interface delete_product_delete_product {
  id: string;
}

export interface delete_product {
  delete_product: delete_product_delete_product;
}

export interface delete_productVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: discard_commodity
// ====================================================

export interface discard_commodity_discard_commodity {
  id: string;
}

export interface discard_commodity {
  discard_commodity: discard_commodity_discard_commodity;
}

export interface discard_commodityVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: discard_parcel
// ====================================================

export interface discard_parcel_discard_parcel {
  id: string;
}

export interface discard_parcel {
  discard_parcel: discard_parcel_discard_parcel;
}

export interface discard_parcelVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: mutate_token
// ====================================================

export interface mutate_token_mutate_token_token {
  key: string;
}

export interface mutate_token_mutate_token {
  token: mutate_token_mutate_token_token | null;
}

export interface mutate_token {
  mutate_token: mutate_token_mutate_token;
}

export interface mutate_tokenVariables {
  data: TokenMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetToken
// ====================================================

export interface GetToken_token {
  key: string;
  created: any;
}

export interface GetToken {
  token: GetToken_token;
}

export interface GetTokenVariables {
  org_id?: string | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_user_connections
// ====================================================

export interface get_user_connections_user_connections_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_user_connections_user_connections_edges_node_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface get_user_connections_user_connections_edges_node {
  id: string;
  carrier_id: string;
  carrier_name: string;
  display_name: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  credentials: any;
  metadata: any | null;
  config: any | null;
  rate_sheet: get_user_connections_user_connections_edges_node_rate_sheet | null;
}

export interface get_user_connections_user_connections_edges {
  node: get_user_connections_user_connections_edges_node;
}

export interface get_user_connections_user_connections {
  page_info: get_user_connections_user_connections_page_info;
  edges: get_user_connections_user_connections_edges[];
}

export interface get_user_connections {
  user_connections: get_user_connections_user_connections;
}

export interface get_user_connectionsVariables {
  filter?: CarrierFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetUser
// ====================================================

export interface GetUser_user {
  email: string;
  full_name: string;
  is_staff: boolean;
  is_superuser: boolean | null;
  last_login: any | null;
  date_joined: any;
  permissions: string[] | null;
}

export interface GetUser {
  user: GetUser_user;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_user
// ====================================================

export interface update_user_update_user_user {
  email: string;
  full_name: string;
  is_staff: boolean;
  is_superuser: boolean | null;
  last_login: any | null;
  date_joined: any;
  permissions: string[] | null;
}

export interface update_user_update_user_errors {
  field: string;
  messages: string[];
}

export interface update_user_update_user {
  user: update_user_update_user_user | null;
  errors: update_user_update_user_errors[] | null;
}

export interface update_user {
  update_user: update_user_update_user;
}

export interface update_userVariables {
  data: UpdateUserInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: change_password
// ====================================================

export interface change_password_change_password_errors {
  field: string;
  messages: string[];
}

export interface change_password_change_password {
  errors: change_password_change_password_errors[] | null;
}

export interface change_password {
  change_password: change_password_change_password;
}

export interface change_passwordVariables {
  data: ChangePasswordMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: register_user
// ====================================================

export interface register_user_register_user_user {
  email: string;
  is_staff: boolean;
  date_joined: any;
}

export interface register_user_register_user_errors {
  field: string;
  messages: string[];
}

export interface register_user_register_user {
  user: register_user_register_user_user | null;
  errors: register_user_register_user_errors[] | null;
}

export interface register_user {
  register_user: register_user_register_user;
}

export interface register_userVariables {
  data: RegisterUserMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: confirm_email
// ====================================================

export interface confirm_email_confirm_email {
  success: boolean;
}

export interface confirm_email {
  confirm_email: confirm_email_confirm_email;
}

export interface confirm_emailVariables {
  data: ConfirmEmailMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: request_email_change
// ====================================================

export interface request_email_change_request_email_change_errors {
  field: string;
  messages: string[];
}

export interface request_email_change_request_email_change {
  errors: request_email_change_request_email_change_errors[] | null;
}

export interface request_email_change {
  request_email_change: request_email_change_request_email_change;
}

export interface request_email_changeVariables {
  data: RequestEmailChangeMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: confirm_email_change
// ====================================================

export interface confirm_email_change_confirm_email_change_user {
  email: string;
}

export interface confirm_email_change_confirm_email_change_errors {
  field: string;
  messages: string[];
}

export interface confirm_email_change_confirm_email_change {
  user: confirm_email_change_confirm_email_change_user | null;
  errors: confirm_email_change_confirm_email_change_errors[] | null;
}

export interface confirm_email_change {
  confirm_email_change: confirm_email_change_confirm_email_change;
}

export interface confirm_email_changeVariables {
  data: ConfirmEmailChangeMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: request_password_reset
// ====================================================

export interface request_password_reset_request_password_reset_errors {
  field: string;
  messages: string[];
}

export interface request_password_reset_request_password_reset {
  errors: request_password_reset_request_password_reset_errors[] | null;
}

export interface request_password_reset {
  request_password_reset: request_password_reset_request_password_reset;
}

export interface request_password_resetVariables {
  data: RequestPasswordResetMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: confirm_password_reset
// ====================================================

export interface confirm_password_reset_confirm_password_reset_errors {
  field: string;
  messages: string[];
}

export interface confirm_password_reset_confirm_password_reset {
  errors: confirm_password_reset_confirm_password_reset_errors[] | null;
}

export interface confirm_password_reset {
  confirm_password_reset: confirm_password_reset_confirm_password_reset;
}

export interface confirm_password_resetVariables {
  data: ConfirmPasswordResetMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_event
// ====================================================

export interface get_event_event {
  id: string;
  type: EventTypes | null;
  data: any | null;
  test_mode: boolean | null;
  pending_webhooks: number | null;
  created_at: any | null;
}

export interface get_event {
  event: get_event_event;
}

export interface get_eventVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_events
// ====================================================

export interface get_events_events_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_events_events_edges_node {
  id: string;
  type: EventTypes | null;
  data: any | null;
  test_mode: boolean | null;
  pending_webhooks: number | null;
  created_at: any | null;
}

export interface get_events_events_edges {
  node: get_events_events_edges_node;
}

export interface get_events_events {
  page_info: get_events_events_page_info;
  edges: get_events_events_edges[];
}

export interface get_events {
  events: get_events_events;
}

export interface get_eventsVariables {
  filter?: EventFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_order
// ====================================================

export interface get_order_order_shipping_to {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipping_from {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_billing_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_line_items {
  id: string;
  weight: number;
  title: string | null;
  description: string | null;
  quantity: number;
  unfulfilled_quantity: number | null;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  weight_unit: WeightUnitEnum | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any;
  parent_id: string | null;
}

export interface get_order_order_created_by {
  email: string;
  full_name: string;
}

export interface get_order_order_shipments_created_by {
  email: string;
  full_name: string;
}

export interface get_order_order_shipments_recipient {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipments_shipper {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipments_return_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipments_billing_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipments_parcels_items {
  id: string | null;
  weight: number | null;
  title: string | null;
  description: string | null;
  quantity: number | null;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  weight_unit: WeightUnitEnum | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
  parent_id: string | null;
}

export interface get_order_order_shipments_parcels {
  id: string | null;
  width: number | null;
  height: number | null;
  length: number | null;
  is_document: boolean | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  freight_class: string | null;
  reference_number: string | null;
  description: string | null;
  items: get_order_order_shipments_parcels_items[] | null;
}

export interface get_order_order_shipments_customs_duty_bill_to {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_order_order_shipments_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
  bill_to: get_order_order_shipments_customs_duty_bill_to | null;
}

export interface get_order_order_shipments_customs_duty_billing_address {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_order_order_shipments_customs_commodities {
  id: string | null;
  sku: string | null;
  hs_code: string | null;
  quantity: number | null;
  description: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
}

export interface get_order_order_shipments_customs {
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  options: any | null;
  duty: get_order_order_shipments_customs_duty | null;
  duty_billing_address: get_order_order_shipments_customs_duty_billing_address | null;
  commodities: get_order_order_shipments_customs_commodities[] | null;
}

export interface get_order_order_shipments_payment {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
}

export interface get_order_order_shipments_selected_rate_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface get_order_order_shipments_selected_rate {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: get_order_order_shipments_selected_rate_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface get_order_order_shipments_rates_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface get_order_order_shipments_rates {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: get_order_order_shipments_rates_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface get_order_order_shipments_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface get_order_order_shipments_tracker {
  id: string;
  tracking_number: string;
  carrier_id: string;
  carrier_name: string;
}

export interface get_order_order_shipments {
  id: string;
  carrier_id: string | null;
  carrier_name: string | null;
  created_at: any;
  updated_at: any;
  created_by: get_order_order_shipments_created_by;
  status: ShipmentStatusEnum;
  recipient: get_order_order_shipments_recipient;
  shipper: get_order_order_shipments_shipper;
  return_address: get_order_order_shipments_return_address | null;
  billing_address: get_order_order_shipments_billing_address | null;
  parcels: get_order_order_shipments_parcels[];
  label_type: LabelTypeEnum | null;
  tracking_number: string | null;
  shipment_identifier: string | null;
  label_url: string | null;
  invoice_url: string | null;
  tracking_url: string | null;
  test_mode: boolean;
  service: string | null;
  reference: string | null;
  customs: get_order_order_shipments_customs | null;
  payment: get_order_order_shipments_payment | null;
  selected_rate_id: string | null;
  selected_rate: get_order_order_shipments_selected_rate | null;
  carrier_ids: string[];
  rates: get_order_order_shipments_rates[];
  options: any;
  metadata: any;
  meta: any | null;
  messages: get_order_order_shipments_messages[];
  tracker_id: string | null;
  tracker: get_order_order_shipments_tracker | null;
}

export interface get_order_order {
  id: string;
  order_id: string;
  source: string;
  status: OrderStatus;
  shipping_to: get_order_order_shipping_to;
  shipping_from: get_order_order_shipping_from | null;
  billing_address: get_order_order_billing_address | null;
  line_items: get_order_order_line_items[];
  created_at: any;
  updated_at: any;
  created_by: get_order_order_created_by;
  test_mode: boolean;
  options: any;
  metadata: any;
  shipments: get_order_order_shipments[];
}

export interface get_order {
  order: get_order_order;
}

export interface get_orderVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_order_data
// ====================================================

export interface get_order_data_order_shipping_to {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_data_order_shipping_from {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_data_order_billing_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_data_order_line_items {
  id: string;
  weight: number;
  title: string | null;
  description: string | null;
  quantity: number;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  weight_unit: WeightUnitEnum | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any;
  parent_id: string | null;
}

export interface get_order_data_order {
  id: string;
  shipping_to: get_order_data_order_shipping_to;
  shipping_from: get_order_data_order_shipping_from | null;
  billing_address: get_order_data_order_billing_address | null;
  line_items: get_order_data_order_line_items[];
  options: any;
  metadata: any;
}

export interface get_order_data {
  order: get_order_data_order;
}

export interface get_order_dataVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_orders
// ====================================================

export interface get_orders_orders_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_orders_orders_edges_node_shipping_to {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipping_from {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_billing_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_line_items {
  id: string;
  weight: number;
  title: string | null;
  description: string | null;
  quantity: number;
  unfulfilled_quantity: number | null;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  weight_unit: WeightUnitEnum | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any;
  parent_id: string | null;
}

export interface get_orders_orders_edges_node_created_by {
  email: string;
  full_name: string;
}

export interface get_orders_orders_edges_node_shipments_created_by {
  email: string;
  full_name: string;
}

export interface get_orders_orders_edges_node_shipments_recipient {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipments_shipper {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipments_return_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipments_billing_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipments_parcels_items {
  id: string | null;
  weight: number | null;
  title: string | null;
  description: string | null;
  quantity: number | null;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  weight_unit: WeightUnitEnum | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
  parent_id: string | null;
}

export interface get_orders_orders_edges_node_shipments_parcels {
  id: string | null;
  width: number | null;
  height: number | null;
  length: number | null;
  is_document: boolean | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  freight_class: string | null;
  reference_number: string | null;
  description: string | null;
  items: get_orders_orders_edges_node_shipments_parcels_items[] | null;
}

export interface get_orders_orders_edges_node_shipments_customs_duty_bill_to {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_orders_orders_edges_node_shipments_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
  bill_to: get_orders_orders_edges_node_shipments_customs_duty_bill_to | null;
}

export interface get_orders_orders_edges_node_shipments_customs_duty_billing_address {
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface get_orders_orders_edges_node_shipments_customs_commodities {
  id: string | null;
  sku: string | null;
  hs_code: string | null;
  quantity: number | null;
  description: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any | null;
}

export interface get_orders_orders_edges_node_shipments_customs {
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  options: any | null;
  duty: get_orders_orders_edges_node_shipments_customs_duty | null;
  duty_billing_address: get_orders_orders_edges_node_shipments_customs_duty_billing_address | null;
  commodities: get_orders_orders_edges_node_shipments_customs_commodities[] | null;
}

export interface get_orders_orders_edges_node_shipments_payment {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
}

export interface get_orders_orders_edges_node_shipments_selected_rate_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface get_orders_orders_edges_node_shipments_selected_rate {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: get_orders_orders_edges_node_shipments_selected_rate_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface get_orders_orders_edges_node_shipments_rates_extra_charges {
  name: string | null;
  amount: number | null;
  currency: CurrencyCodeEnum;
}

export interface get_orders_orders_edges_node_shipments_rates {
  id: string;
  carrier_name: string;
  carrier_id: string;
  currency: CurrencyCodeEnum;
  service: string;
  transit_days: number | null;
  total_charge: number;
  extra_charges: get_orders_orders_edges_node_shipments_rates_extra_charges[];
  test_mode: boolean;
  meta: any | null;
}

export interface get_orders_orders_edges_node_shipments_messages {
  carrier_name: string | null;
  carrier_id: string | null;
  message: string | null;
  code: string | null;
  details: any | null;
}

export interface get_orders_orders_edges_node_shipments_tracker {
  id: string;
  tracking_number: string;
  carrier_id: string;
  carrier_name: string;
}

export interface get_orders_orders_edges_node_shipments {
  id: string;
  carrier_id: string | null;
  carrier_name: string | null;
  created_at: any;
  updated_at: any;
  created_by: get_orders_orders_edges_node_shipments_created_by;
  status: ShipmentStatusEnum;
  recipient: get_orders_orders_edges_node_shipments_recipient;
  shipper: get_orders_orders_edges_node_shipments_shipper;
  return_address: get_orders_orders_edges_node_shipments_return_address | null;
  billing_address: get_orders_orders_edges_node_shipments_billing_address | null;
  parcels: get_orders_orders_edges_node_shipments_parcels[];
  label_type: LabelTypeEnum | null;
  tracking_number: string | null;
  shipment_identifier: string | null;
  label_url: string | null;
  invoice_url: string | null;
  tracking_url: string | null;
  test_mode: boolean;
  service: string | null;
  reference: string | null;
  customs: get_orders_orders_edges_node_shipments_customs | null;
  payment: get_orders_orders_edges_node_shipments_payment | null;
  selected_rate_id: string | null;
  selected_rate: get_orders_orders_edges_node_shipments_selected_rate | null;
  carrier_ids: string[];
  rates: get_orders_orders_edges_node_shipments_rates[];
  options: any;
  metadata: any;
  meta: any | null;
  messages: get_orders_orders_edges_node_shipments_messages[];
  tracker_id: string | null;
  tracker: get_orders_orders_edges_node_shipments_tracker | null;
}

export interface get_orders_orders_edges_node {
  id: string;
  order_id: string;
  source: string;
  status: OrderStatus;
  shipping_to: get_orders_orders_edges_node_shipping_to;
  shipping_from: get_orders_orders_edges_node_shipping_from | null;
  billing_address: get_orders_orders_edges_node_billing_address | null;
  line_items: get_orders_orders_edges_node_line_items[];
  created_at: any;
  updated_at: any;
  created_by: get_orders_orders_edges_node_created_by;
  test_mode: boolean;
  options: any;
  metadata: any;
  shipments: get_orders_orders_edges_node_shipments[];
}

export interface get_orders_orders_edges {
  node: get_orders_orders_edges_node;
}

export interface get_orders_orders {
  page_info: get_orders_orders_page_info;
  edges: get_orders_orders_edges[];
}

export interface get_orders {
  orders: get_orders_orders;
}

export interface get_ordersVariables {
  filter?: OrderFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: mutate_metadata
// ====================================================

export interface mutate_metadata_mutate_metadata_errors {
  field: string;
  messages: string[];
}

export interface mutate_metadata_mutate_metadata {
  id: string;
  metadata: any;
  errors: mutate_metadata_mutate_metadata_errors[] | null;
}

export interface mutate_metadata {
  mutate_metadata: mutate_metadata_mutate_metadata;
}

export interface mutate_metadataVariables {
  data: MetadataMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_document_template
// ====================================================

export interface get_document_template_document_template {
  id: string;
  slug: string;
  name: string;
  template: string;
  description: string | null;
  related_object: TemplateRelatedObject | null;
  active: boolean;
  metadata: any | null;
  options: any | null;
  preview_url: string | null;
  updated_at: any | null;
}

export interface get_document_template {
  document_template: get_document_template_document_template;
}

export interface get_document_templateVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_document_templates
// ====================================================

export interface get_document_templates_document_templates_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_document_templates_document_templates_edges_node {
  id: string;
  slug: string;
  name: string;
  template: string;
  description: string | null;
  related_object: TemplateRelatedObject | null;
  active: boolean;
  metadata: any | null;
  options: any | null;
  updated_at: any | null;
  preview_url: string | null;
}

export interface get_document_templates_document_templates_edges {
  node: get_document_templates_document_templates_edges_node;
}

export interface get_document_templates_document_templates {
  page_info: get_document_templates_document_templates_page_info;
  edges: get_document_templates_document_templates_edges[];
}

export interface get_document_templates {
  document_templates: get_document_templates_document_templates;
}

export interface get_document_templatesVariables {
  filter?: DocumentTemplateFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: create_document_template
// ====================================================

export interface create_document_template_create_document_template_template {
  id: string;
}

export interface create_document_template_create_document_template_errors {
  field: string;
  messages: string[];
}

export interface create_document_template_create_document_template {
  template: create_document_template_create_document_template_template | null;
  errors: create_document_template_create_document_template_errors[] | null;
}

export interface create_document_template {
  create_document_template: create_document_template_create_document_template;
}

export interface create_document_templateVariables {
  data: CreateDocumentTemplateMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_document_template
// ====================================================

export interface update_document_template_update_document_template_template {
  id: string;
}

export interface update_document_template_update_document_template_errors {
  field: string;
  messages: string[];
}

export interface update_document_template_update_document_template {
  template: update_document_template_update_document_template_template | null;
  errors: update_document_template_update_document_template_errors[] | null;
}

export interface update_document_template {
  update_document_template: update_document_template_update_document_template;
}

export interface update_document_templateVariables {
  data: UpdateDocumentTemplateMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: delete_document_template
// ====================================================

export interface delete_document_template_delete_document_template {
  id: string;
}

export interface delete_document_template {
  delete_document_template: delete_document_template_delete_document_template;
}

export interface delete_document_templateVariables {
  data: DeleteMutationInput;
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

export interface UpdateRateSheet_update_rate_sheet_rate_sheet_zones {
  id: string;
  label: string | null;
  country_codes: string[] | null;
  postal_codes: string[] | null;
  cities: string[] | null;
  transit_days: number | null;
  transit_time: number | null;
}

export interface UpdateRateSheet_update_rate_sheet_rate_sheet_surcharges {
  id: string;
  name: string;
  amount: number;
  surcharge_type: string;
  cost: number | null;
  active: boolean;
}

export interface UpdateRateSheet_update_rate_sheet_rate_sheet_service_rates {
  service_id: string;
  zone_id: string;
  rate: number;
  cost: number | null;
  min_weight: number | null;
  max_weight: number | null;
}

export interface UpdateRateSheet_update_rate_sheet_rate_sheet_services {
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
  zone_ids: string[];
  surcharge_ids: string[];
}

export interface UpdateRateSheet_update_rate_sheet_rate_sheet {
  id: string;
  name: string;
  carrier_name: CarrierNameEnum;
  zones: UpdateRateSheet_update_rate_sheet_rate_sheet_zones[] | null;
  surcharges: UpdateRateSheet_update_rate_sheet_rate_sheet_surcharges[] | null;
  service_rates: UpdateRateSheet_update_rate_sheet_rate_sheet_service_rates[] | null;
  services: UpdateRateSheet_update_rate_sheet_rate_sheet_services[];
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

// ====================================================
// GraphQL mutation operation: DeleteRateSheetService
// ====================================================

export interface DeleteRateSheetService_delete_rate_sheet_service_rate_sheet_services {
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
  zone_ids: string[];
  surcharge_ids: string[];
}

export interface DeleteRateSheetService_delete_rate_sheet_service_rate_sheet {
  id: string;
  name: string;
  carrier_name: CarrierNameEnum;
  services: DeleteRateSheetService_delete_rate_sheet_service_rate_sheet_services[];
}

export interface DeleteRateSheetService_delete_rate_sheet_service_errors {
  field: string;
  messages: string[];
}

export interface DeleteRateSheetService_delete_rate_sheet_service {
  rate_sheet: DeleteRateSheetService_delete_rate_sheet_service_rate_sheet | null;
  errors: DeleteRateSheetService_delete_rate_sheet_service_errors[] | null;
}

export interface DeleteRateSheetService {
  delete_rate_sheet_service: DeleteRateSheetService_delete_rate_sheet_service;
}

export interface DeleteRateSheetServiceVariables {
  data: DeleteRateSheetServiceMutationInput;
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
  data: AddSharedZoneMutationInput;
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
  data: UpdateSharedZoneMutationInput;
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
  data: DeleteSharedZoneMutationInput;
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
  data: AddSharedSurchargeMutationInput;
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
  data: UpdateSharedSurchargeMutationInput;
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
  data: DeleteSharedSurchargeMutationInput;
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
  data: BatchUpdateSurchargesMutationInput;
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
  data: UpdateServiceRateMutationInput;
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
  data: BatchUpdateServiceRatesMutationInput;
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
  data: UpdateServiceZoneIdsMutationInput;
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
  data: UpdateServiceSurchargeIdsMutationInput;
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
  domicile: boolean | null;
  international: boolean | null;
  zone_ids: string[];
  surcharge_ids: string[];
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
  carrier_name: CarrierNameEnum;
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
// GraphQL query operation: GetRateSheets
// ====================================================

export interface GetRateSheets_rate_sheets_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

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
}

export interface GetRateSheets_rate_sheets_edges_node_services {
  id: string;
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
  domicile: boolean | null;
  international: boolean | null;
  zone_ids: string[];
  surcharge_ids: string[];
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
  carrier_name: CarrierNameEnum;
  zones: GetRateSheets_rate_sheets_edges_node_zones[] | null;
  surcharges: GetRateSheets_rate_sheets_edges_node_surcharges[] | null;
  service_rates: GetRateSheets_rate_sheets_edges_node_service_rates[] | null;
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
// GraphQL mutation operation: CreateOrder
// ====================================================

export interface CreateOrder_create_order_order {
  id: string;
}

export interface CreateOrder_create_order_errors {
  field: string;
  messages: string[];
}

export interface CreateOrder_create_order {
  order: CreateOrder_create_order_order | null;
  errors: CreateOrder_create_order_errors[] | null;
}

export interface CreateOrder {
  create_order: CreateOrder_create_order;
}

export interface CreateOrderVariables {
  data: CreateOrderMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateOrder
// ====================================================

export interface UpdateOrder_update_order_order {
  id: string;
}

export interface UpdateOrder_update_order_errors {
  field: string;
  messages: string[];
}

export interface UpdateOrder_update_order {
  order: UpdateOrder_update_order_order | null;
  errors: UpdateOrder_update_order_errors[] | null;
}

export interface UpdateOrder {
  update_order: UpdateOrder_update_order;
}

export interface UpdateOrderVariables {
  data: UpdateOrderMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteOrder
// ====================================================

export interface DeleteOrder_delete_order_errors {
  field: string;
  messages: string[];
}

export interface DeleteOrder_delete_order {
  id: string | null;
  errors: DeleteOrder_delete_order_errors[] | null;
}

export interface DeleteOrder {
  delete_order: DeleteOrder_delete_order;
}

export interface DeleteOrderVariables {
  data: DeleteOrderMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_batch_operation
// ====================================================

export interface get_batch_operation_batch_operation_resources {
  id: number;
  status: ResourceStatus | null;
}

export interface get_batch_operation_batch_operation {
  id: number;
  resource_type: ResourceStatus;
  status: BatchOperationStatus;
  test_mode: boolean;
  resources: get_batch_operation_batch_operation_resources[];
}

export interface get_batch_operation {
  batch_operation: get_batch_operation_batch_operation;
}

export interface get_batch_operationVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_batch_operations
// ====================================================

export interface get_batch_operations_batch_operations_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_batch_operations_batch_operations_edges_node_resources {
  id: number;
  status: ResourceStatus | null;
}

export interface get_batch_operations_batch_operations_edges_node {
  id: number;
  resource_type: ResourceStatus;
  status: BatchOperationStatus;
  test_mode: boolean;
  resources: get_batch_operations_batch_operations_edges_node_resources[];
}

export interface get_batch_operations_batch_operations_edges {
  node: get_batch_operations_batch_operations_edges_node;
}

export interface get_batch_operations_batch_operations {
  page_info: get_batch_operations_batch_operations_page_info;
  edges: get_batch_operations_batch_operations_edges[];
}

export interface get_batch_operations {
  batch_operations: get_batch_operations_batch_operations;
}

export interface get_batch_operationsVariables {
  filter?: BatchOperationFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: deleteMetafield
// ====================================================

export interface deleteMetafield_delete_metafield_errors {
  field: string;
  messages: string[];
}

export interface deleteMetafield_delete_metafield {
  id: string;
  errors: deleteMetafield_delete_metafield_errors[] | null;
}

export interface deleteMetafield {
  delete_metafield: deleteMetafield_delete_metafield;
}

export interface deleteMetafieldVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceConfig
// ====================================================

export interface GetWorkspaceConfig_workspace_config {
  object_type: string;
  default_currency: CurrencyCodeEnum | null;
  default_country_code: CountryCodeEnum | null;
  default_weight_unit: WeightUnitEnum | null;
  default_dimension_unit: DimensionUnitEnum | null;
  state_tax_id: string | null;
  federal_tax_id: string | null;
  default_label_type: LabelTypeEnum | null;
  customs_aes: string | null;
  customs_eel_pfc: string | null;
  customs_license_number: string | null;
  customs_certificate_number: string | null;
  customs_nip_number: string | null;
  customs_eori_number: string | null;
  customs_vat_registration_number: string | null;
  insured_by_default: boolean | null;
}

export interface GetWorkspaceConfig {
  workspace_config: GetWorkspaceConfig_workspace_config | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateWorkspaceConfig
// ====================================================

export interface UpdateWorkspaceConfig_update_workspace_config_workspace_config {
  object_type: string;
  default_currency: CurrencyCodeEnum | null;
  default_country_code: CountryCodeEnum | null;
  default_weight_unit: WeightUnitEnum | null;
  default_dimension_unit: DimensionUnitEnum | null;
  state_tax_id: string | null;
  federal_tax_id: string | null;
  default_label_type: LabelTypeEnum | null;
  customs_aes: string | null;
  customs_eel_pfc: string | null;
  customs_license_number: string | null;
  customs_certificate_number: string | null;
  customs_nip_number: string | null;
  customs_eori_number: string | null;
  customs_vat_registration_number: string | null;
  insured_by_default: boolean | null;
}

export interface UpdateWorkspaceConfig_update_workspace_config_errors {
  field: string;
  messages: string[];
}

export interface UpdateWorkspaceConfig_update_workspace_config {
  workspace_config: UpdateWorkspaceConfig_update_workspace_config_workspace_config | null;
  errors: UpdateWorkspaceConfig_update_workspace_config_errors[] | null;
}

export interface UpdateWorkspaceConfig {
  update_workspace_config: UpdateWorkspaceConfig_update_workspace_config;
}

export interface UpdateWorkspaceConfigVariables {
  data: WorkspaceConfigMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetManifests
// ====================================================

export interface GetManifests_manifests_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetManifests_manifests_edges_node_address {
  id: string | null;
  postal_code: string | null;
  city: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface GetManifests_manifests_edges_node_manifest_carrier {
  carrier_id: string;
  carrier_name: string;
  config: any | null;
}

export interface GetManifests_manifests_edges_node_messages {
  message: string | null;
  code: string | null;
}

export interface GetManifests_manifests_edges_node {
  id: string;
  carrier_id: string;
  carrier_name: string;
  manifest_url: string | null;
  shipment_identifiers: string[];
  reference: string | null;
  address: GetManifests_manifests_edges_node_address;
  manifest_carrier: GetManifests_manifests_edges_node_manifest_carrier | null;
  messages: GetManifests_manifests_edges_node_messages[];
  options: any;
  metadata: any;
  meta: any;
  created_at: any;
  updated_at: any;
}

export interface GetManifests_manifests_edges {
  node: GetManifests_manifests_edges_node;
}

export interface GetManifests_manifests {
  page_info: GetManifests_manifests_page_info;
  edges: GetManifests_manifests_edges[];
}

export interface GetManifests {
  manifests: GetManifests_manifests;
}

export interface GetManifestsVariables {
  filter?: ManifestFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetManifest
// ====================================================

export interface GetManifest_manifest_address {
  postal_code: string | null;
  city: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum | null;
  email: string | null;
  phone_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  state_code: string | null;
  street_number: string | null;
}

export interface GetManifest_manifest_messages {
  message: string | null;
  code: string | null;
}

export interface GetManifest_manifest {
  id: string;
  carrier_id: string;
  carrier_name: string;
  manifest_url: string | null;
  shipment_identifiers: string[];
  reference: string | null;
  address: GetManifest_manifest_address;
  messages: GetManifest_manifest_messages[];
  options: any;
  metadata: any;
  meta: any;
  created_at: any;
  updated_at: any;
}

export interface GetManifest {
  manifest: GetManifest_manifest | null;
}

export interface GetManifestVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetAPIKeys
// ====================================================

export interface GetAPIKeys_api_keys {
  object_type: string;
  key: string;
  label: string;
  test_mode: boolean;
  created: any;
  permissions: string[] | null;
}

export interface GetAPIKeys {
  api_keys: GetAPIKeys_api_keys[];
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateAPIKey
// ====================================================

export interface CreateAPIKey_create_api_key_api_key {
  object_type: string;
  key: string;
  label: string;
  test_mode: boolean;
  created: any;
  permissions: string[] | null;
}

export interface CreateAPIKey_create_api_key_errors {
  field: string;
  messages: string[];
}

export interface CreateAPIKey_create_api_key {
  api_key: CreateAPIKey_create_api_key_api_key | null;
  errors: CreateAPIKey_create_api_key_errors[] | null;
}

export interface CreateAPIKey {
  create_api_key: CreateAPIKey_create_api_key;
}

export interface CreateAPIKeyVariables {
  data: CreateAPIKeyMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteAPIKey
// ====================================================

export interface DeleteAPIKey_delete_api_key_errors {
  field: string;
  messages: string[];
}

export interface DeleteAPIKey_delete_api_key {
  label: string | null;
  errors: DeleteAPIKey_delete_api_key_errors[] | null;
}

export interface DeleteAPIKey {
  delete_api_key: DeleteAPIKey_delete_api_key;
}

export interface DeleteAPIKeyVariables {
  data: DeleteAPIKeyMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: search_data
// ====================================================

export interface search_data_shipment_results_edges_node_recipient {
  id: string | null;
  city: string | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  person_name: string | null;
  phone_number: string | null;
  company_name: string | null;
  state_code: string | null;
}

export interface search_data_shipment_results_edges_node {
  id: string;
  status: ShipmentStatusEnum;
  tracking_number: string | null;
  recipient: search_data_shipment_results_edges_node_recipient;
  created_at: any;
}

export interface search_data_shipment_results_edges {
  node: search_data_shipment_results_edges_node;
}

export interface search_data_shipment_results {
  edges: search_data_shipment_results_edges[];
}

export interface search_data_order_results_edges_node_shipping_to {
  id: string | null;
  city: string | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  country_code: CountryCodeEnum | null;
  postal_code: string | null;
  person_name: string | null;
  phone_number: string | null;
  company_name: string | null;
  state_code: string | null;
}

export interface search_data_order_results_edges_node {
  id: string;
  status: OrderStatus;
  order_id: string;
  shipping_to: search_data_order_results_edges_node_shipping_to;
  created_at: any;
}

export interface search_data_order_results_edges {
  node: search_data_order_results_edges_node;
}

export interface search_data_order_results {
  edges: search_data_order_results_edges[];
}

export interface search_data_trackers_results_edges_node {
  id: string;
  status: TrackerStatusEnum;
  tracking_number: string;
  created_at: any;
}

export interface search_data_trackers_results_edges {
  node: search_data_trackers_results_edges_node;
}

export interface search_data_trackers_results {
  edges: search_data_trackers_results_edges[];
}

export interface search_data {
  shipment_results: search_data_shipment_results;
  order_results: search_data_order_results;
  trackers_results: search_data_trackers_results;
}

export interface search_dataVariables {
  keyword?: string | null;
}

/* tslint:disable */
// This file was automatically generated and should not be edited.

//==============================================================
// START Enums and Input Objects
//==============================================================

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

export enum CarrierNameEnum {
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
  teleship = "teleship",
  tge = "tge",
  tnt = "tnt",
  ups = "ups",
  usps = "usps",
  usps_international = "usps_international",
  veho = "veho",
  zoom2u = "zoom2u",
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

export enum LabelTypeEnum {
  PDF = "PDF",
  PNG = "PNG",
  ZPL = "ZPL",
}

export enum CustomsContentTypeEnum {
  documents = "documents",
  gift = "gift",
  merchandise = "merchandise",
  other = "other",
  return_merchandise = "return_merchandise",
  sample = "sample",
}

export enum IncotermCodeEnum {
  CFR = "CFR",
  CIF = "CIF",
  CIP = "CIP",
  CPT = "CPT",
  DAF = "DAF",
  DAP = "DAP",
  DDP = "DDP",
  DDU = "DDU",
  DEQ = "DEQ",
  DES = "DES",
  EXW = "EXW",
  FAS = "FAS",
  FCA = "FCA",
  FOB = "FOB",
}

export enum PaidByEnum {
  recipient = "recipient",
  sender = "sender",
  third_party = "third_party",
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

export enum ManualShipmentStatusEnum {
  delivered = "delivered",
  delivery_failed = "delivery_failed",
  in_transit = "in_transit",
  needs_attention = "needs_attention",
}

export enum EventTypes {
  all = "all",
  batch_completed = "batch_completed",
  batch_failed = "batch_failed",
  batch_queued = "batch_queued",
  batch_running = "batch_running",
  order_cancelled = "order_cancelled",
  order_created = "order_created",
  order_delivered = "order_delivered",
  order_fulfilled = "order_fulfilled",
  order_updated = "order_updated",
  shipment_cancelled = "shipment_cancelled",
  shipment_delivery_failed = "shipment_delivery_failed",
  shipment_fulfilled = "shipment_fulfilled",
  shipment_needs_attention = "shipment_needs_attention",
  shipment_out_for_delivery = "shipment_out_for_delivery",
  shipment_purchased = "shipment_purchased",
  tracker_created = "tracker_created",
  tracker_updated = "tracker_updated",
}

export enum OrderStatus {
  cancelled = "cancelled",
  delivered = "delivered",
  fulfilled = "fulfilled",
  partial = "partial",
  unfulfilled = "unfulfilled",
}

export enum MetadataObjectTypeEnum {
  carrier = "carrier",
  commodity = "commodity",
  order = "order",
  shipment = "shipment",
  tracker = "tracker",
}

export enum TemplateRelatedObject {
  order = "order",
  other = "other",
  shipment = "shipment",
}

export enum ResourceStatus {
  created = "created",
  has_errors = "has_errors",
  incomplete = "incomplete",
  processed = "processed",
  queued = "queued",
}

export enum BatchOperationStatus {
  completed = "completed",
  completed_with_errors = "completed_with_errors",
  failed = "failed",
  queued = "queued",
  running = "running",
}

// null
export interface UsageFilter {
  date_after?: string | null;
  date_before?: string | null;
  omit?: string[] | null;
  surcharge_id?: string | null;
}

// null
export interface AddressFilter {
  offset?: number | null;
  first?: number | null;
  label?: string | null;
  keyword?: string | null;
  address?: string | null;
}

// null
export interface CreateCarrierConnectionMutationInput {
  carrier_name: CarrierNameEnum;
  carrier_id: string;
  credentials: any;
  active?: boolean | null;
  config?: any | null;
  metadata?: any | null;
  capabilities?: string[] | null;
}

// null
export interface UpdateCarrierConnectionMutationInput {
  id: string;
  active?: boolean | null;
  carrier_id?: string | null;
  credentials?: any | null;
  config?: any | null;
  metadata?: any | null;
  capabilities?: string[] | null;
}

// null
export interface DeleteMutationInput {
  id: string;
}

// null
export interface LogFilter {
  offset?: number | null;
  first?: number | null;
  query?: string | null;
  api_endpoint?: string | null;
  remote_addr?: string | null;
  date_after?: any | null;
  date_before?: any | null;
  entity_id?: string | null;
  method?: string[] | null;
  status?: string | null;
  status_code?: number[] | null;
}

// null
export interface ShipmentFilter {
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
}

// null
export interface PartialShipmentMutationInput {
  id: string;
  recipient?: UpdateAddressInput | null;
  shipper?: UpdateAddressInput | null;
  return_address?: UpdateAddressInput | null;
  billing_address?: UpdateAddressInput | null;
  customs?: any | null;
  parcels?: UpdateParcelInput[] | null;
  payment?: PaymentInput | null;
  label_type?: LabelTypeEnum | null;
  metadata?: any | null;
  options?: any | null;
  reference?: string | null;
}

// null
export interface UpdateAddressInput {
  country_code?: CountryCodeEnum | null;
  postal_code?: string | null;
  city?: string | null;
  federal_tax_id?: string | null;
  state_tax_id?: string | null;
  person_name?: string | null;
  company_name?: string | null;
  email?: string | null;
  phone_number?: string | null;
  state_code?: string | null;
  residential?: boolean | null;
  street_number?: string | null;
  address_line1?: string | null;
  address_line2?: string | null;
  validate_location?: boolean | null;
  id?: string | null;
}

// null
export interface UpdateParcelInput {
  weight?: number | null;
  weight_unit?: WeightUnitEnum | null;
  width?: number | null;
  height?: number | null;
  length?: number | null;
  packaging_type?: string | null;
  package_preset?: string | null;
  description?: string | null;
  content?: string | null;
  is_document?: boolean | null;
  dimension_unit?: DimensionUnitEnum | null;
  reference_number?: string | null;
  freight_class?: string | null;
  items?: UpdateCommodityInput[] | null;
  id?: string | null;
}

// null
export interface UpdateCommodityInput {
  weight?: number | null;
  weight_unit?: WeightUnitEnum | null;
  quantity?: number | null;
  sku?: string | null;
  title?: string | null;
  hs_code?: string | null;
  description?: string | null;
  value_amount?: number | null;
  origin_country?: CountryCodeEnum | null;
  value_currency?: CurrencyCodeEnum | null;
  metadata?: any | null;
  parent_id?: string | null;
  id?: string | null;
}

// null
export interface PaymentInput {
  account_number?: string | null;
  paid_by?: PaidByEnum | null;
  currency?: CurrencyCodeEnum | null;
}

// null
export interface ChangeShipmentStatusMutationInput {
  id: string;
  status?: ManualShipmentStatusEnum | null;
}

// null
export interface TrackerFilter {
  offset?: number | null;
  first?: number | null;
  tracking_number?: string | null;
  created_after?: string | null;
  created_before?: string | null;
  carrier_name?: string[] | null;
  status?: string[] | null;
}

// null
export interface WebhookFilter {
  offset?: number | null;
  first?: number | null;
  url?: string | null;
  disabled?: boolean | null;
  test_mode?: boolean | null;
  events?: EventTypes[] | null;
  date_after?: any | null;
  date_before?: any | null;
}

// null
export interface TemplateFilter {
  offset?: number | null;
  first?: number | null;
  label?: string | null;
  keyword?: string | null;
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
export interface SystemCarrierMutationInput {
  id: string;
  enable?: boolean | null;
  config?: any | null;
}

// null
export interface CreateParcelInput {
  label: string;
  parcel: ParcelInput;
  is_default?: boolean | null;
}

// null
export interface ParcelInput {
  weight: number;
  weight_unit: WeightUnitEnum;
  width?: number | null;
  height?: number | null;
  length?: number | null;
  packaging_type?: string | null;
  package_preset?: string | null;
  description?: string | null;
  content?: string | null;
  is_document?: boolean | null;
  dimension_unit?: DimensionUnitEnum | null;
  reference_number?: string | null;
  freight_class?: string | null;
  items?: CommodityInput[] | null;
}

// null
export interface CommodityInput {
  weight: number;
  weight_unit: WeightUnitEnum;
  quantity?: number | null;
  sku?: string | null;
  title?: string | null;
  hs_code?: string | null;
  description?: string | null;
  value_amount?: number | null;
  origin_country?: CountryCodeEnum | null;
  value_currency?: CurrencyCodeEnum | null;
  metadata?: any | null;
  parent_id?: string | null;
}

// null
export interface UpdateParcelInput2 {
  label?: string | null;
  parcel?: UpdateParcelInput | null;
  is_default?: boolean | null;
  id: string;
}

// null
export interface CreateAddressInput {
  label: string;
  address: AddressInput;
  is_default?: boolean | null;
}

// null
export interface AddressInput {
  country_code?: CountryCodeEnum | null;
  postal_code?: string | null;
  city?: string | null;
  federal_tax_id?: string | null;
  state_tax_id?: string | null;
  person_name?: string | null;
  company_name?: string | null;
  email?: string | null;
  phone_number?: string | null;
  state_code?: string | null;
  residential?: boolean | null;
  street_number?: string | null;
  address_line1?: string | null;
  address_line2?: string | null;
  validate_location?: boolean | null;
}

// null
export interface UpdateAddressInput2 {
  label?: string | null;
  address?: UpdateAddressInput | null;
  is_default?: boolean | null;
  id: string;
}

// null
export interface ProductFilter {
  offset?: number | null;
  first?: number | null;
  label?: string | null;
  keyword?: string | null;
  sku?: string | null;
  origin_country?: CountryCodeEnum | null;
}

// null
export interface CreateProductInput {
  label: string;
  weight: number;
  weight_unit: WeightUnitEnum;
  quantity?: number | null;
  sku?: string | null;
  title?: string | null;
  hs_code?: string | null;
  description?: string | null;
  value_amount?: number | null;
  value_currency?: CurrencyCodeEnum | null;
  origin_country?: CountryCodeEnum | null;
  is_default?: boolean | null;
  metadata?: any | null;
}

// null
export interface UpdateProductInput {
  id: string;
  label?: string | null;
  weight?: number | null;
  weight_unit?: WeightUnitEnum | null;
  quantity?: number | null;
  sku?: string | null;
  title?: string | null;
  hs_code?: string | null;
  description?: string | null;
  value_amount?: number | null;
  value_currency?: CurrencyCodeEnum | null;
  origin_country?: CountryCodeEnum | null;
  is_default?: boolean | null;
  metadata?: any | null;
}

// null
export interface TokenMutationInput {
  key: string;
  password?: string | null;
  refresh?: boolean | null;
}

// null
export interface UpdateUserInput {
  full_name?: string | null;
  is_active?: boolean | null;
  metadata?: any | null;
}

// null
export interface ChangePasswordMutationInput {
  old_password: string;
  new_password1: string;
  new_password2: string;
}

// null
export interface RegisterUserMutationInput {
  email: string;
  password1: string;
  password2: string;
  redirect_url: string;
  full_name?: string | null;
}

// null
export interface ConfirmEmailMutationInput {
  token: string;
}

// null
export interface RequestEmailChangeMutationInput {
  email: string;
  password: string;
  redirect_url: string;
}

// null
export interface ConfirmEmailChangeMutationInput {
  token: string;
}

// null
export interface RequestPasswordResetMutationInput {
  email: string;
  redirect_url: string;
}

// null
export interface ConfirmPasswordResetMutationInput {
  uid: string;
  token: string;
  new_password1: string;
  new_password2: string;
}

// null
export interface EventFilter {
  offset?: number | null;
  first?: number | null;
  entity_id?: string | null;
  type?: EventTypes[] | null;
  date_after?: any | null;
  date_before?: any | null;
}

// null
export interface OrderFilter {
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
}

// null
export interface MetadataMutationInput {
  id: string;
  object_type: MetadataObjectTypeEnum;
  added_values: any;
  discarded_keys?: string[] | null;
}

// null
export interface DocumentTemplateFilter {
  offset?: number | null;
  first?: number | null;
  name?: string | null;
  active?: boolean | null;
  related_object?: TemplateRelatedObject | null;
}

// null
export interface CreateDocumentTemplateMutationInput {
  slug: string;
  name: string;
  template: string;
  active?: boolean | null;
  description?: string | null;
  metadata?: any | null;
  related_object?: TemplateRelatedObject | null;
  options?: any | null;
}

// null
export interface UpdateDocumentTemplateMutationInput {
  id: string;
  slug?: string | null;
  name?: string | null;
  template?: string | null;
  active?: boolean | null;
  description?: string | null;
  metadata?: any | null;
  related_object?: TemplateRelatedObject | null;
  options?: any | null;
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
  domicile?: boolean | null;
  international?: boolean | null;
  zone_ids?: string[] | null;
  surcharge_ids?: string[] | null;
  metadata?: any | null;
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
  domicile?: boolean | null;
  international?: boolean | null;
  zone_ids?: string[] | null;
  surcharge_ids?: string[] | null;
  metadata?: any | null;
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
export interface RateSheetFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
}

// null
export interface CreateOrderMutationInput {
  shipping_to: AddressInput;
  line_items: CommodityInput[];
  order_id?: string | null;
  order_date?: string | null;
  shipping_from?: AddressInput | null;
  billing_address?: AddressInput | null;
  metadata?: any | null;
  options?: any | null;
}

// null
export interface UpdateOrderMutationInput {
  id: string;
  order_id?: string | null;
  order_date?: string | null;
  shipping_to?: UpdateAddressInput | null;
  shipping_from?: UpdateAddressInput | null;
  billing_address?: UpdateAddressInput | null;
  metadata?: any | null;
  options?: any | null;
  line_items?: UpdateCommodityInput[] | null;
}

// null
export interface DeleteOrderMutationInput {
  id: string;
}

// null
export interface BatchOperationFilter {
  offset?: number | null;
  first?: number | null;
  resource_type?: ResourceStatus[] | null;
  status?: BatchOperationStatus[] | null;
}

// null
export interface WorkspaceConfigMutationInput {
  default_currency?: CurrencyCodeEnum | null;
  default_country_code?: CountryCodeEnum | null;
  default_label_type?: LabelTypeEnum | null;
  default_weight_unit?: WeightUnitEnum | null;
  default_dimension_unit?: DimensionUnitEnum | null;
  state_tax_id?: string | null;
  federal_tax_id?: string | null;
  customs_aes?: string | null;
  customs_eel_pfc?: string | null;
  customs_eori_number?: string | null;
  customs_license_number?: string | null;
  customs_certificate_number?: string | null;
  customs_nip_number?: string | null;
  customs_vat_registration_number?: string | null;
  insured_by_default?: boolean | null;
  label_message_1?: string | null;
  label_message_2?: string | null;
  label_message_3?: string | null;
  label_logo?: string | null;
}

// null
export interface ManifestFilter {
  offset?: number | null;
  first?: number | null;
  id?: string[] | null;
  created_after?: any | null;
  created_before?: any | null;
  carrier_name?: string[] | null;
}

// null
export interface CreateAPIKeyMutationInput {
  password: string;
  label: string;
  permissions?: string[] | null;
}

// null
export interface DeleteAPIKeyMutationInput {
  password: string;
  key: string;
}

//==============================================================
// END Enums and Input Objects
//==============================================================