import * as React from 'react';
import { KarrioConfig } from '../lib/config';
import { createContext, useContext, useState, useEffect } from 'react';

// Authentication method types
export type AuthMethod = 'oauth' | 'auth-js' | 'token' | 'none';

// Define the context type
type KarrioContextType = {
  isLoading: boolean;
  isAuthenticated: boolean;
  accessToken: string | null;
  userId: string | null;
  sessionData: KarrioSessionData | null;
  authMethod: AuthMethod;
  theme: string;
  setTheme: (theme: string) => void;
  connectCarrier: (carrierId: string) => Promise<any>;
  refreshAccessToken: () => Promise<string | null>;
  logout: () => void;
  initiateOAuth: (options?: { scopes?: string[] }) => void;
};

// Define our own Session interface
export interface KarrioSessionData {
  accessToken?: string;
  error?: string;
  testMode?: boolean;
  orgId?: string;
  user?: {
    id: string;
    name?: string;
    email?: string;
  };
  [key: string]: any;
}

interface KarrioProviderOptions {
  apiUrl: string;
  refreshUrl: string;
  clientId: string;
  redirectUri?: string;
  authUrl?: string;
}

interface KarrioProviderProps {
  children: React.ReactNode;
  clientId?: string;
  accessToken?: string | null;
  userId?: string | null;
  sessionData?: KarrioSessionData | null;
  options?: KarrioProviderOptions;
  defaultTheme?: string;
  onAccessTokenRefresh?: (token: string) => void;
  config?: KarrioConfig;
  // Optional explicit auth method override
  authMethod?: AuthMethod;
}

// Create the context with default values
const KarrioContext = createContext<KarrioContextType | null>(null);

if (process.env.NODE_ENV !== 'production') {
  KarrioContext.displayName = 'KarrioContext';
}

export function KarrioProvider({
  children,
  clientId: propClientId,
  accessToken: initialAccessToken = null,
  userId: initialUserId = null,
  sessionData: initialSessionData = null,
  options,
  defaultTheme = 'light',
  onAccessTokenRefresh,
  config,
  authMethod: explicitAuthMethod,
}: KarrioProviderProps) {
  // Determine the client ID from various sources
  const clientId =
    config?.clientId ||
    propClientId ||
    options?.clientId ||
    (typeof window !== 'undefined' ?
      (localStorage.getItem('karrio_client_id') || sessionStorage.getItem('karrio_client_id')) : null) ||
    (typeof process !== 'undefined' ? process.env.NEXT_PUBLIC_KARRIO_CLIENT_ID : null) || '';

  // Get API URL from various sources
  const apiUrl =
    config?.apiUrl ||
    options?.apiUrl ||
    (typeof process !== 'undefined' ? process.env.NEXT_PUBLIC_KARRIO_API_URL : null) ||
    'https://api.karrio.io';

  // Get auth URL from various sources
  const authUrl =
    config?.authUrl ||
    options?.authUrl ||
    (typeof process !== 'undefined' ? process.env.NEXT_PUBLIC_KARRIO_AUTH_URL : null) ||
    `${apiUrl}/oauth/authorize`;

  // Get refresh URL from various sources
  const refreshUrl =
    config?.refreshUrl ||
    options?.refreshUrl ||
    (typeof process !== 'undefined' ? process.env.NEXT_PUBLIC_KARRIO_TOKEN_URL : null) ||
    `${apiUrl}/oauth/token/`;

  // Get redirect URI
  const redirectUri =
    config?.redirectUri ||
    options?.redirectUri ||
    (typeof process !== 'undefined' ? process.env.NEXT_PUBLIC_KARRIO_REDIRECT_URI : null) ||
    (typeof window !== 'undefined' ? `${window.location.origin}/auth/callback` : null);

  // Initialize with provided tokens or from localStorage if available
  const [accessToken, setAccessToken] = useState<string | null>(() => {
    if (initialAccessToken) return initialAccessToken;
    if (initialSessionData?.accessToken) return initialSessionData.accessToken;
    if (typeof window !== 'undefined') {
      return localStorage.getItem('karrio_access_token');
    }
    return null;
  });

  const [refreshToken, setRefreshToken] = useState<string | null>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('karrio_refresh_token');
    }
    return null;
  });

  const [userId, setUserId] = useState<string | null>(() => {
    if (initialUserId) return initialUserId;
    if (initialSessionData?.user?.id) return initialSessionData.user.id;
    if (typeof window !== 'undefined') {
      return localStorage.getItem('karrio_user_id');
    }
    return null;
  });

  const [tokenExpiry, setTokenExpiry] = useState<string | null>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('karrio_token_expiry');
    }
    return null;
  });

  // Determine the auth method based on provided props
  const [authMethod, setAuthMethod] = useState<AuthMethod>(() => {
    // If explicitly specified, use that
    if (explicitAuthMethod) {
      return explicitAuthMethod;
    }

    // Determine based on provided parameters
    if (initialSessionData) {
      return 'auth-js';
    } else if (clientId && !initialAccessToken) {
      return 'oauth';
    } else if (initialAccessToken) {
      return 'token';
    }

    // Check if we have stored tokens that might indicate previous OAuth flow
    if (typeof window !== 'undefined' && localStorage.getItem('karrio_access_token')) {
      return 'oauth';
    }

    return 'none';
  });

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [theme, setTheme] = useState(defaultTheme);

  // Initialize session data state
  const [sessionData, setSessionData] = useState<KarrioSessionData | null>(() => {
    if (initialSessionData) return initialSessionData;

    // If we have access token and userId but no sessionData, create minimal session data
    if (accessToken) {
      return {
        accessToken,
        user: { id: userId || 'unknown' }
      };
    }

    return null;
  });

  // Check if the user is authenticated (token exists and not expired)
  const isAuthenticated = !!accessToken && (
    authMethod === 'auth-js' || // Auth.js manages token validity
    (tokenExpiry ? new Date(tokenExpiry) > new Date() : true) // Check expiry for other methods
  );

  // Synchronize session data with accessToken changes
  useEffect(() => {
    if (accessToken && !sessionData?.accessToken) {
      setSessionData(prevData => ({
        ...prevData || {},
        accessToken,
        user: {
          ...prevData?.user || {},
          id: userId || prevData?.user?.id || 'unknown'
        }
      }));
    } else if (!accessToken && sessionData?.accessToken) {
      // If token is removed, clear session data
      setSessionData(null);
    }
  }, [accessToken, userId, sessionData]);

  // Setup auto token refresh for OAuth flow
  useEffect(() => {
    // Only handle token refresh for OAuth flow, not Auth.js
    if (authMethod !== 'oauth' || !isAuthenticated || !refreshToken) return;

    // If token is expired or about to expire, refresh it
    const expiryTime = tokenExpiry ? new Date(tokenExpiry).getTime() : 0;
    const currentTime = Date.now();
    const timeUntilExpiry = expiryTime - currentTime;

    // Buffer time before expiry (5 minutes)
    const refreshBuffer = 5 * 60 * 1000;

    if (timeUntilExpiry <= refreshBuffer) {
      refreshAccessToken();
      return;
    }

    // Schedule refresh for before token expires
    const refreshTimeout = setTimeout(() => {
      refreshAccessToken();
    }, timeUntilExpiry - refreshBuffer);

    return () => clearTimeout(refreshTimeout);
  }, [isAuthenticated, refreshToken, tokenExpiry, authMethod]);

  // Function to refresh the access token using PKCE
  const refreshAccessToken = async (): Promise<string | null> => {
    // Don't refresh tokens for Auth.js - it's handled by Auth.js
    if (authMethod === 'auth-js') {
      console.log('Token refresh handled by Auth.js');
      return accessToken;
    }

    if (!refreshToken || !clientId) {
      return null;
    }

    setIsLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('grant_type', 'refresh_token');
      formData.append('refresh_token', refreshToken);
      formData.append('client_id', clientId);

      const response = await fetch(refreshUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });

      const text = await response.text();
      let data;

      try {
        data = JSON.parse(text);
      } catch (e) {
        throw new Error(`Invalid JSON response: ${text.substring(0, 100)}...`);
      }

      if (!response.ok) {
        throw new Error(data.error || `Error ${response.status}: ${response.statusText}`);
      }

      // Calculate expiry time
      const expiresIn = data.expires_in || 3600; // Default to 1 hour
      const expiryTime = new Date(Date.now() + expiresIn * 1000).toISOString();

      // Update tokens in state and localStorage
      setAccessToken(data.access_token);
      setRefreshToken(data.refresh_token || refreshToken); // Use existing if not returned
      setTokenExpiry(expiryTime);
      setIsLoading(false);

      // Store tokens in localStorage
      localStorage.setItem('karrio_access_token', data.access_token);
      if (data.refresh_token) {
        localStorage.setItem('karrio_refresh_token', data.refresh_token);
      }
      localStorage.setItem('karrio_token_expiry', expiryTime);

      // Update user ID if provided
      if (data.user_id) {
        setUserId(data.user_id);
        localStorage.setItem('karrio_user_id', data.user_id);
      }

      // Callback if provided
      if (onAccessTokenRefresh) {
        onAccessTokenRefresh(data.access_token);
      }

      // Update session data
      setSessionData(prevData => ({
        ...prevData || {},
        accessToken: data.access_token,
        user: {
          ...prevData?.user || {},
          id: data.user_id || prevData?.user?.id || userId || 'unknown'
        }
      }));

      return data.access_token;
    } catch (error) {
      console.error('Failed to refresh access token:', error);
      setIsLoading(false);
      return null;
    }
  };

  const logout = () => {
    // Clear all auth-related state
    setAccessToken(null);
    setRefreshToken(null);
    setUserId(null);
    setTokenExpiry(null);

    // Clear localStorage
    localStorage.removeItem('karrio_access_token');
    localStorage.removeItem('karrio_refresh_token');
    localStorage.removeItem('karrio_user_id');
    localStorage.removeItem('karrio_token_expiry');
    localStorage.removeItem('karrio_oauth_state');
    localStorage.removeItem('karrio_code_verifier');

    // Also try sessionStorage for completeness
    sessionStorage.removeItem('karrio_oauth_state');
    sessionStorage.removeItem('karrio_code_verifier');
    sessionStorage.removeItem('karrio_auth_attempts');

    // Clear session data
    setSessionData(null);
  };

  // Generate a random string for PKCE code verifier and state
  const generateRandomString = (length: number): string => {
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
    let text = '';

    const randomValues = new Uint8Array(length);
    if (typeof window !== 'undefined' && window.crypto) {
      window.crypto.getRandomValues(randomValues);

      for (let i = 0; i < length; i++) {
        text += possible.charAt(randomValues[i] % possible.length);
      }
    } else {
      // Fallback for non-browser environments
      for (let i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
      }
    }

    return text;
  };

  // Generate code challenge from code verifier
  const generateCodeChallenge = async (codeVerifier: string): Promise<string> => {
    if (typeof window === 'undefined') {
      throw new Error('Code challenge generation is only available in browser environments');
    }

    // Hash the verifier using SHA-256
    const encoder = new TextEncoder();
    const data = encoder.encode(codeVerifier);
    const digest = await window.crypto.subtle.digest('SHA-256', data);

    // Convert the hash to base64-url format
    return btoa(String.fromCharCode(...new Uint8Array(digest)))
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');
  };

  // Initiate OAuth flow with PKCE
  const initiateOAuth = async (options?: { scopes?: string[] }) => {
    if (typeof window === 'undefined') {
      console.error('OAuth flow can only be initiated in browser environments');
      return;
    }

    if (!clientId || !redirectUri || !authUrl) {
      console.error('Missing required OAuth configuration');
      return;
    }

    // Set auth method to oauth if not already
    if (authMethod !== 'oauth') {
      setAuthMethod('oauth');
    }

    // Generate code verifier (random string between 43-128 chars)
    const codeVerifier = generateRandomString(64);
    // Save it to sessionStorage (will be needed for token exchange)
    sessionStorage.setItem('karrio_code_verifier', codeVerifier);

    // Generate state for CSRF protection
    const state = generateRandomString(32);
    sessionStorage.setItem('karrio_oauth_state', state);

    try {
      // Generate code challenge from verifier
      const codeChallenge = await generateCodeChallenge(codeVerifier);

      // Default scopes if not provided
      const scopes = options?.scopes || ['read', 'write', 'openid'];

      // Build the authorization URL
      const authorizationUrl = new URL(authUrl);

      // Add query parameters
      authorizationUrl.searchParams.append('response_type', 'code');
      authorizationUrl.searchParams.append('client_id', clientId);
      authorizationUrl.searchParams.append('redirect_uri', redirectUri);
      authorizationUrl.searchParams.append('scope', scopes.join(' '));
      authorizationUrl.searchParams.append('state', state);
      authorizationUrl.searchParams.append('code_challenge', codeChallenge);
      authorizationUrl.searchParams.append('code_challenge_method', 'S256');

      // Redirect to authorization URL
      window.location.href = authorizationUrl.toString();
    } catch (error) {
      console.error('Failed to initiate OAuth flow:', error);
    }
  };

  const connectCarrier = async (carrierId: string): Promise<any> => {
    if (!accessToken) {
      throw new Error('Authentication required to connect carrier');
    }

    setIsLoading(true);

    try {
      // This is a placeholder for actual carrier connection logic
      // In a real implementation, you would call the API to connect a carrier
      const response = await fetch(`${apiUrl}/carriers/${carrierId}/connect`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Error ${response.status}: ${response.statusText}`);
      }

      setIsLoading(false);
      return data;
    } catch (error) {
      console.error(`Failed to connect ${carrierId}:`, error);
      setIsLoading(false);
      throw error;
    }
  };

  // Create the context value
  const contextValue: KarrioContextType = {
    isLoading,
    isAuthenticated,
    accessToken,
    userId,
    sessionData,
    authMethod,
    theme,
    setTheme,
    connectCarrier,
    refreshAccessToken,
    logout,
    initiateOAuth,
  };

  // Debug log to help with troubleshooting
  useEffect(() => {
    console.log('KarrioProvider state:', {
      authMethod,
      isAuthenticated,
      hasAccessToken: !!accessToken,
      hasSessionData: !!sessionData,
    });
  }, [authMethod, isAuthenticated, accessToken, sessionData]);

  return (
    <KarrioContext.Provider
      value={contextValue}
    >
      {children}
    </KarrioContext.Provider>
  );
}

export function useKarrio(): KarrioContextType {
  const context = useContext(KarrioContext);
  if (!context) {
    throw new Error('useKarrio must be used within a KarrioProvider');
  }
  return context;
}

// New hook for accessing session data specifically
export function useKarrioSession(): KarrioSessionData | null {
  const { sessionData } = useKarrio();
  return sessionData;
}
