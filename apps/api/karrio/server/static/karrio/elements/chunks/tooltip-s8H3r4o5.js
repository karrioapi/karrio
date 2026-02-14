import{ai as _,r as i,j as s,t as ht,v as q,P as k,B as de,C as T,y as C,H as vt,z as N,M as yt,F as xt,I as Et,J as ue,bB as bt,X as ee,Y as W,s as v,bv as pe,bC as Ct,bD as _e,a$ as Dt,b0 as At,_ as Rt,m as fe,x as me,L as Tt,bE as Nt,V as St,E as It,W as wt}from"./globals-C95u6hwq.js";_`
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
`;_`
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
`;_`
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
`;_`
  query get_config_fieldsets {
    config_fieldsets {
      name
      keys
    }
  }
`;_`
  query get_config_schema {
    config_schema {
      key
      description
      value_type
      default_value
    }
  }
`;_`
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
`;_`
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
`;const nr=_`
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
`;_`
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
`;_`
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
`;const ir=_`
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
`;_`
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
`;_`
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
`;_`
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
`;_`
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
`;_`
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
`;_`
  mutation RemoveUser($input: DeleteUserMutationInput!) {
    remove_user(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;_`
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
`;const cr=_`
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
`,lr=_`
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
`,dr=_`
  mutation DeleteSystemConnection($input: DeleteConnectionMutationInput!) {
    delete_system_carrier_connection(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`,ur=_`
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
`,pr=_`
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
`,_r=_`
  mutation DeleteRateSheet($input: DeleteMutationInput!) {
    delete_rate_sheet(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`,fr=_`
  mutation DeleteRateSheetService($input: DeleteRateSheetServiceMutationInput!) {
    delete_rate_sheet_service(input: $input) {
      errors {
        field
        messages
      }
    }
  }
`,mr=_`
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
`,gr=_`
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
`,hr=_`
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
`,vr=_`
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
`,yr=_`
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
`,xr=_`
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
`,Er=_`
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
`,br=_`
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
`,Cr=_`
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
`,Dr=_`
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
`,Ar=_`
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
`,Rr=_`
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
`,Tr=_`
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
`,Nr=_`
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
`;_`
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
`;_`
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
`;const Sr=_`
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
`,Ir=_`
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
`;function Pt(e){const t=Ot(e),a=i.forwardRef((r,o)=>{const{children:n,...c}=r,d=i.Children.toArray(n),l=d.find(kt);if(l){const u=l.props.children,p=d.map(f=>f===l?i.Children.count(u)>1?i.Children.only(null):i.isValidElement(u)?u.props.children:null:f);return s.jsx(t,{...c,ref:o,children:i.isValidElement(u)?i.cloneElement(u,void 0,p):null})}return s.jsx(t,{...c,ref:o,children:n})});return a.displayName=`${e}.Slot`,a}function Ot(e){const t=i.forwardRef((a,r)=>{const{children:o,...n}=a;if(i.isValidElement(o)){const c=Mt(o),d=jt(n,o.props);return o.type!==i.Fragment&&(d.ref=r?ht(r,c):c),i.cloneElement(o,d)}return i.Children.count(o)>1?i.Children.only(null):null});return t.displayName=`${e}.SlotClone`,t}var $t=Symbol("radix.slottable");function kt(e){return i.isValidElement(e)&&typeof e.type=="function"&&"__radixId"in e.type&&e.type.__radixId===$t}function jt(e,t){const a={...t};for(const r in t){const o=e[r],n=t[r];/^on[A-Z]/.test(r)?o&&n?a[r]=(...d)=>{const l=n(...d);return o(...d),l}:o&&(a[r]=o):r==="style"?a[r]={...o,...n}:r==="className"&&(a[r]=[o,n].filter(Boolean).join(" "))}return{...e,...a}}function Mt(e){var r,o;let t=(r=Object.getOwnPropertyDescriptor(e.props,"ref"))==null?void 0:r.get,a=t&&"isReactWarning"in t&&t.isReactWarning;return a?e.ref:(t=(o=Object.getOwnPropertyDescriptor(e,"ref"))==null?void 0:o.get,a=t&&"isReactWarning"in t&&t.isReactWarning,a?e.props.ref:e.props.ref||e.ref)}var V="Dialog",[ge,he]=q(V),[Lt,D]=ge(V),ve=e=>{const{__scopeDialog:t,children:a,open:r,defaultOpen:o,onOpenChange:n,modal:c=!0}=e,d=i.useRef(null),l=i.useRef(null),[u,p]=ee({prop:r,defaultProp:o??!1,onChange:n,caller:V});return s.jsx(Lt,{scope:t,triggerRef:d,contentRef:l,contentId:W(),titleId:W(),descriptionId:W(),open:u,onOpenChange:p,onOpenToggle:i.useCallback(()=>p(f=>!f),[p]),modal:c,children:a})};ve.displayName=V;var ye="DialogTrigger",xe=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=D(ye,a),n=N(t,o.triggerRef);return s.jsx(T.button,{type:"button","aria-haspopup":"dialog","aria-expanded":o.open,"aria-controls":o.contentId,"data-state":re(o.open),...r,ref:n,onClick:C(e.onClick,o.onOpenToggle)})});xe.displayName=ye;var te="DialogPortal",[Gt,Ee]=ge(te,{forceMount:void 0}),be=e=>{const{__scopeDialog:t,forceMount:a,children:r,container:o}=e,n=D(te,t);return s.jsx(Gt,{scope:t,forceMount:a,children:i.Children.map(r,c=>s.jsx(k,{present:a||n.open,children:s.jsx(de,{asChild:!0,container:o,children:c})}))})};be.displayName=te;var B="DialogOverlay",Ce=i.forwardRef((e,t)=>{const a=Ee(B,e.__scopeDialog),{forceMount:r=a.forceMount,...o}=e,n=D(B,e.__scopeDialog);return n.modal?s.jsx(k,{present:r||n.open,children:s.jsx(Ht,{...o,ref:t})}):null});Ce.displayName=B;var Ut=Pt("DialogOverlay.RemoveScroll"),Ht=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=D(B,a);return s.jsx(vt,{as:Ut,allowPinchZoom:!0,shards:[o.contentRef],children:s.jsx(T.div,{"data-state":re(o.open),...r,ref:t,style:{pointerEvents:"auto",...r.style}})})}),P="DialogContent",De=i.forwardRef((e,t)=>{const a=Ee(P,e.__scopeDialog),{forceMount:r=a.forceMount,...o}=e,n=D(P,e.__scopeDialog);return s.jsx(k,{present:r||n.open,children:n.modal?s.jsx(Ft,{...o,ref:t}):s.jsx(zt,{...o,ref:t})})});De.displayName=P;var Ft=i.forwardRef((e,t)=>{const a=D(P,e.__scopeDialog),r=i.useRef(null),o=N(t,a.contentRef,r);return i.useEffect(()=>{const n=r.current;if(n)return yt(n)},[]),s.jsx(Ae,{...e,ref:o,trapFocus:a.open,disableOutsidePointerEvents:!0,onCloseAutoFocus:C(e.onCloseAutoFocus,n=>{var c;n.preventDefault(),(c=a.triggerRef.current)==null||c.focus()}),onPointerDownOutside:C(e.onPointerDownOutside,n=>{const c=n.detail.originalEvent,d=c.button===0&&c.ctrlKey===!0;(c.button===2||d)&&n.preventDefault()}),onFocusOutside:C(e.onFocusOutside,n=>n.preventDefault())})}),zt=i.forwardRef((e,t)=>{const a=D(P,e.__scopeDialog),r=i.useRef(!1),o=i.useRef(!1);return s.jsx(Ae,{...e,ref:t,trapFocus:!1,disableOutsidePointerEvents:!1,onCloseAutoFocus:n=>{var c,d;(c=e.onCloseAutoFocus)==null||c.call(e,n),n.defaultPrevented||(r.current||(d=a.triggerRef.current)==null||d.focus(),n.preventDefault()),r.current=!1,o.current=!1},onInteractOutside:n=>{var l,u;(l=e.onInteractOutside)==null||l.call(e,n),n.defaultPrevented||(r.current=!0,n.detail.originalEvent.type==="pointerdown"&&(o.current=!0));const c=n.target;((u=a.triggerRef.current)==null?void 0:u.contains(c))&&n.preventDefault(),n.detail.originalEvent.type==="focusin"&&o.current&&n.preventDefault()}})}),Ae=i.forwardRef((e,t)=>{const{__scopeDialog:a,trapFocus:r,onOpenAutoFocus:o,onCloseAutoFocus:n,...c}=e,d=D(P,a),l=i.useRef(null),u=N(t,l);return xt(),s.jsxs(s.Fragment,{children:[s.jsx(Et,{asChild:!0,loop:!0,trapped:r,onMountAutoFocus:o,onUnmountAutoFocus:n,children:s.jsx(ue,{role:"dialog",id:d.contentId,"aria-describedby":d.descriptionId,"aria-labelledby":d.titleId,"data-state":re(d.open),...c,ref:u,onDismiss:()=>d.onOpenChange(!1)})}),s.jsxs(s.Fragment,{children:[s.jsx(Bt,{titleId:d.titleId}),s.jsx(Vt,{contentRef:l,descriptionId:d.descriptionId})]})]})}),ae="DialogTitle",Re=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=D(ae,a);return s.jsx(T.h2,{id:o.titleId,...r,ref:t})});Re.displayName=ae;var Te="DialogDescription",Ne=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=D(Te,a);return s.jsx(T.p,{id:o.descriptionId,...r,ref:t})});Ne.displayName=Te;var Se="DialogClose",Ie=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=D(Se,a);return s.jsx(T.button,{type:"button",...r,ref:t,onClick:C(e.onClick,()=>o.onOpenChange(!1))})});Ie.displayName=Se;function re(e){return e?"open":"closed"}var we="DialogTitleWarning",[Wt,Pe]=bt(we,{contentName:P,titleName:ae,docsSlug:"dialog"}),Bt=({titleId:e})=>{const t=Pe(we),a=`\`${t.contentName}\` requires a \`${t.titleName}\` for the component to be accessible for screen reader users.

If you want to hide the \`${t.titleName}\`, you can wrap it with our VisuallyHidden component.

For more information, see https://radix-ui.com/primitives/docs/components/${t.docsSlug}`;return i.useEffect(()=>{e&&(document.getElementById(e)||console.error(a))},[a,e]),null},qt="DialogDescriptionWarning",Vt=({contentRef:e,descriptionId:t})=>{const r=`Warning: Missing \`Description\` or \`aria-describedby={undefined}\` for {${Pe(qt).contentName}}.`;return i.useEffect(()=>{var n;const o=(n=e.current)==null?void 0:n.getAttribute("aria-describedby");t&&o&&(document.getElementById(t)||console.warn(r))},[r,e,t]),null},oe=ve,Oe=xe,se=be,M=Ce,L=De,G=Re,U=Ne,Z=Ie;const wr=oe,Zt=se,$e=i.forwardRef(({className:e,...t},a)=>s.jsx(M,{className:v("fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",e),...t,ref:a}));$e.displayName=M.displayName;const Yt=Ct("fixed z-50 gap-4 bg-background p-6 shadow-lg transition ease-in-out data-[state=closed]:duration-300 data-[state=open]:duration-500 data-[state=open]:animate-in data-[state=closed]:animate-out",{variants:{side:{top:"inset-x-0 top-0 border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top",bottom:"inset-x-0 bottom-0 border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom",left:"inset-y-0 left-0 h-full w-3/4 border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left sm:max-w-sm",right:"inset-y-0 right-0 h-full w-3/4 border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right sm:max-w-sm"}},defaultVariants:{side:"right"}}),Kt=i.forwardRef(({side:e="right",className:t,children:a,full:r=!1,hideCloseButton:o=!1,...n},c)=>s.jsxs(Zt,{children:[s.jsx($e,{}),s.jsxs(L,{ref:c,className:v(r?"fixed inset-0 z-50 bg-background p-0 shadow-lg transition ease-in-out data-[state=closed]:duration-300 data-[state=open]:duration-500 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right h-[100svh] w-screen max-w-none border-0":Yt({side:e}),t),...n,children:[!o&&s.jsxs(Z,{className:"absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-secondary",children:[s.jsx(pe,{className:"h-4 w-4"}),s.jsx("span",{className:"sr-only",children:"Close"})]}),a]})]}));Kt.displayName=L.displayName;const Xt=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col space-y-2 text-center sm:text-left",e),...t});Xt.displayName="SheetHeader";const Jt=i.forwardRef(({className:e,...t},a)=>s.jsx(G,{ref:a,className:v("text-lg font-semibold text-foreground",e),...t}));Jt.displayName=G.displayName;const Qt=i.forwardRef(({className:e,...t},a)=>s.jsx(U,{ref:a,className:v("text-sm text-muted-foreground",e),...t}));Qt.displayName=U.displayName;var ea=Symbol("radix.slottable");function ta(e){const t=({children:a})=>s.jsx(s.Fragment,{children:a});return t.displayName=`${e}.Slottable`,t.__radixId=ea,t}var ke="AlertDialog",[aa]=q(ke,[he]),S=he(),je=e=>{const{__scopeAlertDialog:t,...a}=e,r=S(t);return s.jsx(oe,{...r,...a,modal:!0})};je.displayName=ke;var ra="AlertDialogTrigger",oa=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=S(a);return s.jsx(Oe,{...o,...r,ref:t})});oa.displayName=ra;var sa="AlertDialogPortal",Me=e=>{const{__scopeAlertDialog:t,...a}=e,r=S(t);return s.jsx(se,{...r,...a})};Me.displayName=sa;var na="AlertDialogOverlay",Le=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=S(a);return s.jsx(M,{...o,...r,ref:t})});Le.displayName=na;var O="AlertDialogContent",[ia,ca]=aa(O),la=ta("AlertDialogContent"),Ge=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,children:r,...o}=e,n=S(a),c=i.useRef(null),d=N(t,c),l=i.useRef(null);return s.jsx(Wt,{contentName:O,titleName:Ue,docsSlug:"alert-dialog",children:s.jsx(ia,{scope:a,cancelRef:l,children:s.jsxs(L,{role:"alertdialog",...n,...o,ref:d,onOpenAutoFocus:C(o.onOpenAutoFocus,u=>{var p;u.preventDefault(),(p=l.current)==null||p.focus({preventScroll:!0})}),onPointerDownOutside:u=>u.preventDefault(),onInteractOutside:u=>u.preventDefault(),children:[s.jsx(la,{children:r}),s.jsx(ua,{contentRef:c})]})})})});Ge.displayName=O;var Ue="AlertDialogTitle",He=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=S(a);return s.jsx(G,{...o,...r,ref:t})});He.displayName=Ue;var Fe="AlertDialogDescription",ze=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=S(a);return s.jsx(U,{...o,...r,ref:t})});ze.displayName=Fe;var da="AlertDialogAction",We=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=S(a);return s.jsx(Z,{...o,...r,ref:t})});We.displayName=da;var Be="AlertDialogCancel",qe=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,{cancelRef:o}=ca(Be,a),n=S(a),c=N(t,o);return s.jsx(Z,{...n,...r,ref:c})});qe.displayName=Be;var ua=({contentRef:e})=>{const t=`\`${O}\` requires a description for the component to be accessible for screen reader users.

You can add a description to the \`${O}\` by passing a \`${Fe}\` component as a child, which also benefits sighted users by adding visible context to the dialog.

Alternatively, you can use your own component as a description by assigning it an \`id\` and passing the same value to the \`aria-describedby\` prop in \`${O}\`. If the description is confusing or duplicative for sighted users, you can use the \`@radix-ui/react-visually-hidden\` primitive as a wrapper around your description component.

For more information, see https://radix-ui.com/primitives/docs/components/alert-dialog`;return i.useEffect(()=>{var r;document.getElementById((r=e.current)==null?void 0:r.getAttribute("aria-describedby"))||console.warn(t)},[t,e]),null},pa=je,_a=Me,Ve=Le,Ze=Ge,Ye=We,Ke=qe,Xe=He,Je=ze;const Pr=pa,fa=_a,Qe=i.forwardRef(({className:e,...t},a)=>s.jsx(Ve,{className:v("fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",e),...t,ref:a}));Qe.displayName=Ve.displayName;const ma=i.forwardRef(({className:e,...t},a)=>s.jsxs(fa,{children:[s.jsx(Qe,{}),s.jsx(Ze,{ref:a,className:v("fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border border-neutral-200 bg-white p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg dark:border-neutral-800 dark:bg-neutral-950",e),...t})]}));ma.displayName=Ze.displayName;const ga=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col space-y-2 text-center sm:text-left",e),...t});ga.displayName="AlertDialogHeader";const ha=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2",e),...t});ha.displayName="AlertDialogFooter";const va=i.forwardRef(({className:e,...t},a)=>s.jsx(Xe,{ref:a,className:v("text-lg font-semibold",e),...t}));va.displayName=Xe.displayName;const ya=i.forwardRef(({className:e,...t},a)=>s.jsx(Je,{ref:a,className:v("text-sm text-neutral-500 dark:text-neutral-400",e),...t}));ya.displayName=Je.displayName;const xa=i.forwardRef(({className:e,...t},a)=>s.jsx(Ye,{ref:a,className:v(_e(),e),...t}));xa.displayName=Ye.displayName;const Ea=i.forwardRef(({className:e,...t},a)=>s.jsx(Ke,{ref:a,className:v(_e({variant:"outline"}),e),...t}));Ea.displayName=Ke.displayName;const Or=oe,$r=Oe,ba=se,et=i.forwardRef(({className:e,...t},a)=>s.jsx(M,{ref:a,className:v("fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",e),...t}));et.displayName=M.displayName;const Ca=i.forwardRef(({className:e,children:t,...a},r)=>s.jsxs(ba,{children:[s.jsx(et,{}),s.jsxs(L,{ref:r,className:v("fixed left-1/2 top-1/2 z-50 flex flex-col w-full max-w-lg -translate-x-1/2 -translate-y-1/2 border bg-background shadow-xl duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] rounded-xl sm:rounded-2xl overflow-hidden max-h-[90vh] sm:max-h-[90vh]",e),...a,children:[t,s.jsxs(Z,{className:"absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground z-10",children:[s.jsx(pe,{className:"h-4 w-4"}),s.jsx("span",{className:"sr-only",children:"Close"})]})]})]}));Ca.displayName=L.displayName;const Da=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col space-y-1.5 text-center sm:text-left px-4 py-3 border-b bg-background",e),...t});Da.displayName="DialogHeader";const Aa=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2 px-4 py-4 border-t bg-background mt-auto",e),...t});Aa.displayName="DialogFooter";const Ra=({className:e,...t})=>s.jsx("div",{className:v("flex-1 overflow-y-auto px-4 py-4",e),...t});Ra.displayName="DialogBody";const Ta=i.forwardRef(({className:e,...t},a)=>s.jsx(G,{ref:a,className:v("text-lg font-semibold leading-none tracking-tight",e),...t}));Ta.displayName=G.displayName;const Na=i.forwardRef(({className:e,...t},a)=>s.jsx(U,{ref:a,className:v("text-sm text-muted-foreground",e),...t}));Na.displayName=U.displayName;var Y="Checkbox",[Sa]=q(Y),[Ia,ne]=Sa(Y);function wa(e){const{__scopeCheckbox:t,checked:a,children:r,defaultChecked:o,disabled:n,form:c,name:d,onCheckedChange:l,required:u,value:p="on",internal_do_not_use_render:f}=e,[g,m]=ee({prop:a,defaultProp:o??!1,onChange:l,caller:Y}),[x,E]=i.useState(null),[b,y]=i.useState(null),h=i.useRef(!1),A=x?!!c||!!x.closest("form"):!0,R={checked:g,disabled:n,setChecked:m,control:x,setControl:E,name:d,form:c,value:p,hasConsumerStoppedPropagationRef:h,required:u,defaultChecked:w(o)?!1:o,isFormControl:A,bubbleInput:b,setBubbleInput:y};return s.jsx(Ia,{scope:t,...R,children:Pa(f)?f(R):r})}var tt="CheckboxTrigger",at=i.forwardRef(({__scopeCheckbox:e,onKeyDown:t,onClick:a,...r},o)=>{const{control:n,value:c,disabled:d,checked:l,required:u,setControl:p,setChecked:f,hasConsumerStoppedPropagationRef:g,isFormControl:m,bubbleInput:x}=ne(tt,e),E=N(o,p),b=i.useRef(l);return i.useEffect(()=>{const y=n==null?void 0:n.form;if(y){const h=()=>f(b.current);return y.addEventListener("reset",h),()=>y.removeEventListener("reset",h)}},[n,f]),s.jsx(T.button,{type:"button",role:"checkbox","aria-checked":w(l)?"mixed":l,"aria-required":u,"data-state":it(l),"data-disabled":d?"":void 0,disabled:d,value:c,...r,ref:E,onKeyDown:C(t,y=>{y.key==="Enter"&&y.preventDefault()}),onClick:C(a,y=>{f(h=>w(h)?!0:!h),x&&m&&(g.current=y.isPropagationStopped(),g.current||y.stopPropagation())})})});at.displayName=tt;var ie=i.forwardRef((e,t)=>{const{__scopeCheckbox:a,name:r,checked:o,defaultChecked:n,required:c,disabled:d,value:l,onCheckedChange:u,form:p,...f}=e;return s.jsx(wa,{__scopeCheckbox:a,checked:o,defaultChecked:n,disabled:d,required:c,onCheckedChange:u,name:r,form:p,value:l,internal_do_not_use_render:({isFormControl:g})=>s.jsxs(s.Fragment,{children:[s.jsx(at,{...f,ref:t,__scopeCheckbox:a}),g&&s.jsx(nt,{__scopeCheckbox:a})]})})});ie.displayName=Y;var rt="CheckboxIndicator",ot=i.forwardRef((e,t)=>{const{__scopeCheckbox:a,forceMount:r,...o}=e,n=ne(rt,a);return s.jsx(k,{present:r||w(n.checked)||n.checked===!0,children:s.jsx(T.span,{"data-state":it(n.checked),"data-disabled":n.disabled?"":void 0,...o,ref:t,style:{pointerEvents:"none",...e.style}})})});ot.displayName=rt;var st="CheckboxBubbleInput",nt=i.forwardRef(({__scopeCheckbox:e,...t},a)=>{const{control:r,hasConsumerStoppedPropagationRef:o,checked:n,defaultChecked:c,required:d,disabled:l,name:u,value:p,form:f,bubbleInput:g,setBubbleInput:m}=ne(st,e),x=N(a,m),E=Dt(n),b=At(r);i.useEffect(()=>{const h=g;if(!h)return;const A=window.HTMLInputElement.prototype,I=Object.getOwnPropertyDescriptor(A,"checked").set,F=!o.current;if(E!==n&&I){const z=new Event("click",{bubbles:F});h.indeterminate=w(n),I.call(h,w(n)?!1:n),h.dispatchEvent(z)}},[g,E,n,o]);const y=i.useRef(w(n)?!1:n);return s.jsx(T.input,{type:"checkbox","aria-hidden":!0,defaultChecked:c??y.current,required:d,disabled:l,name:u,value:p,form:f,...t,tabIndex:-1,ref:x,style:{...t.style,...b,position:"absolute",pointerEvents:"none",opacity:0,margin:0,transform:"translateX(-100%)"}})});nt.displayName=st;function Pa(e){return typeof e=="function"}function w(e){return e==="indeterminate"}function it(e){return w(e)?"indeterminate":e?"checked":"unchecked"}const Oa=i.forwardRef(({className:e,...t},a)=>s.jsx(ie,{ref:a,className:v("peer h-4 w-4 shrink-0 rounded-sm border border-primary shadow focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground",e),...t,children:s.jsx(ot,{className:v("flex items-center justify-center text-current"),children:s.jsx(Rt,{className:"h-4 w-4"})})}));Oa.displayName=ie.displayName;/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const $a=[["path",{d:"M20 6 9 17l-5-5",key:"1gmf2c"}]],kr=fe("check",$a);/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ka=[["path",{d:"M21 12a9 9 0 1 1-6.219-8.56",key:"13zald"}]],jr=fe("loader-circle",ka);var ja=Symbol("radix.slottable");function Ma(e){const t=({children:a})=>s.jsx(s.Fragment,{children:a});return t.displayName=`${e}.Slottable`,t.__radixId=ja,t}var[K]=q("Tooltip",[me]),X=me(),ct="TooltipProvider",La=700,J="tooltip.open",[Ga,ce]=K(ct),lt=e=>{const{__scopeTooltip:t,delayDuration:a=La,skipDelayDuration:r=300,disableHoverableContent:o=!1,children:n}=e,c=i.useRef(!0),d=i.useRef(!1),l=i.useRef(0);return i.useEffect(()=>{const u=l.current;return()=>window.clearTimeout(u)},[]),s.jsx(Ga,{scope:t,isOpenDelayedRef:c,delayDuration:a,onOpen:i.useCallback(()=>{window.clearTimeout(l.current),c.current=!1},[]),onClose:i.useCallback(()=>{window.clearTimeout(l.current),l.current=window.setTimeout(()=>c.current=!0,r)},[r]),isPointerInTransitRef:d,onPointerInTransitChange:i.useCallback(u=>{d.current=u},[]),disableHoverableContent:o,children:n})};lt.displayName=ct;var j="Tooltip",[Ua,H]=K(j),dt=e=>{const{__scopeTooltip:t,children:a,open:r,defaultOpen:o,onOpenChange:n,disableHoverableContent:c,delayDuration:d}=e,l=ce(j,e.__scopeTooltip),u=X(t),[p,f]=i.useState(null),g=W(),m=i.useRef(0),x=c??l.disableHoverableContent,E=d??l.delayDuration,b=i.useRef(!1),[y,h]=ee({prop:r,defaultProp:o??!1,onChange:z=>{z?(l.onOpen(),document.dispatchEvent(new CustomEvent(J))):l.onClose(),n==null||n(z)},caller:j}),A=i.useMemo(()=>y?b.current?"delayed-open":"instant-open":"closed",[y]),R=i.useCallback(()=>{window.clearTimeout(m.current),m.current=0,b.current=!1,h(!0)},[h]),I=i.useCallback(()=>{window.clearTimeout(m.current),m.current=0,h(!1)},[h]),F=i.useCallback(()=>{window.clearTimeout(m.current),m.current=window.setTimeout(()=>{b.current=!0,h(!0),m.current=0},E)},[E,h]);return i.useEffect(()=>()=>{m.current&&(window.clearTimeout(m.current),m.current=0)},[]),s.jsx(St,{...u,children:s.jsx(Ua,{scope:t,contentId:g,open:y,stateAttribute:A,trigger:p,onTriggerChange:f,onTriggerEnter:i.useCallback(()=>{l.isOpenDelayedRef.current?F():R()},[l.isOpenDelayedRef,F,R]),onTriggerLeave:i.useCallback(()=>{x?I():(window.clearTimeout(m.current),m.current=0)},[I,x]),onOpen:R,onClose:I,disableHoverableContent:x,children:a})})};dt.displayName=j;var Q="TooltipTrigger",ut=i.forwardRef((e,t)=>{const{__scopeTooltip:a,...r}=e,o=H(Q,a),n=ce(Q,a),c=X(a),d=i.useRef(null),l=N(t,d,o.onTriggerChange),u=i.useRef(!1),p=i.useRef(!1),f=i.useCallback(()=>u.current=!1,[]);return i.useEffect(()=>()=>document.removeEventListener("pointerup",f),[f]),s.jsx(It,{asChild:!0,...c,children:s.jsx(T.button,{"aria-describedby":o.open?o.contentId:void 0,"data-state":o.stateAttribute,...r,ref:l,onPointerMove:C(e.onPointerMove,g=>{g.pointerType!=="touch"&&!p.current&&!n.isPointerInTransitRef.current&&(o.onTriggerEnter(),p.current=!0)}),onPointerLeave:C(e.onPointerLeave,()=>{o.onTriggerLeave(),p.current=!1}),onPointerDown:C(e.onPointerDown,()=>{o.open&&o.onClose(),u.current=!0,document.addEventListener("pointerup",f,{once:!0})}),onFocus:C(e.onFocus,()=>{u.current||o.onOpen()}),onBlur:C(e.onBlur,o.onClose),onClick:C(e.onClick,o.onClose)})})});ut.displayName=Q;var le="TooltipPortal",[Ha,Fa]=K(le,{forceMount:void 0}),pt=e=>{const{__scopeTooltip:t,forceMount:a,children:r,container:o}=e,n=H(le,t);return s.jsx(Ha,{scope:t,forceMount:a,children:s.jsx(k,{present:a||n.open,children:s.jsx(de,{asChild:!0,container:o,children:r})})})};pt.displayName=le;var $="TooltipContent",_t=i.forwardRef((e,t)=>{const a=Fa($,e.__scopeTooltip),{forceMount:r=a.forceMount,side:o="top",...n}=e,c=H($,e.__scopeTooltip);return s.jsx(k,{present:r||c.open,children:c.disableHoverableContent?s.jsx(ft,{side:o,...n,ref:t}):s.jsx(za,{side:o,...n,ref:t})})}),za=i.forwardRef((e,t)=>{const a=H($,e.__scopeTooltip),r=ce($,e.__scopeTooltip),o=i.useRef(null),n=N(t,o),[c,d]=i.useState(null),{trigger:l,onClose:u}=a,p=o.current,{onPointerInTransitChange:f}=r,g=i.useCallback(()=>{d(null),f(!1)},[f]),m=i.useCallback((x,E)=>{const b=x.currentTarget,y={x:x.clientX,y:x.clientY},h=Za(y,b.getBoundingClientRect()),A=Ya(y,h),R=Ka(E.getBoundingClientRect()),I=Ja([...A,...R]);d(I),f(!0)},[f]);return i.useEffect(()=>()=>g(),[g]),i.useEffect(()=>{if(l&&p){const x=b=>m(b,p),E=b=>m(b,l);return l.addEventListener("pointerleave",x),p.addEventListener("pointerleave",E),()=>{l.removeEventListener("pointerleave",x),p.removeEventListener("pointerleave",E)}}},[l,p,m,g]),i.useEffect(()=>{if(c){const x=E=>{const b=E.target,y={x:E.clientX,y:E.clientY},h=(l==null?void 0:l.contains(b))||(p==null?void 0:p.contains(b)),A=!Xa(y,c);h?g():A&&(g(),u())};return document.addEventListener("pointermove",x),()=>document.removeEventListener("pointermove",x)}},[l,p,c,u,g]),s.jsx(ft,{...e,ref:n})}),[Wa,Ba]=K(j,{isInside:!1}),qa=Ma("TooltipContent"),ft=i.forwardRef((e,t)=>{const{__scopeTooltip:a,children:r,"aria-label":o,onEscapeKeyDown:n,onPointerDownOutside:c,...d}=e,l=H($,a),u=X(a),{onClose:p}=l;return i.useEffect(()=>(document.addEventListener(J,p),()=>document.removeEventListener(J,p)),[p]),i.useEffect(()=>{if(l.trigger){const f=g=>{const m=g.target;m!=null&&m.contains(l.trigger)&&p()};return window.addEventListener("scroll",f,{capture:!0}),()=>window.removeEventListener("scroll",f,{capture:!0})}},[l.trigger,p]),s.jsx(ue,{asChild:!0,disableOutsidePointerEvents:!1,onEscapeKeyDown:n,onPointerDownOutside:c,onFocusOutside:f=>f.preventDefault(),onDismiss:p,children:s.jsxs(Tt,{"data-state":l.stateAttribute,...u,...d,ref:t,style:{...d.style,"--radix-tooltip-content-transform-origin":"var(--radix-popper-transform-origin)","--radix-tooltip-content-available-width":"var(--radix-popper-available-width)","--radix-tooltip-content-available-height":"var(--radix-popper-available-height)","--radix-tooltip-trigger-width":"var(--radix-popper-anchor-width)","--radix-tooltip-trigger-height":"var(--radix-popper-anchor-height)"},children:[s.jsx(qa,{children:r}),s.jsx(Wa,{scope:a,isInside:!0,children:s.jsx(Nt,{id:l.contentId,role:"tooltip",children:o||r})})]})})});_t.displayName=$;var mt="TooltipArrow",Va=i.forwardRef((e,t)=>{const{__scopeTooltip:a,...r}=e,o=X(a);return Ba(mt,a).isInside?null:s.jsx(wt,{...o,...r,ref:t})});Va.displayName=mt;function Za(e,t){const a=Math.abs(t.top-e.y),r=Math.abs(t.bottom-e.y),o=Math.abs(t.right-e.x),n=Math.abs(t.left-e.x);switch(Math.min(a,r,o,n)){case n:return"left";case o:return"right";case a:return"top";case r:return"bottom";default:throw new Error("unreachable")}}function Ya(e,t,a=5){const r=[];switch(t){case"top":r.push({x:e.x-a,y:e.y+a},{x:e.x+a,y:e.y+a});break;case"bottom":r.push({x:e.x-a,y:e.y-a},{x:e.x+a,y:e.y-a});break;case"left":r.push({x:e.x+a,y:e.y-a},{x:e.x+a,y:e.y+a});break;case"right":r.push({x:e.x-a,y:e.y-a},{x:e.x-a,y:e.y+a});break}return r}function Ka(e){const{top:t,right:a,bottom:r,left:o}=e;return[{x:o,y:t},{x:a,y:t},{x:a,y:r},{x:o,y:r}]}function Xa(e,t){const{x:a,y:r}=e;let o=!1;for(let n=0,c=t.length-1;n<t.length;c=n++){const d=t[n],l=t[c],u=d.x,p=d.y,f=l.x,g=l.y;p>r!=g>r&&a<(f-u)*(r-p)/(g-p)+u&&(o=!o)}return o}function Ja(e){const t=e.slice();return t.sort((a,r)=>a.x<r.x?-1:a.x>r.x?1:a.y<r.y?-1:a.y>r.y?1:0),Qa(t)}function Qa(e){if(e.length<=1)return e.slice();const t=[];for(let r=0;r<e.length;r++){const o=e[r];for(;t.length>=2;){const n=t[t.length-1],c=t[t.length-2];if((n.x-c.x)*(o.y-c.y)>=(n.y-c.y)*(o.x-c.x))t.pop();else break}t.push(o)}t.pop();const a=[];for(let r=e.length-1;r>=0;r--){const o=e[r];for(;a.length>=2;){const n=a[a.length-1],c=a[a.length-2];if((n.x-c.x)*(o.y-c.y)>=(n.y-c.y)*(o.x-c.x))a.pop();else break}a.push(o)}return a.pop(),t.length===1&&a.length===1&&t[0].x===a[0].x&&t[0].y===a[0].y?t:t.concat(a)}var er=lt,tr=dt,ar=ut,rr=pt,gt=_t;const Mr=er,Lr=tr,Gr=ar,or=i.forwardRef(({className:e,sideOffset:t=4,...a},r)=>s.jsx(rr,{children:s.jsx(gt,{ref:r,sideOffset:t,className:v("z-50 overflow-hidden rounded-md bg-neutral-900 px-3 py-1.5 text-xs text-neutral-50 animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 dark:bg-neutral-50 dark:text-neutral-900",e),...a})}));or.displayName=gt.displayName;export{gr as $,Pr as A,Kt as B,L as C,U as D,dr as E,cr as F,Ir as G,nr as H,Rr as I,Ar as J,Dr as K,jr as L,Nr as M,Tr as N,M as O,se as P,Cr as Q,oe as R,Xt as S,G as T,lr as U,br as V,Er as W,xr as X,yr as Y,vr as Z,hr as _,ma as a,mr as a0,fr as a1,_r as a2,pr as a3,ur as a4,ir as a5,Ra as a6,ga as b,va as c,ya as d,ha as e,Ea as f,xa as g,Or as h,$r as i,ba as j,Ca as k,Da as l,Ta as m,Na as n,Oa as o,Mr as p,Lr as q,Gr as r,or as s,kr as t,Sr as u,Jt as v,Qt as w,Aa as x,wr as y,Zt as z};
