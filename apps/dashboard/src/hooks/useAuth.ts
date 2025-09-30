import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

const GET_USER = `
  query get_user {
    user {
      id
      email
      full_name
      is_admin
      is_owner
      is_active
      date_joined
      last_login
    }
  }
`

const GET_ORGANIZATIONS = `
  query get_organizations($filter: OrganizationFilter) {
    organizations(filter: $filter) {
      edges {
        node {
          id
          name
          slug
          current_user {
            email
            full_name
            is_admin
            is_owner
          }
        }
      }
    }
  }
`

export interface User {
  id: string
  email: string
  full_name: string
  is_admin: boolean
  is_owner: boolean
  is_active: boolean
  date_joined: string
  last_login?: string
}

export interface Organization {
  id: string
  name: string
  slug: string
  current_user: {
    email: string
    full_name: string
    is_admin: boolean
    is_owner: boolean
  }
}

export function useUser() {
  return useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      const data = await api.graphql<{
        user: User
      }>(GET_USER)

      return data.user
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false,
  })
}

export function useOrganizations() {
  return useQuery({
    queryKey: ['organizations'],
    queryFn: async () => {
      const data = await api.graphql<{
        organizations: {
          edges: Array<{ node: Organization }>
        }
      }>(GET_ORGANIZATIONS, { filter: { is_active: true } })

      return {
        organizations: data.organizations.edges.map(edge => edge.node),
      }
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false,
  })
}

// Get the active organization from local storage or cookies
// In a real app, this might come from a context provider or session
export function useActiveOrganization() {
  const { data: organizations } = useOrganizations()

  // For now, just return the first organization
  // In a real multi-org app, this would come from session/context
  const activeOrganization = organizations?.organizations?.[0]

  return {
    organization: activeOrganization,
    orgId: activeOrganization?.id,
  }
}