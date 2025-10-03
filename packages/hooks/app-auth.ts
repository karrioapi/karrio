import { isNoneOrEmpty } from "@karrio/lib/helper";

export interface AppJWTPayload {
  iss: 'karrio-dashboard';
  aud: 'karrio-api';
  sub: string; // app-{app_id}-{installation_id}
  exp: number;
  iat: number;
  app_id: string;
  installation_id: string;
  user_id: string;
  org_id: string;
  access_scopes: string[];
}

export interface AppAuthContext {
  appId: string;
  installationId: string;
  apiKey: string;
  accessScopes: string[];
  userId: string;
  orgId: string;
}

/**
 * Simple JWT implementation for app authentication
 * This is a lightweight implementation that doesn't require external dependencies
 */
function base64UrlEncode(str: string): string {
  return btoa(str)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}

function base64UrlDecode(str: string): string {
  str += '='.repeat((4 - str.length % 4) % 4);
  return atob(str.replace(/-/g, '+').replace(/_/g, '/'));
}

async function hmacSha256(key: string, data: string): Promise<string> {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(key);
  const messageData = encoder.encode(data);

  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  const signature = await crypto.subtle.sign('HMAC', cryptoKey, messageData);
  return base64UrlEncode(String.fromCharCode(...new Uint8Array(signature)));
}

/**
 * Generate JWT token for app authentication
 */
export async function generateAppJWT(
  appId: string,
  installationId: string,
  userId: string,
  orgId: string,
  accessScopes: string[]
): Promise<string> {
  const header = {
    alg: 'HS256',
    typ: 'JWT'
  };

  const payload: AppJWTPayload = {
    iss: 'karrio-dashboard',
    aud: 'karrio-api',
    sub: `app-${appId}-${installationId}`,
    exp: Math.floor(Date.now() / 1000) + 300, // 5 minutes
    iat: Math.floor(Date.now() / 1000),
    app_id: appId,
    installation_id: installationId,
    user_id: userId,
    org_id: orgId,
    access_scopes: accessScopes
  };

  const headerEncoded = base64UrlEncode(JSON.stringify(header));
  const payloadEncoded = base64UrlEncode(JSON.stringify(payload));
  const data = `${headerEncoded}.${payloadEncoded}`;

  const secret = process.env.JWT_APP_SECRET_KEY || process.env.NEXT_PUBLIC_JWT_APP_SECRET_KEY;
  if (!secret) {
    throw new Error('JWT_APP_SECRET_KEY environment variable is required');
  }

  const signature = await hmacSha256(secret, data);
  return `${data}.${signature}`;
}

/**
 * Get current user and org context from browser context
 */
export function getCurrentContext(): { userId: string; orgId: string } {
  // For browser environment, we'll need to get this from the app component props
  // or from a context provider. For now, return placeholder values that will be
  // passed from the component.
  if (typeof window === 'undefined') {
    throw new Error('getCurrentContext can only be called in browser environment');
  }

  // These should be provided by the app container component
  const userId = (window as any).__KARRIO_USER_ID__ || '';
  const orgId = (window as any).__KARRIO_ORG_ID__ || '';

  if (isNoneOrEmpty(userId) || isNoneOrEmpty(orgId)) {
    throw new Error('User session context not available');
  }

  return { userId, orgId };
}

/**
 * Create authenticated fetch client for app API requests
 */
export function createAppApiClient(appContext: AppAuthContext) {
  return {
    async fetch(url: string, options: RequestInit = {}) {
      const { userId, orgId } = getCurrentContext();

      const jwt = await generateAppJWT(
        appContext.appId,
        appContext.installationId,
        userId,
        orgId,
        appContext.accessScopes
      );

      const headers = {
        'Authorization': `Bearer ${jwt}`,
        'Content-Type': 'application/json',
        ...options.headers,
      };

      return fetch(url, {
        ...options,
        headers,
      });
    },

    async get(url: string, options: RequestInit = {}) {
      return this.fetch(url, { ...options, method: 'GET' });
    },

    async post(url: string, data?: any, options: RequestInit = {}) {
      return this.fetch(url, {
        ...options,
        method: 'POST',
        body: data ? JSON.stringify(data) : undefined,
      });
    },

    async put(url: string, data?: any, options: RequestInit = {}) {
      return this.fetch(url, {
        ...options,
        method: 'PUT',
        body: data ? JSON.stringify(data) : undefined,
      });
    },

    async delete(url: string, options: RequestInit = {}) {
      return this.fetch(url, { ...options, method: 'DELETE' });
    },
  };
}

/**
 * Generate webhook URL with JWT token for external services
 */
export async function generateWebhookUrl(
  baseUrl: string,
  appId: string,
  installationId: string,
  endpoint: string,
  accessScopes: string[]
): Promise<string> {
  const { userId, orgId } = getCurrentContext();

  const jwt = await generateAppJWT(appId, installationId, userId, orgId, accessScopes);

  return `${baseUrl}/api/apps/${appId}/${endpoint}/${installationId}?token=${jwt}`;
}

/**
 * Validate and decode JWT token (server-side only)
 */
export async function validateAppJWT(token: string): Promise<AppJWTPayload> {
  const secret = process.env.JWT_APP_SECRET_KEY;
  if (!secret) {
    throw new Error('JWT_APP_SECRET_KEY environment variable is required');
  }

  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid JWT format');
  }

  const [headerEncoded, payloadEncoded, signatureEncoded] = parts;
  const data = `${headerEncoded}.${payloadEncoded}`;

  const expectedSignature = await hmacSha256(secret, data);
  if (signatureEncoded !== expectedSignature) {
    throw new Error('Invalid JWT signature');
  }

  const payload = JSON.parse(base64UrlDecode(payloadEncoded)) as AppJWTPayload;

  // Validate claims
  if (payload.iss !== 'karrio-dashboard') {
    throw new Error('Invalid JWT issuer');
  }

  if (payload.aud !== 'karrio-api') {
    throw new Error('Invalid JWT audience');
  }

  if (payload.exp < Math.floor(Date.now() / 1000)) {
    throw new Error('JWT token expired');
  }

  return payload;
}

/**
 * Extract app context from JWT token
 */
export async function extractAppContext(token: string): Promise<AppAuthContext> {
  const payload = await validateAppJWT(token);

  return {
    appId: payload.app_id,
    installationId: payload.installation_id,
    apiKey: '', // Not included in JWT for security
    accessScopes: payload.access_scopes,
    userId: payload.user_id,
    orgId: payload.org_id,
  };
}
