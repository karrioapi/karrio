import gql from 'graphql-tag';


// -----------------------------------------------------------
// Platform GraphQL Queries
// -----------------------------------------------------------
//#region


export const GET_ORGANIZATION = gql`query get_organization($id: String!) {
  organization(id: $id) {
    id
    name
    slug
    token
    current_user {
      email
      full_name
      is_admin
      is_owner
      last_login
    }
    members {
      email
      full_name
      is_admin
      is_owner
      invitation {
        id
        guid
        invitee_identifier
        created
        modified
      }
      last_login
    }
    usage {
      members
      order_volume
      total_requests
      total_shipments
      unfulfilled_orders
      api_requests {
        date
        label
        count
      }
      order_volumes {
        date
        label
        count
      }
      shipment_count {
        date
        label
        count
      }
      shipment_spend {
        date
        label
        count
      }
    }
  }
}
`;

export const GET_ORGANIZATIONS = gql`query get_organizations {
  organizations {
    id
    name
    slug
    token
    current_user {
      email
      full_name
      is_admin
      is_owner
      last_login
    }
    members {
      email
      full_name
      is_admin
      is_owner
      invitation {
        id
        guid
        invitee_identifier
        created
        modified
      }
      last_login
    }
    usage {
      members
      order_volume
      total_requests
      total_shipments
      unfulfilled_orders
      api_requests {
        date
        label
        count
      }
      order_volumes {
        date
        label
        count
      }
      shipment_count {
        date
        label
        count
      }
      shipment_spend {
        date
        label
        count
      }
    }
  }
}
`;

//#endregion


// -----------------------------------------------------------
// Platform GraphQL Mutations
// -----------------------------------------------------------
//#region


export const DELETE_ORGANIZATION = gql`mutation delete_organization($data: DeleteOrganizationMutationInput!) {
  delete_organization(input: $data) {
    organization {
      id
    }
    errors {
      field
      messages
    }
  }
}
`;

export const CREATE_ORGANIZATION = gql`mutation create_organization($data: CreateOrganizationMutationInput!) {
  create_organization(input: $data) {
    organization {
      id
    }
    errors {
      field
      messages
    }
  }
}
`;

export const UPDATE_ORGANIZATION = gql`mutation update_organization($data: UpdateOrganizationMutationInput!) {
  update_organization(input: $data) {
    organization {
      id
    }
    errors {
      field
      messages
    }
  }
}
`;

export const CHANGE_ORGANIZATION_OWNER = gql`mutation change_organization_owner($data: ChangeOrganizationOwnerMutationInput!) {
  change_organization_owner(input: $data) {
    organization {
      id
    }
    errors {
      field
      messages
    }
  }
}
`;

export const SET_ORGANIZATION_USER_ROLES = gql`mutation set_organization_user_roles($data: SetOrganizationUserRolesMutationInput!) {
  set_organization_user_roles(input: $data) {
    organization {
      id
    }
    errors {
      field
      messages
    }
  }
}
`;

export const SEND_ORGANIZATION_INVITES = gql`mutation send_organization_invites($data: SendOrganizationInvitesMutationInput!) {
  send_organization_invites(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const GET_ORGANIZATION_INVITATION = gql`query get_organization_invitation($guid: String!) {
  organization_invitation(guid: $guid) {
    invitee_identifier
    organization_name
    invitee {
      email
    }
  }
}
`;

export const ACCEPT_ORGANIZATION_INVITATION = gql`mutation accept_organization_invitation($data: AcceptOrganizationInvitationMutationInput!) {
  accept_organization_invitation(input: $data) {
    organization {
      id
    }
    errors {
      field
      messages
    }
  }
}
`;

export const DELETE_ORGANIZATION_INVITES = gql`mutation delete_organization_invitation($data: DeleteMutationInput!) {
  delete_organization_invitation(input: $data) {
    id
  }
}
`;

//#endregion