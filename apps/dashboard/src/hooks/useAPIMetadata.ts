import { useQuery } from '@tanstack/react-query'
import { authManager } from '@/lib/auth'
import { getRuntimeConfig } from '@/lib/runtime-config'
import { useInitialization } from './useInitialization'

export interface References {
  carriers: Record<string, string>
  connection_fields: Record<string, Record<string, any>>
  connection_configs: Record<string, Record<string, any>>
  carrier_capabilities: Record<string, string[]>
  service_names: Record<string, Record<string, string>>
  option_names: Record<string, Record<string, string>>
  integration_status: Record<string, string>
  countries: Record<string, string>
  currencies: Record<string, string>
  states: Record<string, Record<string, string>>
}

export function useAPIMetadata() {
  const { isInitialized } = useInitialization()

  const query = useQuery({
    queryKey: ['api-metadata'],
    queryFn: async (): Promise<References> => {
      const config = await getRuntimeConfig()
      const authHeader = authManager.getAuthHeader()

      // Build headers with Karrio-specific headers
      const headers: Record<string, string> = {
        ...(authHeader ? { Authorization: authHeader } : {}),
        'x-test-mode': authManager.getTestMode().toString(),
      }

      // Add x-org-id header if an organization is selected
      const orgId = authManager.getCurrentOrgId()
      if (orgId) {
        headers['x-org-id'] = orgId
      }

      const response = await fetch(`${config.KARRIO_API_URL}/v1/references?reduced=false`, {
        headers,
      })

      if (!response.ok) {
        throw new Error('Failed to fetch API metadata')
      }

      return response.json()
    },
    enabled: isInitialized,
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false,
  })

  return {
    query,
    references: query.data,
  }
}
