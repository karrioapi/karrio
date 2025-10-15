import { authManager } from './auth'

export interface ApiRequestConfig {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  headers?: Record<string, string>
  body?: any
}

class KarrioAPI {
  private baseUrl: string

  constructor() {
    this.baseUrl = import.meta.env.VITE_KARRIO_API
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

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
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
