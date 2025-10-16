import { authManager } from './auth'
import { getRuntimeConfig, getRuntimeConfigSync } from './runtime-config'

export interface ApiRequestConfig {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  headers?: Record<string, string>
  body?: any
}

class KarrioAPI {
  private baseUrl: string | null = null
  private initialized = false

  constructor() {
    // Initialize with build-time fallback
    this.baseUrl = import.meta.env.VITE_KARRIO_API || 'http://localhost:5002'
  }

  /**
   * Initialize the API with runtime configuration
   */
  async initialize(): Promise<void> {
    if (this.initialized) return
    
    try {
      const config = await getRuntimeConfig()
      this.baseUrl = config.KARRIO_API_URL
      this.initialized = true
    } catch (error) {
      console.warn('Failed to initialize API with runtime config, using fallback:', error)
      // Keep the fallback baseUrl from constructor
      this.initialized = true
    }
  }

  /**
   * Get the base URL, ensuring initialization
   */
  private async getBaseUrl(): Promise<string> {
    if (!this.initialized) {
      await this.initialize()
    }
    
    // Try to get updated config if available (for client-side updates)
    if (typeof window !== 'undefined') {
      const cachedConfig = getRuntimeConfigSync()
      if (cachedConfig) {
        this.baseUrl = cachedConfig.KARRIO_API_URL
      }
    }
    
    return this.baseUrl!
  }

  private getAuthHeaders(): Record<string, string> {
    if (!authManager.isAuthenticated()) {
      throw new Error('No authentication available')
    }

    const headers: Record<string, string> = {
      Authorization: authManager.getAuthHeader(),
      'Content-Type': 'application/json',
      'x-test-mode': authManager.getTestMode().toString(),
    }

    // Add x-org-id header if an organization is selected
    const orgId = authManager.getCurrentOrgId()
    if (orgId) {
      headers['x-org-id'] = orgId
    }

    return headers
  }

  async request<T>(
    endpoint: string,
    config: ApiRequestConfig = {},
  ): Promise<T> {
    const { method = 'GET', body } = config
    const headers = this.getAuthHeaders()
    const baseUrl = await this.getBaseUrl()

    const response = await fetch(`${baseUrl}${endpoint}`, {
      method,
      headers: {
        ...headers,
        ...config.headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    })

    if (!response.ok) {
      const errorData = await response.text()
      throw new Error(`API request failed: ${response.status} ${errorData}`)
    }

    return response.json()
  }

  async graphql<T>(query: string, variables?: Record<string, any>): Promise<T> {
    const response = await this.request<{ data: T; errors?: Array<any> }>(
      '/graphql',
      {
        method: 'POST',
        body: {
          query,
          variables,
        },
      },
    )

    if (response.errors) {
      throw new Error(
        `GraphQL errors: ${response.errors.map((e: any) => e.message).join(', ')}`,
      )
    }

    return response.data
  }
}

export const api = new KarrioAPI()
