import{g as u,r as i,j as s,z as vt,B as V,P as j,I as pe,J as S,F as C,N as yt,H as N,W as xt,M as bt,S as Et,U as _e,bD as Ct,a0 as ae,a1 as W,y as v,bw as fe,bE as Rt,bF as me,b1 as Tt,b2 as Dt,a3 as St,v as M,E as ge,V as Nt,bG as At,_ as kt,L as wt,$ as $t,R as Q,u as It}from"./globals-sn6rr4S9.js";u`
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
`;u`
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
`;u`
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
`;u`
  query get_config_fieldsets {
    config_fieldsets {
      name
      keys
    }
  }
`;u`
  query get_config_schema {
    config_schema {
      key
      description
      value_type
      default_value
    }
  }
`;u`
  query GetConfigs {
    configs {
      configs
    }
  }
`;u`
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
`;const ur=u`
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
`;u`
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
`;u`
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
`;const pr=u`
  query GetRateSheet($id: String!) {
    rate_sheet(id: $id) {
      id
      name
      slug
      carrier_name
      origin_countries
      metadata
      pricing_config
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
        meta
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
        pricing_config
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
`;u`
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
`;u`
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
`;u`
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
`;u`
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
`;u`
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
`;u`
  mutation RemoveUser($input: DeleteUserMutationInput!) {
    remove_user(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;u`
  mutation UpdateConfigs($input: InstanceConfigMutationInput!) {
    update_configs(input: $input) {
      errors {
        field
        messages
      }
      configs {
        configs
      }
    }
  }
`;const _r=u`
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
`,fr=u`
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
`,mr=u`
  mutation DeleteSystemConnection($input: DeleteConnectionMutationInput!) {
    delete_system_carrier_connection(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`,gr=u`
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
`,hr=u`
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
`,vr=u`
  mutation DeleteRateSheet($input: DeleteMutationInput!) {
    delete_rate_sheet(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`,yr=u`
  mutation DeleteRateSheetService($input: DeleteRateSheetServiceMutationInput!) {
    delete_rate_sheet_service(input: $input) {
      errors {
        field
        messages
      }
    }
  }
`,xr=u`
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
`,br=u`
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
`,Er=u`
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
`,Cr=u`
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
`,Rr=u`
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
`,Tr=u`
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
`,Dr=u`
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
`,Sr=u`
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
          meta
        }
      }
      errors {
        field
        messages
      }
    }
  }
`,Nr=u`
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
          meta
        }
      }
      errors {
        field
        messages
      }
    }
  }
`,Ar=u`
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
          meta
        }
      }
      errors {
        field
        messages
      }
    }
  }
`,kr=u`
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
          meta
        }
      }
      errors {
        field
        messages
      }
    }
  }
`,wr=u`
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
          meta
        }
      }
      errors {
        field
        messages
      }
    }
  }
`,$r=u`
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
`,Ir=u`
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
`;u`
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
`;u`
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
`;const Pr=u`
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
`,jr=u`
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
`,Or=u`
  mutation TriggerTrackerUpdate($input: TriggerTrackerUpdateInput!) {
    trigger_tracker_update(input: $input) {
      errors {
        field
        messages
      }
      task_count
    }
  }
`,Mr=u`
  mutation RetryWebhook($input: RetryWebhookInput!) {
    retry_webhook(input: $input) {
      errors {
        field
        messages
      }
      event_id
    }
  }
`,Ur=u`
  mutation RevokeTask($input: RevokeTaskInput!) {
    revoke_task(input: $input) {
      errors {
        field
        messages
      }
      task_id
    }
  }
`,Lr=u`
  mutation CleanupTaskExecutions($input: CleanupTaskExecutionsInput!) {
    cleanup_task_executions(input: $input) {
      errors {
        field
        messages
      }
      deleted_count
    }
  }
`,Gr=u`
  mutation ResetStuckTasks($input: ResetStuckTasksInput!) {
    reset_stuck_tasks(input: $input) {
      errors {
        field
        messages
      }
      updated_count
    }
  }
`,Fr=u`
  mutation TriggerDataArchiving {
    trigger_data_archiving {
      errors {
        field
        messages
      }
      success
    }
  }
`;function Pt(e){const t=jt(e),a=i.forwardRef((r,o)=>{const{children:n,...c}=r,d=i.Children.toArray(n),l=d.find(Mt);if(l){const p=l.props.children,_=d.map(f=>f===l?i.Children.count(p)>1?i.Children.only(null):i.isValidElement(p)?p.props.children:null:f);return s.jsx(t,{...c,ref:o,children:i.isValidElement(p)?i.cloneElement(p,void 0,_):null})}return s.jsx(t,{...c,ref:o,children:n})});return a.displayName=`${e}.Slot`,a}function jt(e){const t=i.forwardRef((a,r)=>{const{children:o,...n}=a;if(i.isValidElement(o)){const c=Lt(o),d=Ut(n,o.props);return o.type!==i.Fragment&&(d.ref=r?vt(r,c):c),i.cloneElement(o,d)}return i.Children.count(o)>1?i.Children.only(null):null});return t.displayName=`${e}.SlotClone`,t}var Ot=Symbol("radix.slottable");function Mt(e){return i.isValidElement(e)&&typeof e.type=="function"&&"__radixId"in e.type&&e.type.__radixId===Ot}function Ut(e,t){const a={...t};for(const r in t){const o=e[r],n=t[r];/^on[A-Z]/.test(r)?o&&n?a[r]=(...d)=>{const l=n(...d);return o(...d),l}:o&&(a[r]=o):r==="style"?a[r]={...o,...n}:r==="className"&&(a[r]=[o,n].filter(Boolean).join(" "))}return{...e,...a}}function Lt(e){var r,o;let t=(r=Object.getOwnPropertyDescriptor(e.props,"ref"))==null?void 0:r.get,a=t&&"isReactWarning"in t&&t.isReactWarning;return a?e.ref:(t=(o=Object.getOwnPropertyDescriptor(e,"ref"))==null?void 0:o.get,a=t&&"isReactWarning"in t&&t.isReactWarning,a?e.props.ref:e.props.ref||e.ref)}var K="Dialog",[he,ve]=V(K),[Gt,R]=he(K),ye=e=>{const{__scopeDialog:t,children:a,open:r,defaultOpen:o,onOpenChange:n,modal:c=!0}=e,d=i.useRef(null),l=i.useRef(null),[p,_]=ae({prop:r,defaultProp:o??!1,onChange:n,caller:K});return s.jsx(Gt,{scope:t,triggerRef:d,contentRef:l,contentId:W(),titleId:W(),descriptionId:W(),open:p,onOpenChange:_,onOpenToggle:i.useCallback(()=>_(f=>!f),[_]),modal:c,children:a})};ye.displayName=K;var xe="DialogTrigger",be=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=R(xe,a),n=N(t,o.triggerRef);return s.jsx(S.button,{type:"button","aria-haspopup":"dialog","aria-expanded":o.open,"aria-controls":o.contentId,"data-state":se(o.open),...r,ref:n,onClick:C(e.onClick,o.onOpenToggle)})});be.displayName=xe;var re="DialogPortal",[Ft,Ee]=he(re,{forceMount:void 0}),Ce=e=>{const{__scopeDialog:t,forceMount:a,children:r,container:o}=e,n=R(re,t);return s.jsx(Ft,{scope:t,forceMount:a,children:i.Children.map(r,c=>s.jsx(j,{present:a||n.open,children:s.jsx(pe,{asChild:!0,container:o,children:c})}))})};Ce.displayName=re;var B="DialogOverlay",Re=i.forwardRef((e,t)=>{const a=Ee(B,e.__scopeDialog),{forceMount:r=a.forceMount,...o}=e,n=R(B,e.__scopeDialog);return n.modal?s.jsx(j,{present:r||n.open,children:s.jsx(zt,{...o,ref:t})}):null});Re.displayName=B;var Ht=Pt("DialogOverlay.RemoveScroll"),zt=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=R(B,a);return s.jsx(yt,{as:Ht,allowPinchZoom:!0,shards:[o.contentRef],children:s.jsx(S.div,{"data-state":se(o.open),...r,ref:t,style:{pointerEvents:"auto",...r.style}})})}),$="DialogContent",Te=i.forwardRef((e,t)=>{const a=Ee($,e.__scopeDialog),{forceMount:r=a.forceMount,...o}=e,n=R($,e.__scopeDialog);return s.jsx(j,{present:r||n.open,children:n.modal?s.jsx(qt,{...o,ref:t}):s.jsx(Wt,{...o,ref:t})})});Te.displayName=$;var qt=i.forwardRef((e,t)=>{const a=R($,e.__scopeDialog),r=i.useRef(null),o=N(t,a.contentRef,r);return i.useEffect(()=>{const n=r.current;if(n)return xt(n)},[]),s.jsx(De,{...e,ref:o,trapFocus:a.open,disableOutsidePointerEvents:!0,onCloseAutoFocus:C(e.onCloseAutoFocus,n=>{var c;n.preventDefault(),(c=a.triggerRef.current)==null||c.focus()}),onPointerDownOutside:C(e.onPointerDownOutside,n=>{const c=n.detail.originalEvent,d=c.button===0&&c.ctrlKey===!0;(c.button===2||d)&&n.preventDefault()}),onFocusOutside:C(e.onFocusOutside,n=>n.preventDefault())})}),Wt=i.forwardRef((e,t)=>{const a=R($,e.__scopeDialog),r=i.useRef(!1),o=i.useRef(!1);return s.jsx(De,{...e,ref:t,trapFocus:!1,disableOutsidePointerEvents:!1,onCloseAutoFocus:n=>{var c,d;(c=e.onCloseAutoFocus)==null||c.call(e,n),n.defaultPrevented||(r.current||(d=a.triggerRef.current)==null||d.focus(),n.preventDefault()),r.current=!1,o.current=!1},onInteractOutside:n=>{var l,p;(l=e.onInteractOutside)==null||l.call(e,n),n.defaultPrevented||(r.current=!0,n.detail.originalEvent.type==="pointerdown"&&(o.current=!0));const c=n.target;((p=a.triggerRef.current)==null?void 0:p.contains(c))&&n.preventDefault(),n.detail.originalEvent.type==="focusin"&&o.current&&n.preventDefault()}})}),De=i.forwardRef((e,t)=>{const{__scopeDialog:a,trapFocus:r,onOpenAutoFocus:o,onCloseAutoFocus:n,...c}=e,d=R($,a),l=i.useRef(null),p=N(t,l);return bt(),s.jsxs(s.Fragment,{children:[s.jsx(Et,{asChild:!0,loop:!0,trapped:r,onMountAutoFocus:o,onUnmountAutoFocus:n,children:s.jsx(_e,{role:"dialog",id:d.contentId,"aria-describedby":d.descriptionId,"aria-labelledby":d.titleId,"data-state":se(d.open),...c,ref:p,onDismiss:()=>d.onOpenChange(!1)})}),s.jsxs(s.Fragment,{children:[s.jsx(Vt,{titleId:d.titleId}),s.jsx(Zt,{contentRef:l,descriptionId:d.descriptionId})]})]})}),oe="DialogTitle",Se=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=R(oe,a);return s.jsx(S.h2,{id:o.titleId,...r,ref:t})});Se.displayName=oe;var Ne="DialogDescription",Ae=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=R(Ne,a);return s.jsx(S.p,{id:o.descriptionId,...r,ref:t})});Ae.displayName=Ne;var ke="DialogClose",we=i.forwardRef((e,t)=>{const{__scopeDialog:a,...r}=e,o=R(ke,a);return s.jsx(S.button,{type:"button",...r,ref:t,onClick:C(e.onClick,()=>o.onOpenChange(!1))})});we.displayName=ke;function se(e){return e?"open":"closed"}var $e="DialogTitleWarning",[Bt,Ie]=Ct($e,{contentName:$,titleName:oe,docsSlug:"dialog"}),Vt=({titleId:e})=>{const t=Ie($e),a=`\`${t.contentName}\` requires a \`${t.titleName}\` for the component to be accessible for screen reader users.

If you want to hide the \`${t.titleName}\`, you can wrap it with our VisuallyHidden component.

For more information, see https://radix-ui.com/primitives/docs/components/${t.docsSlug}`;return i.useEffect(()=>{e&&(document.getElementById(e)||console.error(a))},[a,e]),null},Kt="DialogDescriptionWarning",Zt=({contentRef:e,descriptionId:t})=>{const r=`Warning: Missing \`Description\` or \`aria-describedby={undefined}\` for {${Ie(Kt).contentName}}.`;return i.useEffect(()=>{var n;const o=(n=e.current)==null?void 0:n.getAttribute("aria-describedby");t&&o&&(document.getElementById(t)||console.warn(r))},[r,e,t]),null},ne=ye,Pe=be,ie=Ce,U=Re,L=Te,G=Se,F=Ae,Z=we;const Hr=ne,Yt=ie,je=i.forwardRef(({className:e,...t},a)=>s.jsx(U,{className:v("fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",e),...t,ref:a}));je.displayName=U.displayName;const Xt=Rt("fixed z-50 gap-4 bg-background p-6 shadow-lg transition ease-in-out data-[state=closed]:duration-300 data-[state=open]:duration-500 data-[state=open]:animate-in data-[state=closed]:animate-out",{variants:{side:{top:"inset-x-0 top-0 border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top",bottom:"inset-x-0 bottom-0 border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom",left:"inset-y-0 left-0 h-full w-3/4 border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left sm:max-w-sm",right:"inset-y-0 right-0 h-full w-3/4 border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right sm:max-w-sm"}},defaultVariants:{side:"right"}}),Jt=i.forwardRef(({side:e="right",className:t,children:a,full:r=!1,hideCloseButton:o=!1,...n},c)=>s.jsxs(Yt,{children:[s.jsx(je,{}),s.jsxs(L,{ref:c,className:v(r?"fixed inset-0 z-50 bg-background p-0 shadow-lg transition ease-in-out data-[state=closed]:duration-300 data-[state=open]:duration-500 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right h-[100svh] w-screen max-w-none border-0":Xt({side:e}),t),...n,children:[!o&&s.jsxs(Z,{className:"absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-secondary",children:[s.jsx(fe,{className:"h-4 w-4"}),s.jsx("span",{className:"sr-only",children:"Close"})]}),a]})]}));Jt.displayName=L.displayName;const Qt=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col space-y-2 text-center sm:text-left",e),...t});Qt.displayName="SheetHeader";const ea=i.forwardRef(({className:e,...t},a)=>s.jsx(G,{ref:a,className:v("text-lg font-semibold text-foreground",e),...t}));ea.displayName=G.displayName;const ta=i.forwardRef(({className:e,...t},a)=>s.jsx(F,{ref:a,className:v("text-sm text-muted-foreground",e),...t}));ta.displayName=F.displayName;var aa=Symbol("radix.slottable");function ra(e){const t=({children:a})=>s.jsx(s.Fragment,{children:a});return t.displayName=`${e}.Slottable`,t.__radixId=aa,t}var Oe="AlertDialog",[oa]=V(Oe,[ve]),A=ve(),Me=e=>{const{__scopeAlertDialog:t,...a}=e,r=A(t);return s.jsx(ne,{...r,...a,modal:!0})};Me.displayName=Oe;var sa="AlertDialogTrigger",na=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=A(a);return s.jsx(Pe,{...o,...r,ref:t})});na.displayName=sa;var ia="AlertDialogPortal",Ue=e=>{const{__scopeAlertDialog:t,...a}=e,r=A(t);return s.jsx(ie,{...r,...a})};Ue.displayName=ia;var ca="AlertDialogOverlay",Le=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=A(a);return s.jsx(U,{...o,...r,ref:t})});Le.displayName=ca;var I="AlertDialogContent",[la,da]=oa(I),ua=ra("AlertDialogContent"),Ge=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,children:r,...o}=e,n=A(a),c=i.useRef(null),d=N(t,c),l=i.useRef(null);return s.jsx(Bt,{contentName:I,titleName:Fe,docsSlug:"alert-dialog",children:s.jsx(la,{scope:a,cancelRef:l,children:s.jsxs(L,{role:"alertdialog",...n,...o,ref:d,onOpenAutoFocus:C(o.onOpenAutoFocus,p=>{var _;p.preventDefault(),(_=l.current)==null||_.focus({preventScroll:!0})}),onPointerDownOutside:p=>p.preventDefault(),onInteractOutside:p=>p.preventDefault(),children:[s.jsx(ua,{children:r}),s.jsx(_a,{contentRef:c})]})})})});Ge.displayName=I;var Fe="AlertDialogTitle",He=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=A(a);return s.jsx(G,{...o,...r,ref:t})});He.displayName=Fe;var ze="AlertDialogDescription",qe=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=A(a);return s.jsx(F,{...o,...r,ref:t})});qe.displayName=ze;var pa="AlertDialogAction",We=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,o=A(a);return s.jsx(Z,{...o,...r,ref:t})});We.displayName=pa;var Be="AlertDialogCancel",Ve=i.forwardRef((e,t)=>{const{__scopeAlertDialog:a,...r}=e,{cancelRef:o}=da(Be,a),n=A(a),c=N(t,o);return s.jsx(Z,{...n,...r,ref:c})});Ve.displayName=Be;var _a=({contentRef:e})=>{const t=`\`${I}\` requires a description for the component to be accessible for screen reader users.

You can add a description to the \`${I}\` by passing a \`${ze}\` component as a child, which also benefits sighted users by adding visible context to the dialog.

Alternatively, you can use your own component as a description by assigning it an \`id\` and passing the same value to the \`aria-describedby\` prop in \`${I}\`. If the description is confusing or duplicative for sighted users, you can use the \`@radix-ui/react-visually-hidden\` primitive as a wrapper around your description component.

For more information, see https://radix-ui.com/primitives/docs/components/alert-dialog`;return i.useEffect(()=>{var r;document.getElementById((r=e.current)==null?void 0:r.getAttribute("aria-describedby"))||console.warn(t)},[t,e]),null},fa=Me,ma=Ue,Ke=Le,Ze=Ge,Ye=We,Xe=Ve,Je=He,Qe=qe;const zr=fa,ga=ma,et=i.forwardRef(({className:e,...t},a)=>s.jsx(Ke,{className:v("fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",e),...t,ref:a}));et.displayName=Ke.displayName;const ha=i.forwardRef(({className:e,...t},a)=>s.jsxs(ga,{children:[s.jsx(et,{}),s.jsx(Ze,{ref:a,className:v("fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border border-neutral-200 bg-white p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg dark:border-neutral-800 dark:bg-neutral-950",e),...t})]}));ha.displayName=Ze.displayName;const va=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col space-y-2 text-center sm:text-left",e),...t});va.displayName="AlertDialogHeader";const ya=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2",e),...t});ya.displayName="AlertDialogFooter";const xa=i.forwardRef(({className:e,...t},a)=>s.jsx(Je,{ref:a,className:v("text-lg font-semibold",e),...t}));xa.displayName=Je.displayName;const ba=i.forwardRef(({className:e,...t},a)=>s.jsx(Qe,{ref:a,className:v("text-sm text-neutral-500 dark:text-neutral-400",e),...t}));ba.displayName=Qe.displayName;const Ea=i.forwardRef(({className:e,...t},a)=>s.jsx(Ye,{ref:a,className:v(me(),e),...t}));Ea.displayName=Ye.displayName;const Ca=i.forwardRef(({className:e,...t},a)=>s.jsx(Xe,{ref:a,className:v(me({variant:"outline"}),e),...t}));Ca.displayName=Xe.displayName;const qr=ne,Wr=Pe,Ra=ie,tt=i.forwardRef(({className:e,...t},a)=>s.jsx(U,{ref:a,className:v("fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",e),...t}));tt.displayName=U.displayName;const Ta=i.forwardRef(({className:e,children:t,...a},r)=>s.jsxs(Ra,{children:[s.jsx(tt,{}),s.jsxs(L,{ref:r,className:v("fixed left-1/2 top-1/2 z-50 flex flex-col w-full max-w-lg -translate-x-1/2 -translate-y-1/2 border bg-background shadow-xl duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] rounded-xl sm:rounded-2xl overflow-hidden max-h-[90vh] sm:max-h-[90vh]",e),...a,children:[t,s.jsxs(Z,{className:"absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground z-10",children:[s.jsx(fe,{className:"h-4 w-4"}),s.jsx("span",{className:"sr-only",children:"Close"})]})]})]}));Ta.displayName=L.displayName;const Da=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col space-y-1.5 text-center sm:text-left px-4 py-3 border-b bg-background",e),...t});Da.displayName="DialogHeader";const Sa=({className:e,...t})=>s.jsx("div",{className:v("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2 px-4 py-4 border-t bg-background mt-auto",e),...t});Sa.displayName="DialogFooter";const Na=({className:e,...t})=>s.jsx("div",{className:v("flex-1 overflow-y-auto px-4 py-4",e),...t});Na.displayName="DialogBody";const Aa=i.forwardRef(({className:e,...t},a)=>s.jsx(G,{ref:a,className:v("text-lg font-semibold leading-none tracking-tight",e),...t}));Aa.displayName=G.displayName;const ka=i.forwardRef(({className:e,...t},a)=>s.jsx(F,{ref:a,className:v("text-sm text-muted-foreground",e),...t}));ka.displayName=F.displayName;var Y="Checkbox",[wa]=V(Y),[$a,ce]=wa(Y);function Ia(e){const{__scopeCheckbox:t,checked:a,children:r,defaultChecked:o,disabled:n,form:c,name:d,onCheckedChange:l,required:p,value:_="on",internal_do_not_use_render:f}=e,[g,m]=ae({prop:a,defaultProp:o??!1,onChange:l,caller:Y}),[x,b]=i.useState(null),[E,y]=i.useState(null),h=i.useRef(!1),T=x?!!c||!!x.closest("form"):!0,D={checked:g,disabled:n,setChecked:m,control:x,setControl:b,name:d,form:c,value:_,hasConsumerStoppedPropagationRef:h,required:p,defaultChecked:w(o)?!1:o,isFormControl:T,bubbleInput:E,setBubbleInput:y};return s.jsx($a,{scope:t,...D,children:Pa(f)?f(D):r})}var at="CheckboxTrigger",rt=i.forwardRef(({__scopeCheckbox:e,onKeyDown:t,onClick:a,...r},o)=>{const{control:n,value:c,disabled:d,checked:l,required:p,setControl:_,setChecked:f,hasConsumerStoppedPropagationRef:g,isFormControl:m,bubbleInput:x}=ce(at,e),b=N(o,_),E=i.useRef(l);return i.useEffect(()=>{const y=n==null?void 0:n.form;if(y){const h=()=>f(E.current);return y.addEventListener("reset",h),()=>y.removeEventListener("reset",h)}},[n,f]),s.jsx(S.button,{type:"button",role:"checkbox","aria-checked":w(l)?"mixed":l,"aria-required":p,"data-state":ct(l),"data-disabled":d?"":void 0,disabled:d,value:c,...r,ref:b,onKeyDown:C(t,y=>{y.key==="Enter"&&y.preventDefault()}),onClick:C(a,y=>{f(h=>w(h)?!0:!h),x&&m&&(g.current=y.isPropagationStopped(),g.current||y.stopPropagation())})})});rt.displayName=at;var le=i.forwardRef((e,t)=>{const{__scopeCheckbox:a,name:r,checked:o,defaultChecked:n,required:c,disabled:d,value:l,onCheckedChange:p,form:_,...f}=e;return s.jsx(Ia,{__scopeCheckbox:a,checked:o,defaultChecked:n,disabled:d,required:c,onCheckedChange:p,name:r,form:_,value:l,internal_do_not_use_render:({isFormControl:g})=>s.jsxs(s.Fragment,{children:[s.jsx(rt,{...f,ref:t,__scopeCheckbox:a}),g&&s.jsx(it,{__scopeCheckbox:a})]})})});le.displayName=Y;var ot="CheckboxIndicator",st=i.forwardRef((e,t)=>{const{__scopeCheckbox:a,forceMount:r,...o}=e,n=ce(ot,a);return s.jsx(j,{present:r||w(n.checked)||n.checked===!0,children:s.jsx(S.span,{"data-state":ct(n.checked),"data-disabled":n.disabled?"":void 0,...o,ref:t,style:{pointerEvents:"none",...e.style}})})});st.displayName=ot;var nt="CheckboxBubbleInput",it=i.forwardRef(({__scopeCheckbox:e,...t},a)=>{const{control:r,hasConsumerStoppedPropagationRef:o,checked:n,defaultChecked:c,required:d,disabled:l,name:p,value:_,form:f,bubbleInput:g,setBubbleInput:m}=ce(nt,e),x=N(a,m),b=Tt(n),E=Dt(r);i.useEffect(()=>{const h=g;if(!h)return;const T=window.HTMLInputElement.prototype,k=Object.getOwnPropertyDescriptor(T,"checked").set,z=!o.current;if(b!==n&&k){const q=new Event("click",{bubbles:z});h.indeterminate=w(n),k.call(h,w(n)?!1:n),h.dispatchEvent(q)}},[g,b,n,o]);const y=i.useRef(w(n)?!1:n);return s.jsx(S.input,{type:"checkbox","aria-hidden":!0,defaultChecked:c??y.current,required:d,disabled:l,name:p,value:_,form:f,...t,tabIndex:-1,ref:x,style:{...t.style,...E,position:"absolute",pointerEvents:"none",opacity:0,margin:0,transform:"translateX(-100%)"}})});it.displayName=nt;function Pa(e){return typeof e=="function"}function w(e){return e==="indeterminate"}function ct(e){return w(e)?"indeterminate":e?"checked":"unchecked"}const ja=i.forwardRef(({className:e,...t},a)=>s.jsx(le,{ref:a,className:v("peer h-4 w-4 shrink-0 rounded-sm border border-primary shadow focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground",e),...t,children:s.jsx(st,{className:v("flex items-center justify-center text-current"),children:s.jsx(St,{className:"h-4 w-4"})})}));ja.displayName=le.displayName;/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Oa=[["path",{d:"M20 6 9 17l-5-5",key:"1gmf2c"}]],Br=M("check",Oa);/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ma=[["path",{d:"m6 9 6 6 6-6",key:"qrunsl"}]],Vr=M("chevron-down",Ma);/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ua=[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["line",{x1:"12",x2:"12",y1:"8",y2:"12",key:"1pkeuh"}],["line",{x1:"12",x2:"12.01",y1:"16",y2:"16",key:"4dfq90"}]],Kr=M("circle-alert",Ua);/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const La=[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m9 12 2 2 4-4",key:"dzmm74"}]],Zr=M("circle-check",La);/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ga=[["path",{d:"M21 12a9 9 0 1 1-6.219-8.56",key:"13zald"}]],Yr=M("loader-circle",Ga);var Fa=Symbol("radix.slottable");function Ha(e){const t=({children:a})=>s.jsx(s.Fragment,{children:a});return t.displayName=`${e}.Slottable`,t.__radixId=Fa,t}var[X]=V("Tooltip",[ge]),J=ge(),lt="TooltipProvider",za=700,ee="tooltip.open",[qa,de]=X(lt),dt=e=>{const{__scopeTooltip:t,delayDuration:a=za,skipDelayDuration:r=300,disableHoverableContent:o=!1,children:n}=e,c=i.useRef(!0),d=i.useRef(!1),l=i.useRef(0);return i.useEffect(()=>{const p=l.current;return()=>window.clearTimeout(p)},[]),s.jsx(qa,{scope:t,isOpenDelayedRef:c,delayDuration:a,onOpen:i.useCallback(()=>{window.clearTimeout(l.current),c.current=!1},[]),onClose:i.useCallback(()=>{window.clearTimeout(l.current),l.current=window.setTimeout(()=>c.current=!0,r)},[r]),isPointerInTransitRef:d,onPointerInTransitChange:i.useCallback(p=>{d.current=p},[]),disableHoverableContent:o,children:n})};dt.displayName=lt;var O="Tooltip",[Wa,H]=X(O),ut=e=>{const{__scopeTooltip:t,children:a,open:r,defaultOpen:o,onOpenChange:n,disableHoverableContent:c,delayDuration:d}=e,l=de(O,e.__scopeTooltip),p=J(t),[_,f]=i.useState(null),g=W(),m=i.useRef(0),x=c??l.disableHoverableContent,b=d??l.delayDuration,E=i.useRef(!1),[y,h]=ae({prop:r,defaultProp:o??!1,onChange:q=>{q?(l.onOpen(),document.dispatchEvent(new CustomEvent(ee))):l.onClose(),n==null||n(q)},caller:O}),T=i.useMemo(()=>y?E.current?"delayed-open":"instant-open":"closed",[y]),D=i.useCallback(()=>{window.clearTimeout(m.current),m.current=0,E.current=!1,h(!0)},[h]),k=i.useCallback(()=>{window.clearTimeout(m.current),m.current=0,h(!1)},[h]),z=i.useCallback(()=>{window.clearTimeout(m.current),m.current=window.setTimeout(()=>{E.current=!0,h(!0),m.current=0},b)},[b,h]);return i.useEffect(()=>()=>{m.current&&(window.clearTimeout(m.current),m.current=0)},[]),s.jsx(kt,{...p,children:s.jsx(Wa,{scope:t,contentId:g,open:y,stateAttribute:T,trigger:_,onTriggerChange:f,onTriggerEnter:i.useCallback(()=>{l.isOpenDelayedRef.current?z():D()},[l.isOpenDelayedRef,z,D]),onTriggerLeave:i.useCallback(()=>{x?k():(window.clearTimeout(m.current),m.current=0)},[k,x]),onOpen:D,onClose:k,disableHoverableContent:x,children:a})})};ut.displayName=O;var te="TooltipTrigger",pt=i.forwardRef((e,t)=>{const{__scopeTooltip:a,...r}=e,o=H(te,a),n=de(te,a),c=J(a),d=i.useRef(null),l=N(t,d,o.onTriggerChange),p=i.useRef(!1),_=i.useRef(!1),f=i.useCallback(()=>p.current=!1,[]);return i.useEffect(()=>()=>document.removeEventListener("pointerup",f),[f]),s.jsx(wt,{asChild:!0,...c,children:s.jsx(S.button,{"aria-describedby":o.open?o.contentId:void 0,"data-state":o.stateAttribute,...r,ref:l,onPointerMove:C(e.onPointerMove,g=>{g.pointerType!=="touch"&&!_.current&&!n.isPointerInTransitRef.current&&(o.onTriggerEnter(),_.current=!0)}),onPointerLeave:C(e.onPointerLeave,()=>{o.onTriggerLeave(),_.current=!1}),onPointerDown:C(e.onPointerDown,()=>{o.open&&o.onClose(),p.current=!0,document.addEventListener("pointerup",f,{once:!0})}),onFocus:C(e.onFocus,()=>{p.current||o.onOpen()}),onBlur:C(e.onBlur,o.onClose),onClick:C(e.onClick,o.onClose)})})});pt.displayName=te;var ue="TooltipPortal",[Ba,Va]=X(ue,{forceMount:void 0}),_t=e=>{const{__scopeTooltip:t,forceMount:a,children:r,container:o}=e,n=H(ue,t);return s.jsx(Ba,{scope:t,forceMount:a,children:s.jsx(j,{present:a||n.open,children:s.jsx(pe,{asChild:!0,container:o,children:r})})})};_t.displayName=ue;var P="TooltipContent",ft=i.forwardRef((e,t)=>{const a=Va(P,e.__scopeTooltip),{forceMount:r=a.forceMount,side:o="top",...n}=e,c=H(P,e.__scopeTooltip);return s.jsx(j,{present:r||c.open,children:c.disableHoverableContent?s.jsx(mt,{side:o,...n,ref:t}):s.jsx(Ka,{side:o,...n,ref:t})})}),Ka=i.forwardRef((e,t)=>{const a=H(P,e.__scopeTooltip),r=de(P,e.__scopeTooltip),o=i.useRef(null),n=N(t,o),[c,d]=i.useState(null),{trigger:l,onClose:p}=a,_=o.current,{onPointerInTransitChange:f}=r,g=i.useCallback(()=>{d(null),f(!1)},[f]),m=i.useCallback((x,b)=>{const E=x.currentTarget,y={x:x.clientX,y:x.clientY},h=Qa(y,E.getBoundingClientRect()),T=er(y,h),D=tr(b.getBoundingClientRect()),k=rr([...T,...D]);d(k),f(!0)},[f]);return i.useEffect(()=>()=>g(),[g]),i.useEffect(()=>{if(l&&_){const x=E=>m(E,_),b=E=>m(E,l);return l.addEventListener("pointerleave",x),_.addEventListener("pointerleave",b),()=>{l.removeEventListener("pointerleave",x),_.removeEventListener("pointerleave",b)}}},[l,_,m,g]),i.useEffect(()=>{if(c){const x=b=>{const E=b.target,y={x:b.clientX,y:b.clientY},h=(l==null?void 0:l.contains(E))||(_==null?void 0:_.contains(E)),T=!ar(y,c);h?g():T&&(g(),p())};return document.addEventListener("pointermove",x),()=>document.removeEventListener("pointermove",x)}},[l,_,c,p,g]),s.jsx(mt,{...e,ref:n})}),[Za,Ya]=X(O,{isInside:!1}),Xa=Ha("TooltipContent"),mt=i.forwardRef((e,t)=>{const{__scopeTooltip:a,children:r,"aria-label":o,onEscapeKeyDown:n,onPointerDownOutside:c,...d}=e,l=H(P,a),p=J(a),{onClose:_}=l;return i.useEffect(()=>(document.addEventListener(ee,_),()=>document.removeEventListener(ee,_)),[_]),i.useEffect(()=>{if(l.trigger){const f=g=>{const m=g.target;m!=null&&m.contains(l.trigger)&&_()};return window.addEventListener("scroll",f,{capture:!0}),()=>window.removeEventListener("scroll",f,{capture:!0})}},[l.trigger,_]),s.jsx(_e,{asChild:!0,disableOutsidePointerEvents:!1,onEscapeKeyDown:n,onPointerDownOutside:c,onFocusOutside:f=>f.preventDefault(),onDismiss:_,children:s.jsxs(Nt,{"data-state":l.stateAttribute,...p,...d,ref:t,style:{...d.style,"--radix-tooltip-content-transform-origin":"var(--radix-popper-transform-origin)","--radix-tooltip-content-available-width":"var(--radix-popper-available-width)","--radix-tooltip-content-available-height":"var(--radix-popper-available-height)","--radix-tooltip-trigger-width":"var(--radix-popper-anchor-width)","--radix-tooltip-trigger-height":"var(--radix-popper-anchor-height)"},children:[s.jsx(Xa,{children:r}),s.jsx(Za,{scope:a,isInside:!0,children:s.jsx(At,{id:l.contentId,role:"tooltip",children:o||r})})]})})});ft.displayName=P;var gt="TooltipArrow",Ja=i.forwardRef((e,t)=>{const{__scopeTooltip:a,...r}=e,o=J(a);return Ya(gt,a).isInside?null:s.jsx($t,{...o,...r,ref:t})});Ja.displayName=gt;function Qa(e,t){const a=Math.abs(t.top-e.y),r=Math.abs(t.bottom-e.y),o=Math.abs(t.right-e.x),n=Math.abs(t.left-e.x);switch(Math.min(a,r,o,n)){case n:return"left";case o:return"right";case a:return"top";case r:return"bottom";default:throw new Error("unreachable")}}function er(e,t,a=5){const r=[];switch(t){case"top":r.push({x:e.x-a,y:e.y+a},{x:e.x+a,y:e.y+a});break;case"bottom":r.push({x:e.x-a,y:e.y-a},{x:e.x+a,y:e.y-a});break;case"left":r.push({x:e.x+a,y:e.y-a},{x:e.x+a,y:e.y+a});break;case"right":r.push({x:e.x-a,y:e.y-a},{x:e.x-a,y:e.y+a});break}return r}function tr(e){const{top:t,right:a,bottom:r,left:o}=e;return[{x:o,y:t},{x:a,y:t},{x:a,y:r},{x:o,y:r}]}function ar(e,t){const{x:a,y:r}=e;let o=!1;for(let n=0,c=t.length-1;n<t.length;c=n++){const d=t[n],l=t[c],p=d.x,_=d.y,f=l.x,g=l.y;_>r!=g>r&&a<(f-p)*(r-_)/(g-_)+p&&(o=!o)}return o}function rr(e){const t=e.slice();return t.sort((a,r)=>a.x<r.x?-1:a.x>r.x?1:a.y<r.y?-1:a.y>r.y?1:0),or(t)}function or(e){if(e.length<=1)return e.slice();const t=[];for(let r=0;r<e.length;r++){const o=e[r];for(;t.length>=2;){const n=t[t.length-1],c=t[t.length-2];if((n.x-c.x)*(o.y-c.y)>=(n.y-c.y)*(o.x-c.x))t.pop();else break}t.push(o)}t.pop();const a=[];for(let r=e.length-1;r>=0;r--){const o=e[r];for(;a.length>=2;){const n=a[a.length-1],c=a[a.length-2];if((n.x-c.x)*(o.y-c.y)>=(n.y-c.y)*(o.x-c.x))a.pop();else break}a.push(o)}return a.pop(),t.length===1&&a.length===1&&t[0].x===a[0].x&&t[0].y===a[0].y?t:t.concat(a)}var sr=dt,nr=ut,ir=pt,cr=_t,ht=ft;const Xr=sr,Jr=nr,Qr=ir,lr=i.forwardRef(({className:e,sideOffset:t=4,...a},r)=>s.jsx(cr,{children:s.jsx(ht,{ref:r,sideOffset:t,className:v("z-50 overflow-hidden rounded-md bg-neutral-900 px-3 py-1.5 text-xs text-neutral-50 animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 dark:bg-neutral-50 dark:text-neutral-900",e),...a})}));lr.displayName=ht.displayName;function eo(){const{token:e}=It(),t=Q.useMemo(()=>({accessToken:e,testMode:!1,orgId:void 0,error:void 0}),[e]);return{query:Q.useMemo(()=>({data:t,isLoading:!1,isError:!1,isSuccess:!0,error:null,status:"success",refetch:()=>Promise.resolve({data:t})}),[t]),isAuthenticated:!0,isLoading:!1}}Q.createContext({session:null,isAuthenticated:!0,isLoading:!1});export{Ar as $,zr as A,Ur as B,L as C,F as D,Mr as E,Or as F,jr as G,ea as H,ta as I,Sa as J,Hr as K,Yr as L,Yt as M,Jt as N,U as O,ie as P,Zr as Q,ne as R,Qt as S,G as T,Vr as U,mr as V,fr as W,_r as X,ur as Y,wr as Z,kr as _,ha as a,Ir as a0,$r as a1,Nr as a2,Sr as a3,Dr as a4,Tr as a5,Rr as a6,Cr as a7,Er as a8,br as a9,xr as aa,yr as ab,vr as ac,hr as ad,gr as ae,pr as af,Na as ag,va as b,xa as c,ba as d,ya as e,Ca as f,Ea as g,qr as h,Wr as i,Ra as j,Ta as k,Da as l,Aa as m,ka as n,ja as o,Xr as p,Jr as q,Qr as r,lr as s,Br as t,eo as u,Kr as v,Pr as w,Fr as x,Gr as y,Lr as z};
