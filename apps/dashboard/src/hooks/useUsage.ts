import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { useActiveOrganization } from '@/hooks/useAuth'

const GET_ORGANIZATION_USAGE = `
  query get_organization($id: String!, $usage: UsageFilter) {
    organization(id: $id) {
      id
      name
      usage(filter: $usage) {
        members
        order_volume
        total_errors
        total_requests
        total_trackers
        total_shipments
        unfulfilled_orders
        total_shipping_spend
        api_errors {
          label
          count
          date
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
        tracker_count {
          date
          label
          count
        }
        shipping_spend {
          date
          label
          count
        }
      }
    }
  }
`

export interface UsageFilter {
  date_after?: string
  date_before?: string
}

export interface UsageDataPoint {
  label: string
  count: number
  date: string
}

export interface OrganizationUsage {
  members: number
  total_errors: number
  order_volume: number
  total_requests: number
  total_trackers: number
  total_shipments: number
  unfulfilled_orders: number
  total_shipping_spend: number
  api_errors: Array<UsageDataPoint>
  api_requests: Array<UsageDataPoint>
  order_volumes: Array<UsageDataPoint>
  shipment_count: Array<UsageDataPoint>
  tracker_count: Array<UsageDataPoint>
  shipping_spend: Array<UsageDataPoint>
}

export function useOrganizationUsage(filter?: UsageFilter) {
  const { orgId } = useActiveOrganization()

  return useQuery({
    queryKey: ['organization_usage', orgId, filter],
    queryFn: async () => {
      if (!orgId) {
        throw new Error('No organization ID available')
      }

      const data = await api.graphql<{
        organization: {
          id: string
          name: string
          usage: OrganizationUsage
        }
      }>(GET_ORGANIZATION_USAGE, {
        id: orgId,
        usage: filter
      })

      return data.organization.usage
    },
    enabled: !!orgId,
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

// Legacy export for backwards compatibility - now redirects to organization usage
export function useSystemUsage(filter?: UsageFilter) {
  return useOrganizationUsage(filter)
}
