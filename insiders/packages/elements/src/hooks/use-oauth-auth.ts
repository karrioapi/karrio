import { useState, useEffect, useCallback } from 'react';
import { useKarrio } from '../provider/karrio-provider';
import { KarrioConfig, defaultConfig } from '../lib/config';

interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
  accessToken: string | null;
  userId: string | null;
  error: string | null;
}

interface UseOAuthAuthOptions {
  config?: Partial<KarrioConfig>;
  onSuccess?: (data: { accessToken: string; userId: string }) => void;
  onError?: (error: string) => void;
}

// Generate random string for PKCE
function generateRandomString(length: number): string {
  let text = '';
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
  for (let i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

// Create code challenge from code verifier
async function generateCodeChallenge(codeVerifier: string): Promise<string> {
  if (typeof crypto === 'undefined' || !crypto.subtle) {
    throw new Error('Crypto API not available');
  }

  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await crypto.subtle.digest('SHA-256', data);

  return base64URLEncode(digest);
}

// Base64URL encode for PKCE
function base64URLEncode(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }

  return btoa(binary)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

export function useOAuthAuth(options: UseOAuthAuthOptions = {}) {
  const karrio = useKarrio();
  // Ensure we have complete configuration by merging defaults with overrides
  const config = { ...defaultConfig, ...options.config };

  // Make sure clientId is never empty (failsafe)
  if (!config.clientId && typeof window !== 'undefined') {
    // Try to get from localStorage or sessionStorage as a fallback
    const storedClientId = localStorage.getItem('karrio_client_id') || sessionStorage.getItem('karrio_client_id');
    if (storedClientId) {
      config.clientId = storedClientId;
    } else if (process.env.NEXT_PUBLIC_KARRIO_CLIENT_ID) {
      config.clientId = process.env.NEXT_PUBLIC_KARRIO_CLIENT_ID;
    }
  }

  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: karrio.isAuthenticated,
    isLoading: false,
    accessToken: karrio.accessToken,
    userId: karrio.userId,
    error: null,
  });

  // Initialize OAuth flow - make safe for SSR
  const initiateOAuth = useCallback(async () => {
    // Exit early if we're in SSR context
    if (typeof window === 'undefined') {
      console.warn('initiateOAuth called during server-side rendering - this is not supported');
      return;
    }

    // Validate essential OAuth parameters
    if (!config.clientId) {
      const errorMessage = 'Client ID is required for OAuth flow';
      console.error(errorMessage);
      setAuthState(prev => ({ ...prev, error: errorMessage }));
      return;
    }

    if (!config.redirectUri) {
      const errorMessage = 'Redirect URI is required for OAuth flow';
      console.error(errorMessage);
      setAuthState(prev => ({ ...prev, error: errorMessage }));
      return;
    }

    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // Generate PKCE code verifier and challenge
      const codeVerifier = generateRandomString(64);
      const codeChallenge = await generateCodeChallenge(codeVerifier);

      // Generate state for CSRF protection
      const state = Math.random().toString(36).substring(2, 15);

      // Store PKCE code verifier and state parameter in session storage
      sessionStorage.setItem('karrio_code_verifier', codeVerifier);
      sessionStorage.setItem('karrio_oauth_state', state);
      sessionStorage.setItem('karrio_client_id', config.clientId);
      sessionStorage.setItem('karrio_redirect_uri', config.redirectUri);

      // Store client secret if available
      if (config.clientSecret) {
        sessionStorage.setItem('karrio_client_secret', config.clientSecret);
      }

      // Debug: Log the config being used
      console.log('OAuth Config:', {
        clientId: config.clientId,
        redirectUri: config.redirectUri,
        authUrl: config.authUrl,
        scopes: config.scopes,
        codeVerifier: `${codeVerifier.substring(0, 5)}...${codeVerifier.substring(codeVerifier.length - 5)}`,
        codeChallenge
      });

      // Construct the authorization URL
      const url = new URL(config.authUrl);
      url.searchParams.append('client_id', config.clientId);
      url.searchParams.append('redirect_uri', config.redirectUri);
      url.searchParams.append('response_type', 'code');
      url.searchParams.append('scope', config.scopes.filter(s => s !== 'openid').join(' '));
      url.searchParams.append('state', state);
      url.searchParams.append('code_challenge', codeChallenge);
      url.searchParams.append('code_challenge_method', 'S256');

      // Redirect to authorization URL
      window.location.href = url.toString();
    } catch (error) {
      console.error('Error initiating OAuth flow:', error);
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to initiate OAuth flow'
      }));
    }
  }, [config]);

  // Handle the OAuth callback
  const handleCallback = useCallback(async (options: {
    onSuccess?: (data: { accessToken: string; userId: string }) => void;
    onError?: (error: string) => void;
  } = {}) => {
    if (typeof window === 'undefined') return;

    const url = new URL(window.location.href);
    const code = url.searchParams.get('code');
    const state = url.searchParams.get('state');
    const error = url.searchParams.get('error');

    if (error) {
      const errorDescription = url.searchParams.get('error_description') || 'Unknown error';
      setAuthState(prev => ({ ...prev, isLoading: false, error: `${error}: ${errorDescription}` }));
      if (options.onError) options.onError(`${error}: ${errorDescription}`);
      return;
    }

    if (!code || !state) {
      const errorMessage = 'Missing code or state in the callback URL';
      setAuthState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
      if (options.onError) options.onError(errorMessage);
      return;
    }

    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    // Verify state
    const savedState = sessionStorage.getItem('karrio_oauth_state');
    if (savedState !== state) {
      const errorMessage = 'Invalid state parameter. Authorization flow may have been tampered with.';
      setAuthState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
      if (options.onError) options.onError(errorMessage);
      return;
    }

    // Get code verifier
    const codeVerifier = sessionStorage.getItem('karrio_code_verifier');
    if (!codeVerifier) {
      const errorMessage = 'Code verifier not found. PKCE flow is broken.';
      setAuthState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
      if (options.onError) options.onError(errorMessage);
      return;
    }

    // Make sure we have a client ID - try to get from session storage if not in config
    const clientId = config.clientId || sessionStorage.getItem('karrio_client_id');
    if (!clientId) {
      const errorMessage = 'Client ID not found. OAuth flow is broken.';
      setAuthState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
      if (options.onError) options.onError(errorMessage);
      return;
    }

    // Get client secret if available - from config or session storage
    const clientSecret = config.clientSecret || sessionStorage.getItem('karrio_client_secret') || '';

    try {
      // Exchange code for tokens using URLSearchParams for x-www-form-urlencoded
      const formData = new URLSearchParams();
      formData.append('grant_type', 'authorization_code');
      formData.append('client_id', clientId);
      formData.append('code', code);
      formData.append('redirect_uri', sessionStorage.getItem('karrio_redirect_uri') || config.redirectUri);
      formData.append('code_verifier', codeVerifier);

      // Add client_secret to the form data if available
      if (clientSecret) {
        formData.append('client_secret', clientSecret);
      }

      console.log('Token Exchange Config:', {
        tokenUrl: config.refreshUrl,
        clientId: clientId,
        redirectUri: config.redirectUri,
        code: `${code.substring(0, 5)}...`,
        codeVerifier: `${codeVerifier.substring(0, 5)}...`
      });

      // Use a timeout to prevent the request from hanging indefinitely
      const fetchWithTimeout = async (url: string, options: RequestInit, timeout = 10000) => {
        const controller = new AbortController();
        const { signal } = controller;

        const timeoutId = setTimeout(() => controller.abort(), timeout);

        try {
          const response = await fetch(url, { ...options, signal });
          clearTimeout(timeoutId);
          return response;
        } catch (error) {
          clearTimeout(timeoutId);
          throw error;
        }
      };

      // Prepare headers for the token request
      const headers: HeadersInit = {
        'Content-Type': 'application/x-www-form-urlencoded',
      };

      // Add HTTP Basic Authentication if client secret is available
      if (clientSecret) {
        const authString = btoa(`${clientId}:${clientSecret}`);
        headers['Authorization'] = `Basic ${authString}`;
      }

      // Try different authentication methods
      let response;
      let responseText;
      let data;

      // First attempt: Try with Authorization header
      try {
        console.log('TOKEN EXCHANGE - Sending request to:', config.refreshUrl);
        console.log('TOKEN EXCHANGE - Form data:', Object.fromEntries(formData.entries()));

        response = await fetchWithTimeout(config.refreshUrl, {
          method: 'POST',
          headers,
          body: formData
        }, 30000); // Increased timeout for token exchange

        responseText = await response.text();

        try {
          data = JSON.parse(responseText);
        } catch (e) {
          console.warn('Failed to parse token response:', responseText);
          data = { error: 'Invalid JSON response' };
        }

        if (response.ok) {
          // Success, proceed with this response
        } else if (response.status === 401 && clientSecret) {
          // If using Authorization header failed, let's try without it
          throw new Error('Auth header method failed, trying alternative');
        }
      } catch (error) {
        console.warn('First auth attempt failed, trying alternative method:', error);

        // Remove Authorization header and rely only on form parameters
        const formDataWithSecret = new URLSearchParams(formData);
        if (clientSecret) {
          formDataWithSecret.append('client_secret', clientSecret);
        }

        response = await fetchWithTimeout(config.refreshUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: formDataWithSecret
        });

        responseText = await response.text();

        try {
          data = JSON.parse(responseText);
        } catch (e) {
          console.error('Failed to parse token response (second attempt):', responseText);
          throw new Error(`Invalid JSON response: ${responseText.substring(0, 100)}...`);
        }
      }

      if (!response.ok) {
        // Add specific handling for invalid_grant errors
        if (data.error === 'invalid_grant') {
          console.error('TOKEN EXCHANGE - Invalid grant error:', data);
          throw new Error('Authorization code expired or invalid. Please try logging in again. (Code likely expired before token exchange)');
        }
        throw new Error(data.error || `Error ${response.status}: ${response.statusText}`);
      }

      // Calculate token expiry
      const expiresIn = data.expires_in || 3600; // Default to 1 hour
      const expiryTime = new Date(Date.now() + expiresIn * 1000).toISOString();

      // Store tokens in localStorage
      localStorage.setItem('karrio_access_token', data.access_token);
      localStorage.setItem('karrio_refresh_token', data.refresh_token || '');
      localStorage.setItem('karrio_token_expiry', expiryTime);
      localStorage.setItem('karrio_user_id', data.user_id || '');

      setAuthState({
        isAuthenticated: true,
        isLoading: false,
        accessToken: data.access_token,
        userId: data.user_id || '',
        error: null,
      });

      if (options.onSuccess) {
        options.onSuccess({ accessToken: data.access_token, userId: data.user_id || '' });
      }

      // Clean up URL and session storage
      const cleanUrl = window.location.href.split('?')[0];
      window.history.replaceState({}, document.title, cleanUrl);
      sessionStorage.removeItem('karrio_oauth_state');
      sessionStorage.removeItem('karrio_code_verifier');
      sessionStorage.removeItem('karrio_client_secret'); // Clean up client secret from session storage
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
      console.error('OAuth callback error:', errorMessage);

      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage
      }));

      if (options.onError) {
        options.onError(errorMessage);
      }
    }
  }, [config]);

  // Parse URL on component mount for OAuth callback
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const url = new URL(window.location.href);
      const code = url.searchParams.get('code');
      const state = url.searchParams.get('state');

      if (code && state) {
        handleCallback({
          onSuccess: options.onSuccess,
          onError: options.onError
        });
      }
    }
  }, [handleCallback, options.onSuccess, options.onError]);

  return {
    ...authState,
    initiateOAuth,
    handleCallback,
    refreshAccessToken: karrio.refreshAccessToken,
    logout: karrio.logout,
  };
}
