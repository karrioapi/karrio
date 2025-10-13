// Shipping Method types matching actual GraphQL schema

export interface User {
  email: string
  full_name?: string
}

export interface ShippingMethod {
  id: string
  object_type: string
  name: string
  slug: string
  description?: string
  carrier_code: string
  carrier_service: string
  carrier_id: string
  carrier_options: Record<string, any>
  metadata?: Record<string, any>
  is_active: boolean
  test_mode: boolean
  created_at?: string
  updated_at?: string
  created_by?: User
}

export interface ShippingMethodFormData {
  name: string
  slug?: string
  description?: string
  carrier_code: string
  carrier_service: string
  carrier_id: string
  carrier_options?: Record<string, any>
  metadata?: Record<string, any>
  is_active: boolean
}

export interface CreateShippingMethodInput {
  name: string
  slug?: string
  description?: string
  carrier_code: string
  carrier_service: string
  carrier_id: string
  carrier_options?: Record<string, any>
  metadata?: Record<string, any>
  is_active?: boolean
}

export interface UpdateShippingMethodInput {
  id: string
  name?: string
  slug?: string
  description?: string
  carrier_code?: string
  carrier_service?: string
  carrier_id?: string
  carrier_options?: Record<string, any>
  metadata?: Record<string, any>
  is_active?: boolean
}

export interface ShippingMethodsResponse {
  shipping_methods: ShippingMethod[]
  total: number
}

// Carrier reference types
export interface CarrierInfo {
  id: string
  carrier_name: string
  display_name: string
  description?: string
  capabilities: string[]
  integration_status: string
  website?: string
  documentation?: string
  shipping_services?: Record<string, string>
  shipping_options?: Record<string, any>
}

export interface CarriersResponse {
  carriers: CarrierInfo[]
}
