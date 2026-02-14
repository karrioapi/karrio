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
          is_superuser
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
      is_superuser
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
// Config Fieldsets & Schema Queries
// -----------------------------------------------------------
export const GET_CONFIG_FIELDSETS = gql`
  query get_config_fieldsets {
    config_fieldsets {
      name
      keys
    }
  }
`;

export const GET_CONFIG_SCHEMA = gql`
  query get_config_schema {
    config_schema {
      key
      description
      value_type
      default_value
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
          rate_sheet {
            id
          }
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
      rate_sheet {
        id
      }
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
          origin_countries
          metadata
          zones {
            id
            label
            country_codes
            postal_codes
            cities
            transit_days
            transit_time
          }
          surcharges {
            id
            name
            amount
            surcharge_type
            cost
            active
          }
          service_rates {
            service_id
            zone_id
            rate
            cost
            min_weight
            max_weight
            transit_days
            transit_time
          }
          services {
            id
            service_name
            service_code
            currency
            transit_days
            transit_time
            max_width
            max_height
            max_length
            dimension_unit
            max_weight
            weight_unit
            active
            dim_factor
            use_volumetric
            zone_ids
            surcharge_ids
            features {
              first_mile
              last_mile
              form_factor
              b2c
              b2b
              shipment_type
              age_check
              signature
              tracked
              insurance
              express
              dangerous_goods
              saturday_delivery
              sunday_delivery
              multicollo
              neighbor_delivery
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
      origin_countries
      metadata
      zones {
        id
        label
        country_codes
        postal_codes
        cities
        transit_days
        transit_time
        radius
        latitude
        longitude
      }
      surcharges {
        id
        name
        amount
        surcharge_type
        cost
        active
      }
      service_rates {
        service_id
        zone_id
        rate
        cost
        min_weight
        max_weight
        transit_days
        transit_time
      }
      services {
        id
        object_type
        service_name
        service_code
        carrier_service_code
        description
        active
        currency
        transit_days
        transit_time
        max_width
        max_height
        max_length
        dimension_unit
        max_weight
        weight_unit
        dim_factor
        use_volumetric
        domicile
        international
        zone_ids
        surcharge_ids
        features {
          first_mile
          last_mile
          form_factor
          b2c
          b2b
          shipment_type
          age_check
          signature
          tracked
          insurance
          express
          dangerous_goods
          saturday_delivery
          sunday_delivery
          multicollo
          neighbor_delivery
        }
      }
      carriers {
        id
        carrier_name
        active
        carrier_id
        display_name
        capabilities
        test_mode
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
// Shared Zone Mutations
// -----------------------------------------------------------

export const ADD_SHARED_ZONE = gql`
  mutation AddSharedZone($input: AddSharedZoneMutationInput!) {
    add_shared_zone(input: $input) {
      rate_sheet {
        id
        zones {
          id
          label
          country_codes
          postal_codes
          cities
          transit_days
          transit_time
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_SHARED_ZONE = gql`
  mutation UpdateSharedZone($input: UpdateSharedZoneMutationInput!) {
    update_shared_zone(input: $input) {
      rate_sheet {
        id
        zones {
          id
          label
          country_codes
          postal_codes
          cities
          transit_days
          transit_time
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const DELETE_SHARED_ZONE = gql`
  mutation DeleteSharedZone($input: DeleteSharedZoneMutationInput!) {
    delete_shared_zone(input: $input) {
      rate_sheet {
        id
        zones {
          id
          label
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

// -----------------------------------------------------------
// Shared Surcharge Mutations
// -----------------------------------------------------------

export const ADD_SHARED_SURCHARGE = gql`
  mutation AddSharedSurcharge($input: AddSharedSurchargeMutationInput!) {
    add_shared_surcharge(input: $input) {
      rate_sheet {
        id
        surcharges {
          id
          name
          amount
          surcharge_type
          cost
          active
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_SHARED_SURCHARGE = gql`
  mutation UpdateSharedSurcharge($input: UpdateSharedSurchargeMutationInput!) {
    update_shared_surcharge(input: $input) {
      rate_sheet {
        id
        surcharges {
          id
          name
          amount
          surcharge_type
          cost
          active
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const DELETE_SHARED_SURCHARGE = gql`
  mutation DeleteSharedSurcharge($input: DeleteSharedSurchargeMutationInput!) {
    delete_shared_surcharge(input: $input) {
      rate_sheet {
        id
        surcharges {
          id
          name
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const BATCH_UPDATE_SURCHARGES = gql`
  mutation BatchUpdateSurcharges($input: BatchUpdateSurchargesMutationInput!) {
    batch_update_surcharges(input: $input) {
      rate_sheet {
        id
        surcharges {
          id
          name
          amount
          surcharge_type
          cost
          active
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

// -----------------------------------------------------------
// Service Rate Mutations
// -----------------------------------------------------------

export const UPDATE_SERVICE_RATE = gql`
  mutation UpdateServiceRate($input: UpdateServiceRateMutationInput!) {
    update_service_rate(input: $input) {
      rate_sheet {
        id
        service_rates {
          service_id
          zone_id
          rate
          cost
          min_weight
          max_weight
          transit_days
          transit_time
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const BATCH_UPDATE_SERVICE_RATES = gql`
  mutation BatchUpdateServiceRates($input: BatchUpdateServiceRatesMutationInput!) {
    batch_update_service_rates(input: $input) {
      rate_sheet {
        id
        service_rates {
          service_id
          zone_id
          rate
          cost
          min_weight
          max_weight
          transit_days
          transit_time
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

// -----------------------------------------------------------
// Weight Range Mutations
// -----------------------------------------------------------

export const ADD_WEIGHT_RANGE = gql`
  mutation AddWeightRange($input: AddWeightRangeMutationInput!) {
    add_weight_range(input: $input) {
      rate_sheet {
        id
        service_rates {
          service_id
          zone_id
          rate
          cost
          min_weight
          max_weight
          transit_days
          transit_time
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const REMOVE_WEIGHT_RANGE = gql`
  mutation RemoveWeightRange($input: RemoveWeightRangeMutationInput!) {
    remove_weight_range(input: $input) {
      rate_sheet {
        id
        service_rates {
          service_id
          zone_id
          rate
          cost
          min_weight
          max_weight
          transit_days
          transit_time
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const DELETE_SERVICE_RATE = gql`
  mutation DeleteServiceRate($input: DeleteServiceRateMutationInput!) {
    delete_service_rate(input: $input) {
      rate_sheet {
        id
        service_rates {
          service_id
          zone_id
          rate
          cost
          min_weight
          max_weight
          transit_days
          transit_time
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

// -----------------------------------------------------------
// Service Zone/Surcharge Assignment Mutations
// -----------------------------------------------------------

export const UPDATE_SERVICE_ZONE_IDS = gql`
  mutation UpdateServiceZoneIds($input: UpdateServiceZoneIdsMutationInput!) {
    update_service_zone_ids(input: $input) {
      rate_sheet {
        id
        services {
          id
          zone_ids
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_SERVICE_SURCHARGE_IDS = gql`
  mutation UpdateServiceSurchargeIds($input: UpdateServiceSurchargeIdsMutationInput!) {
    update_service_surcharge_ids(input: $input) {
      rate_sheet {
        id
        services {
          id
          surcharge_ids
        }
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
          return_shipment {
            tracking_number
            shipment_identifier
            tracking_url
            service
            reference
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

// -----------------------------------------------------------
// Worker Monitoring Queries
// -----------------------------------------------------------
export const GET_TASK_EXECUTIONS = gql`
  query GetTaskExecutions($filter: TaskExecutionFilter) {
    task_executions(filter: $filter) {
      edges {
        node {
          id
          task_id
          task_name
          status
          queued_at
          started_at
          completed_at
          duration_ms
          error
          retries
          args_summary
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

export const GET_WORKER_HEALTH = gql`
  query GetWorkerHealth {
    worker_health {
      is_available
      queue {
        pending_count
        scheduled_count
        result_count
      }
    }
  }
`;

