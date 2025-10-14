/**
 * Authentication Library
 *
 * Supports two authentication methods:
 * 1. JTL Hub OAuth (Bearer token) - OAuth flow with PKCE
 * 2. Karrio API Token (Token auth) - Direct API token
 */

import { jtlOAuth, type AuthResponse } from './jtl-oauth'

export type AuthMethod = 'jtl-oauth' | 'karrio-token'

interface StoredAuth {
  method: AuthMethod
  token: string
  user?: AuthResponse['user']
  org?: AuthResponse['org']
}

class AuthManager {
  private apiUrl: string

  constructor() {
    this.apiUrl = import.meta.env.VITE_KARRIO_API || 'http://localhost:5002'
  }

  /**
   * Sign in with Karrio API Token
   */
  async loginWithToken(apiToken: string): Promise<void> {
    try {
      // Test the token by fetching user info via GraphQL
      const response = await fetch(`${this.apiUrl}/graphql`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${apiToken}`,
        },
        body: JSON.stringify({
          query: `{
            user {
              email
              full_name
              is_staff
            }
          }`,
        }),
      })

      if (!response.ok) {
        throw new Error('Invalid API token')
      }

      const result = await response.json()

      if (result.errors) {
        throw new Error(result.errors[0]?.message || 'Invalid API token')
      }

      if (!result.data?.user) {
        throw new Error('Invalid API token')
      }

      // Store token and auth method
      this.storeTokenAuth(apiToken, result.data.user)

    } catch (error) {
      console.error('Token authentication error:', error)
      throw error
    }
  }

  /**
   * Sign in with JTL Hub OAuth (PKCE flow)
   */
  async loginWithJTLHub(): Promise<void> {
    await jtlOAuth.login()
  }

  /**
   * Handle JTL Hub OAuth callback
   */
  async handleJTLCallback(token: string): Promise<AuthResponse> {
    const data = await jtlOAuth.handleCallback(token)

    // Store JWT and auth method
    this.storeJWTAuth(data)

    return data
  }

  /**
   * Store Token-based authentication
   */
  private storeTokenAuth(token: string, userData: any): void {
    if (typeof window === 'undefined') return

    // Parse full_name into first and last name
    const fullName = userData.full_name || ''
    const nameParts = fullName.split(' ')
    const firstName = nameParts[0] || ''
    const lastName = nameParts.slice(1).join(' ') || ''

    const authData: StoredAuth = {
      method: 'karrio-token',
      token,
      user: {
        id: 0, // GraphQL user endpoint doesn't return ID
        email: userData.email,
        username: userData.email,
        first_name: firstName,
        last_name: lastName,
      },
    }

    localStorage.setItem('auth_method', 'karrio-token')
    localStorage.setItem('karrio_access_token', token)
    localStorage.setItem('karrio_user', JSON.stringify(authData.user))
    localStorage.setItem('isAuthenticated', 'true')
  }

  /**
   * Store JWT-based authentication (from JTL Hub OAuth)
   */
  private storeJWTAuth(data: AuthResponse): void {
    if (typeof window === 'undefined') return

    localStorage.setItem('auth_method', 'jtl-oauth')
    localStorage.setItem('karrio_access_token', data.access_token)
    localStorage.setItem('karrio_refresh_token', data.refresh_token)
    localStorage.setItem('karrio_user', JSON.stringify(data.user))
    localStorage.setItem('karrio_org', JSON.stringify(data.org))
    localStorage.setItem('isAuthenticated', 'true')
  }

  /**
   * Get authentication method
   */
  getAuthMethod(): AuthMethod | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('auth_method') as AuthMethod | null
  }

  /**
   * Get authorization header for API calls
   */
  getAuthHeader(): string {
    if (typeof window === 'undefined') return ''

    const method = this.getAuthMethod()
    const token = localStorage.getItem('karrio_access_token')

    if (!token) {
      return ''
    }

    // Use appropriate auth header based on method
    switch (method) {
      case 'karrio-token':
        return `Token ${token}`
      case 'jtl-oauth':
        return `Bearer ${token}`
      default:
        // Fallback to Token auth for backward compatibility
        return `Token ${token}`
    }
  }

  /**
   * Get stored authentication data
   */
  getStoredAuth(): {
    method: AuthMethod | null
    accessToken: string | null
    refreshToken: string | null
    user: AuthResponse['user'] | null
    org: AuthResponse['org'] | null
  } {
    // SSR-safe: return empty auth during server-side rendering
    if (typeof window === 'undefined') {
      return {
        method: null,
        accessToken: null,
        refreshToken: null,
        user: null,
        org: null,
      }
    }

    const method = this.getAuthMethod()
    const accessToken = localStorage.getItem('karrio_access_token')
    const refreshToken = localStorage.getItem('karrio_refresh_token')

    let user = null
    let org = null

    try {
      const userStr = localStorage.getItem('karrio_user')
      const orgStr = localStorage.getItem('karrio_org')
      if (userStr) user = JSON.parse(userStr)
      if (orgStr) org = JSON.parse(orgStr)
    } catch (e) {
      console.error('Error parsing stored user/org:', e)
    }

    return { method, accessToken, refreshToken, user, org }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const { accessToken } = this.getStoredAuth()
    return !!accessToken
  }

  /**
   * Logout and clear all stored data
   */
  logout(): void {
    if (typeof window === 'undefined') return

    localStorage.removeItem('auth_method')
    localStorage.removeItem('karrio_access_token')
    localStorage.removeItem('karrio_refresh_token')
    localStorage.removeItem('karrio_user')
    localStorage.removeItem('karrio_org')
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('jtl_oauth_state')
  }

  /**
   * Verify state parameter (for JTL Hub OAuth)
   */
  verifyOAuthState(state: string): boolean {
    return jtlOAuth.verifyState(state)
  }
}

// Export singleton instance
export const authManager = new AuthManager()

// Export types
export type { AuthResponse, StoredAuth }
