

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
// GraphQL query operation: get_user_connections
// ====================================================

export interface get_user_connections_user_connections_AlliedExpressSettingsType {
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

export interface get_user_connections_user_connections_AlliedExpressLocalSettingsType {
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

export interface get_user_connections_user_connections_AmazonShippingSettingsType {
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

export interface get_user_connections_user_connections_AramexSettingsType {
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

export interface get_user_connections_user_connections_AsendiaUSSettingsType {
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

export interface get_user_connections_user_connections_AustraliaPostSettingsType {
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

export interface get_user_connections_user_connections_BoxKnightSettingsType {
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

export interface get_user_connections_user_connections_BelgianPostSettingsType_services_zones {
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

export interface get_user_connections_user_connections_BelgianPostSettingsType_services {
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
  zones: get_user_connections_user_connections_BelgianPostSettingsType_services_zones[];
}

export interface get_user_connections_user_connections_BelgianPostSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface get_user_connections_user_connections_BelgianPostSettingsType {
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
  services: get_user_connections_user_connections_BelgianPostSettingsType_services[] | null;
  rate_sheet: get_user_connections_user_connections_BelgianPostSettingsType_rate_sheet | null;
}

export interface get_user_connections_user_connections_CanadaPostSettingsType {
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

export interface get_user_connections_user_connections_CanparSettingsType {
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

export interface get_user_connections_user_connections_ChronopostSettingsType {
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

export interface get_user_connections_user_connections_ColissimoSettingsType_services_zones {
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

export interface get_user_connections_user_connections_ColissimoSettingsType_services {
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
  zones: get_user_connections_user_connections_ColissimoSettingsType_services_zones[];
}

export interface get_user_connections_user_connections_ColissimoSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface get_user_connections_user_connections_ColissimoSettingsType {
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
  services: get_user_connections_user_connections_ColissimoSettingsType_services[] | null;
  rate_sheet: get_user_connections_user_connections_ColissimoSettingsType_rate_sheet | null;
}

export interface get_user_connections_user_connections_DHLParcelDESettingsType_services_zones {
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

export interface get_user_connections_user_connections_DHLParcelDESettingsType_services {
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
  zones: get_user_connections_user_connections_DHLParcelDESettingsType_services_zones[];
}

export interface get_user_connections_user_connections_DHLParcelDESettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface get_user_connections_user_connections_DHLParcelDESettingsType {
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
  services: get_user_connections_user_connections_DHLParcelDESettingsType_services[] | null;
  rate_sheet: get_user_connections_user_connections_DHLParcelDESettingsType_rate_sheet | null;
}

export interface get_user_connections_user_connections_DHLExpressSettingsType {
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

export interface get_user_connections_user_connections_DHLPolandSettingsType_services_zones {
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

export interface get_user_connections_user_connections_DHLPolandSettingsType_services {
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
  zones: get_user_connections_user_connections_DHLPolandSettingsType_services_zones[];
}

export interface get_user_connections_user_connections_DHLPolandSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface get_user_connections_user_connections_DHLPolandSettingsType {
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
  services: get_user_connections_user_connections_DHLPolandSettingsType_services[] | null;
  rate_sheet: get_user_connections_user_connections_DHLPolandSettingsType_rate_sheet | null;
}

export interface get_user_connections_user_connections_DHLUniversalSettingsType {
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

export interface get_user_connections_user_connections_DicomSettingsType {
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

export interface get_user_connections_user_connections_DPDSettingsType_services_zones {
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

export interface get_user_connections_user_connections_DPDSettingsType_services {
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
  zones: get_user_connections_user_connections_DPDSettingsType_services_zones[];
}

export interface get_user_connections_user_connections_DPDSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface get_user_connections_user_connections_DPDSettingsType {
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
  services: get_user_connections_user_connections_DPDSettingsType_services[] | null;
  rate_sheet: get_user_connections_user_connections_DPDSettingsType_rate_sheet | null;
}

export interface get_user_connections_user_connections_DPDHLSettingsType_services_zones {
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

export interface get_user_connections_user_connections_DPDHLSettingsType_services {
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
  zones: get_user_connections_user_connections_DPDHLSettingsType_services_zones[];
}

export interface get_user_connections_user_connections_DPDHLSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface get_user_connections_user_connections_DPDHLSettingsType {
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
  services: get_user_connections_user_connections_DPDHLSettingsType_services[] | null;
  rate_sheet: get_user_connections_user_connections_DPDHLSettingsType_rate_sheet | null;
}

export interface get_user_connections_user_connections_EShipperSettingsType {
  __typename: "EShipperSettingsType";
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

export interface get_user_connections_user_connections_EasyPostSettingsType {
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

export interface get_user_connections_user_connections_FedexSettingsType {
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

export interface get_user_connections_user_connections_FedexWSSettingsType {
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

export interface get_user_connections_user_connections_FreightcomSettingsType {
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

export interface get_user_connections_user_connections_GenericSettingsType_services_zones {
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

export interface get_user_connections_user_connections_GenericSettingsType_services {
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
  zones: get_user_connections_user_connections_GenericSettingsType_services_zones[];
}

export interface get_user_connections_user_connections_GenericSettingsType_label_template {
  id: string;
  slug: string | null;
  template: string | null;
  template_type: LabelTemplateTypeEnum | null;
  shipment_sample: any | null;
  width: number | null;
  height: number | null;
}

export interface get_user_connections_user_connections_GenericSettingsType_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface get_user_connections_user_connections_GenericSettingsType {
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
  services: get_user_connections_user_connections_GenericSettingsType_services[] | null;
  label_template: get_user_connections_user_connections_GenericSettingsType_label_template | null;
  rate_sheet: get_user_connections_user_connections_GenericSettingsType_rate_sheet | null;
}

export interface get_user_connections_user_connections_GEODISSettingsType {
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

export interface get_user_connections_user_connections_LaPosteSettingsType {
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

export interface get_user_connections_user_connections_Locate2uSettingsType {
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

export interface get_user_connections_user_connections_NationexSettingsType {
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

export interface get_user_connections_user_connections_PurolatorSettingsType {
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

export interface get_user_connections_user_connections_RoadieSettingsType {
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

export interface get_user_connections_user_connections_RoyalMailSettingsType {
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

export interface get_user_connections_user_connections_SendleSettingsType {
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

export interface get_user_connections_user_connections_TGESettingsType {
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

export interface get_user_connections_user_connections_TNTSettingsType {
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

export interface get_user_connections_user_connections_UPSSettingsType {
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

export interface get_user_connections_user_connections_USPSSettingsType {
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

export interface get_user_connections_user_connections_USPSInternationalSettingsType {
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

export interface get_user_connections_user_connections_Zoom2uSettingsType {
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

export type get_user_connections_user_connections = get_user_connections_user_connections_AlliedExpressSettingsType | get_user_connections_user_connections_AlliedExpressLocalSettingsType | get_user_connections_user_connections_AmazonShippingSettingsType | get_user_connections_user_connections_AramexSettingsType | get_user_connections_user_connections_AsendiaUSSettingsType | get_user_connections_user_connections_AustraliaPostSettingsType | get_user_connections_user_connections_BoxKnightSettingsType | get_user_connections_user_connections_BelgianPostSettingsType | get_user_connections_user_connections_CanadaPostSettingsType | get_user_connections_user_connections_CanparSettingsType | get_user_connections_user_connections_ChronopostSettingsType | get_user_connections_user_connections_ColissimoSettingsType | get_user_connections_user_connections_DHLParcelDESettingsType | get_user_connections_user_connections_DHLExpressSettingsType | get_user_connections_user_connections_DHLPolandSettingsType | get_user_connections_user_connections_DHLUniversalSettingsType | get_user_connections_user_connections_DicomSettingsType | get_user_connections_user_connections_DPDSettingsType | get_user_connections_user_connections_DPDHLSettingsType | get_user_connections_user_connections_EShipperSettingsType | get_user_connections_user_connections_EasyPostSettingsType | get_user_connections_user_connections_FedexSettingsType | get_user_connections_user_connections_FedexWSSettingsType | get_user_connections_user_connections_FreightcomSettingsType | get_user_connections_user_connections_GenericSettingsType | get_user_connections_user_connections_GEODISSettingsType | get_user_connections_user_connections_LaPosteSettingsType | get_user_connections_user_connections_Locate2uSettingsType | get_user_connections_user_connections_NationexSettingsType | get_user_connections_user_connections_PurolatorSettingsType | get_user_connections_user_connections_RoadieSettingsType | get_user_connections_user_connections_RoyalMailSettingsType | get_user_connections_user_connections_SendleSettingsType | get_user_connections_user_connections_TGESettingsType | get_user_connections_user_connections_TNTSettingsType | get_user_connections_user_connections_UPSSettingsType | get_user_connections_user_connections_USPSSettingsType | get_user_connections_user_connections_USPSInternationalSettingsType | get_user_connections_user_connections_Zoom2uSettingsType;

export interface get_user_connections {
  user_connections: get_user_connections_user_connections[];
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
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_shipment_shipper {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_shipment_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_shipment_parcels_items {
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

export interface get_shipment_shipment_parcels {
  id: string;
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
  items: get_shipment_shipment_parcels_items[];
}

export interface get_shipment_shipment_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
}

export interface get_shipment_shipment_customs_commodities {
  id: string;
  weight: number;
  weight_unit: WeightUnitEnum | null;
  title: string | null;
  description: string | null;
  quantity: number;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any;
  parent_id: string | null;
}

export interface get_shipment_shipment_customs_duty_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_shipment_customs {
  id: string;
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  duty: get_shipment_shipment_customs_duty | null;
  options: any | null;
  commodities: get_shipment_shipment_customs_commodities[];
  duty_billing_address: get_shipment_shipment_customs_duty_billing_address | null;
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
  carrier_id: string;
  carrier_name: string;
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
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipments_shipments_edges_node_shipper {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipments_shipments_edges_node_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipments_shipments_edges_node_parcels_items {
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

export interface get_shipments_shipments_edges_node_parcels {
  id: string;
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
  items: get_shipments_shipments_edges_node_parcels_items[];
}

export interface get_shipments_shipments_edges_node_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
}

export interface get_shipments_shipments_edges_node_customs_commodities {
  id: string;
  weight: number;
  weight_unit: WeightUnitEnum | null;
  title: string | null;
  description: string | null;
  quantity: number;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any;
  parent_id: string | null;
}

export interface get_shipments_shipments_edges_node_customs_duty_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipments_shipments_edges_node_customs {
  id: string;
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  duty: get_shipments_shipments_edges_node_customs_duty | null;
  options: any | null;
  commodities: get_shipments_shipments_edges_node_customs_commodities[];
  duty_billing_address: get_shipments_shipments_edges_node_customs_duty_billing_address | null;
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
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_data_shipment_shipper {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_data_shipment_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_data_shipment_parcels_items {
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

export interface get_shipment_data_shipment_parcels {
  id: string;
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
  items: get_shipment_data_shipment_parcels_items[];
}

export interface get_shipment_data_shipment_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
}

export interface get_shipment_data_shipment_customs_commodities {
  id: string;
  weight: number;
  weight_unit: WeightUnitEnum | null;
  title: string | null;
  description: string | null;
  quantity: number;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any;
  parent_id: string | null;
}

export interface get_shipment_data_shipment_customs_duty_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_shipment_data_shipment_customs {
  id: string;
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  duty: get_shipment_data_shipment_customs_duty | null;
  options: any | null;
  commodities: get_shipment_data_shipment_customs_commodities[];
  duty_billing_address: get_shipment_data_shipment_customs_duty_billing_address | null;
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
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_shipper {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_parcels_items {
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

export interface partial_shipment_update_partial_shipment_update_shipment_parcels {
  id: string;
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
  items: partial_shipment_update_partial_shipment_update_shipment_parcels_items[];
}

export interface partial_shipment_update_partial_shipment_update_shipment_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_customs_commodities {
  id: string;
  weight: number;
  weight_unit: WeightUnitEnum | null;
  title: string | null;
  description: string | null;
  quantity: number;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any;
  parent_id: string | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_customs_duty_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface partial_shipment_update_partial_shipment_update_shipment_customs {
  id: string;
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  duty: partial_shipment_update_partial_shipment_update_shipment_customs_duty | null;
  options: any | null;
  commodities: partial_shipment_update_partial_shipment_update_shipment_customs_commodities[];
  duty_billing_address: partial_shipment_update_partial_shipment_update_shipment_customs_duty_billing_address | null;
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
  country_code: CountryCodeEnum;
}

export interface get_tracker_tracker_shipment_recipient {
  city: string | null;
  country_code: CountryCodeEnum;
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
  country_code: CountryCodeEnum;
}

export interface get_trackers_trackers_edges_node_shipment_recipient {
  city: string | null;
  country_code: CountryCodeEnum;
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
// GraphQL query operation: get_address_templates
// ====================================================

export interface get_address_templates_address_templates_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_address_templates_address_templates_edges_node_address {
  company_name: string | null;
  person_name: string | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  postal_code: string | null;
  residential: boolean | null;
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_address_templates_address_templates_edges_node {
  id: string;
  is_default: boolean | null;
  label: string;
  address: get_address_templates_address_templates_edges_node_address;
}

export interface get_address_templates_address_templates_edges {
  node: get_address_templates_address_templates_edges_node;
}

export interface get_address_templates_address_templates {
  page_info: get_address_templates_address_templates_page_info;
  edges: get_address_templates_address_templates_edges[];
}

export interface get_address_templates {
  address_templates: get_address_templates_address_templates;
}

export interface get_address_templatesVariables {
  filter?: AddressFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_customs_info_templates
// ====================================================

export interface get_customs_info_templates_customs_templates_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_customs_info_templates_customs_templates_edges_node_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
}

export interface get_customs_info_templates_customs_templates_edges_node_customs {
  incoterm: IncotermCodeEnum | null;
  content_type: CustomsContentTypeEnum | null;
  commercial_invoice: boolean | null;
  content_description: string | null;
  duty: get_customs_info_templates_customs_templates_edges_node_customs_duty | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  certify: boolean | null;
  options: any | null;
}

export interface get_customs_info_templates_customs_templates_edges_node {
  id: string;
  label: string;
  is_default: boolean | null;
  customs: get_customs_info_templates_customs_templates_edges_node_customs;
}

export interface get_customs_info_templates_customs_templates_edges {
  node: get_customs_info_templates_customs_templates_edges_node;
}

export interface get_customs_info_templates_customs_templates {
  page_info: get_customs_info_templates_customs_templates_page_info;
  edges: get_customs_info_templates_customs_templates_edges[];
}

export interface get_customs_info_templates {
  customs_templates: get_customs_info_templates_customs_templates;
}

export interface get_customs_info_templatesVariables {
  filter?: TemplateFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_default_templates
// ====================================================

export interface get_default_templates_default_templates_default_address_address {
  company_name: string | null;
  person_name: string | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  postal_code: string | null;
  residential: boolean | null;
  city: string | null;
  state_code: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_default_templates_default_templates_default_address {
  id: string;
  is_default: boolean | null;
  label: string;
  address: get_default_templates_default_templates_default_address_address;
}

export interface get_default_templates_default_templates_default_customs_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
}

export interface get_default_templates_default_templates_default_customs_customs {
  incoterm: IncotermCodeEnum | null;
  content_type: CustomsContentTypeEnum | null;
  commercial_invoice: boolean | null;
  content_description: string | null;
  duty: get_default_templates_default_templates_default_customs_customs_duty | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  certify: boolean | null;
  options: any | null;
}

export interface get_default_templates_default_templates_default_customs {
  id: string;
  label: string;
  is_default: boolean | null;
  customs: get_default_templates_default_templates_default_customs_customs;
}

export interface get_default_templates_default_templates_default_parcel_parcel {
  width: number | null;
  height: number | null;
  length: number | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  is_document: boolean | null;
}

export interface get_default_templates_default_templates_default_parcel {
  id: string;
  is_default: boolean | null;
  label: string;
  parcel: get_default_templates_default_templates_default_parcel_parcel;
}

export interface get_default_templates_default_templates {
  default_address: get_default_templates_default_templates_default_address | null;
  default_customs: get_default_templates_default_templates_default_customs | null;
  default_parcel: get_default_templates_default_templates_default_parcel | null;
}

export interface get_default_templates {
  default_templates: get_default_templates_default_templates;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_parcel_templates
// ====================================================

export interface get_parcel_templates_parcel_templates_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface get_parcel_templates_parcel_templates_edges_node_parcel {
  width: number | null;
  height: number | null;
  length: number | null;
  dimension_unit: DimensionUnitEnum | null;
  weight: number | null;
  weight_unit: WeightUnitEnum | null;
  packaging_type: string | null;
  package_preset: string | null;
  is_document: boolean | null;
}

export interface get_parcel_templates_parcel_templates_edges_node {
  id: string;
  is_default: boolean | null;
  label: string;
  parcel: get_parcel_templates_parcel_templates_edges_node_parcel;
}

export interface get_parcel_templates_parcel_templates_edges {
  node: get_parcel_templates_parcel_templates_edges_node;
}

export interface get_parcel_templates_parcel_templates {
  page_info: get_parcel_templates_parcel_templates_page_info;
  edges: get_parcel_templates_parcel_templates_edges[];
}

export interface get_parcel_templates {
  parcel_templates: get_parcel_templates_parcel_templates;
}

export interface get_parcel_templatesVariables {
  filter?: TemplateFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_system_connections
// ====================================================

export interface get_system_connections_system_connections {
  id: string;
  carrier_id: string;
  test_mode: boolean;
  active: boolean;
  capabilities: string[];
  carrier_name: string;
  display_name: string;
  enabled: boolean;
  config: any | null;
}

export interface get_system_connections {
  system_connections: get_system_connections_system_connections[];
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
// GraphQL mutation operation: create_customs_template
// ====================================================

export interface create_customs_template_create_customs_template_template {
  id: string;
}

export interface create_customs_template_create_customs_template_errors {
  field: string;
  messages: string[];
}

export interface create_customs_template_create_customs_template {
  template: create_customs_template_create_customs_template_template | null;
  errors: create_customs_template_create_customs_template_errors[] | null;
}

export interface create_customs_template {
  create_customs_template: create_customs_template_create_customs_template;
}

export interface create_customs_templateVariables {
  data: CreateCustomsTemplateInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_customs_template
// ====================================================

export interface update_customs_template_update_customs_template_template {
  id: string;
}

export interface update_customs_template_update_customs_template_errors {
  field: string;
  messages: string[];
}

export interface update_customs_template_update_customs_template {
  template: update_customs_template_update_customs_template_template | null;
  errors: update_customs_template_update_customs_template_errors[] | null;
}

export interface update_customs_template {
  update_customs_template: update_customs_template_update_customs_template;
}

export interface update_customs_templateVariables {
  data: UpdateCustomsTemplateInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: delete_template
// ====================================================

export interface delete_template_delete_template {
  id: string;
}

export interface delete_template {
  delete_template: delete_template_delete_template;
}

export interface delete_templateVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: create_parcel_template
// ====================================================

export interface create_parcel_template_create_parcel_template_template {
  id: string;
}

export interface create_parcel_template_create_parcel_template_errors {
  field: string;
  messages: string[];
}

export interface create_parcel_template_create_parcel_template {
  template: create_parcel_template_create_parcel_template_template | null;
  errors: create_parcel_template_create_parcel_template_errors[] | null;
}

export interface create_parcel_template {
  create_parcel_template: create_parcel_template_create_parcel_template;
}

export interface create_parcel_templateVariables {
  data: CreateParcelTemplateInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_parcel_template
// ====================================================

export interface update_parcel_template_update_parcel_template_template {
  id: string;
}

export interface update_parcel_template_update_parcel_template_errors {
  field: string;
  messages: string[];
}

export interface update_parcel_template_update_parcel_template {
  template: update_parcel_template_update_parcel_template_template | null;
  errors: update_parcel_template_update_parcel_template_errors[] | null;
}

export interface update_parcel_template {
  update_parcel_template: update_parcel_template_update_parcel_template;
}

export interface update_parcel_templateVariables {
  data: UpdateParcelTemplateInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: create_address_template
// ====================================================

export interface create_address_template_create_address_template_template {
  id: string;
}

export interface create_address_template_create_address_template_errors {
  field: string;
  messages: string[];
}

export interface create_address_template_create_address_template {
  template: create_address_template_create_address_template_template | null;
  errors: create_address_template_create_address_template_errors[] | null;
}

export interface create_address_template {
  create_address_template: create_address_template_create_address_template;
}

export interface create_address_templateVariables {
  data: CreateAddressTemplateInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_address_template
// ====================================================

export interface update_address_template_update_address_template_template {
  id: string;
}

export interface update_address_template_update_address_template_errors {
  field: string;
  messages: string[];
}

export interface update_address_template_update_address_template {
  template: update_address_template_update_address_template_template | null;
  errors: update_address_template_update_address_template_errors[] | null;
}

export interface update_address_template {
  update_address_template: update_address_template_update_address_template;
}

export interface update_address_templateVariables {
  data: UpdateAddressTemplateInput;
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
// GraphQL mutation operation: discard_customs
// ====================================================

export interface discard_customs_discard_customs {
  id: string;
}

export interface discard_customs {
  discard_customs: discard_customs_discard_customs;
}

export interface discard_customsVariables {
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
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipping_from {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
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
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipments_shipper {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipments_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipments_parcels_items {
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

export interface get_order_order_shipments_parcels {
  id: string;
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
  items: get_order_order_shipments_parcels_items[];
}

export interface get_order_order_shipments_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
}

export interface get_order_order_shipments_customs_commodities {
  id: string;
  weight: number;
  weight_unit: WeightUnitEnum | null;
  title: string | null;
  description: string | null;
  quantity: number;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any;
  parent_id: string | null;
}

export interface get_order_order_shipments_customs_duty_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_order_shipments_customs {
  id: string;
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  duty: get_order_order_shipments_customs_duty | null;
  options: any | null;
  commodities: get_order_order_shipments_customs_commodities[];
  duty_billing_address: get_order_order_shipments_customs_duty_billing_address | null;
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
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_data_order_shipping_from {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_order_data_order_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
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
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipping_from {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
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
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipments_shipper {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipments_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipments_parcels_items {
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

export interface get_orders_orders_edges_node_shipments_parcels {
  id: string;
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
  items: get_orders_orders_edges_node_shipments_parcels_items[];
}

export interface get_orders_orders_edges_node_shipments_customs_duty {
  paid_by: PaidByEnum | null;
  currency: CurrencyCodeEnum | null;
  account_number: string | null;
  declared_value: number | null;
}

export interface get_orders_orders_edges_node_shipments_customs_commodities {
  id: string;
  weight: number;
  weight_unit: WeightUnitEnum | null;
  title: string | null;
  description: string | null;
  quantity: number;
  sku: string | null;
  hs_code: string | null;
  value_amount: number | null;
  value_currency: CurrencyCodeEnum | null;
  origin_country: CountryCodeEnum | null;
  metadata: any;
  parent_id: string | null;
}

export interface get_orders_orders_edges_node_shipments_customs_duty_billing_address {
  id: string;
  postal_code: string | null;
  city: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  suburb: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  validate_location: boolean | null;
}

export interface get_orders_orders_edges_node_shipments_customs {
  id: string;
  certify: boolean | null;
  commercial_invoice: boolean | null;
  content_type: CustomsContentTypeEnum | null;
  content_description: string | null;
  incoterm: IncotermCodeEnum | null;
  invoice: string | null;
  invoice_date: string | null;
  signer: string | null;
  duty: get_orders_orders_edges_node_shipments_customs_duty | null;
  options: any | null;
  commodities: get_orders_orders_edges_node_shipments_customs_commodities[];
  duty_billing_address: get_orders_orders_edges_node_shipments_customs_duty_billing_address | null;
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
  updated_at: any | null;
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
// GraphQL mutation operation: DeteRateSheet
// ====================================================

export interface DeteRateSheet_delete_rate_sheet_errors {
  field: string;
  messages: string[];
}

export interface DeteRateSheet_delete_rate_sheet {
  id: string;
  errors: DeteRateSheet_delete_rate_sheet_errors[] | null;
}

export interface DeteRateSheet {
  delete_rate_sheet: DeteRateSheet_delete_rate_sheet;
}

export interface DeteRateSheetVariables {
  data: DeleteMutationInput;
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
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
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
  cities: string[] | null;
  postal_codes: string[] | null;
  country_codes: CountryCodeEnum[] | null;
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
  id: string;
  postal_code: string | null;
  city: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
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
  id: string;
  postal_code: string | null;
  city: string | null;
  federal_tax_id: string | null;
  state_tax_id: string | null;
  person_name: string | null;
  company_name: string | null;
  country_code: CountryCodeEnum;
  email: string | null;
  phone_number: string | null;
  state_code: string | null;
  residential: boolean | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
}

export interface GetManifest_manifest_manifest_carrier {
  carrier_id: string;
  carrier_name: string;
  config: any | null;
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
  manifest_carrier: GetManifest_manifest_manifest_carrier | null;
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
// GraphQL query operation: GetApp
// ====================================================

export interface GetApp_app_installation {
  id: number;
  access_scopes: string[];
  metadata: any | null;
}

export interface GetApp_app {
  id: string;
  display_name: string;
  developer_name: string;
  is_public: boolean;
  is_builtin: boolean;
  is_embedded: boolean;
  is_published: boolean;
  launch_url: string;
  features: string[];
  metadata: any | null;
  installation: GetApp_app_installation | null;
}

export interface GetApp {
  app: GetApp_app;
}

export interface GetAppVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetApps
// ====================================================

export interface GetApps_apps_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetApps_apps_edges_node_installation {
  id: number;
  access_scopes: string[];
  metadata: any | null;
}

export interface GetApps_apps_edges_node {
  id: string;
  display_name: string;
  developer_name: string;
  is_public: boolean;
  is_builtin: boolean;
  is_embedded: boolean;
  is_published: boolean;
  launch_url: string;
  features: string[];
  metadata: any | null;
  installation: GetApps_apps_edges_node_installation | null;
}

export interface GetApps_apps_edges {
  node: GetApps_apps_edges_node;
}

export interface GetApps_apps {
  page_info: GetApps_apps_page_info;
  edges: GetApps_apps_edges[];
}

export interface GetApps {
  apps: GetApps_apps;
}

export interface GetAppsVariables {
  filter?: AppFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetPrivateApp
// ====================================================

export interface GetPrivateApp_private_app_installation {
  id: number;
  access_scopes: string[];
  metadata: any | null;
}

export interface GetPrivateApp_private_app {
  id: string;
  display_name: string;
  developer_name: string;
  is_public: boolean;
  is_builtin: boolean;
  is_embedded: boolean;
  is_published: boolean;
  launch_url: string;
  features: string[];
  metadata: any | null;
  installation: GetPrivateApp_private_app_installation | null;
}

export interface GetPrivateApp {
  private_app: GetPrivateApp_private_app;
}

export interface GetPrivateAppVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetPrivateApps
// ====================================================

export interface GetPrivateApps_private_apps_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetPrivateApps_private_apps_edges_node_installation {
  id: number;
  access_scopes: string[];
  metadata: any | null;
}

export interface GetPrivateApps_private_apps_edges_node {
  id: string;
  display_name: string;
  developer_name: string;
  is_public: boolean;
  is_builtin: boolean;
  is_embedded: boolean;
  is_published: boolean;
  launch_url: string;
  features: string[];
  metadata: any | null;
  installation: GetPrivateApps_private_apps_edges_node_installation | null;
}

export interface GetPrivateApps_private_apps_edges {
  node: GetPrivateApps_private_apps_edges_node;
}

export interface GetPrivateApps_private_apps {
  page_info: GetPrivateApps_private_apps_page_info;
  edges: GetPrivateApps_private_apps_edges[];
}

export interface GetPrivateApps {
  private_apps: GetPrivateApps_private_apps;
}

export interface GetPrivateAppsVariables {
  filter?: AppFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: InstallApp
// ====================================================

export interface InstallApp_install_app_installation {
  id: number;
  access_scopes: string[];
  created_at: any;
  updated_at: any;
  metadata: any | null;
}

export interface InstallApp_install_app_errors {
  field: string;
  messages: string[];
}

export interface InstallApp_install_app {
  installation: InstallApp_install_app_installation | null;
  errors: InstallApp_install_app_errors[] | null;
}

export interface InstallApp {
  install_app: InstallApp_install_app;
}

export interface InstallAppVariables {
  data: InstallAppMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UninstallApp
// ====================================================

export interface UninstallApp_uninstall_app_app_installation {
  id: number;
  access_scopes: string[];
  metadata: any | null;
}

export interface UninstallApp_uninstall_app_app {
  id: string;
  display_name: string;
  developer_name: string;
  is_public: boolean;
  is_builtin: boolean;
  is_embedded: boolean;
  is_published: boolean;
  launch_url: string;
  features: string[];
  metadata: any | null;
  installation: UninstallApp_uninstall_app_app_installation | null;
}

export interface UninstallApp_uninstall_app_errors {
  field: string;
  messages: string[];
}

export interface UninstallApp_uninstall_app {
  app: UninstallApp_uninstall_app_app | null;
  errors: UninstallApp_uninstall_app_errors[] | null;
}

export interface UninstallApp {
  uninstall_app: UninstallApp_uninstall_app;
}

export interface UninstallAppVariables {
  data: UninstallAppMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: search_data
// ====================================================

export interface search_data_shipment_results_edges_node_recipient {
  id: string;
  city: string | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  country_code: CountryCodeEnum;
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
  id: string;
  city: string | null;
  street_number: string | null;
  address_line1: string | null;
  address_line2: string | null;
  country_code: CountryCodeEnum;
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

//==============================================================
// START Enums and Input Objects
//==============================================================

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

export enum LabelTemplateTypeEnum {
  SVG = "SVG",
  ZPL = "ZPL",
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
  delivered = "delivered",
  delivery_delayed = "delivery_delayed",
  delivery_failed = "delivery_failed",
  in_transit = "in_transit",
  on_hold = "on_hold",
  out_for_delivery = "out_for_delivery",
  pending = "pending",
  ready_for_pickup = "ready_for_pickup",
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

export enum TemplateRelatedObject {
  order = "order",
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

export enum MetadataObjectTypeEnum {
  app = "app",
  carrier = "carrier",
  commodity = "commodity",
  order = "order",
  shipment = "shipment",
  tracker = "tracker",
}

// null
export interface CreateCarrierConnectionMutationInput {
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
  username: string;
  password: string;
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
export interface UpdateCarrierConnectionMutationInput {
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
  username?: string | null;
  password?: string | null;
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
export interface DeleteMutationInput {
  id: string;
}

// null
export interface LogFilter {
  offset?: number | null;
  first?: number | null;
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
  created_after?: any | null;
  created_before?: any | null;
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
  customs?: UpdateCustomsInput | null;
  parcels?: UpdateParcelInput[] | null;
  payment?: PaymentInput | null;
  billing_address?: UpdateAddressInput | null;
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
  suburb?: string | null;
  residential?: boolean | null;
  street_number?: string | null;
  address_line1?: string | null;
  address_line2?: string | null;
  validate_location?: boolean | null;
  id?: string | null;
}

// null
export interface UpdateCustomsInput {
  commodities?: UpdateCommodityInput[] | null;
  certify?: boolean | null;
  commercial_invoice?: boolean | null;
  content_type?: CustomsContentTypeEnum | null;
  content_description?: string | null;
  incoterm?: IncotermCodeEnum | null;
  invoice?: string | null;
  invoice_date?: string | null;
  signer?: string | null;
  duty?: UpdateDutyInput | null;
  duty_billing_address?: UpdateAddressInput | null;
  options?: any | null;
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
export interface UpdateDutyInput {
  paid_by?: PaidByEnum | null;
  currency?: CurrencyCodeEnum | null;
  account_number?: string | null;
  declared_value?: number | null;
  bill_to?: AddressInput | null;
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
  suburb?: string | null;
  residential?: boolean | null;
  street_number?: string | null;
  address_line1?: string | null;
  address_line2?: string | null;
  validate_location?: boolean | null;
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
  created_after?: any | null;
  created_before?: any | null;
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
export interface AddressFilter {
  offset?: number | null;
  first?: number | null;
  label?: string | null;
  keyword?: string | null;
  address?: string | null;
}

// null
export interface TemplateFilter {
  offset?: number | null;
  first?: number | null;
  label?: string | null;
  keyword?: string | null;
}

// null
export interface SystemCarrierMutationInput {
  id: string;
  enable?: boolean | null;
  config?: any | null;
}

// null
export interface CreateCustomsTemplateInput {
  label: string;
  customs: CustomsInput;
  is_default?: boolean | null;
}

// null
export interface CustomsInput {
  commodities: CommodityInput[];
  certify?: boolean | null;
  commercial_invoice?: boolean | null;
  content_type?: CustomsContentTypeEnum | null;
  content_description?: string | null;
  incoterm?: IncotermCodeEnum | null;
  invoice?: string | null;
  invoice_date?: string | null;
  signer?: string | null;
  duty?: DutyInput | null;
  duty_billing_address?: UpdateAddressInput | null;
  options?: any | null;
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
export interface DutyInput {
  paid_by: PaidByEnum;
  currency?: CurrencyCodeEnum | null;
  account_number?: string | null;
  declared_value?: number | null;
  bill_to?: AddressInput | null;
}

// null
export interface UpdateCustomsTemplateInput {
  label?: string | null;
  customs?: UpdateCustomsInput | null;
  is_default?: boolean | null;
  id: string;
}

// null
export interface CreateParcelTemplateInput {
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
export interface UpdateParcelTemplateInput {
  label?: string | null;
  parcel?: UpdateParcelInput | null;
  is_default?: boolean | null;
  id: string;
}

// null
export interface CreateAddressTemplateInput {
  label: string;
  address: AddressInput;
  is_default?: boolean | null;
}

// null
export interface UpdateAddressTemplateInput {
  label?: string | null;
  address?: UpdateAddressInput | null;
  is_default?: boolean | null;
  id: string;
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
  related_object: TemplateRelatedObject;
  active?: boolean | null;
  description?: string | null;
}

// null
export interface UpdateDocumentTemplateMutationInput {
  id: string;
  slug?: string | null;
  name?: string | null;
  template?: string | null;
  active?: boolean | null;
  description?: string | null;
  related_object?: TemplateRelatedObject | null;
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

// null
export interface RateSheetFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
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
export interface AppFilter {
  offset?: number | null;
  first?: number | null;
  features: string[];
  metadata_key?: string | null;
  metadata_value?: string | null;
  created_after?: any | null;
  created_before?: any | null;
}

// null
export interface InstallAppMutationInput {
  app_id: string;
  metadata?: any | null;
}

// null
export interface UninstallAppMutationInput {
  app_id: string;
}

// null
export interface MetadataMutationInput {
  id: string;
  object_type: MetadataObjectTypeEnum;
  added_values: any;
  discarded_keys?: string[] | null;
}

//==============================================================
// END Enums and Input Objects
//==============================================================