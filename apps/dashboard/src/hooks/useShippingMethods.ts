import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import type {
  ShippingMethodsResponse,
  CreateShippingMethodInput,
  UpdateShippingMethodInput,
} from '@/types/shipping-methods'
import { useInitialization } from './useInitialization'

const gql = String.raw

// GraphQL Queries
const GET_SHIPPING_METHODS = gql`
  query GetShippingMethods($filter: ShippingMethodFilter) {
    shipping_methods(filter: $filter) {
      edges {
        node {
          id
          object_type
          name
          slug
          description
          carrier_code
          carrier_service
          carrier_id
          carrier_options
          metadata
          is_active
          test_mode
          created_at
          updated_at
          created_by {
            email
            full_name
          }
        }
      }
      page_info {
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
    }
  }
`

// GraphQL Mutations
const CREATE_SHIPPING_METHOD = gql`
  mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) {
    create_shipping_method(input: $data) {
      shipping_method {
        id
        object_type
        name
        slug
        description
        carrier_code
        carrier_service
        carrier_id
        carrier_options
        metadata
        is_active
        test_mode
        created_at
        updated_at
        created_by {
          email
          full_name
        }
      }
      errors {
        field
        messages
      }
    }
  }
`

const UPDATE_SHIPPING_METHOD = gql`
  mutation UpdateShippingMethod($data: UpdateShippingMethodMutationInput!) {
    update_shipping_method(input: $data) {
      shipping_method {
        id
        object_type
        name
        slug
        description
        carrier_code
        carrier_service
        carrier_id
        carrier_options
        metadata
        is_active
        test_mode
        created_at
        updated_at
        created_by {
          email
          full_name
        }
      }
      errors {
        field
        messages
      }
    }
  }
`

const DELETE_SHIPPING_METHOD = gql`
  mutation DeleteShippingMethod($input: DeleteMutationInput!) {
    delete_shipping_method(input: $input) {
      id
      errors {
        field
        messages
      }
    }
  }
`

// React Query Hooks
export function useShippingMethods(filter?: any) {
  const { isInitialized } = useInitialization()

  return useQuery({
    queryKey: ['shipping-methods', filter],
    queryFn: async (): Promise<ShippingMethodsResponse> => {
      const response: any = await api.graphql(GET_SHIPPING_METHODS, { filter })
      return {
        shipping_methods: response.shipping_methods.edges.map((edge: any) => edge.node),
        total: response.shipping_methods.edges.length,
      }
    },
    enabled: isInitialized,
  })
}

export function useCreateShippingMethod() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: CreateShippingMethodInput) => {
      const response: any = await api.graphql(CREATE_SHIPPING_METHOD, { data })
      if (response.create_shipping_method.errors?.length > 0) {
        throw new Error(
          response.create_shipping_method.errors
            .map((error: any) => error.messages.join(', '))
            .join('; '),
        )
      }
      return response.create_shipping_method.shipping_method
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['shipping-methods'],
        refetchType: 'active',
      })
    },
  })
}

export function useUpdateShippingMethod() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: UpdateShippingMethodInput) => {
      const response: any = await api.graphql(UPDATE_SHIPPING_METHOD, { data })
      if (response.update_shipping_method.errors?.length > 0) {
        throw new Error(
          response.update_shipping_method.errors
            .map((error: any) => error.messages.join(', '))
            .join('; '),
        )
      }
      return response.update_shipping_method.shipping_method
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['shipping-methods'],
        refetchType: 'active',
      })
    },
  })
}

export function useDeleteShippingMethod() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (id: string) => {
      const response: any = await api.graphql(DELETE_SHIPPING_METHOD, {
        input: { id },
      })
      if (response.delete_shipping_method.errors?.length > 0) {
        throw new Error(
          response.delete_shipping_method.errors
            .map((error: any) => error.messages.join(', '))
            .join('; '),
        )
      }
      return response.delete_shipping_method
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['shipping-methods'],
        refetchType: 'active',
      })
    },
  })
}
