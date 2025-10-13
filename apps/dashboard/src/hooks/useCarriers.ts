import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'

// GraphQL Queries
const GET_USER_CONNECTIONS = `
  query get_user_connections($filter: CarrierFilter) {
    user_connections(filter: $filter) {
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
          carrier_id
          carrier_name
          display_name
          test_mode
          active
          capabilities
          credentials
          config
          metadata
        }
      }
    }
  }
`

const GET_SYSTEM_CONNECTIONS = `
  query get_system_connections($filter: CarrierFilter) {
    system_connections(filter: $filter) {
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
          carrier_id
          carrier_name
          display_name
          test_mode
          active
          capabilities
          config
        }
      }
    }
  }
`

const CREATE_CARRIER_CONNECTION = `
  mutation create_carrier_connection($data: CreateCarrierConnectionMutationInput!) {
    create_carrier_connection(input: $data) {
      connection {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        credentials
        config
        metadata
      }
      errors {
        field
        messages
      }
    }
  }
`

const UPDATE_CARRIER_CONNECTION = `
  mutation update_carrier_connection($data: UpdateCarrierConnectionMutationInput!) {
    update_carrier_connection(input: $data) {
      connection {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        credentials
        config
        metadata
      }
      errors {
        field
        messages
      }
    }
  }
`

const DELETE_CARRIER_CONNECTION = `
  mutation delete_carrier_connection($data: DeleteMutationInput!) {
    delete_carrier_connection(input: $data) {
      id
      errors {
        field
        messages
      }
    }
  }
`

// Types
export interface CarrierConnection {
  id: string
  carrier_id: string
  carrier_name: string
  display_name: string
  test_mode: boolean
  active: boolean
  capabilities: Array<string>
  credentials: Record<string, any>
  config: Record<string, any>
  metadata: Record<string, any>
}

export interface CarrierFilter {
  keyword?: string
  active?: boolean
  test_mode?: boolean
  carrier_name?: Array<string>
}

export interface CreateCarrierConnectionInput {
  carrier_name: string
  carrier_id?: string
  display_name?: string
  test_mode?: boolean
  active?: boolean
  capabilities?: Array<string>
  credentials: Record<string, any>
  config?: Record<string, any>
  metadata?: Record<string, any>
}

export interface UpdateCarrierConnectionInput {
  id: string
  carrier_id?: string
  display_name?: string
  test_mode?: boolean
  active?: boolean
  capabilities?: Array<string>
  credentials?: Record<string, any>
  config?: Record<string, any>
  metadata?: Record<string, any>
}

// Hooks
export function useCarrierConnections(filter?: CarrierFilter) {
  return useQuery({
    queryKey: ['user_connections', filter],
    queryFn: async () => {
      const data = await api.graphql<{
        user_connections: {
          edges: Array<{ node: CarrierConnection }>
          page_info: any
        }
      }>(GET_USER_CONNECTIONS, { filter })

      return {
        connections: data.user_connections.edges.map((edge) => edge.node),
        pageInfo: data.user_connections.page_info,
      }
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useSystemConnections(filter?: CarrierFilter) {
  return useQuery({
    queryKey: ['system_connections', filter],
    queryFn: async () => {
      const data = await api.graphql<{
        system_connections: {
          edges: Array<{ node: CarrierConnection }>
          page_info: any
        }
      }>(GET_SYSTEM_CONNECTIONS, { filter })

      return {
        connections: data.system_connections.edges.map((edge) => edge.node),
        pageInfo: data.system_connections.page_info,
      }
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useCarrierConnection(id: string) {
  const { data: userConnections } = useCarrierConnections()
  const { data: systemConnections } = useSystemConnections()

  const allConnections = [
    ...(userConnections?.connections || []),
    ...(systemConnections?.connections || []),
  ]

  return allConnections.find((connection) => connection.id === id)
}

export function useCreateCarrierConnection() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: CreateCarrierConnectionInput) => {
      const result = await api.graphql<{
        create_carrier_connection: {
          connection: CarrierConnection
          errors: Array<{ field: string; messages: Array<string> }> | null
        }
      }>(CREATE_CARRIER_CONNECTION, { data })

      if (result.create_carrier_connection.errors && result.create_carrier_connection.errors.length > 0) {
        throw new Error(
          result.create_carrier_connection.errors
            .map((e) => e.messages.join(', '))
            .join('; '),
        )
      }

      return result.create_carrier_connection.connection
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['user_connections'],
        refetchType: 'active'
      })
    },
  })
}

export function useUpdateCarrierConnection() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: UpdateCarrierConnectionInput) => {
      const result = await api.graphql<{
        update_carrier_connection: {
          connection: CarrierConnection
          errors: Array<{ field: string; messages: Array<string> }> | null
        }
      }>(UPDATE_CARRIER_CONNECTION, { data })

      if (result.update_carrier_connection.errors && result.update_carrier_connection.errors.length > 0) {
        throw new Error(
          result.update_carrier_connection.errors
            .map((e) => e.messages.join(', '))
            .join('; '),
        )
      }

      return result.update_carrier_connection.connection
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['user_connections'],
        refetchType: 'active'
      })
    },
  })
}

export function useDeleteCarrierConnection() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (id: string) => {
      const result = await api.graphql<{
        delete_carrier_connection: {
          id: string
          errors: Array<{ field: string; messages: Array<string> }> | null
        }
      }>(DELETE_CARRIER_CONNECTION, { data: { id } })

      if (result.delete_carrier_connection.errors && result.delete_carrier_connection.errors.length > 0) {
        throw new Error(
          result.delete_carrier_connection.errors
            .map((e) => e.messages.join(', '))
            .join('; '),
        )
      }

      return result.delete_carrier_connection.id
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['user_connections'],
        refetchType: 'active'
      })
    },
  })
}

export function useUpdateSystemConnection() {
  const queryClient = useQueryClient()

  const MUTATE_SYSTEM_CONNECTION = `
    mutation mutate_system_connection($data: SystemCarrierMutationInput!) {
      mutate_system_connection(input: $data) {
        carrier {
          id
          carrier_id
          carrier_name
          display_name
          test_mode
          active
          capabilities
        }
        errors {
          field
          messages
        }
      }
    }
  `

  return useMutation({
    mutationFn: async (data: { id: string; active?: boolean }) => {
      const result = await api.graphql<{
        mutate_system_connection: {
          carrier: CarrierConnection
          errors: Array<{ field: string; messages: Array<string> }> | null
        }
      }>(MUTATE_SYSTEM_CONNECTION, { data })

      if (result.mutate_system_connection.errors && result.mutate_system_connection.errors.length > 0) {
        throw new Error(
          result.mutate_system_connection.errors
            .map((e) => e.messages.join(', '))
            .join('; '),
        )
      }

      return result.mutate_system_connection.carrier
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['system_connections'],
        refetchType: 'active'
      })
    },
  })
}
