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
      __typename
      ... on AlliedExpressSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        username
        password
        account
        service_type
      }
      ... on AlliedExpressLocalSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        username
        password
        account
        service_type
      }
      ... on AmazonShippingSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        seller_id
        developer_id
        mws_auth_token
        aws_region
        config
      }
      ... on AramexSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        username
        password
        account_pin
        account_entity
        account_number
        account_country_code
        config
      }
      ... on AsendiaUSSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        username
        password
        account_number
        api_key
        config
      }
      ... on AustraliaPostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        api_key
        password
        account_number
        config
      }
      ... on BoxKnightSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        username
        password
        config
        metadata
      }
      ... on BelgianPostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        account_id
        passphrase
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on CanadaPostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        username
        password
        customer_number
        contract_id
        config
      }
      ... on CanparSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        config
      }
      ... on ChronopostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        password
        account_number
        account_country_code
        config
      }
      ... on ColissimoSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        password
        contract_number
        laposte_api_key
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on DHLParcelDESettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        customer_number
        dhl_api_key
        tracking_consumer_key
        tracking_consumer_secret
        config
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on DHLExpressSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        site_id
        password
        account_number
        account_country_code
        config
      }
      ... on DHLPolandSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        username
        password
        account_number
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on DHLUniversalSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        consumer_key
        consumer_secret
        config
      }
      ... on DicomSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        billing_account
        config
      }
      ... on DPDSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        config
        capabilities
        delis_id
        password
        depot
        account_country_code
        services {
          active
          currency
          description
          dimension_unit
          domicile
          id
          international
          max_height
          max_length
          max_weight
          max_width
          service_code
          service_name
          carrier_service_code
          transit_days
          transit_time
          weight_unit
          zones {
            cities
            postal_codes
            country_codes
            label
            latitude
            longitude
            max_weight
            min_weight
            radius
            rate
            transit_days
            transit_time
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on DPDHLSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        app_id
        app_token
        zt_id
        zt_password
        account_number
        config
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on EShipperSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        principal
        credential
        config
      }
      ... on EasyPostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        config
      }
      ... on FedexSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        account_number
        api_key
        secret_key
        track_api_key
        track_secret_key
        account_country_code
        config
      }
      ... on FedexWSSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        account_number
        password
        meter_number
        user_key
        account_country_code
        config
      }
      ... on FreightcomSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        config
      }
      ... on GenericSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        custom_carrier_name
        account_number
        test_mode
        active
        metadata
        config
        capabilities
        account_country_code
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        label_template {
          id
          slug
          template
          template_type
          shipment_sample
          width
          height
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on GEODISSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        identifier
        language
        config
      }
      ... on LaPosteSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        lang
        config
      }
      ... on Locate2uSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        account_country_code
        client_id
        client_secret
      }
      ... on NationexSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        customer_id
        billing_account
        language
        config
      }
      ... on PurolatorSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        account_number
        user_token
        config
      }
      ... on RoadieSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        config
      }
      ... on RoyalMailSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        client_id
        client_secret
        config
      }
      ... on SendleSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        sendle_id
        api_key
        account_country_code
        config
      }
      ... on TGESettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        config
        capabilities
        username
        password
        api_key
        toll_username
        toll_password
        my_toll_token
        my_toll_identity
        account_code
      }
      ... on TNTSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        account_number
        account_country_code
        config
      }
      ... on UPSSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        client_id
        client_secret
        account_number
        account_country_code
        config
      }
      ... on USPSSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        mailer_id
        customer_registration_id
        logistics_manager_mailer_id
        config
      }
      ... on USPSInternationalSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        mailer_id
        customer_registration_id
        logistics_manager_mailer_id
        config
      }
      ... on Zoom2uSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        account_country_code
        api_key
      }
    }
  }
`;

export const GET_SYSTEM_CONNECTION = gql`
  query GetSystemConnection($id: String!) {
    system_connection(id: $id) {
      __typename
      ... on AlliedExpressSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        username
        password
        account
        service_type
      }
      ... on AlliedExpressLocalSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        username
        password
        account
        service_type
      }
      ... on AmazonShippingSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        seller_id
        developer_id
        mws_auth_token
        aws_region
        config
      }
      ... on AramexSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        username
        password
        account_pin
        account_entity
        account_number
        account_country_code
        config
      }
      ... on AsendiaUSSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        username
        password
        account_number
        api_key
        config
      }
      ... on AustraliaPostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        api_key
        password
        account_number
        config
      }
      ... on BoxKnightSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        username
        password
        config
        metadata
      }
      ... on BelgianPostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        account_id
        passphrase
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on CanadaPostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        username
        password
        customer_number
        contract_id
        config
      }
      ... on CanparSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        config
      }
      ... on ChronopostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        password
        account_number
        account_country_code
        config
      }
      ... on ColissimoSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        password
        contract_number
        laposte_api_key
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on DHLParcelDESettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        customer_number
        dhl_api_key
        tracking_consumer_key
        tracking_consumer_secret
        config
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on DHLExpressSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        site_id
        password
        account_number
        account_country_code
        config
      }
      ... on DHLPolandSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        username
        password
        account_number
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on DHLUniversalSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        consumer_key
        consumer_secret
        config
      }
      ... on DicomSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        billing_account
        config
      }
      ... on DPDSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        config
        capabilities
        delis_id
        password
        depot
        account_country_code
        services {
          active
          currency
          description
          dimension_unit
          domicile
          id
          international
          max_height
          max_length
          max_weight
          max_width
          service_code
          service_name
          carrier_service_code
          transit_days
          transit_time
          weight_unit
          zones {
            cities
            postal_codes
            country_codes
            label
            latitude
            longitude
            max_weight
            min_weight
            radius
            rate
            transit_days
            transit_time
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on DPDHLSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        app_id
        app_token
        zt_id
        zt_password
        account_number
        config
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on EShipperSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        principal
        credential
        config
      }
      ... on EasyPostSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        config
      }
      ... on FedexSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        account_number
        api_key
        secret_key
        track_api_key
        track_secret_key
        account_country_code
        config
      }
      ... on FedexWSSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        account_number
        password
        meter_number
        user_key
        account_country_code
        config
      }
      ... on FreightcomSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        config
      }
      ... on GenericSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        custom_carrier_name
        account_number
        test_mode
        active
        metadata
        config
        capabilities
        account_country_code
        services {
          id
          active
          service_name
          service_code
          carrier_service_code
          description
          currency
          transit_days
          transit_time
          max_weight
          max_width
          max_height
          max_length
          weight_unit
          dimension_unit
          domicile
          international
          zones {
            label
            rate
            min_weight
            max_weight
            transit_days
            transit_time
            radius
            latitude
            longitude
            cities
            postal_codes
            country_codes
          }
        }
        label_template {
          id
          slug
          template
          template_type
          shipment_sample
          width
          height
        }
        rate_sheet {
          id
          name
          slug
          carrier_name
          metadata
        }
      }
      ... on GEODISSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        identifier
        language
        config
      }
      ... on LaPosteSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        lang
        config
      }
      ... on Locate2uSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        account_country_code
        client_id
        client_secret
      }
      ... on NationexSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        customer_id
        billing_account
        language
        config
      }
      ... on PurolatorSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        account_number
        user_token
        config
      }
      ... on RoadieSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        api_key
        config
      }
      ... on RoyalMailSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        client_id
        client_secret
        config
      }
      ... on SendleSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        sendle_id
        api_key
        account_country_code
        config
      }
      ... on TGESettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        config
        capabilities
        username
        password
        api_key
        toll_username
        toll_password
        my_toll_token
        my_toll_identity
        account_code
      }
      ... on TNTSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        account_number
        account_country_code
        config
      }
      ... on UPSSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        client_id
        client_secret
        account_number
        account_country_code
        config
      }
      ... on USPSSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        mailer_id
        customer_registration_id
        logistics_manager_mailer_id
        config
      }
      ... on USPSInternationalSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        metadata
        capabilities
        username
        password
        mailer_id
        customer_registration_id
        logistics_manager_mailer_id
        config
      }
      ... on Zoom2uSettingsType {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        metadata
        config
        account_country_code
        api_key
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
