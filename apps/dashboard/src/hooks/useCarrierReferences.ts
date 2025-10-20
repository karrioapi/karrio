import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { getRuntimeConfig } from '@/lib/runtime-config'
import { useInitialization } from './useInitialization'

export interface CarrierReferences {
  carriers: Record<string, string> // carrier_id -> display_name
  services: Record<string, Record<string, string>> // carrier_id -> service_code -> service_name
  countries: Record<string, string> // country_code -> country_name
  states: Record<string, Record<string, string>> // country_code -> state_code -> state_name
  carrier_hubs: Record<string, string>
  address_validators: Record<string, string>
}

export interface CarrierMetadata {
  id: string
  carrier_name: string
  display_name: string
  description?: string
  integration_status: 'production-ready' | 'beta' | 'alpha'
  website?: string
  documentation?: string
  is_enabled: boolean
  capabilities: string[]
  connection_fields: Record<string, any>
  config_fields: Record<string, any>
  shipping_services: Record<string, string>
  shipping_options: Record<string, any>
  readme?: string
}

// Hook to fetch reference data (carriers, services, countries, etc.) - aligned with Karrio pattern
export function useCarrierReferences() {
  const { isInitialized } = useInitialization()

  return useQuery({
    queryKey: ['references'],
    queryFn: async (): Promise<CarrierReferences> => {
      const config = await getRuntimeConfig()
      const response = await axios.get<CarrierReferences>(
        `${config.KARRIO_API_URL}/v1/references?reduced=false`
      )
      return response.data
    },
    enabled: isInitialized,
    refetchOnWindowFocus: false,
    staleTime: 300000, // 5 minutes (matching Karrio pattern)
    gcTime: 1000 * 60 * 60 * 24, // 24 hours
  })
}

// Hook to fetch detailed carrier metadata - aligned with Karrio pattern
export function useCarrierMetadata() {
  const { isInitialized } = useInitialization()

  return useQuery({
    queryKey: ['carriers'],
    queryFn: async (): Promise<CarrierMetadata[]> => {
      const config = await getRuntimeConfig()
      const response = await axios.get<CarrierMetadata[]>(
        `${config.KARRIO_API_URL}/v1/carriers`
      )
      return response.data
    },
    enabled: isInitialized,
    refetchOnWindowFocus: false,
    staleTime: 300000, // 5 minutes (matching Karrio pattern)
    gcTime: 1000 * 60 * 60 * 12, // 12 hours
  })
}

// Helper function to get services for a specific carrier
export function useCarrierServices(carrierName?: string) {
  const { data: references } = useCarrierReferences()
  const { data: metadata } = useCarrierMetadata()

  if (!carrierName || !references || !metadata) {
    return { services: [], options: [] }
  }

  const carrierMeta = metadata.find((c) => c.carrier_name === carrierName)
  const services = references.services[carrierName] || {}

  return {
    services: Object.entries(services).map(([code, name]) => ({
      code,
      name,
    })),
    options: carrierMeta?.shipping_options
      ? Object.entries(carrierMeta.shipping_options).map(([code, config]: [string, any]) => ({
          code,
          name: config.name || code,
          type: config.type || 'string',
          required: config.required || false,
          default: config.default,
          enum: config.enum,
          description: config.description,
        }))
      : [],
    capabilities: carrierMeta?.capabilities || [],
    metadata: carrierMeta,
  }
}

// Helper function to get all available carriers with their info
export function useAvailableCarriersWithServices() {
  const { data: references } = useCarrierReferences()
  const { data: metadata } = useCarrierMetadata()

  if (!references || !metadata) {
    return []
  }

  return metadata
    .filter((carrier) => carrier.is_enabled)
    .map((carrier) => ({
      ...carrier,
      services: Object.entries(references.services[carrier.carrier_name] || {}).map(
        ([code, name]) => ({
          code,
          name,
        }),
      ),
      options: Object.entries(carrier.shipping_options || {}).map(
        ([code, config]: [string, any]) => ({
          code,
          name: config.name || code,
          type: config.type || 'string',
          required: config.required || false,
          default: config.default,
          enum: config.enum,
          description: config.description,
        }),
      ),
    }))
}