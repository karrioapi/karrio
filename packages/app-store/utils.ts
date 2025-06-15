import type {
  AppManifest,
  AppModule,
  AppStoreConfig,
  AppInstance,
  AppLoadError,
  AppError
} from "./types";

// Cache for loaded app modules
const appModuleCache = new Map<string, AppModule>();

// Cache for app manifests
const appManifestCache = new Map<string, AppManifest>();

/**
 * Creates a cached import function similar to Cal.com's implementation
 */
export function createCachedImport<T>(importFunc: () => Promise<T>): () => Promise<T> {
  let cachedModule: T | undefined;

  return async () => {
    if (!cachedModule) {
      cachedModule = await importFunc();
    }
    return cachedModule;
  };
}

/**
 * Loads an app module with caching and error handling
 */
export async function loadAppModule(
  appId: string,
  importFunc: () => Promise<AppModule>,
  options?: {
    timeout?: number;
    retries?: number;
  }
): Promise<AppModule> {
  const cacheKey = appId;

  // Check cache first
  if (appModuleCache.has(cacheKey)) {
    return appModuleCache.get(cacheKey)!;
  }

  try {
    // Load with timeout
    const timeout = options?.timeout || 10000; // 10 seconds default
    const modulePromise = importFunc();

    const timeoutPromise = new Promise<never>((_, reject) => {
      setTimeout(() => reject(new Error(`App ${appId} failed to load within ${timeout}ms`)), timeout);
    });

    const module = await Promise.race([modulePromise, timeoutPromise]);

    // Validate module structure
    if (!module.default) {
      throw new Error(`App ${appId} does not export a default manifest`);
    }

    // Cache the loaded module
    appModuleCache.set(cacheKey, module);
    appManifestCache.set(cacheKey, module.default);

    return module;
  } catch (error) {
    const appError: AppLoadError = {
      code: "APP_LOAD_ERROR",
      message: `Failed to load app ${appId}: ${error}`,
      app_id: appId,
      details: { error }
    };
    throw appError;
  }
}

/**
 * Gets app manifest from cache or loads it
 */
export async function getAppManifest(
  appId: string,
  importFunc?: () => Promise<AppModule>
): Promise<AppManifest | null> {
  // Check cache first
  if (appManifestCache.has(appId)) {
    return appManifestCache.get(appId)!;
  }

  // If import function is provided, load the module
  if (importFunc) {
    try {
      const module = await loadAppModule(appId, importFunc);
      return module.default;
    } catch (error) {
      console.error(`Failed to load manifest for app ${appId}:`, error);
      return null;
    }
  }

  return null;
}

/**
 * Validates an app manifest
 */
export function validateAppManifest(manifest: any): manifest is AppManifest {
  if (!manifest || typeof manifest !== 'object') {
    return false;
  }

  const required = ['id', 'name', 'slug', 'version', 'description', 'developer', 'category', 'type'];

  for (const field of required) {
    if (!(field in manifest)) {
      console.warn(`App manifest missing required field: ${field}`);
      return false;
    }
  }

  // Validate developer object
  if (!manifest.developer || typeof manifest.developer !== 'object') {
    console.warn('App manifest missing or invalid developer object');
    return false;
  }

  if (!manifest.developer.name || !manifest.developer.email) {
    console.warn('App manifest developer missing name or email');
    return false;
  }

  return true;
}

/**
 * Gets the full path to an app asset
 */
export function getAppAssetPath(appId: string, assetPath: string): string {
  // For local development, assets should be in the app's static folder
  // In production, these would be served from a CDN
  return `/apps/${appId}/static/${assetPath}`;
}

/**
 * Normalizes app metadata from different sources
 */
export function normalizeAppMetadata(rawApp: any): Partial<AppInstance> {
  if (!rawApp || typeof rawApp !== 'object') {
    return {};
  }
  return {
    id: rawApp.id,
    isInstalled: !!rawApp.installation,
    isEnabled: rawApp.installation ? rawApp.installation.enabled !== false : false,
    installation: rawApp.installation ? {
      id: rawApp.installation.id,
      app_id: rawApp.id,
      access_scopes: rawApp.installation.access_scopes || [],
      config: rawApp.installation.metadata || {},
      metadata: rawApp.installation.metadata || {},
      installed_at: rawApp.installation.created_at,
      updated_at: rawApp.installation.updated_at,
    } : undefined,
    config: rawApp.installation?.metadata || {},
  };
}

/**
 * Checks if an app supports a specific viewport
 */
export function appSupportsViewport(manifest: AppManifest, viewport: string): boolean {
  if (!manifest.ui?.viewports) {
    return false;
  }

  return manifest.ui.viewports.includes(viewport as any) ||
    manifest.ui.viewports.includes('everywhere');
}

/**
 * Checks if an app has a specific feature
 */
export function appHasFeature(manifest: AppManifest, feature: string): boolean {
  return manifest.features.includes(feature as any);
}

/**
 * Gets app permissions/scopes from manifest
 */
export function getAppRequiredScopes(manifest: AppManifest): string[] {
  if (!manifest.oauth?.required) {
    return [];
  }

  return manifest.oauth.scopes || [];
}

/**
 * Creates an error for app operations
 */
export function createAppError(
  code: string,
  message: string,
  details?: Record<string, any>
): AppError {
  return {
    code,
    message,
    details
  };
}

/**
 * Retries an async operation with exponential backoff
 */
export async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error as Error;

      if (attempt === maxRetries) {
        break;
      }

      // Exponential backoff: wait longer between each retry
      const delay = baseDelay * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}

/**
 * Safe JSON parse with error handling
 */
export function safeJsonParse<T = any>(json: string, fallback: T): T {
  try {
    return JSON.parse(json);
  } catch {
    return fallback;
  }
}

/**
 * Deep merge two objects
 */
export function deepMerge<T extends Record<string, any>>(target: T, source: Partial<T>): T {
  const result = { ...target };

  for (const key in source) {
    if (source.hasOwnProperty(key)) {
      const sourceValue = source[key];
      const targetValue = result[key];

      if (
        sourceValue &&
        typeof sourceValue === 'object' &&
        !Array.isArray(sourceValue) &&
        targetValue &&
        typeof targetValue === 'object' &&
        !Array.isArray(targetValue)
      ) {
        result[key] = deepMerge(targetValue, sourceValue);
      } else {
        result[key] = sourceValue as T[Extract<keyof T, string>];
      }
    }
  }

  return result;
}
