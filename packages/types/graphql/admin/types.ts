

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

export interface GetSystemConnections_system_connections_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnections_system_connections {
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
  rate_sheet: GetSystemConnections_system_connections_rate_sheet | null;
}

export interface GetSystemConnections {
  system_connections: GetSystemConnections_system_connections[];
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSystemConnection
// ====================================================

export interface GetSystemConnection_system_connection_rate_sheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: CarrierNameEnum;
  metadata: any | null;
}

export interface GetSystemConnection_system_connection {
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
  rate_sheet: GetSystemConnection_system_connection_rate_sheet | null;
}

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
  easyship = "easyship",
  eshipper = "eshipper",
  fedex = "fedex",
  fedex_ws = "fedex_ws",
  freightcom = "freightcom",
  generic = "generic",
  geodis = "geodis",
  hay_post = "hay_post",
  laposte = "laposte",
  locate2u = "locate2u",
  nationex = "nationex",
  purolator = "purolator",
  roadie = "roadie",
  royalmail = "royalmail",
  sapient = "sapient",
  seko = "seko",
  sendle = "sendle",
  tge = "tge",
  tnt = "tnt",
  ups = "ups",
  usps = "usps",
  usps_international = "usps_international",
  usps_wt = "usps_wt",
  usps_wt_international = "usps_wt_international",
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
export interface UpdateRateSheetMutationInput {
  id: string;
  name?: string | null;
  services?: UpdateServiceLevelInput[] | null;
  carriers?: string[] | null;
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

//==============================================================
// END Enums and Input Objects
//==============================================================