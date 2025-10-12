/**
 * API Client
 *
 * Automatically uses the correct authentication method:
 * - Token: "Token KARRIO_API_KEY" (for Karrio API token auth)
 * - Bearer: "Bearer JWT_TOKEN" (for JTL Hub OAuth)
 */

import { authManager } from './auth'

interface ApiClientConfig {
  baseUrl?: string
}

class ApiClient {
  private baseUrl: string

  constructor(config: ApiClientConfig = {}) {
    this.baseUrl = config.baseUrl || import.meta.env.VITE_KARRIO_API || 'http://localhost:5002'
  }

  /**
   * Make authenticated API request
   */
  async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const authHeader = authManager.getAuthHeader()

    if (!authHeader) {
      throw new Error('Not authenticated')
    }

    const url = endpoint.startsWith('http')
      ? endpoint
      : `${this.baseUrl}${endpoint}`

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        Authorization: authHeader,
        ...options.headers,
      },
    })

    if (response.status === 401) {
      // Unauthorized - clear auth and redirect to login
      authManager.logout()
      window.location.href = '/signin'
      throw new Error('Unauthorized')
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.message || `API error: ${response.status}`)
    }

    return response.json()
  }

  /**
   * GET request
   */
  async get<T = any>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' })
  }

  /**
   * POST request
   */
  async post<T = any>(
    endpoint: string,
    data?: any,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  /**
   * PUT request
   */
  async put<T = any>(
    endpoint: string,
    data?: any,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  /**
   * PATCH request
   */
  async patch<T = any>(
    endpoint: string,
    data?: any,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  /**
   * DELETE request
   */
  async delete<T = any>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' })
  }
}

// Export singleton instance
export const apiClient = new ApiClient()

// Export class for custom instances
export { ApiClient }

// Example usage:
// import { apiClient } from '@/lib/api-client'
//
// // GET request
// const user = await apiClient.get('/api/v1/user')
//
// // POST request
// const shipment = await apiClient.post('/api/v1/shipments', { data: {...} })
//
// The client automatically uses:
// - "Token xxx" header for Karrio API token auth
// - "Bearer xxx" header for JTL Hub OAuth
