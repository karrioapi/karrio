import gql from "graphql-tag";

// -----------------------------------------------------------
// Admin GraphQL Queries
// -----------------------------------------------------------
//#region

export const GET_SYSTEM_USAGE = gql`
  query GetSystemUsage($filter: UsageFilter) {
    system_usage(filter: $filter) {
      total_errors
      order_volume
      total_requests
      total_trackers
      total_shipments
      organization_count
      total_shipping_spend
      api_errors {
        label
        count
        date
      }
      api_requests {
        label
        count
        date
      }
      order_volumes {
        label
        count
        date
      }
      shipment_count {
        label
        count
        date
      }
      tracker_count {
        label
        count
        date
      }
      shipping_spend {
        label
        count
        date
      }
    }
  }
`;

export const GET_ACCOUNTS = gql`
  query GetAccounts($filter: AccountFilter) {
    accounts(filter: $filter) {
      page_info {
        count
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
          is_active
          created
          modified
          usage {
            members
            order_volume
            total_errors
            total_requests
            total_trackers
            total_shipments
            total_shipping_spend
            api_errors {
              label
              count
              date
            }
            api_requests {
              label
              count
              date
            }
            order_volumes {
              label
              count
              date
            }
            shipment_count {
              label
              count
              date
            }
            tracker_count {
              label
              count
              date
            }
            shipping_spend {
              label
              count
              date
            }
          }
        }
      }
    }
  }
`;

export const GET_USERS = gql`
  query GetUsers($filter: UserFilter) {
    users(filter: $filter) {
      page_info {
        count
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
      edges {
        node {
          id
          email
          full_name
          is_staff
          is_active
          is_superuser
          date_joined
          last_login
          permissions
        }
      }
    }
  }
`;

export const GET_SURCHARGES = gql`
  query GetSurcharges($filter: SurchargeFilter) {
    surcharges(filter: $filter) {
      object_type
      id
      name
      active
      amount
      carriers
      services
      surcharge_type
      carrier_accounts {
        id
        active
        carrier_id
        test_mode
        capabilities
        carrier_name
        display_name
      }
    }
  }
`;

export const GET_SURCHARGE = gql`
  query GetSurcharge($id: String!) {
    surcharge(id: $id) {
      object_type
      id
      name
      active
      amount
      carriers
      services
      surcharge_type
      carrier_accounts {
        id
        active
        carrier_id
        test_mode
        capabilities
        carrier_name
        display_name
      }
    }
  }
`;

export const GET_SYSTEM_CONNECTIONS = gql`
  query GetSystemConnections {
    system_connections {
      id
      carrier_id
      carrier_name
      display_name
      test_mode
      active
      capabilities
      credentials
      metadata
      config
      rate_sheet {
        id
        name
        slug
        carrier_name
        metadata
      }
    }
  }
`;

export const GET_SYSTEM_CONNECTION = gql`
  query GetSystemConnection($id: String!) {
    system_connection(id: $id) {
      id
      carrier_id
      carrier_name
      display_name
      test_mode
      active
      capabilities
      credentials
      metadata
      config
      rate_sheet {
        id
        name
        slug
        carrier_name
        metadata
      }
    }
  }
`;

export const GET_RATE_SHEET = gql`
  query GetRateSheet($id: String!) {
    rate_sheet(id: $id) {
      id
      name
      slug
      carrier_name
      services {
        id
        object_type
        service_name
        service_code
        description
        active
        currency
        transit_days
        transit_time
        max_width
        max_height
        max_length
        dimension_unit
        zones {
          object_type
          label
          rate
          min_weight
          max_weight
          transit_days
        }
      }
      carriers {
        id
        active
        carrier_id
        carrier_name
        display_name
        capabilities
        test_mode
      }
    }
  }
`;

export const GET_RATE_SHEETS = gql`
  query GetRateSheets($filter: RateSheetFilter) {
    rate_sheets(filter: $filter) {
      page_info {
        count
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
          carrier_name
          services {
            id
            service_name
            service_code
            description
            active
            currency
            transit_days
            transit_time
            max_width
            max_height
            max_length
            dimension_unit
            zones {
              label
              rate
              min_weight
              max_weight
              transit_days
            }
          }
          carriers {
            id
            active
            carrier_id
            carrier_name
            display_name
            capabilities
            test_mode
          }
        }
      }
    }
  }
`;

export const GET_GROUP_PERMISSIONS = gql`
  query GetPermissionGroups($filter: PermissionGroupFilter) {
    permission_groups(filter: $filter) {
      page_info {
        count
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
      edges {
        node {
          id
          name
          permissions
        }
      }
    }
  }
`;

//#endregion

// -----------------------------------------------------------
// Admin GraphQL Mutations
// -----------------------------------------------------------
//#region

export const CREATE_USER = gql`
  mutation CreateUser($data: CreateUserMutationInput!) {
    create_user(input: $data) {
      errors {
        field
        messages
      }
      user {
        email
        full_name
        is_staff
        is_active
        is_superuser
        date_joined
        last_login
      }
    }
  }
`;

export const UPDATE_USER = gql`
  mutation UpdateUser($data: UpdateUserMutationInput!) {
    update_user(input: $data) {
      errors {
        field
        messages
      }
    }
  }
`;

export const REMOVE_USER = gql`
  mutation RemoveUser($data: DeleteUserMutationInput!) {
    remove_user(input: $data) {
      id
      errors {
        field
        messages
      }
    }
  }
`;

export const CREATE_SURCHARGE = gql`
  mutation CreateSurcharge($data: CreateSurchargeMutationInput!) {
    create_surcharge(input: $data) {
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_SURCHARGE = gql`
  mutation UpdateSurcharge($data: UpdateSurchargeMutationInput!) {
    update_surcharge(input: $data) {
      errors {
        field
        messages
      }
    }
  }
`;

export const DELETE_SURCHARGE = gql`
  mutation DeleteSurcharge($data: DeleteMutationInput!) {
    delete_surcharge(input: $data) {
      id
      errors {
        field
        messages
      }
    }
  }
`;

export const CREATE_CARRIER_CONNECTION = gql`
  mutation CreateCarrierConnection($data: CreateConnectionMutationInput!) {
    create_carrier_connection(input: $data) {
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_CARRIER_CONNECTION = gql`
  mutation UpdateCarrierConnection($data: UpdateConnectionMutationInput!) {
    update_carrier_connection(input: $data) {
      errors {
        field
        messages
      }
    }
  }
`;

export const DELETE_CARRIER_CONNECTION = gql`
  mutation DeleteCarrierConnection($data: DeleteConnectionMutationInput!) {
    delete_carrier_connection(input: $data) {
      id
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_ORGANIZATION_ACCOUNT = gql`
  mutation UpdateOrganizationAccount(
    $data: UpdateOrganizationAccountMutationInput!
  ) {
    update_organization_account(input: $data) {
      errors {
        field
        messages
      }
    }
  }
`;

export const CREATE_RATE_SHEET = gql`
  mutation CreateRateSheet($data: CreateRateSheetMutationInput!) {
    create_rate_sheet(input: $data) {
      rate_sheet {
        id
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_RATE_SHEET = gql`
  mutation UpdateRateSheet($data: UpdateRateSheetMutationInput!) {
    update_rate_sheet(input: $data) {
      rate_sheet {
        id
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const DELETE_RATE_SHEET = gql`
  mutation DeleteRateSheet($data: DeleteMutationInput!) {
    delete_rate_sheet(input: $data) {
      id
      errors {
        field
        messages
      }
    }
  }
`;

//#endregion
