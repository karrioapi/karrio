// App assets utility functions
// Handles loading and resolving app static assets and README files

import type { AppManifest } from '../types';

/**
 * Clean asset path by removing common prefixes
 */
function cleanAssetPath(assetPath: string): string {
  let cleanPath = assetPath;

  // Remove leading ./ if present
  if (cleanPath.startsWith('./')) {
    cleanPath = cleanPath.slice(2);
  }

  // Remove leading assets/ if present
  if (cleanPath.startsWith('assets/')) {
    cleanPath = cleanPath.slice('assets/'.length);
  }

  return cleanPath;
}

/**
 * Get the asset URL for an app, handling both development and production
 */
function getAssetUrl(appSlug: string, assetPath: string): string {
  // In development, use the dev-assets API route
  if (process.env.NODE_ENV === 'development') {
    return `/api/dev-assets/${appSlug}/${assetPath}`;
  }

  // In production, use the build-time copied assets from public directory
  return `/app-assets/${appSlug}/${assetPath}`;
}

/**
 * Resolves an asset path relative to the app directory
 */
export function resolveAssetPath(appId: string, assetPath: string): string {
  // Remove leading ./ if present
  let cleanPath = assetPath.startsWith('./') ? assetPath.slice(2) : assetPath;

  // Remove leading assets/ if present to avoid double assets path
  if (cleanPath.startsWith('assets/')) {
    cleanPath = cleanPath.slice('assets/'.length);
  }

  // For development, use the source path
  if (process.env.NODE_ENV === 'development') {
    return `/api/apps/${appId}/assets/${cleanPath}`;
  }

  // For production, assets should be served from a static location
  return `/static/apps/${appId}/${cleanPath}`;
}

/**
 * Get the logo URL for an app
 */
export function getAppLogo(manifest: AppManifest): string {
  // Extract app slug from manifest or ID
  const appSlug = getAppSlug(manifest);

  // Check for custom logo in assets
  if (manifest.assets?.logo) {
    // Clean the asset path (remove ./assets/ prefix if present)
    const cleanPath = cleanAssetPath(manifest.assets.logo);
    return getAssetUrl(appSlug, cleanPath);
  }

  // Try common logo file names (these are directly in the assets folder)
  const commonLogoNames = ['logo.svg', 'logo.png', 'logo.jpg', 'icon.svg', 'icon.png'];

  // Return the first common logo name (the browser will handle 404s gracefully)
  return getAssetUrl(appSlug, commonLogoNames[0]);
}

/**
 * Get screenshot URLs for an app
 */
export function getAppScreenshots(manifest: AppManifest): string[] {
  const appSlug = getAppSlug(manifest);

  if (!manifest.assets?.screenshots || manifest.assets.screenshots.length === 0) {
    return [];
  }

  return manifest.assets.screenshots.map(screenshot => {
    // Clean the asset path and ensure it's in screenshots directory
    const cleanPath = cleanAssetPath(screenshot);
    // If the path doesn't start with screenshots/, add it
    const finalPath = cleanPath.startsWith('screenshots/') ? cleanPath : `screenshots/${cleanPath}`;
    return getAssetUrl(appSlug, finalPath);
  });
}

/**
 * Load README content for an app
 */
export async function loadAppReadme(manifest: AppManifest): Promise<string | null> {
  const appSlug = getAppSlug(manifest);

  if (!manifest.assets?.readme) {
    return null;
  }

  try {
    // Clean the asset path (remove ./assets/ prefix if present)
    const cleanPath = cleanAssetPath(manifest.assets.readme);
    const response = await fetch(getAssetUrl(appSlug, cleanPath));

    if (!response.ok) {
      return null;
    }

    return await response.text();
  } catch (error) {
    console.warn(`Failed to load README for app ${appSlug}:`, error);
    return null;
  }
}

/**
 * Get app slug from manifest
 */
function getAppSlug(manifest: AppManifest): string {
  // Use manifest slug if available
  if (manifest.slug) {
    return manifest.slug;
  }

  // Extract from ID if it follows the pattern "karrio.app.slug"
  if (manifest.id && manifest.id.includes('.')) {
    const parts = manifest.id.split('.');
    if (parts.length > 2 && parts[0] === 'karrio' && parts[1] === 'app') {
      return parts.slice(2).join('-');
    }
  }

  // Fallback to ID
  return manifest.id || 'unknown';
}

/**
 * Get asset URL for any app asset
 */
export function getAppAssetUrl(manifest: AppManifest, assetPath: string): string {
  const appSlug = getAppSlug(manifest);
  return getAssetUrl(appSlug, assetPath);
}

/**
 * Gets the README URL for an app
 */
export function getAppReadme(app: AppManifest): string | null {
  if (app.assets?.readme) {
    return resolveAssetPath(app.id, app.assets.readme);
  }

  return null;
}

/**
 * Checks if an asset exists for an app
 */
export async function checkAssetExists(appId: string, assetPath: string): Promise<boolean> {
  const fullPath = resolveAssetPath(appId, assetPath);

  try {
    const response = await fetch(fullPath, { method: 'HEAD' });
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Gets app asset metadata
 */
export function getAppAssetInfo(app: AppManifest) {
  return {
    logo: getAppLogo(app),
    screenshots: getAppScreenshots(app),
    readme: getAppReadme(app),
    hasAssets: !!(app.assets?.logo || app.assets?.screenshots || app.assets?.readme),
    hasLegacyAssets: !!(app.logo || app.screenshots),
  };
}
