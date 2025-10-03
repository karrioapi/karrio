import { NextRequest } from 'next/server';
import { createKarrioClient } from './karrio-client';

export interface AppAuthContext {
  appId: string;
  installation: AppInstallationAuth;
  apiKey: string;
  accessScopes: string[];
  karrio: ReturnType<typeof createKarrioClient>;
}

export interface AppInstallationAuth {
  id: string;
  app_id: string;
  app_name: string;
  api_key: string;           // Auto-generated API key
  access_scopes: string[];   // Permissions for this API key
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface MetafieldData {
  id: string;
  key: string;
  value: string;
  type: string;
  is_required: boolean;
  is_sensitive: boolean;
}

/**
 * Gets app installation using app's own authentication
 * This works without active user sessions (for webhooks, background jobs, etc.)
 */
export async function getAppInstallation(
  appId: string,
  request: NextRequest
): Promise<AppInstallationAuth> {
  // Try to get installation using app's own API key first
  try {
    const appApiKey = request.headers.get('x-app-api-key') ||
      request.headers.get('authorization')?.replace('Bearer ', '');

    if (!appApiKey) {
      throw new Error('No app API key found');
    }

    return await getAppInstallationByApiKey(appId, appApiKey);
  } catch (error) {
    // Fallback to user session-based lookup (for UI requests)
    return await getAppInstallationByUserSession(appId, request);
  }
}

/**
 * Gets app installation using the app's own API key (session-independent)
 */
async function getAppInstallationByApiKey(
  appId: string,
  apiKey: string
): Promise<AppInstallationAuth> {
  // Use the app's API key to authenticate with Karrio and get installation
  const response = await fetch(`${getApiBaseUrl()}/api/app-installations`, {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch app installations with app API key');
  }

  const installations = await response.json();
  const installation = installations.find((inst: AppInstallationAuth) =>
    inst.app_id === appId && inst.api_key === apiKey && inst.is_active
  );

  if (!installation) {
    throw new Error(`App ${appId} is not installed or API key is invalid`);
  }

  return installation;
}

/**
 * Gets app installation using user session (fallback for UI requests)
 */
async function getAppInstallationByUserSession(
  appId: string,
  request: NextRequest
): Promise<AppInstallationAuth> {
  // Extract user/org context from request (implement based on your auth system)
  const userId = getUserIdFromRequest(request);
  const orgId = getOrgIdFromRequest(request);
  const userToken = getAuthTokenFromRequest(request);

  if (!userToken && (!userId && !orgId)) {
    throw new Error('No authentication context found');
  }

  // Query app installation using user session
  const response = await fetch(`${getApiBaseUrl()}/api/app-installations`, {
    headers: {
      'Authorization': `Bearer ${userToken}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch app installations');
  }

  const installations = await response.json();
  const installation = installations.find((inst: AppInstallationAuth) =>
    inst.app_id === appId && inst.is_active
  );

  if (!installation) {
    throw new Error(`App ${appId} is not installed or not active`);
  }

  return installation;
}

/**
 * Gets app metafields for the installation using app's own API key
 */
export async function getAppMetafields(
  installationId: string,
  apiKey?: string
): Promise<MetafieldData[]> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // Use app's API key if provided, otherwise rely on session
  if (apiKey) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  }

  const response = await fetch(`${getApiBaseUrl()}/api/app-installations/${installationId}/metafields`, {
    headers,
  });

  if (!response.ok) {
    throw new Error('Failed to fetch app metafields');
  }

  return response.json();
}

/**
 * Validates app API key with Karrio
 */
export async function validateAppApiKey(apiKey: string): Promise<boolean> {
  try {
    const response = await fetch(`${getApiBaseUrl()}/api/user`, {
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
    });

    return response.ok;
  } catch (error) {
    console.error('API key validation error:', error);
    return false;
  }
}

/**
 * Creates authenticated context for app request
 * Handles both session-based and session-independent authentication
 */
export async function createAppContext(
  appId: string,
  request: NextRequest
): Promise<AppAuthContext> {
  // Try session-independent authentication first (using app's own API key)
  try {
    return await createSessionIndependentAppContext(appId, request);
  } catch (error) {
    // Fallback to session-based authentication (for UI requests)
    return await createSessionBasedAppContext(appId, request);
  }
}

/**
 * Creates app context using app's own API key (session-independent)
 * This works for webhooks, background jobs, etc.
 */
async function createSessionIndependentAppContext(
  appId: string,
  request: NextRequest
): Promise<AppAuthContext> {
  // Extract app API key from request headers
  const appApiKey = request.headers.get('x-app-api-key') ||
    request.headers.get('authorization')?.replace('Bearer ', '');

  if (!appApiKey) {
    throw new Error('No app API key found in request');
  }

  // Get installation directly using the API key (much simpler!)
  const installation = await getAppInstallationByApiKey(appId, appApiKey);

  // Validate that the API key matches the installation
  if (installation.api_key !== appApiKey) {
    throw new Error('API key mismatch');
  }

  // Create Karrio client
  const karrio = createKarrioClient(installation.api_key);

  return {
    appId,
    installation,
    apiKey: installation.api_key,
    accessScopes: installation.access_scopes,
    karrio,
  };
}

/**
 * Creates app context using user session (fallback for UI requests)
 */
async function createSessionBasedAppContext(
  appId: string,
  request: NextRequest
): Promise<AppAuthContext> {
  // Get app installation using user session
  const installation = await getAppInstallationByUserSession(appId, request);

  // API key is now directly on the installation - much simpler!
  if (!installation.api_key) {
    throw new Error('App installation missing API key');
  }

  // Validate API key
  const isValid = await validateAppApiKey(installation.api_key);
  if (!isValid) {
    throw new Error('Invalid API key on installation');
  }

  // Create Karrio client using app's API key
  const karrio = createKarrioClient(installation.api_key);

  return {
    appId,
    installation,
    apiKey: installation.api_key,
    accessScopes: installation.access_scopes,
    karrio,
  };
}

/**
 * Middleware to authenticate app requests
 */
export async function authenticateAppRequest(
  appId: string,
  request: NextRequest
): Promise<AppAuthContext> {
  try {
    return await createAppContext(appId, request);
  } catch (error) {
    console.error(`App authentication error [${appId}]:`, error);
    throw new Error('Authentication failed');
  }
}

/**
 * Gets credentials for an app from metafields
 */
export async function getAppCredentials(
  installationId: string,
  keys: string[]
): Promise<Record<string, string>> {
  const metafields = await getAppMetafields(installationId);
  const credentials: Record<string, string> = {};

  for (const key of keys) {
    const field = metafields.find(m => m.key === key);
    if (field) {
      credentials[key] = field.value;
    }
  }

  return credentials;
}

/**
 * No longer needed - API key is auto-generated during installation
 * This function is kept for backward compatibility but does nothing
 */
export async function setupAppOAuth(
  appId: string,
  installationId: string
): Promise<void> {
  console.log(`OAuth setup not needed for app ${appId} - API key is auto-generated during installation`);
}

/**
 * Rotates API key for an app installation
 */
export async function rotateAppApiKey(
  appId: string,
  installationId: string
): Promise<string> {
  // Call backend API to rotate the API key on the installation
  const response = await fetch(`${getApiBaseUrl()}/api/app-installations/${installationId}/rotate-api-key`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to rotate API key');
  }

  const result = await response.json();
  return result.api_key;
}

// Helper functions (implement based on your auth system)
function getUserIdFromRequest(request: NextRequest): string | null {
  // Implement based on your authentication system
  // This might extract from JWT token, session, etc.
  return null;
}

function getOrgIdFromRequest(request: NextRequest): string | null {
  // Implement based on your organization system
  return null;
}

function getAuthTokenFromRequest(request: NextRequest): string {
  // Extract auth token from request headers/cookies
  const authHeader = request.headers.get('authorization');
  if (authHeader?.startsWith('Bearer ')) {
    return authHeader.substring(7);
  }
  return '';
}

function getApiBaseUrl(): string {
  return process.env.KARRIO_API_URL || 'http://localhost:8000';
}
