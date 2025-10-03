/**
 * Default configuration for Karrio Insiders
 */

export interface KarrioConfig {
  /**
   * The URL of the Karrio API
   */
  apiUrl: string;

  /**
   * The client ID for OAuth2 authentication
   */
  clientId: string;

  /**
   * The client secret for OAuth2 authentication (optional)
   */
  clientSecret?: string;

  /**
   * The redirect URI for OAuth2 authentication
   */
  redirectUri: string;

  /**
   * The URL for refreshing access tokens
   */
  refreshUrl: string;

  /**
   * The URL for authorizing users
   */
  authUrl: string;

  /**
   * Supported scopes for the OAuth2 flow
   */
  scopes: string[];
}

/**
 * Default environment variable names
 */
export const ENV_VARIABLES = {
  API_URL: 'NEXT_PUBLIC_KARRIO_API_URL',
  CLIENT_ID: 'NEXT_PUBLIC_KARRIO_CLIENT_ID',
  CLIENT_SECRET: 'NEXT_PUBLIC_KARRIO_CLIENT_SECRET',
  REDIRECT_URI: 'NEXT_PUBLIC_KARRIO_REDIRECT_URI',
  REFRESH_URL: 'NEXT_PUBLIC_KARRIO_TOKEN_URL',
  AUTH_URL: 'NEXT_PUBLIC_KARRIO_AUTH_URL',
  SCOPES: 'NEXT_PUBLIC_KARRIO_SCOPES',
};

/**
 * Gets the environment variable value or fallback
 */
export function getEnv(name: string, fallback: string = ''): string {
  // For client-side code
  if (typeof window !== 'undefined') {
    // For Next.js public environment variables
    if (typeof process !== 'undefined' && process.env && name.startsWith('NEXT_PUBLIC_')) {
      return process.env[name] || fallback;
    }
  }
  // For server-side code
  else if (typeof process !== 'undefined' && process.env) {
    return process.env[name] || fallback;
  }

  return fallback;
}

/**
 * Default configuration values
 */
export const defaultConfig: KarrioConfig = {
  apiUrl: getEnv(ENV_VARIABLES.API_URL, 'http://localhost:5002'),
  clientId: getEnv(ENV_VARIABLES.CLIENT_ID, ''),
  clientSecret: getEnv(ENV_VARIABLES.CLIENT_SECRET, ''),
  redirectUri: getEnv(ENV_VARIABLES.REDIRECT_URI, typeof window !== 'undefined' ? `${window.location.origin}/auth/callback` : ''),
  refreshUrl: getEnv(ENV_VARIABLES.REFRESH_URL, 'http://localhost:5002/oauth/token/'),
  authUrl: getEnv(ENV_VARIABLES.AUTH_URL, 'http://localhost:5002/oauth/authorize'),
  scopes: getEnv(ENV_VARIABLES.SCOPES, 'read,write').split(','),
};

/**
 * Creates a configuration object with the provided overrides
 */
export function createConfig(overrides: Partial<KarrioConfig> = {}): KarrioConfig {
  // Override defaults with environment variables first
  const envConfig = {
    apiUrl: process.env.NEXT_PUBLIC_KARRIO_API_URL || defaultConfig.apiUrl,
    clientId: process.env.NEXT_PUBLIC_KARRIO_CLIENT_ID || defaultConfig.clientId,
    clientSecret: process.env.NEXT_PUBLIC_KARRIO_CLIENT_SECRET || defaultConfig.clientSecret,
    redirectUri: process.env.NEXT_PUBLIC_KARRIO_REDIRECT_URI || defaultConfig.redirectUri,
    refreshUrl: process.env.NEXT_PUBLIC_KARRIO_TOKEN_URL || defaultConfig.refreshUrl,
    authUrl: process.env.NEXT_PUBLIC_KARRIO_AUTH_URL || defaultConfig.authUrl,
    scopes: process.env.NEXT_PUBLIC_KARRIO_SCOPES ?
      process.env.NEXT_PUBLIC_KARRIO_SCOPES.split(',') :
      defaultConfig.scopes,
  };

  // Then apply any specific overrides
  return {
    ...envConfig,
    ...overrides,
  };
}
