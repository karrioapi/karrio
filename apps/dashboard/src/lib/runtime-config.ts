/**
 * Runtime Configuration Management
 * 
 * This module provides a way to load configuration at runtime rather than build time.
 * It supports both client-side and server-side environments in TanStack Start.
 */

interface RuntimeConfig {
  KARRIO_API_URL: string
  KARRIO_TEST_MODE: boolean
  OAUTH_CLIENT_ID?: string
  OAUTH_CLIENT_SECRET?: string
  OAUTH_REDIRECT_URI?: string
  JTL_CLIENT_ID?: string
  JTL_CLIENT_SECRET?: string
}

let runtimeConfig: RuntimeConfig | null = null

/**
 * Get configuration from environment variables (server-side)
 */
function getServerConfig(): RuntimeConfig {
  return {
    KARRIO_API_URL: process.env.VITE_KARRIO_API || process.env.KARRIO_PUBLIC_URL || 'http://localhost:5002',
    KARRIO_TEST_MODE: process.env.VITE_KARRIO_TEST_MODE === 'true',
    OAUTH_CLIENT_ID: process.env.VITE_KARRIO_OAUTH_CLIENT_ID || process.env.OAUTH_CLIENT_ID,
    OAUTH_CLIENT_SECRET: process.env.VITE_KARRIO_OAUTH_CLIENT_SECRET || process.env.OAUTH_CLIENT_SECRET,
    OAUTH_REDIRECT_URI: process.env.VITE_KARRIO_OAUTH_REDIRECT_URI || `${process.env.DASHBOARD_URL || 'http://localhost:3102'}/auth/callback`,
    JTL_CLIENT_ID: process.env.VITE_JTL_CLIENT_ID || process.env.JTL_CLIENT_ID,
    JTL_CLIENT_SECRET: process.env.VITE_JTL_CLIENT_SECRET || process.env.JTL_CLIENT_SECRET,
  }
}

/**
 * Get configuration from build-time environment (client-side fallback)
 */
function getBuildTimeConfig(): RuntimeConfig {
  return {
    KARRIO_API_URL: import.meta.env.VITE_KARRIO_API || 'http://localhost:5002',
    KARRIO_TEST_MODE: import.meta.env.VITE_KARRIO_TEST_MODE === 'true',
    OAUTH_CLIENT_ID: import.meta.env.VITE_KARRIO_OAUTH_CLIENT_ID,
    OAUTH_CLIENT_SECRET: import.meta.env.VITE_KARRIO_OAUTH_CLIENT_SECRET,
    OAUTH_REDIRECT_URI: import.meta.env.VITE_KARRIO_OAUTH_REDIRECT_URI,
    JTL_CLIENT_ID: import.meta.env.VITE_JTL_CLIENT_ID,
    JTL_CLIENT_SECRET: import.meta.env.VITE_JTL_CLIENT_SECRET,
  }
}

/**
 * Load configuration from runtime config endpoint (client-side)
 */
async function loadClientConfig(): Promise<RuntimeConfig> {
  try {
    const response = await fetch('/api/config')
    if (response.ok) {
      return await response.json()
    }
  } catch (error) {
    console.warn('Failed to load runtime config, falling back to build-time config:', error)
  }
  
  // Fallback to build-time config if runtime config fails
  return getBuildTimeConfig()
}

/**
 * Get the runtime configuration
 * - Server-side: reads from environment variables
 * - Client-side: loads from /api/config endpoint or falls back to build-time config
 */
export async function getRuntimeConfig(): Promise<RuntimeConfig> {
  // If already cached, return it
  if (runtimeConfig) {
    return runtimeConfig
  }

  // Server-side: read from environment
  if (typeof window === 'undefined') {
    runtimeConfig = getServerConfig()
    return runtimeConfig
  }

  // Client-side: load from runtime endpoint
  runtimeConfig = await loadClientConfig()
  return runtimeConfig
}

/**
 * Synchronous getter for already-loaded config (client-side only)
 */
export function getRuntimeConfigSync(): RuntimeConfig | null {
  return runtimeConfig
}

/**
 * Initialize the runtime config (should be called early in app lifecycle)
 */
export async function initializeRuntimeConfig(): Promise<void> {
  await getRuntimeConfig()
}

/**
 * Clear the cached config (useful for testing)
 */
export function clearRuntimeConfig(): void {
  runtimeConfig = null
}