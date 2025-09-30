import { gql } from 'graphql-request'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import type {
  ShipmentMethod,
  ShipmentMethodsResponse,
  CreateShipmentMethodInput,
  UpdateShipmentMethodInput,
  CarriersResponse,
} from '@/types/shipment-methods'

// GraphQL Queries
const GET_SHIPMENT_METHODS = gql`
  query GetShipmentMethods(
    $first: Int
    $offset: Int
    $filter: ShipmentMethodFilter
  ) {
    shipment_methods(first: $first, offset: $offset, filter: $filter) {
      edges {
        node {
          id
          name
          display_name
          description
          carrier_id
          carrier_name
          service_code
          service_name
          active
          test_mode
          currency
          base_rate
          estimated_delivery_days {
            min
            max
          }
          shipping_options {
            code
            value
            enabled
          }
          max_weight
          max_length
          max_width
          max_height
          supported_countries
          requires_signature
          insurance_available
          tracking_enabled
          pickup_enabled
          metadata
          created_at
          updated_at
        }
      }
      page_info {
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
      total_count
    }
  }
`

const GET_AVAILABLE_CARRIERS = gql`
  query GetAvailableCarriers {
    available_carriers {
      id
      carrier_name
      display_name
      description
      capabilities
      integration_status
      website
      documentation
      shipping_services {
        code
        name
        description
      }
      shipping_options {
        code
        name
        type
        required
        default
        enum
        description
      }
    }
  }
`

// GraphQL Mutations
const CREATE_SHIPMENT_METHOD = gql`
  mutation CreateShipmentMethod($input: CreateShipmentMethodInput!) {
    create_shipment_method(input: $input) {
      shipment_method {
        id
        name
        display_name
        description
        carrier_id
        carrier_name
        service_code
        service_name
        active
        test_mode
        currency
        base_rate
        estimated_delivery_days {
          min
          max
        }
        shipping_options {
          code
          value
          enabled
        }
        max_weight
        max_length
        max_width
        max_height
        supported_countries
        metadata
        created_at
        updated_at
      }
      errors {
        field
        messages
      }
    }
  }
`

const UPDATE_SHIPMENT_METHOD = gql`
  mutation UpdateShipmentMethod($input: UpdateShipmentMethodInput!) {
    update_shipment_method(input: $input) {
      shipment_method {
        id
        name
        display_name
        description
        carrier_id
        carrier_name
        service_code
        service_name
        active
        test_mode
        currency
        base_rate
        estimated_delivery_days {
          min
          max
        }
        shipping_options {
          code
          value
          enabled
        }
        max_weight
        max_length
        max_width
        max_height
        supported_countries
        metadata
        created_at
        updated_at
      }
      errors {
        field
        messages
      }
    }
  }
`

const DELETE_SHIPMENT_METHOD = gql`
  mutation DeleteShipmentMethod($id: String!) {
    delete_shipment_method(id: $id) {
      id
      errors {
        field
        messages
      }
    }
  }
`

// React Query Hooks
export function useShipmentMethods(filter?: any) {
  return useQuery({
    queryKey: ['shipment-methods', filter],
    queryFn: async (): Promise<ShipmentMethodsResponse> => {
      const response = await api.request(GET_SHIPMENT_METHODS, {
        first: 50,
        offset: 0,
        filter,
      })
      return {
        shipment_methods: response.shipment_methods.edges.map(
          (edge: any) => edge.node,
        ),
        total: response.shipment_methods.total_count,
      }
    },
  })
}

export function useAvailableCarriers() {
  return useQuery({
    queryKey: ['available-carriers'],
    queryFn: async (): Promise<CarriersResponse> => {
      const response = await api.request(GET_AVAILABLE_CARRIERS)
      return {
        carriers: response.available_carriers,
      }
    },
  })
}

export function useCreateShipmentMethod() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (input: CreateShipmentMethodInput) => {
      const response = await api.request(CREATE_SHIPMENT_METHOD, { input })
      if (response.create_shipment_method.errors?.length > 0) {
        throw new Error(
          response.create_shipment_method.errors
            .map((error: any) => error.messages.join(', '))
            .join('; '),
        )
      }
      return response.create_shipment_method.shipment_method
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['shipment-methods'] })
    },
  })
}

export function useUpdateShipmentMethod() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (input: UpdateShipmentMethodInput) => {
      const response = await api.request(UPDATE_SHIPMENT_METHOD, { input })
      if (response.update_shipment_method.errors?.length > 0) {
        throw new Error(
          response.update_shipment_method.errors
            .map((error: any) => error.messages.join(', '))
            .join('; '),
        )
      }
      return response.update_shipment_method.shipment_method
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['shipment-methods'] })
    },
  })
}

export function useDeleteShipmentMethod() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (id: string) => {
      const response = await api.request(DELETE_SHIPMENT_METHOD, { id })
      if (response.delete_shipment_method.errors?.length > 0) {
        throw new Error(
          response.delete_shipment_method.errors
            .map((error: any) => error.messages.join(', '))
            .join('; '),
        )
      }
      return response.delete_shipment_method
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['shipment-methods'] })
    },
  })
}