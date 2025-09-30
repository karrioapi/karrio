import { oauth } from './oauth'

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

  private async getAuthHeaders(): Promise<Record<string, string>> {
    const { accessToken } = oauth.getStoredTokens()

    if (!accessToken) {
      throw new Error('No access token available')
    }

    // Check if token is valid and refresh if needed
    if (!oauth.isTokenValid()) {
      const { refreshToken } = oauth.getStoredTokens()
      if (refreshToken) {
        try {
          const newTokens = await oauth.refreshToken(refreshToken)
          oauth.storeTokens(newTokens)
          return {
            Authorization: `Bearer ${newTokens.access_token}`,
            'Content-Type': 'application/json',
          }
        } catch (error) {
          oauth.clearTokens()
          throw new Error('Token refresh failed')
        }
      } else {
        oauth.clearTokens()
        throw new Error('No refresh token available')
      }
    }

    return {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    }
  }

  async request<T>(
    endpoint: string,
    config: ApiRequestConfig = {},
  ): Promise<T> {
    const { method = 'GET', body } = config
    const headers = await this.getAuthHeaders()

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
