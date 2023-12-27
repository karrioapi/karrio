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

export const GET_WORKFLOW = gql`query GetWorkflow($id: String!) {
  workflow(id: $id) {
    id
    name
    slug
    description
    trigger {
      object_type
      id
      slug
      trigger_type
      schedule
      secret
      secret_key
    }
    action_nodes {
      order
      slug
    }
    actions {
      object_type
      id
      slug
      name
      action_type
      description
      port
      host
      endpoint
      method
      content_type
      header_template
      parameters_type
      parameters_template
      connection {
        object_type
        id
        name
        slug
        auth_type
        port
        host
        endpoint
        description
        parameters_template
        auth_template
        credentials
        metadata
        template_slug
      }
      metadata
      template_slug
    }
    metadata
    template_slug
  }
}
`;

export const GET_WORKFLOWS = gql`query GetWorkflows($filter: WorkflowFilter) {
  workflows(filter: $filter) {
    page_info {
      has_next_page
      has_previous_page
      start_cursor
      end_cursor
    }
    edges {
      node {
        id
        name
        slug
        description
        trigger {
          object_type
          id
          slug
          trigger_type
          schedule
          id
          secret
          secret_key
        }
        action_nodes {
          order
          slug
        }
        actions {
          object_type
          id
          slug
          name
          action_type
          description
          port
          host
          endpoint
          method
          content_type
          header_template
          parameters_type
          parameters_template
          connection {
            object_type
            id
            name
            slug
            auth_type
            port
            host
            endpoint
            description
            parameters_template
            auth_template
            credentials
            metadata
            template_slug
          }
          metadata
          template_slug
        }
        metadata
        template_slug
      }
    }
  }
}
`;

export const GET_WORKFLOW_CONNECTION = gql`query GetWorkflowConnection($id: String!) {
  workflow_connection(id: $id) {
    id
    name
    slug
    auth_type
    description
    host
    port
    endpoint
    parameters_template
    auth_template
    credentials
    metadata
    template_slug
  }
}
`;

export const GET_WORKFLOW_CONNECTIONS = gql`query GetWorkflowConnections($filter: WorkflowConnectionFilter) {
  workflow_connections(filter: $filter) {
    page_info {
      has_next_page
      has_previous_page
      start_cursor
      end_cursor
    }
    edges {
      node {
        id
        name
        slug
        auth_type
        description
        host
        port
        endpoint
        parameters_template
        auth_template
        credentials
        metadata
        template_slug
      }
    }
  }
}
`;

export const GET_WORKFLOW_ACTION = gql`query GetWorkflowAction($id: String!) {
  workflow_action(id: $id) {
    object_type
    id
    slug
    name
    action_type
    description
    port
    host
    endpoint
    method
    content_type
    header_template
    parameters_type
    parameters_template
    connection {
      object_type
      id
      name
      slug
      auth_type
      port
      host
      endpoint
      description
      parameters_template
      auth_template
      credentials
      metadata
      template_slug
    }
    metadata
    template_slug
  }
}
`;

export const GET_WORKFLOW_ACTIONS = gql`query GetWorkflowActions($filter: WorkflowActionFilter) {
  workflow_actions(filter: $filter) {
    page_info {
      has_next_page
      has_previous_page
      start_cursor
      end_cursor
    }
    edges {
      node {
        object_type
        id
        slug
        name
        action_type
        description
        port
        host
        endpoint
        method
        content_type
        header_template
        parameters_type
        parameters_template
        connection {
          object_type
          id
          name
          slug
          auth_type
          port
          host
          endpoint
          description
          parameters_template
          auth_template
          credentials
          metadata
          template_slug
        }
        metadata
        template_slug
      }
    }
  }
}
`;

export const GET_WORKFLOW_EVENT = gql`query GetWorkflowEvent($id: String!) {
  workflow_event(id: $id) {
    object_type
    id
    status
    event_type
    parameters
    test_mode
    records {
      object_type
      id
      key
      timestamp
      test_mode
      record
      meta
    }
  }
}
`;

export const GET_WORKFLOW_EVENTS = gql`query GetWorkflowEvents($filter: WorkflowEventFilter) {
  workflow_events(filter: $filter) {
    page_info {
      has_next_page
      has_previous_page
      start_cursor
      end_cursor
    }
    edges {
      node {
        object_type
        id
        status
        event_type
        parameters
        test_mode
        records {
          object_type
          id
          key
          timestamp
          test_mode
          record
          meta
        }
      }
    }
  }
}
`;

export const GET_WORKFLOW_TEMPLATES = gql`query GetWorkflowTemplates($filter: WorkflowFilter) {
  workflow_templates(filter: $filter) {
    page_info {
      has_next_page
      has_previous_page
      start_cursor
      end_cursor
    }
    edges {
      node {
        name
        slug
        description
        trigger {
          object_type
          slug
          trigger_type
          schedule
        }
        action_nodes {
          order
          slug
        }
        actions {
          object_type
          slug
          name
          action_type
          description
          port
          host
          endpoint
          method
          content_type
          header_template
          parameters_type
          parameters_template
          connection {
            object_type
            name
            slug
            auth_type
            port
            host
            endpoint
            description
            parameters_template
            auth_template
            template_slug
          }
          template_slug
        }
      }
    }
  }
}
`;

export const GET_WORKFLOW_ACTION_TEMPLATES = gql`query GetWorkflowActionTemplates($filter: WorkflowActionFilter) {
  workflow_action_templates(filter: $filter) {
    page_info {
      has_next_page
      has_previous_page
      start_cursor
      end_cursor
    }
    edges {
      node {
        object_type
        slug
        name
        action_type
        description
        port
        host
        endpoint
        method
        content_type
        header_template
        parameters_type
        parameters_template
        connection {
          object_type
          name
          slug
          auth_type
          port
          host
          endpoint
          description
          parameters_template
          auth_template
          template_slug
        }
        template_slug
      }
    }
  }
}
`;

export const GET_WORKFLOW_CONNECTION_TEMPLATES = gql`query GetWorkflowConnectionTemplates($filter: WorkflowConnectionFilter) {
  workflow_connection_templates(filter: $filter) {
    page_info {
      has_next_page
      has_previous_page
      start_cursor
      end_cursor
    }
    edges {
      node {
        name
        slug
        auth_type
        description
        host
        port
        endpoint
        parameters_template
        auth_template
        template_slug
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

export const CREATE_WORKFLOW = gql`mutation CreateWorkflow($data: CreateWorkflowMutationInput!) {
  create_workflow(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const UPDATE_WORKFLOW = gql`mutation UpdateWorkflow($data: UpdateWorkflowMutationInput!) {
  update_workflow(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const DELETE_WORKFLOW = gql`mutation DeleteWorkflow($data: DeleteMutationInput!) {
  delete_workflow(input: $data) {
    id
    errors {
      field
      messages
    }
  }
}
`;

export const CREATE_WORKFLOW_CONNECTION = gql`mutation CreateWorkflowConnection($data: CreateWorkflowConnectionMutationInput!) {
  create_workflow_connection(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const UPDATE_WORKFLOW_CONNECTION = gql`mutation UpdateWorkflowConnection($data: UpdateWorkflowConnectionMutationInput!) {
  update_workflow_connection(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const DELETE_WORKFLOW_CONNECTION = gql`mutation DeleteWorkflowConnection($data: DeleteMutationInput!) {
  delete_workflow_connection(input: $data) {
    id
  }
}
`;

export const CREATE_WORKFLOW_ACTION = gql`mutation CreateWorkflowAction($data: CreateWorkflowActionMutationInput!) {
  create_workflow_action(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const UPDATE_WORKFLOW_ACTION = gql`mutation UpdateWorkflowAction($data: UpdateWorkflowActionMutationInput!) {
  update_workflow_action(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const DELETE_WORKFLOW_ACTION = gql`mutation DeleteWorkflowAction($data: DeleteMutationInput!) {
  delete_workflow_action(input: $data) {
    id
    errors {
      field
      messages
    }
  }
}
`;

export const CREATE_WORKFLOW_EVENT = gql`mutation CreateWorkflowEvent($data: CreateWorkflowEventMutationInput!) {
  create_workflow_event(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const CANCEL_WORKFLOW_EVENT = gql`mutation CancelWorkflowEvent($data: CancelWorkflowEventMutationInput!) {
  cancel_workflow_event(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const CREATE_WORKFLOW_TRIGGER = gql`mutation CreateWorkflowTrigger($data: CreateWorkflowTriggerMutationInput!) {
  create_workflow_trigger(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const UPDATE_WORKFLOW_TRIGGER = gql`mutation UpdateWorkflowTrigger($data: UpdateWorkflowTriggerMutationInput!) {
  update_workflow_trigger(input: $data) {
    errors {
      field
      messages
    }
  }
}
`;

export const DELETE_WORKFLOW_TRIGGER = gql`mutation DeleteWorkflowTrigger($data: DeleteMutationInput!) {
  delete_workflow_trigger(input: $data) {
    id
  }
}
`;

//#endregion