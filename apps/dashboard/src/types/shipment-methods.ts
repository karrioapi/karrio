// Shipment Method types based on Karrio carrier metadata structure

export interface CarrierInfo {
  id: string
  carrier_name: string
  display_name: string
  description?: string
  capabilities: Array<'shipping' | 'rating' | 'tracking' | 'pickup' | 'manifest' | 'paperless'>
  integration_status: 'production-ready' | 'beta' | 'alpha'
  website?: string
  documentation?: string
}

export interface ShippingService {
  code: string
  name: string
  description?: string
}

export interface ShippingOption {
  code: string
  name: string
  type: 'string' | 'boolean' | 'float' | 'integer' | 'object' | 'list'
  required: boolean
  default?: any
  enum?: string[]
  description?: string
}

export interface PricingZone {
  id: string
  label: string
  countries?: string[]
  postal_codes?: string[]
  rate: number
  currency: string
}

export interface ShipmentMethod {
  id: string
  name: string
  display_name: string
  description?: string

  // Connection reference (links to existing carrier connection)
  connection_id: string
  connection_name: string // display name of the connection

  // Carrier information (inherited from connection)
  carrier_id: string
  carrier_name: string

  // Service configuration (selected from available services)
  service_code: string
  service_name: string

  // Configuration
  active: boolean
  currency: string

  // Pricing
  base_rate?: number
  pricing_zones: PricingZone[]

  // Transit Coverage (fields from screenshot)
  transit_coverage?: {
    domestic: boolean
    international: boolean
    zones: string[] // Array of supported zones/regions
  }

  // Service options (selected from available carrier options)
  shipping_options: Array<{
    code: string
    name: string
    value: any
    enabled: boolean
  }>

  // Delivery settings (can be customized from service defaults)
  estimated_delivery_days?: {
    min: number
    max: number
  }

  // Service features (from screenshot)
  features?: string[] // e.g., ['tracking', 'insurance', 'signature_required']

  // Restrictions (can be customized from service defaults)
  max_weight?: number
  max_length?: number
  max_width?: number
  max_height?: number
  supported_countries?: string[]

  // Additional charges (from screenshot)
  additional_charges?: Array<{
    name: string
    amount: number
    currency: string
  }>

  // Additional settings (derived from carrier capabilities and options)
  requires_signature?: boolean
  insurance_available?: boolean
  tracking_enabled?: boolean
  pickup_enabled?: boolean

  // Metadata
  metadata?: Record<string, any>
  created_at?: string
  updated_at?: string
}

export interface ShipmentMethodFormData {
  name: string
  display_name: string
  description?: string
  connection_id: string  // Reference to existing carrier connection
  service_code: string   // Selected from connection's available services
  active: boolean
  currency: string
  base_rate?: number
  shipping_options: Array<{
    code: string
    name: string
    value: any
    enabled: boolean
  }>
  estimated_delivery_days?: {
    min: number
    max: number
  }
  max_weight?: number
  max_length?: number
  max_width?: number
  max_height?: number
  supported_countries?: string[]
  metadata?: Record<string, any>
}

// GraphQL mutations and queries interfaces
export interface CreateShipmentMethodInput {
  method: ShipmentMethodFormData
}

export interface UpdateShipmentMethodInput {
  id: string
  method: Partial<ShipmentMethodFormData>
}

export interface ShipmentMethodsResponse {
  shipment_methods: ShipmentMethod[]
  total: number
}

export interface CarriersResponse {
  carriers: CarrierInfo[]
}