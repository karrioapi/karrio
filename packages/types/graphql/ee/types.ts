

/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetOAuthApps
// ====================================================

export interface GetOAuthApps_oauth_apps_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetOAuthApps_oauth_apps_edges_node_created_by {
  email: string;
  full_name: string;
}

export interface GetOAuthApps_oauth_apps_edges_node {
  id: string;
  object_type: string;
  display_name: string;
  description: string | null;
  launch_url: string;
  redirect_uris: string;
  features: string[];
  client_id: string;
  created_at: any;
  updated_at: any;
  metadata: any | null;
  created_by: GetOAuthApps_oauth_apps_edges_node_created_by;
}

export interface GetOAuthApps_oauth_apps_edges {
  node: GetOAuthApps_oauth_apps_edges_node;
}

export interface GetOAuthApps_oauth_apps {
  page_info: GetOAuthApps_oauth_apps_page_info;
  edges: GetOAuthApps_oauth_apps_edges[];
}

export interface GetOAuthApps {
  oauth_apps: GetOAuthApps_oauth_apps;
}

export interface GetOAuthAppsVariables {
  filter?: OAuthAppFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetOAuthApp
// ====================================================

export interface GetOAuthApp_oauth_app_created_by {
  email: string;
  full_name: string;
}

export interface GetOAuthApp_oauth_app {
  id: string;
  object_type: string;
  display_name: string;
  description: string | null;
  launch_url: string;
  redirect_uris: string;
  features: string[];
  client_id: string;
  created_at: any;
  updated_at: any;
  metadata: any | null;
  created_by: GetOAuthApp_oauth_app_created_by;
}

export interface GetOAuthApp {
  oauth_app: GetOAuthApp_oauth_app;
}

export interface GetOAuthAppVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetAppInstallations
// ====================================================

export interface GetAppInstallations_app_installations_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetAppInstallations_app_installations_edges_node_created_by {
  email: string;
  full_name: string;
}

export interface GetAppInstallations_app_installations_edges_node_oauth_app {
  id: string;
  display_name: string;
  client_id: string;
  features: string[];
}

export interface GetAppInstallations_app_installations_edges_node_metafields {
  id: string;
  key: string;
  value: any | null;
  is_required: boolean;
  type: MetafieldTypeEnum;
}

export interface GetAppInstallations_app_installations_edges_node {
  id: string;
  object_type: string;
  app_id: string;
  app_type: string;
  access_scopes: string[];
  api_key: string | null;
  is_active: boolean;
  requires_oauth: boolean;
  created_at: any;
  updated_at: any;
  metadata: any | null;
  created_by: GetAppInstallations_app_installations_edges_node_created_by;
  oauth_app: GetAppInstallations_app_installations_edges_node_oauth_app | null;
  metafields: GetAppInstallations_app_installations_edges_node_metafields[];
}

export interface GetAppInstallations_app_installations_edges {
  node: GetAppInstallations_app_installations_edges_node;
}

export interface GetAppInstallations_app_installations {
  page_info: GetAppInstallations_app_installations_page_info;
  edges: GetAppInstallations_app_installations_edges[];
}

export interface GetAppInstallations {
  app_installations: GetAppInstallations_app_installations;
}

export interface GetAppInstallationsVariables {
  filter?: AppInstallationFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetAppInstallation
// ====================================================

export interface GetAppInstallation_app_installation_created_by {
  email: string;
  full_name: string;
}

export interface GetAppInstallation_app_installation_oauth_app {
  id: string;
  display_name: string;
  client_id: string;
  features: string[];
}

export interface GetAppInstallation_app_installation_metafields {
  id: string;
  key: string;
  value: any | null;
  is_required: boolean;
  type: MetafieldTypeEnum;
}

export interface GetAppInstallation_app_installation {
  id: string;
  object_type: string;
  app_id: string;
  app_type: string;
  access_scopes: string[];
  api_key: string | null;
  is_active: boolean;
  requires_oauth: boolean;
  created_at: any;
  updated_at: any;
  metadata: any | null;
  created_by: GetAppInstallation_app_installation_created_by;
  oauth_app: GetAppInstallation_app_installation_oauth_app | null;
  metafields: GetAppInstallation_app_installation_metafields[];
}

export interface GetAppInstallation {
  app_installation: GetAppInstallation_app_installation;
}

export interface GetAppInstallationVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetAppInstallationByAppId
// ====================================================

export interface GetAppInstallationByAppId_app_installation_by_app_id_oauth_app {
  id: string;
  display_name: string;
  client_id: string;
  features: string[];
}

export interface GetAppInstallationByAppId_app_installation_by_app_id_metafields {
  id: string;
  key: string;
  value: any | null;
  is_required: boolean;
  type: MetafieldTypeEnum;
}

export interface GetAppInstallationByAppId_app_installation_by_app_id {
  id: string;
  object_type: string;
  app_id: string;
  app_type: string;
  access_scopes: string[];
  api_key: string | null;
  is_active: boolean;
  requires_oauth: boolean;
  created_at: any;
  updated_at: any;
  metadata: any | null;
  oauth_app: GetAppInstallationByAppId_app_installation_by_app_id_oauth_app | null;
  metafields: GetAppInstallationByAppId_app_installation_by_app_id_metafields[];
}

export interface GetAppInstallationByAppId {
  app_installation_by_app_id: GetAppInstallationByAppId_app_installation_by_app_id;
}

export interface GetAppInstallationByAppIdVariables {
  app_id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateOAuthApp
// ====================================================

export interface CreateOAuthApp_create_oauth_app_oauth_app {
  id: string;
  object_type: string;
  display_name: string;
  description: string | null;
  launch_url: string;
  redirect_uris: string;
  features: string[];
  client_id: string;
  client_secret: string;
  created_at: any;
  updated_at: any;
  metadata: any | null;
}

export interface CreateOAuthApp_create_oauth_app_errors {
  field: string;
  messages: string[];
}

export interface CreateOAuthApp_create_oauth_app {
  oauth_app: CreateOAuthApp_create_oauth_app_oauth_app | null;
  errors: CreateOAuthApp_create_oauth_app_errors[] | null;
}

export interface CreateOAuthApp {
  create_oauth_app: CreateOAuthApp_create_oauth_app;
}

export interface CreateOAuthAppVariables {
  data: CreateOAuthAppMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateOAuthApp
// ====================================================

export interface UpdateOAuthApp_update_oauth_app_oauth_app {
  id: string;
  object_type: string;
  display_name: string;
  description: string | null;
  launch_url: string;
  redirect_uris: string;
  features: string[];
  client_id: string;
  created_at: any;
  updated_at: any;
  metadata: any | null;
}

export interface UpdateOAuthApp_update_oauth_app_errors {
  field: string;
  messages: string[];
}

export interface UpdateOAuthApp_update_oauth_app {
  oauth_app: UpdateOAuthApp_update_oauth_app_oauth_app | null;
  errors: UpdateOAuthApp_update_oauth_app_errors[] | null;
}

export interface UpdateOAuthApp {
  update_oauth_app: UpdateOAuthApp_update_oauth_app;
}

export interface UpdateOAuthAppVariables {
  data: UpdateOAuthAppMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteOAuthApp
// ====================================================

export interface DeleteOAuthApp_delete_oauth_app_errors {
  field: string;
  messages: string[];
}

export interface DeleteOAuthApp_delete_oauth_app {
  success: boolean;
  errors: DeleteOAuthApp_delete_oauth_app_errors[] | null;
}

export interface DeleteOAuthApp {
  delete_oauth_app: DeleteOAuthApp_delete_oauth_app;
}

export interface DeleteOAuthAppVariables {
  data: DeleteOAuthAppMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: InstallApp
// ====================================================

export interface InstallApp_install_app_installation_oauth_app {
  id: string;
  display_name: string;
  client_id: string;
  features: string[];
}

export interface InstallApp_install_app_installation_metafields {
  id: string;
  key: string;
  value: any | null;
  is_required: boolean;
  type: MetafieldTypeEnum;
}

export interface InstallApp_install_app_installation {
  id: string;
  object_type: string;
  app_id: string;
  app_type: string;
  access_scopes: string[];
  api_key: string | null;
  is_active: boolean;
  requires_oauth: boolean;
  created_at: any;
  updated_at: any;
  metadata: any | null;
  oauth_app: InstallApp_install_app_installation_oauth_app | null;
  metafields: InstallApp_install_app_installation_metafields[];
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

export interface UninstallApp_uninstall_app_errors {
  field: string;
  messages: string[];
}

export interface UninstallApp_uninstall_app {
  success: boolean;
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
// GraphQL mutation operation: UpdateAppInstallation
// ====================================================

export interface UpdateAppInstallation_update_app_installation_installation_oauth_app {
  id: string;
  display_name: string;
  client_id: string;
  features: string[];
}

export interface UpdateAppInstallation_update_app_installation_installation_metafields {
  id: string;
  key: string;
  value: any | null;
  is_required: boolean;
  type: MetafieldTypeEnum;
}

export interface UpdateAppInstallation_update_app_installation_installation {
  id: string;
  object_type: string;
  app_id: string;
  app_type: string;
  access_scopes: string[];
  api_key: string | null;
  is_active: boolean;
  requires_oauth: boolean;
  created_at: any;
  updated_at: any;
  metadata: any | null;
  oauth_app: UpdateAppInstallation_update_app_installation_installation_oauth_app | null;
  metafields: UpdateAppInstallation_update_app_installation_installation_metafields[];
}

export interface UpdateAppInstallation_update_app_installation_errors {
  field: string;
  messages: string[];
}

export interface UpdateAppInstallation_update_app_installation {
  installation: UpdateAppInstallation_update_app_installation_installation | null;
  errors: UpdateAppInstallation_update_app_installation_errors[] | null;
}

export interface UpdateAppInstallation {
  update_app_installation: UpdateAppInstallation_update_app_installation;
}

export interface UpdateAppInstallationVariables {
  data: UpdateAppInstallationMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: RotateAppApiKey
// ====================================================

export interface RotateAppApiKey_rotate_app_api_key_installation {
  id: string;
  app_id: string;
  api_key: string | null;
}

export interface RotateAppApiKey_rotate_app_api_key_errors {
  field: string;
  messages: string[];
}

export interface RotateAppApiKey_rotate_app_api_key {
  installation: RotateAppApiKey_rotate_app_api_key_installation | null;
  errors: RotateAppApiKey_rotate_app_api_key_errors[] | null;
}

export interface RotateAppApiKey {
  rotate_app_api_key: RotateAppApiKey_rotate_app_api_key;
}

export interface RotateAppApiKeyVariables {
  data: RotateAppApiKeyMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: EnsureAppApiKey
// ====================================================

export interface EnsureAppApiKey_ensure_app_api_key_installation {
  id: string;
  app_id: string;
  api_key: string | null;
}

export interface EnsureAppApiKey_ensure_app_api_key_errors {
  field: string;
  messages: string[];
}

export interface EnsureAppApiKey_ensure_app_api_key {
  installation: EnsureAppApiKey_ensure_app_api_key_installation | null;
  errors: EnsureAppApiKey_ensure_app_api_key_errors[] | null;
}

export interface EnsureAppApiKey {
  ensure_app_api_key: EnsureAppApiKey_ensure_app_api_key;
}

export interface EnsureAppApiKeyVariables {
  data: EnsureAppApiKeyMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_organization
// ====================================================

export interface get_organization_organization_current_user {
  email: string;
  full_name: string | null;
  is_admin: boolean;
  is_owner: boolean | null;
  last_login: any | null;
}

export interface get_organization_organization_members_invitation {
  id: string;
  guid: string;
  invitee_identifier: string;
  created: any;
  modified: any;
}

export interface get_organization_organization_members {
  email: string;
  full_name: string | null;
  is_admin: boolean;
  is_owner: boolean | null;
  user_id: string | null;
  invitation: get_organization_organization_members_invitation | null;
  last_login: any | null;
}

export interface get_organization_organization_usage_api_errors {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface get_organization_organization_usage_api_requests {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organization_organization_usage_order_volumes {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organization_organization_usage_shipment_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organization_organization_usage_tracker_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organization_organization_usage_shipping_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organization_organization_usage {
  members: number | null;
  order_volume: number | null;
  total_errors: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  unfulfilled_orders: number | null;
  total_shipping_spend: number | null;
  api_errors: get_organization_organization_usage_api_errors[] | null;
  api_requests: get_organization_organization_usage_api_requests[] | null;
  order_volumes: get_organization_organization_usage_order_volumes[] | null;
  shipment_count: get_organization_organization_usage_shipment_count[] | null;
  tracker_count: get_organization_organization_usage_tracker_count[] | null;
  shipping_spend: get_organization_organization_usage_shipping_spend[] | null;
}

export interface get_organization_organization {
  id: string;
  name: string;
  slug: string;
  token: string;
  current_user: get_organization_organization_current_user;
  members: get_organization_organization_members[];
  usage: get_organization_organization_usage;
}

export interface get_organization {
  organization: get_organization_organization | null;
}

export interface get_organizationVariables {
  id: string;
  usage?: UsageFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_organizations
// ====================================================

export interface get_organizations_organizations_current_user {
  email: string;
  full_name: string | null;
  is_admin: boolean;
  is_owner: boolean | null;
  last_login: any | null;
}

export interface get_organizations_organizations_members_invitation {
  id: string;
  guid: string;
  invitee_identifier: string;
  created: any;
  modified: any;
}

export interface get_organizations_organizations_members {
  email: string;
  full_name: string | null;
  is_admin: boolean;
  is_owner: boolean | null;
  user_id: string | null;
  invitation: get_organizations_organizations_members_invitation | null;
  last_login: any | null;
}

export interface get_organizations_organizations_usage_api_errors {
  label: string | null;
  count: number | null;
  date: string | null;
}

export interface get_organizations_organizations_usage_api_requests {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organizations_organizations_usage_order_volumes {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organizations_organizations_usage_shipment_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organizations_organizations_usage_tracker_count {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organizations_organizations_usage_shipping_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organizations_organizations_usage {
  members: number | null;
  order_volume: number | null;
  total_errors: number | null;
  total_requests: number | null;
  total_trackers: number | null;
  total_shipments: number | null;
  unfulfilled_orders: number | null;
  total_shipping_spend: number | null;
  api_errors: get_organizations_organizations_usage_api_errors[] | null;
  api_requests: get_organizations_organizations_usage_api_requests[] | null;
  order_volumes: get_organizations_organizations_usage_order_volumes[] | null;
  shipment_count: get_organizations_organizations_usage_shipment_count[] | null;
  tracker_count: get_organizations_organizations_usage_tracker_count[] | null;
  shipping_spend: get_organizations_organizations_usage_shipping_spend[] | null;
}

export interface get_organizations_organizations {
  id: string;
  name: string;
  slug: string;
  token: string;
  current_user: get_organizations_organizations_current_user;
  members: get_organizations_organizations_members[];
  usage: get_organizations_organizations_usage;
}

export interface get_organizations {
  organizations: get_organizations_organizations[];
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: delete_organization
// ====================================================

export interface delete_organization_delete_organization_organization {
  id: string;
}

export interface delete_organization_delete_organization_errors {
  field: string;
  messages: string[];
}

export interface delete_organization_delete_organization {
  organization: delete_organization_delete_organization_organization | null;
  errors: delete_organization_delete_organization_errors[] | null;
}

export interface delete_organization {
  delete_organization: delete_organization_delete_organization;
}

export interface delete_organizationVariables {
  data: DeleteOrganizationMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: create_organization
// ====================================================

export interface create_organization_create_organization_organization {
  id: string;
}

export interface create_organization_create_organization_errors {
  field: string;
  messages: string[];
}

export interface create_organization_create_organization {
  organization: create_organization_create_organization_organization | null;
  errors: create_organization_create_organization_errors[] | null;
}

export interface create_organization {
  create_organization: create_organization_create_organization;
}

export interface create_organizationVariables {
  data: CreateOrganizationMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_organization
// ====================================================

export interface update_organization_update_organization_organization {
  id: string;
}

export interface update_organization_update_organization_errors {
  field: string;
  messages: string[];
}

export interface update_organization_update_organization {
  organization: update_organization_update_organization_organization | null;
  errors: update_organization_update_organization_errors[] | null;
}

export interface update_organization {
  update_organization: update_organization_update_organization;
}

export interface update_organizationVariables {
  data: UpdateOrganizationMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: change_organization_owner
// ====================================================

export interface change_organization_owner_change_organization_owner_organization {
  id: string;
}

export interface change_organization_owner_change_organization_owner_errors {
  field: string;
  messages: string[];
}

export interface change_organization_owner_change_organization_owner {
  organization: change_organization_owner_change_organization_owner_organization | null;
  errors: change_organization_owner_change_organization_owner_errors[] | null;
}

export interface change_organization_owner {
  change_organization_owner: change_organization_owner_change_organization_owner;
}

export interface change_organization_ownerVariables {
  data: ChangeOrganizationOwnerMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: set_organization_user_roles
// ====================================================

export interface set_organization_user_roles_set_organization_user_roles_organization {
  id: string;
}

export interface set_organization_user_roles_set_organization_user_roles_errors {
  field: string;
  messages: string[];
}

export interface set_organization_user_roles_set_organization_user_roles {
  organization: set_organization_user_roles_set_organization_user_roles_organization | null;
  errors: set_organization_user_roles_set_organization_user_roles_errors[] | null;
}

export interface set_organization_user_roles {
  set_organization_user_roles: set_organization_user_roles_set_organization_user_roles;
}

export interface set_organization_user_rolesVariables {
  data: SetOrganizationUserRolesMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: send_organization_invites
// ====================================================

export interface send_organization_invites_send_organization_invites_errors {
  field: string;
  messages: string[];
}

export interface send_organization_invites_send_organization_invites {
  errors: send_organization_invites_send_organization_invites_errors[] | null;
}

export interface send_organization_invites {
  send_organization_invites: send_organization_invites_send_organization_invites;
}

export interface send_organization_invitesVariables {
  data: SendOrganizationInvitesMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: get_organization_invitation
// ====================================================

export interface get_organization_invitation_organization_invitation_invitee {
  email: string;
}

export interface get_organization_invitation_organization_invitation {
  invitee_identifier: string;
  organization_name: string;
  invitee: get_organization_invitation_organization_invitation_invitee | null;
}

export interface get_organization_invitation {
  organization_invitation: get_organization_invitation_organization_invitation | null;
}

export interface get_organization_invitationVariables {
  guid: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: accept_organization_invitation
// ====================================================

export interface accept_organization_invitation_accept_organization_invitation_organization {
  id: string;
}

export interface accept_organization_invitation_accept_organization_invitation_errors {
  field: string;
  messages: string[];
}

export interface accept_organization_invitation_accept_organization_invitation {
  organization: accept_organization_invitation_accept_organization_invitation_organization | null;
  errors: accept_organization_invitation_accept_organization_invitation_errors[] | null;
}

export interface accept_organization_invitation {
  accept_organization_invitation: accept_organization_invitation_accept_organization_invitation;
}

export interface accept_organization_invitationVariables {
  data: AcceptOrganizationInvitationMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: delete_organization_invitation
// ====================================================

export interface delete_organization_invitation_delete_organization_invitation {
  id: string;
}

export interface delete_organization_invitation {
  delete_organization_invitation: delete_organization_invitation_delete_organization_invitation;
}

export interface delete_organization_invitationVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: remove_organization_member
// ====================================================

export interface remove_organization_member_remove_organization_member_organization_members_invitation {
  id: string;
  guid: string;
  invitee_identifier: string;
  created: any;
  modified: any;
}

export interface remove_organization_member_remove_organization_member_organization_members {
  email: string;
  full_name: string | null;
  is_admin: boolean;
  is_owner: boolean | null;
  user_id: string | null;
  invitation: remove_organization_member_remove_organization_member_organization_members_invitation | null;
  last_login: any | null;
}

export interface remove_organization_member_remove_organization_member_organization {
  id: string;
  members: remove_organization_member_remove_organization_member_organization_members[];
}

export interface remove_organization_member_remove_organization_member_errors {
  field: string;
  messages: string[];
}

export interface remove_organization_member_remove_organization_member {
  organization: remove_organization_member_remove_organization_member_organization | null;
  errors: remove_organization_member_remove_organization_member_errors[] | null;
}

export interface remove_organization_member {
  remove_organization_member: remove_organization_member_remove_organization_member;
}

export interface remove_organization_memberVariables {
  data: RemoveOrganizationMemberMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: update_member_status
// ====================================================

export interface update_member_status_update_member_status_organization_members_invitation {
  id: string;
  guid: string;
  invitee_identifier: string;
  created: any;
  modified: any;
}

export interface update_member_status_update_member_status_organization_members {
  email: string;
  full_name: string | null;
  is_admin: boolean;
  is_owner: boolean | null;
  user_id: string | null;
  invitation: update_member_status_update_member_status_organization_members_invitation | null;
  last_login: any | null;
}

export interface update_member_status_update_member_status_organization {
  id: string;
  members: update_member_status_update_member_status_organization_members[];
}

export interface update_member_status_update_member_status_errors {
  field: string;
  messages: string[];
}

export interface update_member_status_update_member_status {
  organization: update_member_status_update_member_status_organization | null;
  errors: update_member_status_update_member_status_errors[] | null;
}

export interface update_member_status {
  update_member_status: update_member_status_update_member_status;
}

export interface update_member_statusVariables {
  data: UpdateMemberStatusMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: resend_organization_invite
// ====================================================

export interface resend_organization_invite_resend_organization_invite_invitation {
  id: string;
  invitee_identifier: string;
  created: any;
  modified: any;
}

export interface resend_organization_invite_resend_organization_invite_errors {
  field: string;
  messages: string[];
}

export interface resend_organization_invite_resend_organization_invite {
  invitation: resend_organization_invite_resend_organization_invite_invitation | null;
  errors: resend_organization_invite_resend_organization_invite_errors[] | null;
}

export interface resend_organization_invite {
  resend_organization_invite: resend_organization_invite_resend_organization_invite;
}

export interface resend_organization_inviteVariables {
  data: ResendOrganizationInviteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflow
// ====================================================

export interface GetWorkflow_workflow_trigger {
  id: string;
  trigger_type: AutomationTriggerType;
  schedule: string | null;
  secret: string | null;
  secret_key: string | null;
}

export interface GetWorkflow_workflow_action_nodes {
  order: number;
  slug: string;
}

export interface GetWorkflow_workflow_actions_connection_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflow_workflow_actions_connection {
  id: string;
  name: string;
  auth_type: AutomationAuthType;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  description: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  credentials: any | null;
  credentials_from_metafields: any | null;
  required_credentials: string[];
  is_credentials_complete: boolean;
  credential_validation: any;
  template_slug: string | null;
  metadata: any | null;
  metafields: GetWorkflow_workflow_actions_connection_metafields[];
}

export interface GetWorkflow_workflow_actions_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflow_workflow_actions {
  id: string;
  slug: string;
  name: string;
  action_type: AutomationActionType;
  description: string | null;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  method: AutomationHTTPMethod | null;
  content_type: AutomationHTTPContentType | null;
  header_template: string | null;
  parameters_type: AutomationParametersType | null;
  parameters_template: string | null;
  connection: GetWorkflow_workflow_actions_connection | null;
  template_slug: string | null;
  metadata: any | null;
  metafields: GetWorkflow_workflow_actions_metafields[];
}

export interface GetWorkflow_workflow {
  id: string;
  name: string;
  description: string | null;
  trigger: GetWorkflow_workflow_trigger | null;
  action_nodes: GetWorkflow_workflow_action_nodes[];
  actions: GetWorkflow_workflow_actions[];
  metadata: any | null;
  template_slug: string | null;
}

export interface GetWorkflow {
  workflow: GetWorkflow_workflow | null;
}

export interface GetWorkflowVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflows
// ====================================================

export interface GetWorkflows_workflows_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetWorkflows_workflows_edges_node_trigger {
  object_type: string;
  id: string;
  slug: string;
  trigger_type: AutomationTriggerType;
  schedule: string | null;
  secret: string | null;
  secret_key: string | null;
  is_due: boolean;
  next_run_description: string | null;
  created_at: any;
  updated_at: any;
}

export interface GetWorkflows_workflows_edges_node_action_nodes {
  order: number;
  slug: string;
}

export interface GetWorkflows_workflows_edges_node_actions_connection_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflows_workflows_edges_node_actions_connection {
  object_type: string;
  id: string;
  name: string;
  slug: string;
  auth_type: AutomationAuthType;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  description: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  credentials: any | null;
  credentials_from_metafields: any | null;
  required_credentials: string[];
  is_credentials_complete: boolean;
  credential_validation: any;
  metadata: any | null;
  template_slug: string | null;
  metafields: GetWorkflows_workflows_edges_node_actions_connection_metafields[];
  created_at: any;
  updated_at: any;
}

export interface GetWorkflows_workflows_edges_node_actions_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflows_workflows_edges_node_actions {
  object_type: string;
  id: string;
  slug: string;
  name: string;
  action_type: AutomationActionType;
  description: string | null;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  method: AutomationHTTPMethod | null;
  content_type: AutomationHTTPContentType | null;
  header_template: string | null;
  parameters_type: AutomationParametersType | null;
  parameters_template: string | null;
  connection: GetWorkflows_workflows_edges_node_actions_connection | null;
  template_slug: string | null;
  metadata: any | null;
  metafields: GetWorkflows_workflows_edges_node_actions_metafields[];
  created_at: any;
  updated_at: any;
}

export interface GetWorkflows_workflows_edges_node {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  trigger: GetWorkflows_workflows_edges_node_trigger | null;
  action_nodes: GetWorkflows_workflows_edges_node_action_nodes[];
  actions: GetWorkflows_workflows_edges_node_actions[];
  metadata: any | null;
  template_slug: string | null;
  created_at: any;
  updated_at: any;
}

export interface GetWorkflows_workflows_edges {
  node: GetWorkflows_workflows_edges_node;
}

export interface GetWorkflows_workflows {
  page_info: GetWorkflows_workflows_page_info;
  edges: GetWorkflows_workflows_edges[];
}

export interface GetWorkflows {
  workflows: GetWorkflows_workflows;
}

export interface GetWorkflowsVariables {
  filter?: WorkflowFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetScheduledWorkflows
// ====================================================

export interface GetScheduledWorkflows_scheduled_workflows_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetScheduledWorkflows_scheduled_workflows_edges_node_trigger {
  object_type: string;
  id: string;
  slug: string;
  trigger_type: AutomationTriggerType;
  schedule: string | null;
  is_due: boolean;
  next_run_description: string | null;
  created_at: any;
  updated_at: any;
}

export interface GetScheduledWorkflows_scheduled_workflows_edges_node_action_nodes {
  order: number;
  slug: string;
}

export interface GetScheduledWorkflows_scheduled_workflows_edges_node_actions_connection_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetScheduledWorkflows_scheduled_workflows_edges_node_actions_connection {
  object_type: string;
  id: string;
  name: string;
  slug: string;
  auth_type: AutomationAuthType;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  description: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  credentials: any | null;
  credentials_from_metafields: any | null;
  required_credentials: string[];
  is_credentials_complete: boolean;
  credential_validation: any;
  metadata: any | null;
  template_slug: string | null;
  metafields: GetScheduledWorkflows_scheduled_workflows_edges_node_actions_connection_metafields[];
  created_at: any;
  updated_at: any;
}

export interface GetScheduledWorkflows_scheduled_workflows_edges_node_actions_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetScheduledWorkflows_scheduled_workflows_edges_node_actions {
  object_type: string;
  id: string;
  slug: string;
  name: string;
  action_type: AutomationActionType;
  description: string | null;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  method: AutomationHTTPMethod | null;
  content_type: AutomationHTTPContentType | null;
  header_template: string | null;
  parameters_type: AutomationParametersType | null;
  parameters_template: string | null;
  connection: GetScheduledWorkflows_scheduled_workflows_edges_node_actions_connection | null;
  template_slug: string | null;
  metadata: any | null;
  metafields: GetScheduledWorkflows_scheduled_workflows_edges_node_actions_metafields[];
  created_at: any;
  updated_at: any;
}

export interface GetScheduledWorkflows_scheduled_workflows_edges_node {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  trigger: GetScheduledWorkflows_scheduled_workflows_edges_node_trigger | null;
  action_nodes: GetScheduledWorkflows_scheduled_workflows_edges_node_action_nodes[];
  actions: GetScheduledWorkflows_scheduled_workflows_edges_node_actions[];
  metadata: any | null;
  template_slug: string | null;
  created_at: any;
  updated_at: any;
}

export interface GetScheduledWorkflows_scheduled_workflows_edges {
  node: GetScheduledWorkflows_scheduled_workflows_edges_node;
}

export interface GetScheduledWorkflows_scheduled_workflows {
  page_info: GetScheduledWorkflows_scheduled_workflows_page_info;
  edges: GetScheduledWorkflows_scheduled_workflows_edges[];
}

export interface GetScheduledWorkflows {
  scheduled_workflows: GetScheduledWorkflows_scheduled_workflows;
}

export interface GetScheduledWorkflowsVariables {
  filter?: WorkflowFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflowConnection
// ====================================================

export interface GetWorkflowConnection_workflow_connection_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowConnection_workflow_connection {
  id: string;
  name: string;
  slug: string;
  auth_type: AutomationAuthType;
  description: string | null;
  host: string | null;
  port: number | null;
  endpoint: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  credentials: any | null;
  credentials_from_metafields: any | null;
  required_credentials: string[];
  is_credentials_complete: boolean;
  credential_validation: any;
  template_slug: string | null;
  metadata: any | null;
  metafields: GetWorkflowConnection_workflow_connection_metafields[];
}

export interface GetWorkflowConnection {
  workflow_connection: GetWorkflowConnection_workflow_connection | null;
}

export interface GetWorkflowConnectionVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflowConnections
// ====================================================

export interface GetWorkflowConnections_workflow_connections_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetWorkflowConnections_workflow_connections_edges_node_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowConnections_workflow_connections_edges_node {
  id: string;
  name: string;
  slug: string;
  auth_type: AutomationAuthType;
  description: string | null;
  host: string | null;
  port: number | null;
  endpoint: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  credentials: any | null;
  credentials_from_metafields: any | null;
  required_credentials: string[];
  is_credentials_complete: boolean;
  credential_validation: any;
  metadata: any | null;
  template_slug: string | null;
  metafields: GetWorkflowConnections_workflow_connections_edges_node_metafields[];
  created_at: any;
  updated_at: any;
}

export interface GetWorkflowConnections_workflow_connections_edges {
  node: GetWorkflowConnections_workflow_connections_edges_node;
}

export interface GetWorkflowConnections_workflow_connections {
  page_info: GetWorkflowConnections_workflow_connections_page_info;
  edges: GetWorkflowConnections_workflow_connections_edges[];
}

export interface GetWorkflowConnections {
  workflow_connections: GetWorkflowConnections_workflow_connections;
}

export interface GetWorkflowConnectionsVariables {
  filter?: WorkflowConnectionFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflowAction
// ====================================================

export interface GetWorkflowAction_workflow_action_connection_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowAction_workflow_action_connection {
  id: string;
  name: string;
  auth_type: AutomationAuthType;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  description: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  credentials: any | null;
  credentials_from_metafields: any | null;
  required_credentials: string[];
  is_credentials_complete: boolean;
  credential_validation: any;
  metadata: any | null;
  template_slug: string | null;
  metafields: GetWorkflowAction_workflow_action_connection_metafields[];
}

export interface GetWorkflowAction_workflow_action_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowAction_workflow_action {
  id: string;
  slug: string;
  name: string;
  action_type: AutomationActionType;
  description: string | null;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  method: AutomationHTTPMethod | null;
  content_type: AutomationHTTPContentType | null;
  header_template: string | null;
  parameters_type: AutomationParametersType | null;
  parameters_template: string | null;
  connection: GetWorkflowAction_workflow_action_connection | null;
  metadata: any | null;
  template_slug: string | null;
  metafields: GetWorkflowAction_workflow_action_metafields[];
}

export interface GetWorkflowAction {
  workflow_action: GetWorkflowAction_workflow_action | null;
}

export interface GetWorkflowActionVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflowActions
// ====================================================

export interface GetWorkflowActions_workflow_actions_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetWorkflowActions_workflow_actions_edges_node_connection_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowActions_workflow_actions_edges_node_connection {
  object_type: string;
  id: string;
  name: string;
  slug: string;
  auth_type: AutomationAuthType;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  description: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  credentials: any | null;
  credentials_from_metafields: any | null;
  required_credentials: string[];
  is_credentials_complete: boolean;
  credential_validation: any;
  template_slug: string | null;
  metadata: any | null;
  metafields: GetWorkflowActions_workflow_actions_edges_node_connection_metafields[];
  created_at: any;
  updated_at: any;
}

export interface GetWorkflowActions_workflow_actions_edges_node_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowActions_workflow_actions_edges_node {
  object_type: string;
  id: string;
  slug: string;
  name: string;
  action_type: AutomationActionType;
  description: string | null;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  method: AutomationHTTPMethod | null;
  content_type: AutomationHTTPContentType | null;
  header_template: string | null;
  parameters_type: AutomationParametersType | null;
  parameters_template: string | null;
  connection: GetWorkflowActions_workflow_actions_edges_node_connection | null;
  metadata: any | null;
  metafields: GetWorkflowActions_workflow_actions_edges_node_metafields[];
  template_slug: string | null;
  created_at: any;
  updated_at: any;
}

export interface GetWorkflowActions_workflow_actions_edges {
  node: GetWorkflowActions_workflow_actions_edges_node;
}

export interface GetWorkflowActions_workflow_actions {
  page_info: GetWorkflowActions_workflow_actions_page_info;
  edges: GetWorkflowActions_workflow_actions_edges[];
}

export interface GetWorkflowActions {
  workflow_actions: GetWorkflowActions_workflow_actions;
}

export interface GetWorkflowActionsVariables {
  filter?: WorkflowActionFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflowEvent
// ====================================================

export interface GetWorkflowEvent_workflow_event_workflow_action_nodes {
  order: number;
  slug: string;
}

export interface GetWorkflowEvent_workflow_event_workflow {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  action_nodes: GetWorkflowEvent_workflow_event_workflow_action_nodes[];
}

export interface GetWorkflowEvent_workflow_event_records {
  object_type: string;
  id: string | null;
  key: string | null;
  timestamp: number | null;
  test_mode: boolean | null;
  record: any | null;
  meta: any | null;
  created_at: any | null;
  updated_at: any | null;
}

export interface GetWorkflowEvent_workflow_event {
  object_type: string;
  id: string;
  status: AutomationEventStatus;
  event_type: AutomationEventType;
  parameters: any | null;
  test_mode: boolean;
  workflow: GetWorkflowEvent_workflow_event_workflow;
  records: GetWorkflowEvent_workflow_event_records[];
  created_at: any;
  updated_at: any;
}

export interface GetWorkflowEvent {
  workflow_event: GetWorkflowEvent_workflow_event | null;
}

export interface GetWorkflowEventVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflowEvents
// ====================================================

export interface GetWorkflowEvents_workflow_events_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetWorkflowEvents_workflow_events_edges_node_workflow_action_nodes {
  order: number;
  slug: string;
}

export interface GetWorkflowEvents_workflow_events_edges_node_workflow {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  action_nodes: GetWorkflowEvents_workflow_events_edges_node_workflow_action_nodes[];
}

export interface GetWorkflowEvents_workflow_events_edges_node_records {
  object_type: string;
  id: string | null;
  key: string | null;
  timestamp: number | null;
  test_mode: boolean | null;
  record: any | null;
  meta: any | null;
  created_at: any | null;
  updated_at: any | null;
}

export interface GetWorkflowEvents_workflow_events_edges_node {
  object_type: string;
  id: string;
  status: AutomationEventStatus;
  event_type: AutomationEventType;
  parameters: any | null;
  test_mode: boolean;
  workflow: GetWorkflowEvents_workflow_events_edges_node_workflow;
  records: GetWorkflowEvents_workflow_events_edges_node_records[];
  created_at: any;
  updated_at: any;
}

export interface GetWorkflowEvents_workflow_events_edges {
  node: GetWorkflowEvents_workflow_events_edges_node;
}

export interface GetWorkflowEvents_workflow_events {
  page_info: GetWorkflowEvents_workflow_events_page_info;
  edges: GetWorkflowEvents_workflow_events_edges[];
}

export interface GetWorkflowEvents {
  workflow_events: GetWorkflowEvents_workflow_events;
}

export interface GetWorkflowEventsVariables {
  filter?: WorkflowEventFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflowTemplates
// ====================================================

export interface GetWorkflowTemplates_workflow_templates_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetWorkflowTemplates_workflow_templates_edges_node_trigger {
  slug: string;
  trigger_type: AutomationTriggerType;
  schedule: string | null;
}

export interface GetWorkflowTemplates_workflow_templates_edges_node_action_nodes {
  order: number;
  slug: string;
}

export interface GetWorkflowTemplates_workflow_templates_edges_node_actions_connection_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowTemplates_workflow_templates_edges_node_actions_connection {
  name: string;
  slug: string;
  auth_type: AutomationAuthType;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  description: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  template_slug: string | null;
  metafields: GetWorkflowTemplates_workflow_templates_edges_node_actions_connection_metafields[];
}

export interface GetWorkflowTemplates_workflow_templates_edges_node_actions_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowTemplates_workflow_templates_edges_node_actions {
  slug: string;
  name: string;
  action_type: AutomationActionType;
  description: string | null;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  method: AutomationHTTPMethod | null;
  content_type: AutomationHTTPContentType | null;
  header_template: string | null;
  parameters_type: AutomationParametersType | null;
  parameters_template: string | null;
  connection: GetWorkflowTemplates_workflow_templates_edges_node_actions_connection | null;
  template_slug: string | null;
  metafields: GetWorkflowTemplates_workflow_templates_edges_node_actions_metafields[];
}

export interface GetWorkflowTemplates_workflow_templates_edges_node {
  name: string;
  slug: string;
  description: string | null;
  trigger: GetWorkflowTemplates_workflow_templates_edges_node_trigger | null;
  action_nodes: GetWorkflowTemplates_workflow_templates_edges_node_action_nodes[];
  actions: GetWorkflowTemplates_workflow_templates_edges_node_actions[];
}

export interface GetWorkflowTemplates_workflow_templates_edges {
  node: GetWorkflowTemplates_workflow_templates_edges_node;
}

export interface GetWorkflowTemplates_workflow_templates {
  page_info: GetWorkflowTemplates_workflow_templates_page_info;
  edges: GetWorkflowTemplates_workflow_templates_edges[];
}

export interface GetWorkflowTemplates {
  workflow_templates: GetWorkflowTemplates_workflow_templates;
}

export interface GetWorkflowTemplatesVariables {
  filter?: WorkflowFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflowActionTemplates
// ====================================================

export interface GetWorkflowActionTemplates_workflow_action_templates_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetWorkflowActionTemplates_workflow_action_templates_edges_node_connection_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowActionTemplates_workflow_action_templates_edges_node_connection {
  name: string;
  slug: string;
  auth_type: AutomationAuthType;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  description: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  template_slug: string | null;
  metafields: GetWorkflowActionTemplates_workflow_action_templates_edges_node_connection_metafields[];
}

export interface GetWorkflowActionTemplates_workflow_action_templates_edges_node_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowActionTemplates_workflow_action_templates_edges_node {
  slug: string;
  name: string;
  action_type: AutomationActionType;
  description: string | null;
  port: number | null;
  host: string | null;
  endpoint: string | null;
  method: AutomationHTTPMethod | null;
  content_type: AutomationHTTPContentType | null;
  header_template: string | null;
  parameters_type: AutomationParametersType | null;
  parameters_template: string | null;
  connection: GetWorkflowActionTemplates_workflow_action_templates_edges_node_connection | null;
  template_slug: string | null;
  metafields: GetWorkflowActionTemplates_workflow_action_templates_edges_node_metafields[];
}

export interface GetWorkflowActionTemplates_workflow_action_templates_edges {
  node: GetWorkflowActionTemplates_workflow_action_templates_edges_node;
}

export interface GetWorkflowActionTemplates_workflow_action_templates {
  page_info: GetWorkflowActionTemplates_workflow_action_templates_page_info;
  edges: GetWorkflowActionTemplates_workflow_action_templates_edges[];
}

export interface GetWorkflowActionTemplates {
  workflow_action_templates: GetWorkflowActionTemplates_workflow_action_templates;
}

export interface GetWorkflowActionTemplatesVariables {
  filter?: WorkflowActionFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkflowConnectionTemplates
// ====================================================

export interface GetWorkflowConnectionTemplates_workflow_connection_templates_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetWorkflowConnectionTemplates_workflow_connection_templates_edges_node_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: any | null;
}

export interface GetWorkflowConnectionTemplates_workflow_connection_templates_edges_node {
  name: string;
  slug: string;
  auth_type: AutomationAuthType;
  description: string | null;
  host: string | null;
  port: number | null;
  endpoint: string | null;
  parameters_template: string | null;
  auth_template: string | null;
  template_slug: string | null;
  metafields: GetWorkflowConnectionTemplates_workflow_connection_templates_edges_node_metafields[];
}

export interface GetWorkflowConnectionTemplates_workflow_connection_templates_edges {
  node: GetWorkflowConnectionTemplates_workflow_connection_templates_edges_node;
}

export interface GetWorkflowConnectionTemplates_workflow_connection_templates {
  page_info: GetWorkflowConnectionTemplates_workflow_connection_templates_page_info;
  edges: GetWorkflowConnectionTemplates_workflow_connection_templates_edges[];
}

export interface GetWorkflowConnectionTemplates {
  workflow_connection_templates: GetWorkflowConnectionTemplates_workflow_connection_templates;
}

export interface GetWorkflowConnectionTemplatesVariables {
  filter?: WorkflowConnectionFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateWorkflow
// ====================================================

export interface CreateWorkflow_create_workflow_workflow {
  id: string;
}

export interface CreateWorkflow_create_workflow_errors {
  field: string;
  messages: string[];
}

export interface CreateWorkflow_create_workflow {
  workflow: CreateWorkflow_create_workflow_workflow | null;
  errors: CreateWorkflow_create_workflow_errors[] | null;
}

export interface CreateWorkflow {
  create_workflow: CreateWorkflow_create_workflow;
}

export interface CreateWorkflowVariables {
  data: CreateWorkflowMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateWorkflow
// ====================================================

export interface UpdateWorkflow_update_workflow_workflow {
  id: string;
}

export interface UpdateWorkflow_update_workflow_errors {
  field: string;
  messages: string[];
}

export interface UpdateWorkflow_update_workflow {
  workflow: UpdateWorkflow_update_workflow_workflow | null;
  errors: UpdateWorkflow_update_workflow_errors[] | null;
}

export interface UpdateWorkflow {
  update_workflow: UpdateWorkflow_update_workflow;
}

export interface UpdateWorkflowVariables {
  data: UpdateWorkflowMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteWorkflow
// ====================================================

export interface DeleteWorkflow_delete_workflow_errors {
  field: string;
  messages: string[];
}

export interface DeleteWorkflow_delete_workflow {
  id: string;
  errors: DeleteWorkflow_delete_workflow_errors[] | null;
}

export interface DeleteWorkflow {
  delete_workflow: DeleteWorkflow_delete_workflow;
}

export interface DeleteWorkflowVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateWorkflowConnection
// ====================================================

export interface CreateWorkflowConnection_create_workflow_connection_workflow_connection {
  id: string;
}

export interface CreateWorkflowConnection_create_workflow_connection_errors {
  field: string;
  messages: string[];
}

export interface CreateWorkflowConnection_create_workflow_connection {
  workflow_connection: CreateWorkflowConnection_create_workflow_connection_workflow_connection | null;
  errors: CreateWorkflowConnection_create_workflow_connection_errors[] | null;
}

export interface CreateWorkflowConnection {
  create_workflow_connection: CreateWorkflowConnection_create_workflow_connection;
}

export interface CreateWorkflowConnectionVariables {
  data: CreateWorkflowConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateWorkflowConnection
// ====================================================

export interface UpdateWorkflowConnection_update_workflow_connection_workflow_connection {
  id: string;
}

export interface UpdateWorkflowConnection_update_workflow_connection_errors {
  field: string;
  messages: string[];
}

export interface UpdateWorkflowConnection_update_workflow_connection {
  workflow_connection: UpdateWorkflowConnection_update_workflow_connection_workflow_connection | null;
  errors: UpdateWorkflowConnection_update_workflow_connection_errors[] | null;
}

export interface UpdateWorkflowConnection {
  update_workflow_connection: UpdateWorkflowConnection_update_workflow_connection;
}

export interface UpdateWorkflowConnectionVariables {
  data: UpdateWorkflowConnectionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteWorkflowConnection
// ====================================================

export interface DeleteWorkflowConnection_delete_workflow_connection_errors {
  field: string;
  messages: string[];
}

export interface DeleteWorkflowConnection_delete_workflow_connection {
  id: string;
  errors: DeleteWorkflowConnection_delete_workflow_connection_errors[] | null;
}

export interface DeleteWorkflowConnection {
  delete_workflow_connection: DeleteWorkflowConnection_delete_workflow_connection;
}

export interface DeleteWorkflowConnectionVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateWorkflowAction
// ====================================================

export interface CreateWorkflowAction_create_workflow_action_workflow_action {
  id: string;
}

export interface CreateWorkflowAction_create_workflow_action_errors {
  field: string;
  messages: string[];
}

export interface CreateWorkflowAction_create_workflow_action {
  workflow_action: CreateWorkflowAction_create_workflow_action_workflow_action | null;
  errors: CreateWorkflowAction_create_workflow_action_errors[] | null;
}

export interface CreateWorkflowAction {
  create_workflow_action: CreateWorkflowAction_create_workflow_action;
}

export interface CreateWorkflowActionVariables {
  data: CreateWorkflowActionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateWorkflowAction
// ====================================================

export interface UpdateWorkflowAction_update_workflow_action_workflow_action {
  id: string;
}

export interface UpdateWorkflowAction_update_workflow_action_errors {
  field: string;
  messages: string[];
}

export interface UpdateWorkflowAction_update_workflow_action {
  workflow_action: UpdateWorkflowAction_update_workflow_action_workflow_action | null;
  errors: UpdateWorkflowAction_update_workflow_action_errors[] | null;
}

export interface UpdateWorkflowAction {
  update_workflow_action: UpdateWorkflowAction_update_workflow_action;
}

export interface UpdateWorkflowActionVariables {
  data: UpdateWorkflowActionMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteWorkflowAction
// ====================================================

export interface DeleteWorkflowAction_delete_workflow_action_errors {
  field: string;
  messages: string[];
}

export interface DeleteWorkflowAction_delete_workflow_action {
  id: string;
  errors: DeleteWorkflowAction_delete_workflow_action_errors[] | null;
}

export interface DeleteWorkflowAction {
  delete_workflow_action: DeleteWorkflowAction_delete_workflow_action;
}

export interface DeleteWorkflowActionVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateWorkflowEvent
// ====================================================

export interface CreateWorkflowEvent_create_workflow_event_workflow_event {
  id: string;
}

export interface CreateWorkflowEvent_create_workflow_event_errors {
  field: string;
  messages: string[];
}

export interface CreateWorkflowEvent_create_workflow_event {
  workflow_event: CreateWorkflowEvent_create_workflow_event_workflow_event | null;
  errors: CreateWorkflowEvent_create_workflow_event_errors[] | null;
}

export interface CreateWorkflowEvent {
  create_workflow_event: CreateWorkflowEvent_create_workflow_event;
}

export interface CreateWorkflowEventVariables {
  data: CreateWorkflowEventMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CancelWorkflowEvent
// ====================================================

export interface CancelWorkflowEvent_cancel_workflow_event_workflow_event {
  id: string;
}

export interface CancelWorkflowEvent_cancel_workflow_event_errors {
  field: string;
  messages: string[];
}

export interface CancelWorkflowEvent_cancel_workflow_event {
  workflow_event: CancelWorkflowEvent_cancel_workflow_event_workflow_event | null;
  errors: CancelWorkflowEvent_cancel_workflow_event_errors[] | null;
}

export interface CancelWorkflowEvent {
  cancel_workflow_event: CancelWorkflowEvent_cancel_workflow_event;
}

export interface CancelWorkflowEventVariables {
  data: CancelWorkflowEventMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateWorkflowTrigger
// ====================================================

export interface CreateWorkflowTrigger_create_workflow_trigger_workflow_trigger {
  id: string;
}

export interface CreateWorkflowTrigger_create_workflow_trigger_errors {
  field: string;
  messages: string[];
}

export interface CreateWorkflowTrigger_create_workflow_trigger {
  workflow_trigger: CreateWorkflowTrigger_create_workflow_trigger_workflow_trigger | null;
  errors: CreateWorkflowTrigger_create_workflow_trigger_errors[] | null;
}

export interface CreateWorkflowTrigger {
  create_workflow_trigger: CreateWorkflowTrigger_create_workflow_trigger;
}

export interface CreateWorkflowTriggerVariables {
  data: CreateWorkflowTriggerMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateWorkflowTrigger
// ====================================================

export interface UpdateWorkflowTrigger_update_workflow_trigger_workflow_trigger {
  id: string;
}

export interface UpdateWorkflowTrigger_update_workflow_trigger_errors {
  field: string;
  messages: string[];
}

export interface UpdateWorkflowTrigger_update_workflow_trigger {
  workflow_trigger: UpdateWorkflowTrigger_update_workflow_trigger_workflow_trigger | null;
  errors: UpdateWorkflowTrigger_update_workflow_trigger_errors[] | null;
}

export interface UpdateWorkflowTrigger {
  update_workflow_trigger: UpdateWorkflowTrigger_update_workflow_trigger;
}

export interface UpdateWorkflowTriggerVariables {
  data: UpdateWorkflowTriggerMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteWorkflowTrigger
// ====================================================

export interface DeleteWorkflowTrigger_delete_workflow_trigger_errors {
  field: string;
  messages: string[];
}

export interface DeleteWorkflowTrigger_delete_workflow_trigger {
  id: string;
  errors: DeleteWorkflowTrigger_delete_workflow_trigger_errors[] | null;
}

export interface DeleteWorkflowTrigger {
  delete_workflow_trigger: DeleteWorkflowTrigger_delete_workflow_trigger;
}

export interface DeleteWorkflowTriggerVariables {
  data: DeleteMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: TriggerScheduledWorkflow
// ====================================================

export interface TriggerScheduledWorkflow_trigger_scheduled_workflow_workflow_event {
  id: string;
  status: AutomationEventStatus;
  created_at: any;
}

export interface TriggerScheduledWorkflow_trigger_scheduled_workflow_errors {
  field: string;
  messages: string[];
}

export interface TriggerScheduledWorkflow_trigger_scheduled_workflow {
  workflow_event: TriggerScheduledWorkflow_trigger_scheduled_workflow_workflow_event | null;
  errors: TriggerScheduledWorkflow_trigger_scheduled_workflow_errors[] | null;
}

export interface TriggerScheduledWorkflow {
  trigger_scheduled_workflow: TriggerScheduledWorkflow_trigger_scheduled_workflow;
}

export interface TriggerScheduledWorkflowVariables {
  trigger_id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: ValidateCronExpression
// ====================================================

export interface ValidateCronExpression_validate_cron_expression_errors {
  field: string;
  messages: string[];
}

export interface ValidateCronExpression_validate_cron_expression {
  is_valid: boolean;
  description: string | null;
  next_run_times: any[] | null;
  error_message: string | null;
  errors: ValidateCronExpression_validate_cron_expression_errors[] | null;
}

export interface ValidateCronExpression {
  validate_cron_expression: ValidateCronExpression_validate_cron_expression;
}

export interface ValidateCronExpressionVariables {
  input: ValidateCronExpressionInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetShippingRule
// ====================================================

export interface GetShippingRule_shipping_rule_conditions_destination {
  country_code: string | null;
  postal_code: string[] | null;
}

export interface GetShippingRule_shipping_rule_conditions_weight {
  min: number | null;
  max: number | null;
  unit: string | null;
}

export interface GetShippingRule_shipping_rule_conditions_rate_comparison {
  compare: RateComparisonField;
  operator: ComparisonOperator;
  value: number;
}

export interface GetShippingRule_shipping_rule_conditions_address_type {
  type: string;
}

export interface GetShippingRule_shipping_rule_conditions {
  destination: GetShippingRule_shipping_rule_conditions_destination | null;
  carrier_id: string | null;
  service: string | null;
  weight: GetShippingRule_shipping_rule_conditions_weight | null;
  rate_comparison: GetShippingRule_shipping_rule_conditions_rate_comparison | null;
  address_type: GetShippingRule_shipping_rule_conditions_address_type | null;
  value: number | null;
  metadata: any | null;
}

export interface GetShippingRule_shipping_rule_actions_select_service {
  carrier_code: string | null;
  carrier_id: string | null;
  service_code: string | null;
  strategy: SelectServiceStrategy;
}

export interface GetShippingRule_shipping_rule_actions {
  select_service: GetShippingRule_shipping_rule_actions_select_service | null;
  block_service: boolean | null;
}

export interface GetShippingRule_shipping_rule {
  object_type: string;
  id: string;
  name: string;
  slug: string;
  priority: number;
  is_active: boolean;
  description: string | null;
  conditions: GetShippingRule_shipping_rule_conditions | null;
  actions: GetShippingRule_shipping_rule_actions | null;
  metadata: any | null;
  created_at: any;
  updated_at: any;
}

export interface GetShippingRule {
  shipping_rule: GetShippingRule_shipping_rule | null;
}

export interface GetShippingRuleVariables {
  id: string;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetShippingRules
// ====================================================

export interface GetShippingRules_shipping_rules_page_info {
  count: number;
  has_next_page: boolean;
  has_previous_page: boolean;
  start_cursor: string | null;
  end_cursor: string | null;
}

export interface GetShippingRules_shipping_rules_edges_node_conditions_destination {
  country_code: string | null;
  postal_code: string[] | null;
}

export interface GetShippingRules_shipping_rules_edges_node_conditions_weight {
  min: number | null;
  max: number | null;
  unit: string | null;
}

export interface GetShippingRules_shipping_rules_edges_node_conditions_rate_comparison {
  compare: RateComparisonField;
  operator: ComparisonOperator;
  value: number;
}

export interface GetShippingRules_shipping_rules_edges_node_conditions_address_type {
  type: string;
}

export interface GetShippingRules_shipping_rules_edges_node_conditions {
  destination: GetShippingRules_shipping_rules_edges_node_conditions_destination | null;
  carrier_id: string | null;
  service: string | null;
  weight: GetShippingRules_shipping_rules_edges_node_conditions_weight | null;
  rate_comparison: GetShippingRules_shipping_rules_edges_node_conditions_rate_comparison | null;
  address_type: GetShippingRules_shipping_rules_edges_node_conditions_address_type | null;
  value: number | null;
  metadata: any | null;
}

export interface GetShippingRules_shipping_rules_edges_node_actions_select_service {
  carrier_code: string | null;
  carrier_id: string | null;
  service_code: string | null;
  strategy: SelectServiceStrategy;
}

export interface GetShippingRules_shipping_rules_edges_node_actions {
  select_service: GetShippingRules_shipping_rules_edges_node_actions_select_service | null;
  block_service: boolean | null;
}

export interface GetShippingRules_shipping_rules_edges_node {
  object_type: string;
  id: string;
  name: string;
  slug: string;
  priority: number;
  is_active: boolean;
  description: string | null;
  conditions: GetShippingRules_shipping_rules_edges_node_conditions | null;
  actions: GetShippingRules_shipping_rules_edges_node_actions | null;
  metadata: any | null;
  created_at: any;
  updated_at: any;
}

export interface GetShippingRules_shipping_rules_edges {
  node: GetShippingRules_shipping_rules_edges_node;
}

export interface GetShippingRules_shipping_rules {
  page_info: GetShippingRules_shipping_rules_page_info;
  edges: GetShippingRules_shipping_rules_edges[];
}

export interface GetShippingRules {
  shipping_rules: GetShippingRules_shipping_rules;
}

export interface GetShippingRulesVariables {
  filter?: ShippingRuleFilter | null;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateShippingRule
// ====================================================

export interface CreateShippingRule_create_shipping_rule_shipping_rule {
  id: string;
}

export interface CreateShippingRule_create_shipping_rule_errors {
  field: string;
  messages: string[];
}

export interface CreateShippingRule_create_shipping_rule {
  shipping_rule: CreateShippingRule_create_shipping_rule_shipping_rule | null;
  errors: CreateShippingRule_create_shipping_rule_errors[] | null;
}

export interface CreateShippingRule {
  create_shipping_rule: CreateShippingRule_create_shipping_rule;
}

export interface CreateShippingRuleVariables {
  data: CreateShippingRuleMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateShippingRule
// ====================================================

export interface UpdateShippingRule_update_shipping_rule_shipping_rule {
  id: string;
}

export interface UpdateShippingRule_update_shipping_rule_errors {
  field: string;
  messages: string[];
}

export interface UpdateShippingRule_update_shipping_rule {
  shipping_rule: UpdateShippingRule_update_shipping_rule_shipping_rule | null;
  errors: UpdateShippingRule_update_shipping_rule_errors[] | null;
}

export interface UpdateShippingRule {
  update_shipping_rule: UpdateShippingRule_update_shipping_rule;
}

export interface UpdateShippingRuleVariables {
  data: UpdateShippingRuleMutationInput;
}


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: DeleteShippingRule
// ====================================================

export interface DeleteShippingRule_delete_shipping_rule_errors {
  field: string;
  messages: string[];
}

export interface DeleteShippingRule_delete_shipping_rule {
  id: string;
  errors: DeleteShippingRule_delete_shipping_rule_errors[] | null;
}

export interface DeleteShippingRule {
  delete_shipping_rule: DeleteShippingRule_delete_shipping_rule;
}

export interface DeleteShippingRuleVariables {
  data: DeleteMutationInput;
}

/* tslint:disable */
// This file was automatically generated and should not be edited.

//==============================================================
// START Enums and Input Objects
//==============================================================

export enum MetafieldTypeEnum {
  boolean = "boolean",
  date = "date",
  date_time = "date_time",
  json = "json",
  number = "number",
  password = "password",
  text = "text",
}

export enum UserRole {
  admin = "admin",
  developer = "developer",
  member = "member",
}

export enum AutomationTriggerType {
  manual = "manual",
  scheduled = "scheduled",
  webhook = "webhook",
}

export enum AutomationActionType {
  conditional = "conditional",
  data_mapping = "data_mapping",
  function_call = "function_call",
  http_request = "http_request",
}

export enum AutomationHTTPMethod {
  delete = "delete",
  get = "get",
  patch = "patch",
  post = "post",
  put = "put",
}

export enum AutomationHTTPContentType {
  form = "form",
  json = "json",
  text = "text",
  xml = "xml",
}

export enum AutomationParametersType {
  data = "data",
  querystring = "querystring",
}

export enum AutomationAuthType {
  api_key = "api_key",
  basic = "basic",
  jwt = "jwt",
  oauth2 = "oauth2",
}

export enum AutomationEventStatus {
  aborted = "aborted",
  cancelled = "cancelled",
  failed = "failed",
  pending = "pending",
  running = "running",
  success = "success",
}

export enum AutomationEventType {
  auto = "auto",
  manual = "manual",
  scheduled = "scheduled",
  webhook = "webhook",
}

export enum RateComparisonField {
  duty_charge = "duty_charge",
  estimated_delivery = "estimated_delivery",
  fuel_surcharge = "fuel_surcharge",
  insurance_charge = "insurance_charge",
  tax_charge = "tax_charge",
  total_charge = "total_charge",
  transit_days = "transit_days",
}

export enum ComparisonOperator {
  eq = "eq",
  gt = "gt",
  gte = "gte",
  lt = "lt",
  lte = "lte",
}

export enum SelectServiceStrategy {
  cheapest = "cheapest",
  fastest = "fastest",
  preferred = "preferred",
}

// null
export interface OAuthAppFilter {
  offset?: number | null;
  first?: number | null;
  display_name?: string | null;
  features?: string[] | null;
  metadata_key?: string | null;
  metadata_value?: string | null;
  created_after?: any | null;
  created_before?: any | null;
}

// null
export interface AppInstallationFilter {
  offset?: number | null;
  first?: number | null;
  app_id?: string | null;
  app_type?: string | null;
  is_active?: boolean | null;
  metadata_key?: string | null;
  metadata_value?: string | null;
  created_after?: any | null;
  created_before?: any | null;
}

// null
export interface CreateOAuthAppMutationInput {
  display_name: string;
  description?: string | null;
  launch_url: string;
  redirect_uris: string;
  features?: string[] | null;
  metadata?: any | null;
}

// null
export interface UpdateOAuthAppMutationInput {
  id: string;
  display_name?: string | null;
  description?: string | null;
  launch_url?: string | null;
  redirect_uris?: string | null;
  features?: string[] | null;
  metadata?: any | null;
}

// null
export interface DeleteOAuthAppMutationInput {
  id: string;
}

// null
export interface InstallAppMutationInput {
  app_id: string;
  app_type?: string | null;
  access_scopes?: string[] | null;
  metadata?: any | null;
  metafields?: CreateMetafieldInput[] | null;
  requires_oauth?: boolean | null;
  oauth_app_data?: CreateOAuthAppMutationInput | null;
}

// null
export interface CreateMetafieldInput {
  key: string;
  type: MetafieldTypeEnum;
  value?: any | null;
  is_required?: boolean | null;
}

// null
export interface UninstallAppMutationInput {
  app_id?: string | null;
  installation_id?: string | null;
}

// null
export interface UpdateAppInstallationMutationInput {
  id: string;
  access_scopes?: string[] | null;
  is_active?: boolean | null;
  metadata?: any | null;
  metafields?: MetafieldInput[] | null;
}

// null
export interface MetafieldInput {
  key: string;
  type: MetafieldTypeEnum;
  value?: any | null;
  is_required?: boolean | null;
  id?: string | null;
}

// null
export interface RotateAppApiKeyMutationInput {
  id: string;
}

// null
export interface EnsureAppApiKeyMutationInput {
  id: string;
}

// null
export interface UsageFilter {
  date_after?: string | null;
  date_before?: string | null;
  omit?: string[] | null;
}

// null
export interface DeleteOrganizationMutationInput {
  id: string;
  password: string;
}

// null
export interface CreateOrganizationMutationInput {
  name: string;
}

// null
export interface UpdateOrganizationMutationInput {
  id: string;
  name?: string | null;
}

// null
export interface ChangeOrganizationOwnerMutationInput {
  org_id: string;
  email: string;
  password: string;
}

// null
export interface SetOrganizationUserRolesMutationInput {
  org_id: string;
  user_id: string;
  roles: UserRole[];
}

// null
export interface SendOrganizationInvitesMutationInput {
  org_id: string;
  emails: string[];
  redirect_url: string;
  roles?: UserRole[] | null;
}

// null
export interface AcceptOrganizationInvitationMutationInput {
  guid: string;
}

// null
export interface DeleteMutationInput {
  id: string;
}

// null
export interface RemoveOrganizationMemberMutationInput {
  org_id: string;
  user_id: string;
}

// null
export interface UpdateMemberStatusMutationInput {
  org_id: string;
  user_id: string;
  is_active: boolean;
}

// null
export interface ResendOrganizationInviteMutationInput {
  invitation_id: string;
  redirect_url: string;
}

// null
export interface WorkflowFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
  trigger_type?: AutomationTriggerType | null;
  is_active?: boolean | null;
}

// null
export interface WorkflowConnectionFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
  auth_type?: AutomationAuthType | null;
}

// null
export interface WorkflowActionFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
  action_type?: AutomationActionType | null;
}

// null
export interface WorkflowEventFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
  parameters_key?: string[] | null;
  status?: AutomationEventStatus | null;
  event_type?: AutomationEventType | null;
}

// null
export interface CreateWorkflowMutationInput {
  name: string;
  action_nodes: ActionNodeInput[];
  description?: string | null;
  metadata?: any | null;
  template_slug?: string | null;
  trigger?: PartialWorkflowTriggerMutationInput | null;
  actions?: PartialWorkflowActionMutationInput[] | null;
}

// null
export interface ActionNodeInput {
  order: number;
  slug?: string | null;
  index?: number | null;
}

// null
export interface PartialWorkflowTriggerMutationInput {
  id?: string | null;
  trigger_type?: AutomationTriggerType | null;
  schedule?: string | null;
  secret?: string | null;
  secret_key?: string | null;
  template_slug?: string | null;
}

// null
export interface PartialWorkflowActionMutationInput {
  name?: string | null;
  action_type?: AutomationActionType | null;
  port?: number | null;
  host?: string | null;
  endpoint?: string | null;
  description?: string | null;
  method?: AutomationHTTPMethod | null;
  parameters_type?: AutomationParametersType | null;
  parameters_template?: string | null;
  header_template?: string | null;
  content_type?: AutomationHTTPContentType | null;
  metadata?: any | null;
  template_slug?: string | null;
  metafields?: MetafieldInput[] | null;
  connection?: PartialWorkflowConnectionMutationInput | null;
  id?: string | null;
  slug?: string | null;
}

// null
export interface PartialWorkflowConnectionMutationInput {
  name?: string | null;
  auth_type?: AutomationAuthType | null;
  port?: number | null;
  host?: string | null;
  endpoint?: string | null;
  description?: string | null;
  credentials?: any | null;
  auth_template?: string | null;
  metadata?: any | null;
  parameters_template?: string | null;
  template_slug?: string | null;
  metafields?: MetafieldInput[] | null;
  id?: string | null;
}

// null
export interface UpdateWorkflowMutationInput {
  id: string;
  name?: string | null;
  description?: string | null;
  metadata?: any | null;
  action_nodes?: ActionNodeInput[] | null;
  template_slug?: string | null;
  trigger?: PartialWorkflowTriggerMutationInput | null;
  actions?: PartialWorkflowActionMutationInput[] | null;
}

// null
export interface CreateWorkflowConnectionMutationInput {
  name: string;
  auth_type: AutomationAuthType;
  port?: number | null;
  host?: string | null;
  endpoint?: string | null;
  description?: string | null;
  credentials?: any | null;
  auth_template?: string | null;
  metadata?: any | null;
  parameters_template?: string | null;
  template_slug?: string | null;
  metafields?: CreateMetafieldInput[] | null;
}

// null
export interface UpdateWorkflowConnectionMutationInput {
  name?: string | null;
  auth_type?: AutomationAuthType | null;
  port?: number | null;
  host?: string | null;
  endpoint?: string | null;
  description?: string | null;
  credentials?: any | null;
  auth_template?: string | null;
  metadata?: any | null;
  parameters_template?: string | null;
  template_slug?: string | null;
  metafields?: MetafieldInput[] | null;
  id: string;
}

// null
export interface CreateWorkflowActionMutationInput {
  name: string;
  action_type: AutomationActionType;
  port?: number | null;
  host?: string | null;
  endpoint?: string | null;
  description?: string | null;
  method?: AutomationHTTPMethod | null;
  parameters_type?: AutomationParametersType | null;
  parameters_template?: string | null;
  header_template?: string | null;
  content_type?: AutomationHTTPContentType | null;
  metadata?: any | null;
  template_slug?: string | null;
  metafields?: CreateMetafieldInput[] | null;
  connection?: PartialWorkflowConnectionMutationInput | null;
}

// null
export interface UpdateWorkflowActionMutationInput {
  name?: string | null;
  action_type?: AutomationActionType | null;
  port?: number | null;
  host?: string | null;
  endpoint?: string | null;
  description?: string | null;
  method?: AutomationHTTPMethod | null;
  parameters_type?: AutomationParametersType | null;
  parameters_template?: string | null;
  header_template?: string | null;
  content_type?: AutomationHTTPContentType | null;
  metadata?: any | null;
  template_slug?: string | null;
  metafields?: MetafieldInput[] | null;
  connection?: PartialWorkflowConnectionMutationInput | null;
  id: string;
}

// null
export interface CreateWorkflowEventMutationInput {
  workflow_id: string;
  event_type: AutomationEventType;
  parameters?: any | null;
}

// null
export interface CancelWorkflowEventMutationInput {
  id: string;
}

// null
export interface CreateWorkflowTriggerMutationInput {
  workflow_id: string;
  trigger_type: AutomationTriggerType;
  schedule?: string | null;
  secret?: string | null;
  secret_key?: string | null;
  template_slug?: string | null;
}

// null
export interface UpdateWorkflowTriggerMutationInput {
  id: string;
  trigger_type?: AutomationTriggerType | null;
  schedule?: string | null;
  secret?: string | null;
  secret_key?: string | null;
  template_slug?: string | null;
}

// null
export interface ValidateCronExpressionInput {
  expression: string;
}

// null
export interface ShippingRuleFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
  is_active?: boolean | null;
  priority?: number | null;
}

// null
export interface CreateShippingRuleMutationInput {
  name: string;
  description?: string | null;
  priority?: number | null;
  conditions?: ShippingRuleConditionsInput | null;
  actions?: ShippingRuleActionsInput | null;
  metadata?: any | null;
  is_active?: boolean | null;
}

// null
export interface ShippingRuleConditionsInput {
  destination?: DestinationConditionInput | null;
  carrier_id?: string | null;
  service?: string | null;
  weight?: WeightConditionInput | null;
  rate_comparison?: RateComparisonConditionInput | null;
  metadata?: any | null;
  address_type?: AddressTypeConditionInput | null;
  value?: number | null;
}

// null
export interface DestinationConditionInput {
  country_code?: string | null;
  postal_code?: string[] | null;
}

// null
export interface WeightConditionInput {
  min?: number | null;
  max?: number | null;
  unit?: string | null;
}

// null
export interface RateComparisonConditionInput {
  compare: RateComparisonField;
  operator: ComparisonOperator;
  value: number;
}

// null
export interface AddressTypeConditionInput {
  type: string;
}

// null
export interface ShippingRuleActionsInput {
  select_service?: SelectServiceActionInput | null;
  block_service?: boolean | null;
}

// null
export interface SelectServiceActionInput {
  carrier_code?: string | null;
  carrier_id?: string | null;
  service_code?: string | null;
  strategy?: SelectServiceStrategy | null;
}

// null
export interface UpdateShippingRuleMutationInput {
  id: string;
  name?: string | null;
  description?: string | null;
  priority?: number | null;
  conditions?: ShippingRuleConditionsInput | null;
  actions?: ShippingRuleActionsInput | null;
  metadata?: any | null;
  is_active?: boolean | null;
}

//==============================================================
// END Enums and Input Objects
//==============================================================