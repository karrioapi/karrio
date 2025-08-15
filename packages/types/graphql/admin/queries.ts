import gql from "graphql-tag";

// -----------------------------------------------------------
// User Management Queries
// -----------------------------------------------------------
export const GET_USERS = gql`
  query GetUsers($filter: UserFilter) {
    users(filter: $filter) {
      edges {
        node {
          id
          email
          full_name
          is_staff
          is_active
          last_login
          date_joined
          permissions
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

export const GET_USER = gql`
  query GetUser($email: String!) {
    user(email: $email) {
      id
      email
      full_name
      is_staff
      is_active
      last_login
      date_joined
      permissions
    }
  }
`;

export const GET_PERMISSION_GROUPS = gql`
  query GetPermissionGroups {
    permission_groups {
      edges {
        node {
          id
          name
        }
      }
    }
  }
`;

// -----------------------------------------------------------
// System Configuration Queries
// -----------------------------------------------------------
export const GET_CONFIGS = gql`
  query GetConfigs {
    configs {
      APP_NAME
      APP_WEBSITE
      EMAIL_USE_TLS
      EMAIL_HOST_USER
      EMAIL_HOST_PASSWORD
      EMAIL_HOST
      EMAIL_PORT
      EMAIL_FROM_ADDRESS
      GOOGLE_CLOUD_API_KEY
      CANADAPOST_ADDRESS_COMPLETE_API_KEY
      ORDER_DATA_RETENTION
      TRACKER_DATA_RETENTION
      SHIPMENT_DATA_RETENTION
      API_LOGS_DATA_RETENTION
      AUDIT_LOGGING
      ALLOW_SIGNUP
      ALLOW_ADMIN_APPROVED_SIGNUP
      ALLOW_MULTI_ACCOUNT
      ADMIN_DASHBOARD
      MULTI_ORGANIZATIONS
      ORDERS_MANAGEMENT
      APPS_MANAGEMENT
      DOCUMENTS_MANAGEMENT
      DATA_IMPORT_EXPORT
      WORKFLOW_MANAGEMENT
      SHIPPING_RULES
      PERSIST_SDK_TRACING
    }
  }
`;

export const GET_ADMIN_SYSTEM_USAGE = gql`
  query GetAdminSystemUsage($filter: UsageFilter) {
    usage(filter: $filter) {
      total_requests
      total_trackers
      total_shipments
      total_shipping_spend
      total_errors
      order_volume
      organization_count
      user_count
      total_addons_charges
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
      shipping_spend {
        date
        count
        label
      }
      addons_charges {
        date
        amount
      }
    }
  }
`;

// -----------------------------------------------------------
// System Carrier Connections Queries
// -----------------------------------------------------------
export const GET_SYSTEM_CONNECTIONS = gql`
  query GetSystemConnections($filter: CarrierFilter, $usageFilter: UsageFilter) {
    system_carrier_connections(filter: $filter) {
      edges {
        node {
          id
          carrier_id
          carrier_name
          display_name
          active
          capabilities
          credentials
          config
          metadata
          test_mode
          usage(filter: $usageFilter) {
            total_trackers
            total_shipments
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

export const GET_SYSTEM_CONNECTION = gql`
  query GetSystemConnection($id: String!) {
    system_carrier_connection(id: $id) {
      id
      carrier_id
      carrier_name
      display_name
      active
      capabilities
      credentials
      config
      metadata
      test_mode
    }
  }
`;

// -----------------------------------------------------------
// Rate Sheets Queries
// -----------------------------------------------------------
export const GET_RATE_SHEETS = gql`
  query GetRateSheets($filter: RateSheetFilter) {
    rate_sheets(filter: $filter) {
      edges {
        node {
          id
          name
          slug
          carrier_name
          metadata
          services {
            id
            service_name
            service_code
            zones {
              label
              rate
              min_weight
              max_weight
            }
          }
          carriers {
            id
            carrier_name
            active
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

export const GET_RATE_SHEET = gql`
  query GetRateSheet($id: String!) {
    rate_sheet(id: $id) {
      id
      name
      slug
      carrier_name
      metadata
      services {
        id
        service_name
        service_code
        zones {
          label
          rate
          min_weight
          max_weight
        }
      }
      carriers {
        id
        carrier_name
        active
      }
    }
  }
`;

// -----------------------------------------------------------
// Addons Queries
// -----------------------------------------------------------
export const GET_ADDONS = gql`
  query GetAddons($filter: AddonFilter, $usageFilter: UsageFilter) {
    addons(filter: $filter) {
      edges {
        node {
          id
          name
          active
          amount
          surcharge_type
          carriers
          services
          carrier_accounts {
            id
            usage {
              total_shipments
              total_addons_charges
            }
          }
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

export const GET_ADDON = gql`
  query GetAddon($id: String!) {
    addon(id: $id) {
      id
      name
      active
      amount
      surcharge_type
      carriers
      services
      carrier_accounts {
        id
        usage {
          total_shipments
          total_addons_charges
        }
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

// -----------------------------------------------------------
// System-wide Management Queries
// -----------------------------------------------------------
export const GET_SHIPMENTS = gql`
  query GetShipments($filter: SystemShipmentFilter) {
    shipments(filter: $filter) {
      edges {
        node {
          id
          tracking_number
          status
          carrier_name
          service
          created_at
          updated_at
          selected_rate {
            id
            service
            total_charge
            currency
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

export const GET_TRACKERS = gql`
  query GetTrackers($filter: SystemTrackerFilter) {
    trackers(filter: $filter) {
      edges {
        node {
          id
          tracking_number
          status
          carrier_name
          carrier_id
          created_at
          updated_at
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

export const GET_ORDERS = gql`
  query GetOrders($filter: SystemOrderFilter) {
    orders(filter: $filter) {
      edges {
        node {
          id
          order_id
          status
          created_at
          updated_at
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
// User Management Mutations
// -----------------------------------------------------------
export const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserMutationInput!) {
    create_user(input: $input) {
      errors {
        field
        messages
      }
      user {
        id
        email
        full_name
        is_staff
        is_active
        last_login
        date_joined
        permissions
      }
    }
  }
`;

export const UPDATE_USER = gql`
  mutation UpdateUser($input: UpdateUserMutationInput!) {
    update_user(input: $input) {
      errors {
        field
        messages
      }
      user {
        id
        email
        full_name
        is_staff
        is_active
        last_login
        date_joined
        permissions
      }
    }
  }
`;

export const REMOVE_USER = gql`
  mutation RemoveUser($input: DeleteUserMutationInput!) {
    remove_user(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;

// -----------------------------------------------------------
// System Configuration Mutations
// -----------------------------------------------------------
export const UPDATE_CONFIGS = gql`
  mutation UpdateConfigs($input: InstanceConfigMutationInput!) {
    update_configs(input: $input) {
      errors {
        field
        messages
      }
      configs {
        ALLOW_SIGNUP
        ALLOW_ADMIN_APPROVED_SIGNUP
        ALLOW_MULTI_ACCOUNT
        ADMIN_DASHBOARD
        AUDIT_LOGGING
        ORDERS_MANAGEMENT
        APPS_MANAGEMENT
        MULTI_ORGANIZATIONS
        PERSIST_SDK_TRACING
      }
    }
  }
`;

// -----------------------------------------------------------
// System Carrier Connection Mutations
// -----------------------------------------------------------
export const CREATE_SYSTEM_CONNECTION = gql`
  mutation CreateSystemConnection($input: CreateConnectionMutationInput!) {
    create_system_carrier_connection(input: $input) {
      errors {
        field
        messages
      }
      connection {
        id
        carrier_id
        carrier_name
        display_name
        active
        capabilities
        credentials
        config
        metadata
        test_mode
      }
    }
  }
`;

export const UPDATE_SYSTEM_CONNECTION = gql`
  mutation UpdateSystemConnection($input: UpdateConnectionMutationInput!) {
    update_system_carrier_connection(input: $input) {
      errors {
        field
        messages
      }
      connection {
        id
        carrier_id
        carrier_name
        display_name
        active
        capabilities
        credentials
        config
        metadata
        test_mode
      }
    }
  }
`;

export const DELETE_SYSTEM_CONNECTION = gql`
  mutation DeleteSystemConnection($input: DeleteConnectionMutationInput!) {
    delete_system_carrier_connection(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;

// -----------------------------------------------------------
// Rate Sheet Mutations
// -----------------------------------------------------------
export const CREATE_RATE_SHEET = gql`
  mutation CreateRateSheet($input: CreateRateSheetMutationInput!) {
    create_rate_sheet(input: $input) {
      errors {
        field
        messages
      }
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

export const UPDATE_RATE_SHEET = gql`
  mutation UpdateRateSheet($input: UpdateRateSheetMutationInput!) {
    update_rate_sheet(input: $input) {
      errors {
        field
        messages
      }
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

export const DELETE_RATE_SHEET = gql`
  mutation DeleteRateSheet($input: DeleteMutationInput!) {
    delete_rate_sheet(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;

export const UPDATE_RATE_SHEET_ZONE_CELL = gql`
  mutation UpdateRateSheetZoneCell($input: UpdateRateSheetZoneCellMutationInput!) {
    update_rate_sheet_zone_cell(input: $input) {
      errors {
        field
        messages
      }
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

export const BATCH_UPDATE_RATE_SHEET_CELLS = gql`
  mutation BatchUpdateRateSheetCells($input: BatchUpdateRateSheetCellsMutationInput!) {
    batch_update_rate_sheet_cells(input: $input) {
      errors {
        field
        messages
      }
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

export const DELETE_RATE_SHEET_SERVICE = gql`
  mutation DeleteRateSheetService($input: DeleteRateSheetServiceMutationInput!) {
    delete_rate_sheet_service(input: $input) {
      errors {
        field
        messages
      }
    }
  }
`;

// -----------------------------------------------------------
// Addon Mutations
// -----------------------------------------------------------
export const CREATE_ADDON = gql`
  mutation CreateAddon($input: CreateAddonMutationInput!) {
    create_addon(input: $input) {
      errors {
        field
        messages
      }
      addon {
        id
        name
        active
        amount
        surcharge_type
        carriers
        services
      }
    }
  }
`;

export const UPDATE_ADDON = gql`
  mutation UpdateAddon($input: UpdateAddonMutationInput!) {
    update_addon(input: $input) {
      errors {
        field
        messages
      }
      addon {
        id
        name
        active
        amount
        surcharge_type
        carriers
        services
      }
    }
  }
`;

export const DELETE_ADDON = gql`
  mutation DeleteAddon($input: DeleteMutationInput!) {
    delete_addon(input: $input) {
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

// -----------------------------------------------------------
// System Shipments and Trackers Queries
// -----------------------------------------------------------
export const GET_SYSTEM_SHIPMENTS = gql`
  query GetSystemShipments($filter: SystemShipmentFilter) {
    shipments(filter: $filter) {
      edges {
        node {
          id
          tracking_number
          recipient {
            company_name
            person_name
            address_line1
            city
            state_code
            postal_code
            country_code
          }
          shipper {
            company_name
            person_name
            address_line1
            city
            state_code
            postal_code
            country_code
          }
          status
          service
          carrier_name
          carrier_id
          created_at
          updated_at
          test_mode
          meta
          options
          selected_rate {
            carrier_name
            carrier_id
            service
            total_charge
            currency
          }
          parcels {
            id
            weight
            width
            height
            length
            packaging_type
          }
          messages {
            carrier_name
            carrier_id
            message
            code
            details
          }
          tracker {
            id
            tracking_number
            events {
              code
              date
              description
              location
              time
            }
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

export const GET_SYSTEM_TRACKERS = gql`
  query GetSystemTrackers($filter: SystemTrackerFilter) {
    trackers(filter: $filter) {
      edges {
        node {
          id
          tracking_number
          carrier_name
          carrier_id
          status
          delivered
          test_mode
          created_at
          updated_at
          info {
            customer_name
            expected_delivery
            note
            order_date
            order_id
            package_weight
            shipment_package_count
            shipment_pickup_date
            shipment_delivery_date
            shipment_service
            shipment_origin_country
            shipment_origin_postal_code
            shipment_destination_country
            shipment_destination_postal_code
          }
          meta
          messages {
            carrier_name
            carrier_id
            message
            code
            details
          }
          events {
            code
            date
            description
            location
            time
          }
          shipment {
            id
            service
            status
            meta
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
