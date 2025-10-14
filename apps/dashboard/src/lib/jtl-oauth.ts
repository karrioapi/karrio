/**
 * JTL Hub OAuth Client
 *
 * Implements Authorization Code Flow with PKCE (Proof Key for Code Exchange)
 * per OAuth 2.0 best practices:
 * 1. Generate PKCE code verifier and challenge
 * 2. Redirect to JTL Hub for authentication
 * 3. Handle callback with authorization code
 * 4. Exchange code for tokens (id_token, access_token, refresh_token)
 * 5. Exchange JTL tokens for Karrio JWT
 */

interface JTLOAuthConfig {
  clientId: string
  authorizeUrl: string
  tokenUrl: string
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

interface JTLTokenResponse {
  access_token: string
  token_type: string
  expires_in: number
  refresh_token?: string
  id_token?: string
  scope: string
}

class JTLHubOAuth {
  private config: JTLOAuthConfig

  constructor() {
    this.config = {
      clientId: import.meta.env.VITE_JTL_HUB_CLIENT_ID || '',
      authorizeUrl: import.meta.env.VITE_JTL_HUB_AUTHORIZE_URL || 'https://auth.jtl-cloud.com/oauth2/auth',
      tokenUrl: import.meta.env.VITE_JTL_HUB_TOKEN_URL || 'https://auth.jtl-cloud.com/oauth2/token',
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
   * Generate PKCE code verifier (random 43-128 character string)
   */
  private generateCodeVerifier(): string {
    const array = new Uint8Array(32)
    crypto.getRandomValues(array)
    return this.base64UrlEncode(array)
  }

  /**
   * Generate PKCE code challenge from verifier (SHA-256 hash, base64url encoded)
   */
  private async generateCodeChallenge(verifier: string): Promise<string> {
    const encoder = new TextEncoder()
    const data = encoder.encode(verifier)
    const hash = await crypto.subtle.digest('SHA-256', data)
    return this.base64UrlEncode(new Uint8Array(hash))
  }

  /**
   * Base64URL encode (without padding)
   */
  private base64UrlEncode(array: Uint8Array): string {
    const base64 = btoa(String.fromCharCode(...array))
    return base64
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '')
  }

  /**
   * Redirect to JTL Hub for authentication with PKCE
   */
  async login(): Promise<void> {
    if (!this.config.clientId) {
      throw new Error('JTL Hub CLIENT_ID not configured')
    }

    // Generate PKCE codes
    const codeVerifier = this.generateCodeVerifier()
    const codeChallenge = await this.generateCodeChallenge(codeVerifier)

    // Store code verifier for token exchange
    sessionStorage.setItem('jtl_oauth_code_verifier', codeVerifier)

    const state = this.generateState()
    const params = new URLSearchParams({
      client_id: this.config.clientId,
      response_type: 'code',  // Authorization code flow
      redirect_uri: this.config.redirectUri,
      state,
      scope: 'openid offline_access',  // OpenID Connect + refresh token
      code_challenge: codeChallenge,
      code_challenge_method: 'S256',
    })

    const authUrl = `${this.config.authorizeUrl}?${params.toString()}`
    console.log('Redirecting to JTL Hub with PKCE:', authUrl)
    window.location.href = authUrl
  }

  /**
   * Exchange authorization code for JTL Hub tokens, then exchange for Karrio tokens
   *
   * @param code - Authorization code from JTL Hub
   * @returns Promise with Karrio JWT and user/org info
   */
  async handleCallback(code: string): Promise<AuthResponse> {
    try {
      // Step 1: Exchange authorization code for JTL Hub tokens
      const jtlTokens = await this.exchangeCodeForToken(code)

      // Step 2: Exchange JTL access token for Karrio JWT
      const response = await fetch(`${this.config.apiUrl}/auth/jtl/callback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: jtlTokens.access_token }),
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
   * Exchange authorization code for JTL Hub tokens using PKCE
   *
   * @param code - Authorization code from callback
   * @returns Promise with JTL Hub token response
   */
  private async exchangeCodeForToken(code: string): Promise<JTLTokenResponse> {
    // Retrieve code verifier from session storage
    const codeVerifier = sessionStorage.getItem('jtl_oauth_code_verifier')
    sessionStorage.removeItem('jtl_oauth_code_verifier')

    if (!codeVerifier) {
      throw new Error('PKCE code verifier not found - possible session timeout')
    }

    const params = new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: this.config.redirectUri,
      client_id: this.config.clientId,
      code_verifier: codeVerifier,
    })

    const response = await fetch(this.config.tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: params.toString(),
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.error_description || error.error || `Token exchange failed: ${response.status}`)
    }

    const tokens: JTLTokenResponse = await response.json()
    console.log('JTL Hub tokens obtained:', {
      hasAccessToken: !!tokens.access_token,
      hasRefreshToken: !!tokens.refresh_token,
      hasIdToken: !!tokens.id_token,
      expiresIn: tokens.expires_in,
      scope: tokens.scope,
    })

    return tokens
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
