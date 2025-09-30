interface OAuthConfig {
  clientId: string
  clientSecret: string
  redirectUri: string
  apiUrl: string
}

interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

interface UserInfo {
  id: string
  email: string
  name: string
}

class KarrioOAuth {
  private config: OAuthConfig

  constructor() {
    this.config = {
      clientId: import.meta.env.VITE_KARRIO_OAUTH_CLIENT_ID,
      clientSecret: import.meta.env.VITE_KARRIO_OAUTH_CLIENT_SECRET,
      redirectUri: import.meta.env.VITE_KARRIO_OAUTH_REDIRECT_URI,
      apiUrl: import.meta.env.VITE_KARRIO_API,
    }

    // Validate configuration
    if (!this.config.clientId || !this.config.clientSecret) {
      throw new Error(
        'OAuth configuration missing. Please check your .env file.',
      )
    }
  }

  /**
   * Generate OAuth authorization URL
   */
  getAuthorizationUrl(): string {
    const params = new URLSearchParams({
      client_id: this.config.clientId,
      response_type: 'code',
      redirect_uri: this.config.redirectUri,
      scope: 'read write',
      state: this.generateState(),
    })

    return `${this.config.apiUrl}/oauth/authorize/?${params.toString()}`
  }

  /**
   * Exchange authorization code for access token
   */
  async exchangeCodeForToken(
    code: string,
    state?: string,
  ): Promise<TokenResponse> {
    // Verify state if provided
    if (state && !this.verifyState(state)) {
      throw new Error('Invalid state parameter')
    }

    const response = await fetch(`${this.config.apiUrl}/oauth/token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        redirect_uri: this.config.redirectUri,
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(
        `Token exchange failed: ${error.error_description || error.error}`,
      )
    }

    return response.json()
  }

  /**
   * Refresh access token using refresh token
   */
  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    const response = await fetch(`${this.config.apiUrl}/oauth/token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(
        `Token refresh failed: ${error.error_description || error.error}`,
      )
    }

    return response.json()
  }

  /**
   * Get user info using access token
   */
  async getUserInfo(accessToken: string): Promise<UserInfo> {
    const response = await fetch(`${this.config.apiUrl}/graphql`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: `
          query GetUser {
            user {
              email
              full_name
              is_staff
              is_superuser
              date_joined
              permissions
            }
          }
        `,
      }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(
        `Failed to fetch user info: ${response.status} ${errorText}`,
      )
    }

    const data = await response.json()
    if (data.errors) {
      throw new Error(
        `GraphQL errors: ${data.errors.map((e: any) => e.message).join(', ')}`,
      )
    }

    const user = data.data.user
    return {
      id: user.email, // Use email as ID since it's unique
      email: user.email,
      name: user.full_name,
    }
  }

  /**
   * Store tokens securely in localStorage
   */
  storeTokens(tokens: TokenResponse): void {
    localStorage.setItem('karrio_access_token', tokens.access_token)
    localStorage.setItem('karrio_refresh_token', tokens.refresh_token)
    localStorage.setItem(
      'karrio_token_expires_at',
      (Date.now() + tokens.expires_in * 1000).toString(),
    )
  }

  /**
   * Get stored tokens
   */
  getStoredTokens(): {
    accessToken: string | null
    refreshToken: string | null
    expiresAt: number | null
  } {
    return {
      accessToken: localStorage.getItem('karrio_access_token'),
      refreshToken: localStorage.getItem('karrio_refresh_token'),
      expiresAt: localStorage.getItem('karrio_token_expires_at')
        ? parseInt(localStorage.getItem('karrio_token_expires_at')!)
        : null,
    }
  }

  /**
   * Check if current token is valid (not expired)
   */
  isTokenValid(): boolean {
    const { accessToken, expiresAt } = this.getStoredTokens()
    if (!accessToken || !expiresAt) return false

    // Check if token expires in the next 5 minutes
    return Date.now() < expiresAt - 5 * 60 * 1000
  }

  /**
   * Clear stored tokens
   */
  clearTokens(): void {
    localStorage.removeItem('karrio_access_token')
    localStorage.removeItem('karrio_refresh_token')
    localStorage.removeItem('karrio_token_expires_at')
    localStorage.removeItem('karrio_user_info')
    localStorage.removeItem('oauth_state')
  }

  /**
   * Generate and store random state for CSRF protection
   */
  private generateState(): string {
    const state =
      Math.random().toString(36).substring(2, 15) +
      Math.random().toString(36).substring(2, 15)
    localStorage.setItem('oauth_state', state)
    return state
  }

  /**
   * Verify state parameter
   */
  private verifyState(state: string): boolean {
    const storedState = localStorage.getItem('oauth_state')
    localStorage.removeItem('oauth_state') // Clean up after verification
    return storedState === state
  }

  /**
   * Check if user is authenticated
   */
  async isAuthenticated(): Promise<boolean> {
    const { accessToken, refreshToken } = this.getStoredTokens()

    if (!accessToken) return false

    if (this.isTokenValid()) {
      return true
    }

    // Try to refresh token if we have a refresh token
    if (refreshToken) {
      try {
        const newTokens = await this.refreshToken(refreshToken)
        this.storeTokens(newTokens)
        return true
      } catch (error) {
        console.error('Token refresh failed:', error)
        this.clearTokens()
        return false
      }
    }

    return false
  }
}

export const oauth = new KarrioOAuth()
export type { TokenResponse, UserInfo }
