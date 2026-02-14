import gql from "graphql-tag";

// -----------------------------------------------------------
// Markups Queries
// -----------------------------------------------------------
export const GET_MARKUPS = gql`
  query GetMarkups($filter: MarkupFilter, $usageFilter: UsageFilter) {
    markups(filter: $filter) {
      edges {
        node {
          id
          name
          active
          amount
          markup_type
          is_visible
          carrier_codes
          service_codes
          connection_ids
          organization_ids
          metadata
          usage(filter: $usageFilter) {
            total_shipments
            total_addons_charges
          }
        }
      }
      page_info {
        count
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
    }
  }
`;

export const GET_MARKUP = gql`
  query GetMarkup($id: String!) {
    markup(id: $id) {
      id
      name
      active
      amount
      markup_type
      is_visible
      carrier_codes
      service_codes
      connection_ids
      organization_ids
      metadata
      usage {
        total_shipments
        total_addons_charges
      }
    }
  }
`;

// -----------------------------------------------------------
// Organization Management Queries
// -----------------------------------------------------------
export const GET_ORGANIZATION_DETAILS = gql`
  query GetOrganizationDetails($id: String!, $usageFilter: OrgUsageFilter) {
    account(id: $id) {
      id
      name
      slug
      is_active
      created
      modified

      # Member details
      members {
        email
        is_admin
        roles
        is_owner
        full_name
        last_login
        user_id
      }

      usage(filter: $usageFilter) {
        members
        total_requests
        total_errors
        order_volume
        total_shipments
        total_shipping_spend
        unfulfilled_orders
        total_trackers
        total_addons_charges

        # Time-series data for charts
        api_requests {
          date
          count
          label
        }
        api_errors {
          date
          count
          label
        }
        shipping_spend {
          date
          count
          label
        }
        shipment_count {
          date
          count
          label
        }
        tracker_count {
          date
          count
          label
        }
        order_volumes {
          date
          count
          label
        }
      }
    }
  }
`;

export const GET_ORGANIZATIONS = gql`
  query GetOrganizations($filter: AccountFilter) {
    accounts(filter: $filter) {
      edges {
        node {
          id
          name
          slug
          is_active
          created
          modified
          usage {
            members
            total_shipments
            total_trackers
            total_requests
            total_shipping_spend
            total_addons_charges
            total_errors
            order_volume
            unfulfilled_orders
          }
        }
        cursor
      }
      page_info {
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
    }
  }
`;

// -----------------------------------------------------------
// Carrier Connections (Account level)
// -----------------------------------------------------------
export const GET_CARRIER_CONNECTIONS = gql`
  query GetCarrierConnections($filter: AccountCarrierConnectionFilter) {
    carrier_connections(filter: $filter) {
      edges {
        node {
          id
          carrier_id
          carrier_name
          display_name
          active
          capabilities
          config
          test_mode
          usage {
            total_shipments
            total_trackers
            total_shipping_spend
            total_addons_charges
          }
        }
      }
      page_info {
        count
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
    }
  }
`;

export const GET_CARRIER_CONNECTION = gql`
  query GetCarrierConnection($id: String!) {
    carrier_connection(id: $id) {
      id
      carrier_id
      carrier_name
      display_name
      active
      capabilities
      config
      test_mode
      usage {
        total_shipments
        total_trackers
        total_shipping_spend
        total_addons_charges
      }
    }
  }
`;

export const GET_ACCOUNT_CARRIER_CONNECTIONS = gql`
  query GetAccountCarrierConnections($filter: AccountCarrierConnectionFilter, $usageFilter: UsageFilter) {
    carrier_connections(filter: $filter) {
      edges {
        node {
          id
          carrier_id
          carrier_name
          display_name
          active
          test_mode
          capabilities
          config
          created_at
          updated_at
          usage(filter: $usageFilter) {
            total_shipments
            total_trackers
            total_shipping_spend
            total_addons_charges
          }
        }
      }
      page_info {
        count
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
    }
  }
`;

// -----------------------------------------------------------
// Markup Mutations
// -----------------------------------------------------------
export const CREATE_MARKUP = gql`
  mutation CreateMarkup($input: CreateMarkupMutationInput!) {
    create_markup(input: $input) {
      errors {
        field
        messages
      }
      markup {
        id
        name
        active
        amount
        markup_type
        is_visible
        carrier_codes
        service_codes
        connection_ids
        metadata
      }
    }
  }
`;

export const UPDATE_MARKUP = gql`
  mutation UpdateMarkup($input: UpdateMarkupMutationInput!) {
    update_markup(input: $input) {
      errors {
        field
        messages
      }
      markup {
        id
        name
        active
        amount
        markup_type
        is_visible
        carrier_codes
        service_codes
        connection_ids
        metadata
      }
    }
  }
`;

export const DELETE_MARKUP = gql`
  mutation DeleteMarkup($input: DeleteMutationInput!) {
    delete_markup(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;

// -----------------------------------------------------------
// Organization Management Mutations
// -----------------------------------------------------------
export const CREATE_ORGANIZATION_ACCOUNT = gql`
  mutation CreateOrganizationAccount(
    $input: CreateOrganizationAccountMutationInput!
  ) {
    create_organization_account(input: $input) {
      account {
        id
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_ORGANIZATION_ACCOUNT = gql`
  mutation UpdateOrganizationAccount(
    $input: UpdateOrganizationAccountMutationInput!
  ) {
    update_organization_account(input: $input) {
      account {
        id
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const DISABLE_ORGANIZATION_ACCOUNT = gql`
  mutation DisableOrganizationAccount(
    $input: DisableOrganizationAccountMutationInput!
  ) {
    disable_organization_account(input: $input) {
      account {
        id
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const DELETE_ORGANIZATION_ACCOUNT = gql`
  mutation DeleteOrganizationAccount(
    $input: DeleteOrganizationAccountMutationInput!
  ) {
    delete_organization_account(input: $input) {
      account_id
      errors {
        field
        messages
      }
    }
  }
`;

export const INVITE_ORGANIZATION_USER = gql`
  mutation InviteOrganizationUser(
    $input: InviteOrganizationUserMutationInput!
  ) {
    invite_organization_user(input: $input) {
      account {
        id
      }
      errors {
        field
        messages
      }
    }
  }
`;
