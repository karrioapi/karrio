import{g as r,u as l,a as g,o as c,b as d,c as h,d as p,e as f,j as s,r as _,K as k,A as v,T as M}from"./chunks/globals-NA-RwBT2.js";import{R as b,u as $,a as y}from"./chunks/rate-sheet-editor-ILMFNqdQ.js";import"./chunks/tooltip-DR24atVF.js";const E=r`
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
          meta
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
`;r`
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
      meta
      metadata
      usage {
        total_shipments
        total_addons_charges
      }
    }
  }
`;r`
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
`;r`
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
`;r`
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
`;r`
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
`;r`
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
`;const A=r`
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
        meta
        metadata
      }
    }
  }
`,C=r`
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
        meta
        metadata
      }
    }
  }
`,I=r`
  mutation DeleteMarkup($input: DeleteMutationInput!) {
    delete_markup(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;r`
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
`;r`
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
`;r`
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
`;r`
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
`;r`
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
`;function q(a=!0){var e,u,o;const{graphqlRequest:i}=l(),t=g({queryKey:["admin_markups"],queryFn:()=>i(d(E),{filter:{}}),enabled:a,onError:c}),n=((o=(u=(e=t.data)==null?void 0:e.markups)==null?void 0:u.edges)==null?void 0:o.map(m=>m.node))||[];return{query:t,markups:n}}function z(){const a=h(),{graphqlRequest:i}=l(),t=()=>{a.invalidateQueries(["admin_markups"])},n=p(o=>i(d(A),{input:o}),{onSuccess:t,onError:c}),e=p(o=>i(d(C),{input:o}),{onSuccess:t,onError:c}),u=p(o=>i(d(I),{input:o}),{onSuccess:t,onError:c});return{createMarkup:n,updateMarkup:e,deleteMarkup:u}}function R({config:a}){const i=()=>{window.parent.postMessage({source:"karrio-embed",type:"EVENT",event:"close"},"*")};return s.jsx(k,{host:a.host,token:a.token,admin:a.admin,children:s.jsxs(v,{children:[s.jsx(S,{config:a,onClose:i}),s.jsx(M,{})]})})}function S({config:a,onClose:i}){const t=!!a.admin,{markups:n}=q(t),e=z();return s.jsx(b,{rateSheetId:a.rateSheetId||"new",onClose:i,preloadCarrier:a.carrier,linkConnectionId:a.connectionId,isAdmin:t,useRateSheet:y,useRateSheetMutation:$,markups:t?n:void 0,markupMutations:t?e:void 0})}function x(){const[a,i]=_.useState(null);return _.useEffect(()=>{const t=n=>{const{data:e}=n;(e==null?void 0:e.source)==="karrio-host"&&e.type==="INIT"&&i({host:e.host,token:e.token,rateSheetId:e.rateSheetId,carrier:e.carrier,connectionId:e.connectionId,admin:e.admin??!1})};return window.addEventListener("message",t),window.parent.postMessage({source:"karrio-embed",type:"READY"},"*"),()=>window.removeEventListener("message",t)},[]),_.useEffect(()=>{const t=new ResizeObserver(n=>{for(const e of n)window.parent.postMessage({source:"karrio-embed",type:"RESIZE",height:e.contentRect.height},"*")});return t.observe(document.body),()=>t.disconnect()},[]),a?s.jsx(R,{config:a}):s.jsx("div",{className:"flex items-center justify-center h-screen",children:s.jsx("div",{className:"animate-spin rounded-full h-8 w-8 border-b-2 border-gray-400"})})}const w=f(document.getElementById("root"));w.render(s.jsx(x,{}));
