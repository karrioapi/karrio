

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
  meta: any | null;
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
  meta: any | null;
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
  meta: any | null;
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
  meta: any | null;
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

//==============================================================
// START Enums and Input Objects
//==============================================================

export enum MarkupTypeEnum {
  AMOUNT = "AMOUNT",
  PERCENTAGE = "PERCENTAGE",
}

export enum UserRole {
  admin = "admin",
  developer = "developer",
  member = "member",
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
  meta_key?: string | null;
  meta_value?: string | null;
  metadata_key?: string | null;
  metadata_value?: string | null;
}

// null
export interface UsageFilter {
  date_after?: string | null;
  date_before?: string | null;
  omit?: string[] | null;
  surcharge_id?: string | null;
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
  meta?: any | null;
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
  meta?: any | null;
  metadata?: any | null;
}

// null
export interface DeleteMutationInput {
  id: string;
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