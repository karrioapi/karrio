import{aS as i,t as o,s as c,y as A,Z as ge,bc as he,w as B,as as j,P,aG as W,v as N,x as S,bd as fe,be as ve,aI as ye,at as be,ar as Z,ay as Ee,az as xe,bf as Ce,E as Te,aE as Se,au as Re,aF as Ae}from"./globals-D8PkUKNZ.js";import{O as V,P as Ie,C as K,a as ke,T as X,D as Y,R as $e}from"./loader-circle-CPmrdKrG.js";i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;const pt=i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
  mutation RemoveUser($input: DeleteUserMutationInput!) {
    remove_user(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;i`
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
`;i`
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
`;i`
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
`;i`
  mutation DeleteSystemConnection($input: DeleteConnectionMutationInput!) {
    delete_system_carrier_connection(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;const mt=i`
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
`,gt=i`
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
`,ht=i`
  mutation DeleteRateSheet($input: DeleteMutationInput!) {
    delete_rate_sheet(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`,ft=i`
  mutation DeleteRateSheetService($input: DeleteRateSheetServiceMutationInput!) {
    delete_rate_sheet_service(input: $input) {
      errors {
        field
        messages
      }
    }
  }
`,vt=i`
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
`,yt=i`
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
`,bt=i`
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
`,Et=i`
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
`,xt=i`
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
`,Ct=i`
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
`,Tt=i`
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
`,St=i`
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
`,Rt=i`
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
`,At=i`
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
`,It=i`
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
`,kt=i`
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
`,$t=i`
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
`,Dt=i`
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
`;i`
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
`;i`
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
`;i`
  mutation DeleteMarkup($input: DeleteMutationInput!) {
    delete_markup(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;i`
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
`;const wt=$e,De=Ie,J=o.forwardRef(({className:e,...r},t)=>c.jsx(V,{className:A("fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",e),...r,ref:t}));J.displayName=V.displayName;const we=he("fixed z-50 gap-4 bg-background p-6 shadow-lg transition ease-in-out data-[state=closed]:duration-300 data-[state=open]:duration-500 data-[state=open]:animate-in data-[state=closed]:animate-out",{variants:{side:{top:"inset-x-0 top-0 border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top",bottom:"inset-x-0 bottom-0 border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom",left:"inset-y-0 left-0 h-full w-3/4 border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left sm:max-w-sm",right:"inset-y-0 right-0 h-full w-3/4 border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right sm:max-w-sm"}},defaultVariants:{side:"right"}}),Pe=o.forwardRef(({side:e="right",className:r,children:t,full:a=!1,hideCloseButton:s=!1,...n},u)=>c.jsxs(De,{children:[c.jsx(J,{}),c.jsxs(K,{ref:u,className:A(a?"fixed inset-0 z-50 bg-background p-0 shadow-lg transition ease-in-out data-[state=closed]:duration-300 data-[state=open]:duration-500 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right h-[100svh] w-screen max-w-none border-0":we({side:e}),r),...n,children:[!s&&c.jsxs(ke,{className:"absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-secondary",children:[c.jsx(ge,{className:"h-4 w-4"}),c.jsx("span",{className:"sr-only",children:"Close"})]}),t]})]}));Pe.displayName=K.displayName;const Ne=({className:e,...r})=>c.jsx("div",{className:A("flex flex-col space-y-2 text-center sm:text-left",e),...r});Ne.displayName="SheetHeader";const Me=o.forwardRef(({className:e,...r},t)=>c.jsx(X,{ref:t,className:A("text-lg font-semibold text-foreground",e),...r}));Me.displayName=X.displayName;const Oe=o.forwardRef(({className:e,...r},t)=>c.jsx(Y,{ref:t,className:A("text-sm text-muted-foreground",e),...r}));Oe.displayName=Y.displayName;var M="Checkbox",[Ue]=B(M),[Ge,z]=Ue(M);function Le(e){const{__scopeCheckbox:r,checked:t,children:a,defaultChecked:s,disabled:n,form:u,name:h,onCheckedChange:d,required:m,value:l="on",internal_do_not_use_render:_}=e,[g,p]=W({prop:t,defaultProp:s??!1,onChange:d,caller:M}),[y,b]=o.useState(null),[E,v]=o.useState(null),f=o.useRef(!1),x=y?!!u||!!y.closest("form"):!0,C={checked:g,disabled:n,setChecked:p,control:y,setControl:b,name:h,form:u,value:l,hasConsumerStoppedPropagationRef:f,required:m,defaultChecked:R(s)?!1:s,isFormControl:x,bubbleInput:E,setBubbleInput:v};return c.jsx(Ge,{scope:r,...C,children:je(_)?_(C):a})}var Q="CheckboxTrigger",ee=o.forwardRef(({__scopeCheckbox:e,onKeyDown:r,onClick:t,...a},s)=>{const{control:n,value:u,disabled:h,checked:d,required:m,setControl:l,setChecked:_,hasConsumerStoppedPropagationRef:g,isFormControl:p,bubbleInput:y}=z(Q,e),b=N(s,l),E=o.useRef(d);return o.useEffect(()=>{const v=n==null?void 0:n.form;if(v){const f=()=>_(E.current);return v.addEventListener("reset",f),()=>v.removeEventListener("reset",f)}},[n,_]),c.jsx(P.button,{type:"button",role:"checkbox","aria-checked":R(d)?"mixed":d,"aria-required":m,"data-state":ne(d),"data-disabled":h?"":void 0,disabled:h,value:u,...a,ref:b,onKeyDown:S(r,v=>{v.key==="Enter"&&v.preventDefault()}),onClick:S(t,v=>{_(f=>R(f)?!0:!f),y&&p&&(g.current=v.isPropagationStopped(),g.current||v.stopPropagation())})})});ee.displayName=Q;var H=o.forwardRef((e,r)=>{const{__scopeCheckbox:t,name:a,checked:s,defaultChecked:n,required:u,disabled:h,value:d,onCheckedChange:m,form:l,..._}=e;return c.jsx(Le,{__scopeCheckbox:t,checked:s,defaultChecked:n,disabled:h,required:u,onCheckedChange:m,name:a,form:l,value:d,internal_do_not_use_render:({isFormControl:g})=>c.jsxs(c.Fragment,{children:[c.jsx(ee,{..._,ref:r,__scopeCheckbox:t}),g&&c.jsx(se,{__scopeCheckbox:t})]})})});H.displayName=M;var te="CheckboxIndicator",re=o.forwardRef((e,r)=>{const{__scopeCheckbox:t,forceMount:a,...s}=e,n=z(te,t);return c.jsx(j,{present:a||R(n.checked)||n.checked===!0,children:c.jsx(P.span,{"data-state":ne(n.checked),"data-disabled":n.disabled?"":void 0,...s,ref:r,style:{pointerEvents:"none",...e.style}})})});re.displayName=te;var ae="CheckboxBubbleInput",se=o.forwardRef(({__scopeCheckbox:e,...r},t)=>{const{control:a,hasConsumerStoppedPropagationRef:s,checked:n,defaultChecked:u,required:h,disabled:d,name:m,value:l,form:_,bubbleInput:g,setBubbleInput:p}=z(ae,e),y=N(t,p),b=fe(n),E=ve(a);o.useEffect(()=>{const f=g;if(!f)return;const x=window.HTMLInputElement.prototype,T=Object.getOwnPropertyDescriptor(x,"checked").set,D=!s.current;if(b!==n&&T){const w=new Event("click",{bubbles:D});f.indeterminate=R(n),T.call(f,R(n)?!1:n),f.dispatchEvent(w)}},[g,b,n,s]);const v=o.useRef(R(n)?!1:n);return c.jsx(P.input,{type:"checkbox","aria-hidden":!0,defaultChecked:u??v.current,required:h,disabled:d,name:m,value:l,form:_,...r,tabIndex:-1,ref:y,style:{...r.style,...E,position:"absolute",pointerEvents:"none",opacity:0,margin:0,transform:"translateX(-100%)"}})});se.displayName=ae;function je(e){return typeof e=="function"}function R(e){return e==="indeterminate"}function ne(e){return R(e)?"indeterminate":e?"checked":"unchecked"}const ze=o.forwardRef(({className:e,...r},t)=>c.jsx(H,{ref:t,className:A("peer h-4 w-4 shrink-0 rounded-sm border border-primary shadow focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground",e),...r,children:c.jsx(re,{className:A("flex items-center justify-center text-current"),children:c.jsx(ye,{className:"h-4 w-4"})})}));ze.displayName=H.displayName;var He=Symbol("radix.slottable");function Fe(e){const r=({children:t})=>c.jsx(c.Fragment,{children:t});return r.displayName=`${e}.Slottable`,r.__radixId=He,r}var[O]=B("Tooltip",[Z]),U=Z(),ie="TooltipProvider",qe=700,G="tooltip.open",[Be,F]=O(ie),oe=e=>{const{__scopeTooltip:r,delayDuration:t=qe,skipDelayDuration:a=300,disableHoverableContent:s=!1,children:n}=e,u=o.useRef(!0),h=o.useRef(!1),d=o.useRef(0);return o.useEffect(()=>{const m=d.current;return()=>window.clearTimeout(m)},[]),c.jsx(Be,{scope:r,isOpenDelayedRef:u,delayDuration:t,onOpen:o.useCallback(()=>{window.clearTimeout(d.current),u.current=!1},[]),onClose:o.useCallback(()=>{window.clearTimeout(d.current),d.current=window.setTimeout(()=>u.current=!0,a)},[a]),isPointerInTransitRef:h,onPointerInTransitChange:o.useCallback(m=>{h.current=m},[]),disableHoverableContent:s,children:n})};oe.displayName=ie;var k="Tooltip",[We,$]=O(k),ce=e=>{const{__scopeTooltip:r,children:t,open:a,defaultOpen:s,onOpenChange:n,disableHoverableContent:u,delayDuration:h}=e,d=F(k,e.__scopeTooltip),m=U(r),[l,_]=o.useState(null),g=Te(),p=o.useRef(0),y=u??d.disableHoverableContent,b=h??d.delayDuration,E=o.useRef(!1),[v,f]=W({prop:a,defaultProp:s??!1,onChange:w=>{w?(d.onOpen(),document.dispatchEvent(new CustomEvent(G))):d.onClose(),n==null||n(w)},caller:k}),x=o.useMemo(()=>v?E.current?"delayed-open":"instant-open":"closed",[v]),C=o.useCallback(()=>{window.clearTimeout(p.current),p.current=0,E.current=!1,f(!0)},[f]),T=o.useCallback(()=>{window.clearTimeout(p.current),p.current=0,f(!1)},[f]),D=o.useCallback(()=>{window.clearTimeout(p.current),p.current=window.setTimeout(()=>{E.current=!0,f(!0),p.current=0},b)},[b,f]);return o.useEffect(()=>()=>{p.current&&(window.clearTimeout(p.current),p.current=0)},[]),c.jsx(Se,{...m,children:c.jsx(We,{scope:r,contentId:g,open:v,stateAttribute:x,trigger:l,onTriggerChange:_,onTriggerEnter:o.useCallback(()=>{d.isOpenDelayedRef.current?D():C()},[d.isOpenDelayedRef,D,C]),onTriggerLeave:o.useCallback(()=>{y?T():(window.clearTimeout(p.current),p.current=0)},[T,y]),onOpen:C,onClose:T,disableHoverableContent:y,children:t})})};ce.displayName=k;var L="TooltipTrigger",de=o.forwardRef((e,r)=>{const{__scopeTooltip:t,...a}=e,s=$(L,t),n=F(L,t),u=U(t),h=o.useRef(null),d=N(r,h,s.onTriggerChange),m=o.useRef(!1),l=o.useRef(!1),_=o.useCallback(()=>m.current=!1,[]);return o.useEffect(()=>()=>document.removeEventListener("pointerup",_),[_]),c.jsx(Re,{asChild:!0,...u,children:c.jsx(P.button,{"aria-describedby":s.open?s.contentId:void 0,"data-state":s.stateAttribute,...a,ref:d,onPointerMove:S(e.onPointerMove,g=>{g.pointerType!=="touch"&&!l.current&&!n.isPointerInTransitRef.current&&(s.onTriggerEnter(),l.current=!0)}),onPointerLeave:S(e.onPointerLeave,()=>{s.onTriggerLeave(),l.current=!1}),onPointerDown:S(e.onPointerDown,()=>{s.open&&s.onClose(),m.current=!0,document.addEventListener("pointerup",_,{once:!0})}),onFocus:S(e.onFocus,()=>{m.current||s.onOpen()}),onBlur:S(e.onBlur,s.onClose),onClick:S(e.onClick,s.onClose)})})});de.displayName=L;var q="TooltipPortal",[Ze,Ve]=O(q,{forceMount:void 0}),ue=e=>{const{__scopeTooltip:r,forceMount:t,children:a,container:s}=e,n=$(q,r);return c.jsx(Ze,{scope:r,forceMount:t,children:c.jsx(j,{present:t||n.open,children:c.jsx(be,{asChild:!0,container:s,children:a})})})};ue.displayName=q;var I="TooltipContent",le=o.forwardRef((e,r)=>{const t=Ve(I,e.__scopeTooltip),{forceMount:a=t.forceMount,side:s="top",...n}=e,u=$(I,e.__scopeTooltip);return c.jsx(j,{present:a||u.open,children:u.disableHoverableContent?c.jsx(_e,{side:s,...n,ref:r}):c.jsx(Ke,{side:s,...n,ref:r})})}),Ke=o.forwardRef((e,r)=>{const t=$(I,e.__scopeTooltip),a=F(I,e.__scopeTooltip),s=o.useRef(null),n=N(r,s),[u,h]=o.useState(null),{trigger:d,onClose:m}=t,l=s.current,{onPointerInTransitChange:_}=a,g=o.useCallback(()=>{h(null),_(!1)},[_]),p=o.useCallback((y,b)=>{const E=y.currentTarget,v={x:y.clientX,y:y.clientY},f=et(v,E.getBoundingClientRect()),x=tt(v,f),C=rt(b.getBoundingClientRect()),T=st([...x,...C]);h(T),_(!0)},[_]);return o.useEffect(()=>()=>g(),[g]),o.useEffect(()=>{if(d&&l){const y=E=>p(E,l),b=E=>p(E,d);return d.addEventListener("pointerleave",y),l.addEventListener("pointerleave",b),()=>{d.removeEventListener("pointerleave",y),l.removeEventListener("pointerleave",b)}}},[d,l,p,g]),o.useEffect(()=>{if(u){const y=b=>{const E=b.target,v={x:b.clientX,y:b.clientY},f=(d==null?void 0:d.contains(E))||(l==null?void 0:l.contains(E)),x=!at(v,u);f?g():x&&(g(),m())};return document.addEventListener("pointermove",y),()=>document.removeEventListener("pointermove",y)}},[d,l,u,m,g]),c.jsx(_e,{...e,ref:n})}),[Xe,Ye]=O(k,{isInside:!1}),Je=Fe("TooltipContent"),_e=o.forwardRef((e,r)=>{const{__scopeTooltip:t,children:a,"aria-label":s,onEscapeKeyDown:n,onPointerDownOutside:u,...h}=e,d=$(I,t),m=U(t),{onClose:l}=d;return o.useEffect(()=>(document.addEventListener(G,l),()=>document.removeEventListener(G,l)),[l]),o.useEffect(()=>{if(d.trigger){const _=g=>{const p=g.target;p!=null&&p.contains(d.trigger)&&l()};return window.addEventListener("scroll",_,{capture:!0}),()=>window.removeEventListener("scroll",_,{capture:!0})}},[d.trigger,l]),c.jsx(Ee,{asChild:!0,disableOutsidePointerEvents:!1,onEscapeKeyDown:n,onPointerDownOutside:u,onFocusOutside:_=>_.preventDefault(),onDismiss:l,children:c.jsxs(xe,{"data-state":d.stateAttribute,...m,...h,ref:r,style:{...h.style,"--radix-tooltip-content-transform-origin":"var(--radix-popper-transform-origin)","--radix-tooltip-content-available-width":"var(--radix-popper-available-width)","--radix-tooltip-content-available-height":"var(--radix-popper-available-height)","--radix-tooltip-trigger-width":"var(--radix-popper-anchor-width)","--radix-tooltip-trigger-height":"var(--radix-popper-anchor-height)"},children:[c.jsx(Je,{children:a}),c.jsx(Xe,{scope:t,isInside:!0,children:c.jsx(Ce,{id:d.contentId,role:"tooltip",children:s||a})})]})})});le.displayName=I;var pe="TooltipArrow",Qe=o.forwardRef((e,r)=>{const{__scopeTooltip:t,...a}=e,s=U(t);return Ye(pe,t).isInside?null:c.jsx(Ae,{...s,...a,ref:r})});Qe.displayName=pe;function et(e,r){const t=Math.abs(r.top-e.y),a=Math.abs(r.bottom-e.y),s=Math.abs(r.right-e.x),n=Math.abs(r.left-e.x);switch(Math.min(t,a,s,n)){case n:return"left";case s:return"right";case t:return"top";case a:return"bottom";default:throw new Error("unreachable")}}function tt(e,r,t=5){const a=[];switch(r){case"top":a.push({x:e.x-t,y:e.y+t},{x:e.x+t,y:e.y+t});break;case"bottom":a.push({x:e.x-t,y:e.y-t},{x:e.x+t,y:e.y-t});break;case"left":a.push({x:e.x+t,y:e.y-t},{x:e.x+t,y:e.y+t});break;case"right":a.push({x:e.x-t,y:e.y-t},{x:e.x-t,y:e.y+t});break}return a}function rt(e){const{top:r,right:t,bottom:a,left:s}=e;return[{x:s,y:r},{x:t,y:r},{x:t,y:a},{x:s,y:a}]}function at(e,r){const{x:t,y:a}=e;let s=!1;for(let n=0,u=r.length-1;n<r.length;u=n++){const h=r[n],d=r[u],m=h.x,l=h.y,_=d.x,g=d.y;l>a!=g>a&&t<(_-m)*(a-l)/(g-l)+m&&(s=!s)}return s}function st(e){const r=e.slice();return r.sort((t,a)=>t.x<a.x?-1:t.x>a.x?1:t.y<a.y?-1:t.y>a.y?1:0),nt(r)}function nt(e){if(e.length<=1)return e.slice();const r=[];for(let a=0;a<e.length;a++){const s=e[a];for(;r.length>=2;){const n=r[r.length-1],u=r[r.length-2];if((n.x-u.x)*(s.y-u.y)>=(n.y-u.y)*(s.x-u.x))r.pop();else break}r.push(s)}r.pop();const t=[];for(let a=e.length-1;a>=0;a--){const s=e[a];for(;t.length>=2;){const n=t[t.length-1],u=t[t.length-2];if((n.x-u.x)*(s.y-u.y)>=(n.y-u.y)*(s.x-u.x))t.pop();else break}t.push(s)}return t.pop(),r.length===1&&t.length===1&&r[0].x===t[0].x&&r[0].y===t[0].y?r:r.concat(t)}var it=oe,ot=ce,ct=de,dt=ue,me=le;const Pt=it,Nt=ot,Mt=ct,ut=o.forwardRef(({className:e,sideOffset:r=4,...t},a)=>c.jsx(dt,{children:c.jsx(me,{ref:a,sideOffset:r,className:A("z-50 overflow-hidden rounded-md bg-neutral-900 px-3 py-1.5 text-xs text-neutral-50 animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 dark:bg-neutral-50 dark:text-neutral-900",e),...t})}));ut.displayName=me.displayName;export{At as A,Rt as B,mt as C,kt as D,pt as G,It as R,wt as S,Pt as T,Dt as U,$t as a,St as b,Tt as c,Ct as d,xt as e,Et as f,bt as g,yt as h,vt as i,ft as j,ht as k,gt as l,ze as m,Nt as n,Mt as o,ut as p,Pe as q,Ne as r,Me as s,Oe as t,De as u};
