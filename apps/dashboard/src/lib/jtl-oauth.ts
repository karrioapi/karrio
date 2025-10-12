/**
 * JTL Hub OAuth Client
 *
 * Handles authentication flow with JTL Hub:
 * 1. Redirect to JTL Hub for authentication
 * 2. Handle callback with JWT token
 * 3. Exchange JWT for Karrio tokens
 */

interface JTLOAuthConfig {
  clientId: string
  authorizeUrl: string
  redirectUri: string
  apiUrl: string
}

interface AuthResponse {
  access_token: string
  refresh_token: string
  user: {
    id: number
    email: string
    username: string
    first_name: string
    last_name: string
  }
  org: {
    id: string
    name: string
    slug: string
  }
}

class JTLHubOAuth {
  private config: JTLOAuthConfig

  constructor() {
    this.config = {
      clientId: import.meta.env.VITE_JTL_HUB_CLIENT_ID || '',
      authorizeUrl: import.meta.env.VITE_JTL_HUB_AUTHORIZE_URL || '',
      redirectUri: import.meta.env.VITE_JTL_HUB_REDIRECT_URI || '',
      apiUrl: import.meta.env.VITE_KARRIO_API || '',
    }

    // Validate configuration
    if (!this.config.clientId || !this.config.authorizeUrl || !this.config.redirectUri) {
      console.warn('JTL Hub OAuth not configured. Check environment variables:', {
        clientId: !!this.config.clientId,
        authorizeUrl: !!this.config.authorizeUrl,
        redirectUri: !!this.config.redirectUri,
      })
    }
  }

  /**
   * Redirect to JTL Hub for authentication
   */
  login(): void {
    if (!this.config.clientId) {
      throw new Error('JTL Hub CLIENT_ID not configured')
    }

    const state = this.generateState()
    const params = new URLSearchParams({
      client_id: this.config.clientId,
      response_type: 'token',  // Implicit flow - returns JWT directly
      redirect_uri: this.config.redirectUri,
      state,
      scope: 'openid profile',  // Request OpenID Connect scopes
    })

    const authUrl = `${this.config.authorizeUrl}?${params.toString()}`
    console.log('Redirecting to JTL Hub:', authUrl)
    window.location.href = authUrl
  }

  /**
   * Handle callback from JTL Hub
   *
   * @param token - JWT token from JTL Hub
   * @returns Promise with Karrio JWT and user/org info
   */
  async handleCallback(token: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${this.config.apiUrl}/auth/jtl/callback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
      })

      if (!response.ok) {
        const error = await response.json().catch(() => ({}))
        throw new Error(error.error || `Authentication failed: ${response.status}`)
      }

      const data: AuthResponse = await response.json()

      // Store Karrio tokens
      this.storeTokens(data)

      return data
    } catch (error) {
      console.error('JTL Hub callback error:', error)
      throw error
    }
  }

  /**
   * Store Karrio JWT tokens and user info
   */
  private storeTokens(data: AuthResponse): void {
    localStorage.setItem('karrio_access_token', data.access_token)
    localStorage.setItem('karrio_refresh_token', data.refresh_token)
    localStorage.setItem('karrio_user', JSON.stringify(data.user))
    localStorage.setItem('karrio_org', JSON.stringify(data.org))
    localStorage.setItem('isAuthenticated', 'true')
  }

  /**
   * Get stored tokens and user info
   */
  getStoredAuth(): {
    accessToken: string | null
    refreshToken: string | null
    user: AuthResponse['user'] | null
    org: AuthResponse['org'] | null
  } {
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

    return { accessToken, refreshToken, user, org }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const { accessToken } = this.getStoredAuth()
    return !!accessToken
  }

  /**
   * Clear stored tokens and logout
   */
  logout(): void {
    localStorage.removeItem('karrio_access_token')
    localStorage.removeItem('karrio_refresh_token')
    localStorage.removeItem('karrio_user')
    localStorage.removeItem('karrio_org')
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('jtl_oauth_state')
  }

  /**
   * Generate and store random state for CSRF protection
   */
  private generateState(): string {
    const state =
      Math.random().toString(36).substring(2, 15) +
      Math.random().toString(36).substring(2, 15)

    sessionStorage.setItem('jtl_oauth_state', state)
    return state
  }

  /**
   * Verify state parameter from callback
   */
  verifyState(state: string): boolean {
    const stored = sessionStorage.getItem('jtl_oauth_state')
    sessionStorage.removeItem('jtl_oauth_state')
    return stored === state
  }
}

// Export singleton instance
export const jtlOAuth = new JTLHubOAuth()

// Export types
export type { AuthResponse, JTLOAuthConfig }
