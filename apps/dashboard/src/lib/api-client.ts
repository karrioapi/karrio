/**
 * API Client
 *
 * Automatically uses Bearer JWT authentication for all API requests:
 * - Authorization: "Bearer JWT_TOKEN"
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
   * Make authenticated API request with automatic token refresh
   */
  async request<T = any>(
    endpoint: string,
    options: RequestInit = {},
    retryCount = 0
  ): Promise<T> {
    const authHeader = authManager.getAuthHeader()

    if (!authHeader) {
      throw new Error('Not authenticated')
    }

    const url = endpoint.startsWith('http')
      ? endpoint
      : `${this.baseUrl}${endpoint}`

    // Build headers with Karrio-specific headers
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      Authorization: authHeader,
      'x-test-mode': authManager.getTestMode().toString(),
    }

    // Add x-org-id header if an organization is selected
    const orgId = authManager.getCurrentOrgId()
    if (orgId) {
      headers['x-org-id'] = orgId
    }

    const response = await fetch(url, {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    })

    // Handle 401 Unauthorized with token refresh
    if (response.status === 401 && retryCount === 0) {
      try {
        // Try to refresh the token
        await authManager.refreshAccessToken()

        // Retry the request with the new token
        return this.request<T>(endpoint, options, retryCount + 1)
      } catch (error) {
        // Refresh failed - clear auth and redirect to login
        authManager.logout()
        window.location.href = '/signin'
        throw new Error('Session expired. Please sign in again.')
      }
    }

    if (response.status === 401) {
      // Already retried - clear auth and redirect
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
// The client automatically includes Bearer JWT authentication header
