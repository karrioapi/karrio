// Production-ready app route registry
// Uses side-effect imports to ensure all routes are registered

// Registry interface
export interface AppRouteHandler {
  GET?: (request: any, context?: any) => Promise<any>;
  POST?: (request: any, context?: any) => Promise<any>;
  PUT?: (request: any, context?: any) => Promise<any>;
  DELETE?: (request: any, context?: any) => Promise<any>;
  PATCH?: (request: any, context?: any) => Promise<any>;
}

// Static route registry - populated at build time
const staticRoutes: Record<string, Record<string, AppRouteHandler>> = {};

// Cache for route lookups
const routeCache = new Map<string, AppRouteHandler | null>();

// Initialize flag to ensure routes are loaded
let routesInitialized = false;

/**
 * Initialize all app routes using side-effect imports
 * This ensures all routes are registered properly
 */
function initializeRoutes() {
  if (routesInitialized) return;

  try {
    // Import app registration modules to trigger route registration
    // These imports have side effects that populate the staticRoutes registry
    require('../apps/shopify/api');
    // Add other app imports here as needed

    routesInitialized = true;
  } catch (error) {
    console.warn('Failed to initialize app routes:', error);
    routesInitialized = true; // Mark as initialized to avoid repeated attempts
  }
}

/**
 * Gets an app route handler from the static registry
 * This approach works reliably in both development and production
 */
export async function getAppRoute(appId: string, apiPath: string): Promise<AppRouteHandler | null> {
  // Ensure routes are initialized
  initializeRoutes();

  const cacheKey = `${appId}:${apiPath}`;

  // Return cached result if available
  if (routeCache.has(cacheKey)) {
    return routeCache.get(cacheKey) || null;
  }

  // Look up route in static registry
  const routeHandler = staticRoutes[appId]?.[apiPath] || null;

  // Cache the result
  routeCache.set(cacheKey, routeHandler);

  return routeHandler;
}

// Helper function to check if route exists
export async function hasAppRoute(appId: string, apiPath: string): Promise<boolean> {
  const route = await getAppRoute(appId, apiPath);
  return !!route;
}

// Function to register new app routes (for extensibility)
export function registerAppRoutes(appId: string, routes: Record<string, AppRouteHandler>) {
  if (!staticRoutes[appId]) {
    staticRoutes[appId] = {};
  }
  Object.assign(staticRoutes[appId], routes);

  // Clear cache for this app
  const keysToDelete: string[] = [];
  routeCache.forEach((value, key) => {
    if (key.startsWith(`${appId}:`)) {
      keysToDelete.push(key);
    }
  });
  keysToDelete.forEach(key => routeCache.delete(key));
}
