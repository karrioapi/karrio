

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

export interface get_organization_organization_usage_shipment_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organization_organization_usage {
  members: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_shipments: number | null;
  unfulfilled_orders: number | null;
  api_requests: get_organization_organization_usage_api_requests[] | null;
  order_volumes: get_organization_organization_usage_order_volumes[] | null;
  shipment_count: get_organization_organization_usage_shipment_count[] | null;
  shipment_spend: get_organization_organization_usage_shipment_spend[] | null;
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

export interface get_organizations_organizations_usage_shipment_spend {
  date: string | null;
  label: string | null;
  count: number | null;
}

export interface get_organizations_organizations_usage {
  members: number | null;
  order_volume: number | null;
  total_requests: number | null;
  total_shipments: number | null;
  unfulfilled_orders: number | null;
  api_requests: get_organizations_organizations_usage_api_requests[] | null;
  order_volumes: get_organizations_organizations_usage_order_volumes[] | null;
  shipment_count: get_organizations_organizations_usage_shipment_count[] | null;
  shipment_spend: get_organizations_organizations_usage_shipment_spend[] | null;
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

//==============================================================
// START Enums and Input Objects
//==============================================================

export enum UserRole {
  admin = "admin",
  developer = "developer",
  member = "member",
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

//==============================================================
// END Enums and Input Objects
//==============================================================