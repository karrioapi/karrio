

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
  value: string | null;
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
  template_slug: string | null;
  metadata: any | null;
  metafields: GetWorkflow_workflow_actions_connection_metafields[];
}

export interface GetWorkflow_workflow_actions_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: string | null;
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
  value: string | null;
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
  value: string | null;
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
// GraphQL query operation: GetWorkflowConnection
// ====================================================

export interface GetWorkflowConnection_workflow_connection_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: string | null;
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
  value: string | null;
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
  value: string | null;
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
  metadata: any | null;
  template_slug: string | null;
  metafields: GetWorkflowAction_workflow_action_connection_metafields[];
}

export interface GetWorkflowAction_workflow_action_metafields {
  id: string;
  key: string;
  is_required: boolean;
  type: MetafieldTypeEnum;
  value: string | null;
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
  value: string | null;
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
  value: string | null;
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
  value: string | null;
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
  value: string | null;
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
  value: string | null;
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
  value: string | null;
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
  value: string | null;
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

//==============================================================
// START Enums and Input Objects
//==============================================================

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

export enum MetafieldTypeEnum {
  boolean = "boolean",
  number = "number",
  text = "text",
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

// null
export interface AppFilter {
  offset?: number | null;
  first?: number | null;
  features?: string[] | null;
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
export interface WorkflowFilter {
  offset?: number | null;
  first?: number | null;
  keyword?: string | null;
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
export interface MetafieldInput {
  key: string;
  type: MetafieldTypeEnum;
  value?: string | null;
  namespace?: string | null;
  is_required?: boolean | null;
  id?: string | null;
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
export interface CreateMetafieldInput {
  key: string;
  type: MetafieldTypeEnum;
  value?: string | null;
  namespace?: string | null;
  is_required?: boolean | null;
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

//==============================================================
// END Enums and Input Objects
//==============================================================