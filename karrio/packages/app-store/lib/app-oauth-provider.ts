export interface AppCredentials {
  karrio_client_id: string;
  karrio_client_secret: string;
  karrio_api_key: string;
  [key: string]: any; // For external service credentials
}

export interface OAuthAppResponse {
  client_id: string;
  client_secret: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  scope: string;
}

export class AppOAuthProvider {
  private appId: string;
  private installationId: string;
  private baseURL: string;

  constructor(appId: string, installationId: string) {
    this.appId = appId;
    this.installationId = installationId;
    this.baseURL = typeof window !== 'undefined' ? window.location.origin : process.env.KARRIO_API_URL || 'http://localhost:8000';
  }

  /**
   * Creates a Karrio OAuth application for the app
   */
  async createKarrioOAuthApp(): Promise<OAuthAppResponse> {
    const response = await fetch(`${this.baseURL}/api/oauth/applications`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.getAuthToken()}`
      },
      body: JSON.stringify({
        name: `${this.appId}-app-${this.installationId}`,
        description: `OAuth app for ${this.appId} embedded application`,
        redirect_uris: [
          `${this.baseURL}/api/apps/${this.appId}/oauth/callback`
        ],
        client_type: 'confidential',
        authorization_grant_type: 'client_credentials'
      })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to create OAuth app: ${error}`);
    }

    return response.json();
  }

  /**
   * Gets an API key using client credentials flow
   */
  async getApiKey(clientId: string, clientSecret: string): Promise<string> {
    const tokenResponse = await fetch(`${this.baseURL}/api/oauth/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        grant_type: 'client_credentials',
        client_id: clientId,
        client_secret: clientSecret,
        scope: 'read write' // App-specific scopes
      })
    });

    if (!tokenResponse.ok) {
      const error = await tokenResponse.text();
      throw new Error(`Failed to get API key: ${error}`);
    }

    const tokenData: TokenResponse = await tokenResponse.json();
    return tokenData.access_token;
  }

  /**
   * Stores credentials in app installation metafields
   */
  async storeCredentials(credentials: AppCredentials): Promise<void> {
    const response = await fetch(`${this.baseURL}/api/app-installations/${this.installationId}/metafields`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.getAuthToken()}`
      },
      body: JSON.stringify({
        metafields: Object.entries(credentials).map(([key, value]) => ({
          key,
          value: typeof value === 'object' ? JSON.stringify(value) : value.toString(),
          type: 'string',
          is_sensitive: key.includes('secret') || key.includes('key') || key.includes('token')
        }))
      })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to store credentials: ${error}`);
    }
  }

  /**
   * Retrieves stored credentials from metafields
   */
  async getCredentials(): Promise<Record<string, string>> {
    const response = await fetch(`${this.baseURL}/api/app-installations/${this.installationId}/metafields`, {
      headers: {
        'Authorization': `Bearer ${this.getAuthToken()}`
      }
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to get credentials: ${error}`);
    }

    const metafields = await response.json();
    const credentials: Record<string, string> = {};

    for (const field of metafields) {
      credentials[field.key] = field.value;
    }

    return credentials;
  }

  /**
   * Updates specific credentials without affecting others
   */
  async updateCredentials(updates: Partial<AppCredentials>): Promise<void> {
    const existingCredentials = await this.getCredentials();
    const updatedCredentials = { ...existingCredentials, ...updates };
    await this.storeCredentials(updatedCredentials as AppCredentials);
  }

  /**
   * Rotates the Karrio API key
   */
  async rotateApiKey(): Promise<string> {
    const credentials = await this.getCredentials();
    const clientId = credentials.karrio_client_id;
    const clientSecret = credentials.karrio_client_secret;

    if (!clientId || !clientSecret) {
      throw new Error('Karrio OAuth credentials not found');
    }

    const newApiKey = await this.getApiKey(clientId, clientSecret);
    await this.updateCredentials({ karrio_api_key: newApiKey });

    return newApiKey;
  }

  /**
   * Gets the current authentication token (from session or context)
   */
  private getAuthToken(): string {
    // This would be implemented based on your auth system
    // For now, assuming it's available in the environment or context
    if (typeof window !== 'undefined') {
      // Client-side: get from session/cookies
      return ''; // Would implement actual token retrieval
    } else {
      // Server-side: get from request context
      return process.env.KARRIO_API_TOKEN || '';
    }
  }
}

/**
 * Helper function to handle app installation with OAuth setup
 */
export async function handleAppInstallation(appId: string, installationId: string): Promise<void> {
  const oauthProvider = new AppOAuthProvider(appId, installationId);

  try {
    // 1. Create Karrio OAuth app
    const { client_id, client_secret } = await oauthProvider.createKarrioOAuthApp();

    // 2. Get API key using client credentials
    const api_key = await oauthProvider.getApiKey(client_id, client_secret);

    // 3. Store credentials in metafields
    await oauthProvider.storeCredentials({
      karrio_client_id: client_id,
      karrio_client_secret: client_secret,
      karrio_api_key: api_key
    });

    console.log('App OAuth setup completed successfully');
  } catch (error) {
    console.error('Failed to setup app OAuth:', error);
    throw error;
  }
}

/**
 * Extended provider for apps that need dual OAuth (Karrio + External service)
 */
export class DualOAuthProvider extends AppOAuthProvider {
  /**
   * Sets up both Karrio and external service OAuth
   */
  async setupDualOAuth(externalCredentials: Record<string, any>): Promise<void> {
    // 1. Setup Karrio OAuth (inherited)
    const { client_id, client_secret } = await this.createKarrioOAuthApp();
    const karrio_api_key = await this.getApiKey(client_id, client_secret);

    // 2. Store both Karrio and external service credentials
    await this.storeCredentials({
      // Karrio OAuth
      karrio_client_id: client_id,
      karrio_client_secret: client_secret,
      karrio_api_key: karrio_api_key,

      // External service credentials
      ...externalCredentials
    });
  }

  /**
   * Updates external service credentials after OAuth flow completion
   */
  async completeExternalOAuth(externalUpdates: Record<string, any>): Promise<void> {
    await this.updateCredentials(externalUpdates);
  }
}
