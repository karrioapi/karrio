/**
 * Authentication Library
 *
 * Handles email/password authentication with JWT tokens
 */

import { getRuntimeConfig, getRuntimeConfigSync } from './runtime-config'

export type AuthResponse = {
  access_token: string
  refresh_token: string
  user: {
    id: number
    email: string
    username: string
    first_name: string
    last_name: string
  }
  org?: {
    id: string
    name: string
    slug: string
  }
}

interface StoredAuth {
  accessToken: string
  refreshToken: string
  user: AuthResponse['user']
  org?: AuthResponse['org']
  testMode?: boolean
}

class AuthManager {
  private apiUrl: string | null = null
  private initialized = false

  constructor() {
    // Initialize with build-time fallback
    this.apiUrl = import.meta.env.VITE_KARRIO_API || 'http://localhost:5002'
  }

  /**
   * Initialize the auth manager with runtime configuration
   */
  async initialize(): Promise<void> {
    if (this.initialized) return
    
    try {
      const config = await getRuntimeConfig()
      this.apiUrl = config.KARRIO_API_URL
      this.initialized = true
    } catch (error) {
      console.warn('Failed to initialize auth with runtime config, using fallback:', error)
      // Keep the fallback apiUrl from constructor
      this.initialized = true
    }
  }

  /**
   * Get the API URL, ensuring initialization
   */
  private async getApiUrl(): Promise<string> {
    if (!this.initialized) {
      await this.initialize()
    }
    
    // Try to get updated config if available (for client-side updates)
    if (typeof window !== 'undefined') {
      const cachedConfig = getRuntimeConfigSync()
      if (cachedConfig) {
        this.apiUrl = cachedConfig.KARRIO_API_URL
      }
    }
    
    return this.apiUrl!
  }

  /**
   * Get current test mode setting
   */
  getTestMode(): boolean {
    if (typeof window === 'undefined') return false

    const testMode = localStorage.getItem('karrio_test_mode')

    // If test mode has been explicitly set, use that value
    if (testMode !== null) {
      return testMode === 'true'
    }

    // Otherwise, use the default from runtime config or environment variable
    const cachedConfig = getRuntimeConfigSync()
    if (cachedConfig) {
      return cachedConfig.KARRIO_TEST_MODE
    }

    // Final fallback to build-time environment variable
    const defaultTestMode = import.meta.env.VITE_KARRIO_TEST_MODE
    return defaultTestMode === 'true'
  }

  /**
   * Set test mode
   */
  setTestMode(enabled: boolean): void {
    if (typeof window === 'undefined') return
    localStorage.setItem('karrio_test_mode', enabled ? 'true' : 'false')
  }

  /**
   * Get current organization ID
   */
  getCurrentOrgId(): string | null {
    if (typeof window === 'undefined') return null
    const orgStr = localStorage.getItem('karrio_org')
    if (!orgStr) return null
    try {
      const org = JSON.parse(orgStr)
      return org?.id || null
    } catch {
      return null
    }
  }

  /**
   * Switch to a different organization
   */
  setCurrentOrg(org: AuthResponse['org']): void {
    if (typeof window === 'undefined') return
    if (org) {
      localStorage.setItem('karrio_org', JSON.stringify(org))
    } else {
      localStorage.removeItem('karrio_org')
    }
  }

  /**
   * Sign in with email and password (Karrio authentication)
   */
  async loginWithEmailPassword(email: string, password: string): Promise<void> {
    try {
      const apiUrl = await this.getApiUrl()
      // Authenticate with Karrio API
      const response = await fetch(`${apiUrl}/api/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Invalid email or password')
      }

      const result = await response.json()

      if (!result.access || !result.refresh) {
        throw new Error('Invalid response from server')
      }

      // Fetch user info using the access token
      const userResponse = await fetch(`${apiUrl}/graphql`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${result.access}`,
        },
        body: JSON.stringify({
          query: `{
            user {
              email
              full_name
              is_staff
            }
            organizations {
              edges {
                node {
                  id
                  name
                  slug
                }
              }
            }
          }`,
        }),
      })

      const userData = await userResponse.json()

      if (userData.errors) {
        throw new Error(userData.errors[0]?.message || 'Failed to fetch user data')
      }

      // Store JWT auth
      const authData: AuthResponse = {
        access_token: result.access,
        refresh_token: result.refresh,
        user: {
          id: 0,
          email: userData.data.user.email,
          username: userData.data.user.email,
          first_name: userData.data.user.full_name?.split(' ')[0] || '',
          last_name: userData.data.user.full_name?.split(' ').slice(1).join(' ') || '',
        },
        org: userData.data.organizations.edges[0]?.node || undefined,
      }

      this.storeAuth(authData)

    } catch (error) {
      console.error('Email/password authentication error:', error)
      throw error
    }
  }

  /**
   * Register/onboard a new JTL tenant
   * Note: Does NOT automatically log the user in - they must sign in after registration
   */
  async registerJTLTenant(data: {
    tenantId: string
    userId: string
    email: string
    password: string
  }): Promise<void> {
    try {
      const apiUrl = await this.getApiUrl()
      // Call the JTL onboarding API
      const response = await fetch(`${apiUrl}/jtl/tenants/onboarding`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Registration failed')
      }

      // Registration successful - user can now sign in
      // We intentionally do NOT store auth here to require explicit signin
    } catch (error) {
      console.error('JTL tenant registration error:', error)
      throw error
    }
  }

  /**
   * Store authentication data
   */
  private storeAuth(data: AuthResponse): void {
    if (typeof window === 'undefined') return

    localStorage.setItem('karrio_access_token', data.access_token)
    localStorage.setItem('karrio_refresh_token', data.refresh_token)
    localStorage.setItem('karrio_user', JSON.stringify(data.user))
    if (data.org) {
      localStorage.setItem('karrio_org', JSON.stringify(data.org))
    }
    localStorage.setItem('isAuthenticated', 'true')
  }

  /**
   * Get authorization header for API calls (always Bearer JWT)
   */
  getAuthHeader(): string {
    if (typeof window === 'undefined') return ''

    const token = localStorage.getItem('karrio_access_token')

    if (!token) {
      return ''
    }

    return `Bearer ${token}`
  }

  /**
   * Get access token
   */
  getAccessToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('karrio_access_token')
  }

  /**
   * Get refresh token
   */
  getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('karrio_refresh_token')
  }

  /**
   * Get stored authentication data
   */
  getStoredAuth(): StoredAuth | null {
    // SSR-safe: return null during server-side rendering
    if (typeof window === 'undefined') {
      return null
    }

    const accessToken = localStorage.getItem('karrio_access_token')
    const refreshToken = localStorage.getItem('karrio_refresh_token')

    if (!accessToken || !refreshToken) {
      return null
    }

    let user = null
    let org = null

    try {
      const userStr = localStorage.getItem('karrio_user')
      const orgStr = localStorage.getItem('karrio_org')
      if (userStr) user = JSON.parse(userStr)
      if (orgStr) org = JSON.parse(orgStr)
    } catch (e) {
      console.error('Error parsing stored user/org:', e)
      return null
    }

    if (!user) {
      return null
    }

    return { accessToken, refreshToken, user, org }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const auth = this.getStoredAuth()
    return !!auth?.accessToken
  }

  /**
   * Refresh the access token using the refresh token
   */
  async refreshAccessToken(): Promise<string> {
    const refreshToken = this.getRefreshToken()

    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    try {
      const apiUrl = await this.getApiUrl()
      const response = await fetch(`${apiUrl}/api/token/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      })

      if (!response.ok) {
        throw new Error('Failed to refresh token')
      }

      const result = await response.json()

      if (!result.access) {
        throw new Error('Invalid refresh response')
      }

      // Update stored access token
      localStorage.setItem('karrio_access_token', result.access)

      // Update refresh token if returned
      if (result.refresh) {
        localStorage.setItem('karrio_refresh_token', result.refresh)
      }

      return result.access
    } catch (error) {
      console.error('Token refresh error:', error)
      // Clear auth on refresh failure
      this.logout()
      throw error
    }
  }

  /**
   * Fetch all organizations for the current user
   */
  async fetchOrganizations(): Promise<AuthResponse['org'][]> {
    const accessToken = this.getAccessToken()
    if (!accessToken) {
      throw new Error('Not authenticated')
    }

    const apiUrl = await this.getApiUrl()
    const response = await fetch(`${apiUrl}/graphql`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
        'x-test-mode': this.getTestMode().toString(),
      },
      body: JSON.stringify({
        query: `{
          organizations {
            edges {
              node {
                id
                name
                slug
              }
            }
          }
        }`,
      }),
    })

    const result = await response.json()

    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to fetch organizations')
    }

    return result.data.organizations.edges.map((e: any) => e.node) || []
  }

  /**
   * Logout and clear all stored data
   */
  logout(): void {
    if (typeof window === 'undefined') return

    localStorage.removeItem('karrio_access_token')
    localStorage.removeItem('karrio_refresh_token')
    localStorage.removeItem('karrio_user')
    localStorage.removeItem('karrio_org')
    localStorage.removeItem('karrio_test_mode')
    localStorage.removeItem('isAuthenticated')
  }
}

// Export singleton instance
export const authManager = new AuthManager()

// Export types
export type { StoredAuth }
