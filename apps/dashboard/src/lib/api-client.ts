/**
 * API Client
 *
 * Automatically uses Bearer JWT authentication for all API requests:
 * - Authorization: "Bearer JWT_TOKEN"
 */

import { authManager } from './auth'
import { getRuntimeConfig } from './runtime-config'

interface ApiClientConfig {
  baseUrl?: string
}

class ApiClient {
  private baseUrl: string | null = null
  private initialized = false

  constructor(config: ApiClientConfig = {}) {
    // Initialize with build-time fallback or provided config
    this.baseUrl = config.baseUrl || import.meta.env.VITE_KARRIO_API || 'http://localhost:5002'
  }

  /**
   * Initialize the API client with runtime configuration
   */
  async initialize(): Promise<void> {
    if (this.initialized) return
    
    try {
      const config = await getRuntimeConfig()
      this.baseUrl = config.KARRIO_API_URL
      this.initialized = true
    } catch (error) {
      console.warn('Failed to initialize API client with runtime config, using fallback:', error)
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
    
    return this.baseUrl!
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

    const baseUrl = await this.getBaseUrl()
    const url = endpoint.startsWith('http')
      ? endpoint
      : `${baseUrl}${endpoint}`

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
