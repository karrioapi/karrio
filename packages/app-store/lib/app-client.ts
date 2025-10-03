import { AppOAuthProvider } from './app-oauth-provider';

export interface AppApiClientConfig {
  appId: string;
  installationId: string;
  baseURL?: string;
}

export class AppApiClient {
  private appId: string;
  private installationId: string;
  private baseURL: string;
  private apiKey: string | null = null;

  constructor(config: AppApiClientConfig) {
    this.appId = config.appId;
    this.installationId = config.installationId;
    this.baseURL = config.baseURL || (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3002');
  }

  /**
   * Initializes the client by getting the app's API key
   */
  async initialize(): Promise<void> {
    if (this.apiKey) return; // Already initialized

    const oauthProvider = new AppOAuthProvider(this.appId, this.installationId);
    const credentials = await oauthProvider.getCredentials();

    this.apiKey = credentials.karrio_api_key;
    if (!this.apiKey) {
      throw new Error('App API key not found - app may not be properly configured');
    }
  }

  /**
   * Makes an authenticated request to the app's API
   */
  private async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    await this.initialize();

    if (!this.apiKey) {
      throw new Error('App not initialized - no API key available');
    }

    const url = `${this.baseURL}/api/apps/${this.appId}/${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'X-App-API-Key': this.apiKey,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`App API error (${response.status}): ${errorText}`);
    }

    return response.json();
  }

  /**
   * GET request to app API
   */
  async get<T = any>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const queryParams = params ? `?${new URLSearchParams(params).toString()}` : '';
    return this.request(`${endpoint}${queryParams}`);
  }

  /**
   * POST request to app API
   */
  async post<T = any>(endpoint: string, data?: any): Promise<T> {
    return this.request(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * PUT request to app API
   */
  async put<T = any>(endpoint: string, data?: any): Promise<T> {
    return this.request(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * DELETE request to app API
   */
  async delete<T = any>(endpoint: string): Promise<T> {
    return this.request(endpoint, {
      method: 'DELETE',
    });
  }

  /**
   * PATCH request to app API
   */
  async patch<T = any>(endpoint: string, data?: any): Promise<T> {
    return this.request(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }
}

/**
 * Factory function to create an app API client
 */
export function createAppApiClient(config: AppApiClientConfig): AppApiClient {
  return new AppApiClient(config);
}

/**
 * Helper function for external services (like Shopify) to call app APIs
 */
export async function callAppApi(
  appId: string,
  installationId: string,
  endpoint: string,
  options: {
    method?: string;
    data?: any;
    baseURL?: string;
  } = {}
): Promise<any> {
  const client = createAppApiClient({
    appId,
    installationId,
    baseURL: options.baseURL,
  });

  const method = options.method?.toLowerCase() || 'get';

  switch (method) {
    case 'get':
      return client.get(endpoint);
    case 'post':
      return client.post(endpoint, options.data);
    case 'put':
      return client.put(endpoint, options.data);
    case 'delete':
      return client.delete(endpoint);
    case 'patch':
      return client.patch(endpoint, options.data);
    default:
      throw new Error(`Unsupported HTTP method: ${method}`);
  }
}

/**
 * Hook for React components to use app API client
 */
export function useAppApiClient(appId: string, installationId: string): AppApiClient {
  // In a real React app, you might want to memoize this and handle initialization
  return createAppApiClient({ appId, installationId });
}
