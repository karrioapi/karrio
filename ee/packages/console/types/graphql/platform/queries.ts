import gql from "graphql-tag";

// -----------------------------------------------------------
// Tenant queries and mutations
// -----------------------------------------------------------
//#region

export const GET_TENANT = gql`
  query GetTenant($id: String!) {
    tenant(id: $id) {
      object_type
      id
      name
      schema_name
      feature_flags
      app_domains
      created_at
      updated_at
      usage {
        total_errors
        order_volume
        total_requests
        total_trackers
        total_shipments
        organization_count
        user_count
        total_shipping_spend
        api_errors {
          date
          label
          count
        }
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
        shipping_spend {
          date
          label
          count
        }
        tracker_count {
          date
          label
          count
        }
      }
      domains {
        object_type
        id
        domain
        is_primary
      }
      api_domains
    }
  }
`;

export const GET_TENANTS = gql`
  query GetTenants($filter: TenantFilter) {
    tenants(filter: $filter) {
      page_info {
        count
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
      edges {
        node {
          object_type
          id
          name
          schema_name
          feature_flags
          app_domains
          created_at
          updated_at
          usage {
            total_errors
            order_volume
            total_requests
            total_trackers
            total_shipments
            organization_count
            user_count
            total_shipping_spend
            api_errors {
              date
              label
              count
            }
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
            shipping_spend {
              date
              label
              count
            }
            tracker_count {
              date
              label
              count
            }
          }
          domains {
            object_type
            id
            domain
            is_primary
          }
          api_domains
        }
        cursor
      }
    }
  }
`;

export const CREATE_TENANT = gql`
  mutation CreateTenant($input: CreateTenantMutationInput!) {
    create_tenant(input: $input) {
      errors {
        field
        messages
      }
      tenant {
        object_type
        id
        name
        schema_name
        feature_flags
        app_domains
        created_at
        updated_at
        usage {
          total_errors
          order_volume
          total_requests
          total_trackers
          total_shipments
          organization_count
          user_count
          total_shipping_spend
          api_errors {
            date
            label
            count
          }
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
          shipping_spend {
            date
            label
            count
          }
          tracker_count {
            date
            label
            count
          }
        }
        domains {
          object_type
          id
          domain
          is_primary
        }
        api_domains
      }
    }
  }
`;

export const UPDATE_TENANT = gql`
  mutation UpdateTenant($input: UpdateTenantMutationInput!) {
    update_tenant(input: $input) {
      errors {
        field
        messages
      }
      tenant {
        object_type
        id
        name
        schema_name
        feature_flags
        app_domains
        created_at
        updated_at
        usage {
          total_errors
          order_volume
          total_requests
          total_trackers
          total_shipments
          organization_count
          user_count
          total_shipping_spend
          api_errors {
            date
            label
            count
          }
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
          shipping_spend {
            date
            label
            count
          }
          tracker_count {
            date
            label
            count
          }
        }
        domains {
          object_type
          id
          domain
          is_primary
        }
        api_domains
      }
    }
  }
`;

export const DELETE_TENANT = gql`
  mutation DeleteTenant($input: DeleteTenantMutationInput!) {
    delete_tenant(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;

//#endregion

// -----------------------------------------------------------
// Domain queries and mutations
// -----------------------------------------------------------
//#region

export const ADD_CUSTOM_DOMAIN = gql`
  mutation AddCustomDomain($input: AddCustomDomainMutationInput!) {
    add_custom_domain(input: $input) {
      errors {
        field
        messages
      }
      domain {
        object_type
        id
        domain
        is_primary
      }
    }
  }
`;

export const UPDATE_CUSTOM_DOMAIN = gql`
  mutation UpdateCustomDomain($input: UpdateCustomDomainMutationInput!) {
    update_custom_domain(input: $input) {
      errors {
        field
        messages
      }
      domain {
        object_type
        id
        domain
        is_primary
      }
    }
  }
`;

export const DELETE_CUSTOM_DOMAIN = gql`
  mutation DeleteCustomDomain($input: DeleteCustomDomainMutationInput!) {
    delete_custom_domain(input: $input) {
      errors {
        field
        messages
      }
      id
    }
  }
`;

//#endregion

// -----------------------------------------------------------
// Usage Stats queries
// -----------------------------------------------------------
//#region

export const GET_USAGE_STATS = gql`
  query GetUsageStats($tenant_id: String!, $filter: UsageFilter) {
    usage_stats(tenant_id: $tenant_id, filter: $filter) {
      total_errors
      order_volume
      total_requests
      total_trackers
      total_shipments
      organization_count
      user_count
      total_shipping_spend
      api_errors {
        date
        label
        count
      }
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
      shipping_spend {
        date
        label
        count
      }
      tracker_count {
        date
        label
        count
      }
    }
  }
`;

//#endregion

// -----------------------------------------------------------
// Account Management Mutations
// -----------------------------------------------------------
//#region

export const RESET_TENANT_ADMIN_PASSWORD = gql`
  mutation ResetTenantAdminPassword(
    $input: ResetTenantAdminPasswordMutationInput!
  ) {
    reset_tenant_admin_password(input: $input) {
      errors {
        field
        messages
      }
      success
    }
  }
`;

//#endregion

// -----------------------------------------------------------
// Connected Account queries and mutations
// -----------------------------------------------------------
//#region

export const GET_CONNECTED_ACCOUNT = gql`
  query GetConnectedAccount($tenant_id: String!, $id: String!) {
    connected_account(tenant_id: $tenant_id, id: $id) {
      id
      name
      slug
      is_active
      created
      modified
      usage {
        total_errors
        order_volume
        total_requests
        total_trackers
        total_shipments
        members
        unfulfilled_orders
        total_shipping_spend
        api_errors {
          date
          label
          count
        }
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
        shipping_spend {
          date
          label
          count
        }
        tracker_count {
          date
          label
          count
        }
      }
    }
  }
`;

export const GET_CONNECTED_ACCOUNTS = gql`
  query GetConnectedAccounts($tenant_id: String!, $filter: AccountFilter) {
    connected_accounts(tenant_id: $tenant_id, filter: $filter) {
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
            total_errors
            order_volume
            total_requests
            total_trackers
            total_shipments
            members
            unfulfilled_orders
            total_shipping_spend
            api_errors {
              date
              label
              count
            }
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
            shipping_spend {
              date
              label
              count
            }
            tracker_count {
              date
              label
              count
            }
          }
        }
        cursor
      }
    }
  }
`;

//#endregion
