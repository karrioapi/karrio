/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTenant
// ====================================================

export interface GetTenant_tenant_usage_api_errors {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenant_tenant_usage_api_requests {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenant_tenant_usage_order_volumes {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenant_tenant_usage_shipment_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenant_tenant_usage_shipping_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenant_tenant_usage_tracker_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenant_tenant_usage {
  total_errors: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  organization_count: number | null;
  user_count: number | null;
  total_shipping_spend: number | null;
  api_errors: GetTenant_tenant_usage_api_errors[] | null;
  api_requests: GetTenant_tenant_usage_api_requests[] | null;
  order_volumes: GetTenant_tenant_usage_order_volumes[] | null;
  shipment_count: GetTenant_tenant_usage_shipment_count[] | null;
  shipping_spend: GetTenant_tenant_usage_shipping_spend[] | null;
  tracker_count: GetTenant_tenant_usage_tracker_count[] | null;
}

export interface GetTenant_tenant_domains {
  object_type: string;
  id: string;
  domain: string;
  is_primary: boolean;
}

export interface GetTenant_tenant {
  object_type: string;
  id: string;
  name: string;
  schema_name: string;
  feature_flags: any | null;
  app_domains: string[] | null;
  created_at: any | null;
  updated_at: any | null;
  usage: GetTenant_tenant_usage | null;
  domains: GetTenant_tenant_domains[];
  api_domains: string[] | null;
}

export interface GetTenant {
  tenant: GetTenant_tenant;
}

export interface GetTenantVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTenants
// ====================================================

export interface GetTenants_tenants_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetTenants_tenants_edges_node_usage_api_errors {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenants_tenants_edges_node_usage_api_requests {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenants_tenants_edges_node_usage_order_volumes {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenants_tenants_edges_node_usage_shipment_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenants_tenants_edges_node_usage_shipping_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenants_tenants_edges_node_usage_tracker_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetTenants_tenants_edges_node_usage {
  total_errors: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  organization_count: number | null;
  user_count: number | null;
  total_shipping_spend: number | null;
  api_errors: GetTenants_tenants_edges_node_usage_api_errors[] | null;
  api_requests: GetTenants_tenants_edges_node_usage_api_requests[] | null;
  order_volumes: GetTenants_tenants_edges_node_usage_order_volumes[] | null;
  shipment_count: GetTenants_tenants_edges_node_usage_shipment_count[] | null;
  shipping_spend: GetTenants_tenants_edges_node_usage_shipping_spend[] | null;
  tracker_count: GetTenants_tenants_edges_node_usage_tracker_count[] | null;
}

export interface GetTenants_tenants_edges_node_domains {
  object_type: string;
  id: string;
  domain: string;
  is_primary: boolean;
}

export interface GetTenants_tenants_edges_node {
  object_type: string;
  id: string;
  name: string;
  schema_name: string;
  feature_flags: any | null;
  app_domains: string[] | null;
  created_at: any | null;
  updated_at: any | null;
  usage: GetTenants_tenants_edges_node_usage | null;
  domains: GetTenants_tenants_edges_node_domains[];
  api_domains: string[] | null;
}

export interface GetTenants_tenants_edges {
  node: GetTenants_tenants_edges_node;
  cursor: string;
}

export interface GetTenants_tenants {
  page_info: GetTenants_tenants_page_info;
  edges: GetTenants_tenants_edges[];
}

export interface GetTenants {
  tenants: GetTenants_tenants;
}

export interface GetTenantsVariables {
  filter?: TenantFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateTenant
// ====================================================

export interface CreateTenant_create_tenant_errors {
  field: string;
  messages: string[];
}

export interface CreateTenant_create_tenant_tenant_usage_api_errors {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface CreateTenant_create_tenant_tenant_usage_api_requests {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface CreateTenant_create_tenant_tenant_usage_order_volumes {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface CreateTenant_create_tenant_tenant_usage_shipment_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface CreateTenant_create_tenant_tenant_usage_shipping_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface CreateTenant_create_tenant_tenant_usage_tracker_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface CreateTenant_create_tenant_tenant_usage {
  total_errors: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  organization_count: number | null;
  user_count: number | null;
  total_shipping_spend: number | null;
  api_errors: CreateTenant_create_tenant_tenant_usage_api_errors[] | null;
  api_requests: CreateTenant_create_tenant_tenant_usage_api_requests[] | null;
  order_volumes: CreateTenant_create_tenant_tenant_usage_order_volumes[] | null;
  shipment_count: CreateTenant_create_tenant_tenant_usage_shipment_count[] | null;
  shipping_spend: CreateTenant_create_tenant_tenant_usage_shipping_spend[] | null;
  tracker_count: CreateTenant_create_tenant_tenant_usage_tracker_count[] | null;
}

export interface CreateTenant_create_tenant_tenant_domains {
  object_type: string;
  id: string;
  domain: string;
  is_primary: boolean;
}

export interface CreateTenant_create_tenant_tenant {
  object_type: string;
  id: string;
  name: string;
  schema_name: string;
  feature_flags: any | null;
  app_domains: string[] | null;
  created_at: any | null;
  updated_at: any | null;
  usage: CreateTenant_create_tenant_tenant_usage | null;
  domains: CreateTenant_create_tenant_tenant_domains[];
  api_domains: string[] | null;
}

export interface CreateTenant_create_tenant {
  errors: CreateTenant_create_tenant_errors[] | null;
  tenant: CreateTenant_create_tenant_tenant | null;
}

export interface CreateTenant {
  create_tenant: CreateTenant_create_tenant;
}

export interface CreateTenantVariables {
  input: CreateTenantMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateTenant
// ====================================================

export interface UpdateTenant_update_tenant_errors {
  field: string;
  messages: string[];
}

export interface UpdateTenant_update_tenant_tenant_usage_api_errors {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface UpdateTenant_update_tenant_tenant_usage_api_requests {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface UpdateTenant_update_tenant_tenant_usage_order_volumes {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface UpdateTenant_update_tenant_tenant_usage_shipment_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface UpdateTenant_update_tenant_tenant_usage_shipping_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface UpdateTenant_update_tenant_tenant_usage_tracker_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface UpdateTenant_update_tenant_tenant_usage {
  total_errors: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  organization_count: number | null;
  user_count: number | null;
  total_shipping_spend: number | null;
  api_errors: UpdateTenant_update_tenant_tenant_usage_api_errors[] | null;
  api_requests: UpdateTenant_update_tenant_tenant_usage_api_requests[] | null;
  order_volumes: UpdateTenant_update_tenant_tenant_usage_order_volumes[] | null;
  shipment_count: UpdateTenant_update_tenant_tenant_usage_shipment_count[] | null;
  shipping_spend: UpdateTenant_update_tenant_tenant_usage_shipping_spend[] | null;
  tracker_count: UpdateTenant_update_tenant_tenant_usage_tracker_count[] | null;
}

export interface UpdateTenant_update_tenant_tenant_domains {
  object_type: string;
  id: string;
  domain: string;
  is_primary: boolean;
}

export interface UpdateTenant_update_tenant_tenant {
  object_type: string;
  id: string;
  name: string;
  schema_name: string;
  feature_flags: any | null;
  app_domains: string[] | null;
  created_at: any | null;
  updated_at: any | null;
  usage: UpdateTenant_update_tenant_tenant_usage | null;
  domains: UpdateTenant_update_tenant_tenant_domains[];
  api_domains: string[] | null;
}

export interface UpdateTenant_update_tenant {
  errors: UpdateTenant_update_tenant_errors[] | null;
  tenant: UpdateTenant_update_tenant_tenant | null;
}

export interface UpdateTenant {
  update_tenant: UpdateTenant_update_tenant;
}

export interface UpdateTenantVariables {
  input: UpdateTenantMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteTenant
// ====================================================

export interface DeleteTenant_delete_tenant_errors {
  field: string;
  messages: string[];
}

export interface DeleteTenant_delete_tenant {
  errors: DeleteTenant_delete_tenant_errors[] | null;
  id: string;
}

export interface DeleteTenant {
  delete_tenant: DeleteTenant_delete_tenant;
}

export interface DeleteTenantVariables {
  input: DeleteTenantMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: AddCustomDomain
// ====================================================

export interface AddCustomDomain_add_custom_domain_errors {
  field: string;
  messages: string[];
}

export interface AddCustomDomain_add_custom_domain_domain {
  object_type: string;
  id: string;
  domain: string;
  is_primary: boolean;
}

export interface AddCustomDomain_add_custom_domain {
  errors: AddCustomDomain_add_custom_domain_errors[] | null;
  domain: AddCustomDomain_add_custom_domain_domain | null;
}

export interface AddCustomDomain {
  add_custom_domain: AddCustomDomain_add_custom_domain;
}

export interface AddCustomDomainVariables {
  input: AddCustomDomainMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateCustomDomain
// ====================================================

export interface UpdateCustomDomain_update_custom_domain_errors {
  field: string;
  messages: string[];
}

export interface UpdateCustomDomain_update_custom_domain_domain {
  object_type: string;
  id: string;
  domain: string;
  is_primary: boolean;
}

export interface UpdateCustomDomain_update_custom_domain {
  errors: UpdateCustomDomain_update_custom_domain_errors[] | null;
  domain: UpdateCustomDomain_update_custom_domain_domain | null;
}

export interface UpdateCustomDomain {
  update_custom_domain: UpdateCustomDomain_update_custom_domain;
}

export interface UpdateCustomDomainVariables {
  input: UpdateCustomDomainMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteCustomDomain
// ====================================================

export interface DeleteCustomDomain_delete_custom_domain_errors {
  field: string;
  messages: string[];
}

export interface DeleteCustomDomain_delete_custom_domain {
  errors: DeleteCustomDomain_delete_custom_domain_errors[] | null;
  id: string | null;
}

export interface DeleteCustomDomain {
  delete_custom_domain: DeleteCustomDomain_delete_custom_domain;
}

export interface DeleteCustomDomainVariables {
  input: DeleteCustomDomainMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetUsageStats
// ====================================================

export interface GetUsageStats_usage_stats_api_errors {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetUsageStats_usage_stats_api_requests {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetUsageStats_usage_stats_order_volumes {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetUsageStats_usage_stats_shipment_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetUsageStats_usage_stats_shipping_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetUsageStats_usage_stats_tracker_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetUsageStats_usage_stats {
  total_errors: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  organization_count: number | null;
  user_count: number | null;
  total_shipping_spend: number | null;
  api_errors: GetUsageStats_usage_stats_api_errors[] | null;
  api_requests: GetUsageStats_usage_stats_api_requests[] | null;
  order_volumes: GetUsageStats_usage_stats_order_volumes[] | null;
  shipment_count: GetUsageStats_usage_stats_shipment_count[] | null;
  shipping_spend: GetUsageStats_usage_stats_shipping_spend[] | null;
  tracker_count: GetUsageStats_usage_stats_tracker_count[] | null;
}

export interface GetUsageStats {
  usage_stats: GetUsageStats_usage_stats;
}

export interface GetUsageStatsVariables {
  tenant_id: string;
  filter?: UsageFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: ResetTenantAdminPassword
// ====================================================

export interface ResetTenantAdminPassword_reset_tenant_admin_password_errors {
  field: string;
  messages: string[];
}

export interface ResetTenantAdminPassword_reset_tenant_admin_password {
  errors: ResetTenantAdminPassword_reset_tenant_admin_password_errors[] | null;
  success: boolean;
  password: string | null;
}

export interface ResetTenantAdminPassword {
  reset_tenant_admin_password: ResetTenantAdminPassword_reset_tenant_admin_password;
}

export interface ResetTenantAdminPasswordVariables {
  input: ResetTenantAdminPasswordMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnectedAccount
// ====================================================

export interface GetConnectedAccount_connected_account_usage_api_errors {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccount_connected_account_usage_api_requests {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccount_connected_account_usage_order_volumes {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccount_connected_account_usage_shipment_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccount_connected_account_usage_shipping_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccount_connected_account_usage_tracker_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccount_connected_account_usage {
  total_errors: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  members: number | null;
  unfulfilled_orders: number | null;
  total_shipping_spend: number | null;
  api_errors: GetConnectedAccount_connected_account_usage_api_errors[] | null;
  api_requests: GetConnectedAccount_connected_account_usage_api_requests[] | null;
  order_volumes: GetConnectedAccount_connected_account_usage_order_volumes[] | null;
  shipment_count: GetConnectedAccount_connected_account_usage_shipment_count[] | null;
  shipping_spend: GetConnectedAccount_connected_account_usage_shipping_spend[] | null;
  tracker_count: GetConnectedAccount_connected_account_usage_tracker_count[] | null;
}

export interface GetConnectedAccount_connected_account {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  created: any;
  modified: any;
  usage: GetConnectedAccount_connected_account_usage | null;
}

export interface GetConnectedAccount {
  connected_account: GetConnectedAccount_connected_account | null;
}

export interface GetConnectedAccountVariables {
  tenant_id: string;
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnectedAccounts
// ====================================================

export interface GetConnectedAccounts_connected_accounts_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetConnectedAccounts_connected_accounts_edges_node_usage_api_errors {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccounts_connected_accounts_edges_node_usage_api_requests {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccounts_connected_accounts_edges_node_usage_order_volumes {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccounts_connected_accounts_edges_node_usage_shipment_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccounts_connected_accounts_edges_node_usage_shipping_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccounts_connected_accounts_edges_node_usage_tracker_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface GetConnectedAccounts_connected_accounts_edges_node_usage {
  total_errors: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  members: number | null;
  unfulfilled_orders: number | null;
  total_shipping_spend: number | null;
  api_errors: GetConnectedAccounts_connected_accounts_edges_node_usage_api_errors[] | null;
  api_requests: GetConnectedAccounts_connected_accounts_edges_node_usage_api_requests[] | null;
  order_volumes: GetConnectedAccounts_connected_accounts_edges_node_usage_order_volumes[] | null;
  shipment_count: GetConnectedAccounts_connected_accounts_edges_node_usage_shipment_count[] | null;
  shipping_spend: GetConnectedAccounts_connected_accounts_edges_node_usage_shipping_spend[] | null;
  tracker_count: GetConnectedAccounts_connected_accounts_edges_node_usage_tracker_count[] | null;
}

export interface GetConnectedAccounts_connected_accounts_edges_node {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  created: any;
  modified: any;
  usage: GetConnectedAccounts_connected_accounts_edges_node_usage | null;
}

export interface GetConnectedAccounts_connected_accounts_edges {
  node: GetConnectedAccounts_connected_accounts_edges_node;
  cursor: string;
}

export interface GetConnectedAccounts_connected_accounts {
  page_info: GetConnectedAccounts_connected_accounts_page_info;
  edges: GetConnectedAccounts_connected_accounts_edges[];
}

export interface GetConnectedAccounts {
  connected_accounts: GetConnectedAccounts_connected_accounts | null;
}

export interface GetConnectedAccountsVariables {
  tenant_id: string;
  filter?: AccountFilter | null;
}

/* tslint:disable */
// This file was automatically generated and should not be edited.

//==============================================================
// START Enums and Input Objects
//==============================================================

// null
export interface TenantFilter {
  offset?: number | null;
  first?: number | null;
  app_domain?: string | null;
  api_domain?: string | null;
  schema_name?: string | null;
}

// null
export interface CreateTenantMutationInput {
  name: string;
  domain: string;
  schema_name: string;
  admin_email: string;
  feature_flags?: any | null;
  app_domains?: string[] | null;
}

// null
export interface UpdateTenantMutationInput {
  id: string;
  name?: string | null;
  feature_flags?: any | null;
  app_domains?: string[] | null;
}

// null
export interface DeleteTenantMutationInput {
  id: string;
}

// null
export interface AddCustomDomainMutationInput {
  id: string;
  domain: string;
}

// null
export interface UpdateCustomDomainMutationInput {
  id: string;
  domain?: string | null;
}

// null
export interface DeleteCustomDomainMutationInput {
  id: string;
}

// null
export interface UsageFilter {
  date_after?: string | null;
  date_before?: string | null;
  omit?: string[] | null;
}

// null
export interface ResetTenantAdminPasswordMutationInput {
  id: string;
  email: string;
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

//==============================================================
// END Enums and Input Objects
//==============================================================
