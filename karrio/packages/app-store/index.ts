import { createCachedImport } from "./utils";
import type { AppStoreConfig } from "./types";

// App Store Registry - similar to Cal.com's implementation
const appStore: AppStoreConfig = {
  apps: {
    // Built-in apps - using manifest IDs for consistency
    "karrio.app.shipping-tasks": createCachedImport(() => import("./apps/shipping-tasks")),
    "shopify": createCachedImport(() => import("./apps/shopify")),

    // Example marketplace apps (these would be loaded dynamically in production)
    // shipstation: createCachedImport(() => import("./apps/shipstation")),
    // woocommerce: createCachedImport(() => import("./apps/woocommerce")),
  },
  loading: {
    timeout: 10000, // 10 seconds
    retries: 3,
  },
};

/**
 * Gets the app store configuration
 */
export function getAppStore(): AppStoreConfig {
  return appStore;
}

/**
 * Registers a new app in the store
 */
export function registerApp(appId: string, importFunc: () => Promise<any>) {
  appStore.apps[appId] = createCachedImport(importFunc);
}

/**
 * Unregisters an app from the store
 */
export function unregisterApp(appId: string) {
  delete appStore.apps[appId];
}

/**
 * Gets list of registered app IDs
 */
export function getRegisteredApps(): string[] {
  return Object.keys(appStore.apps);
}

// Export types and components
export * from "./types";
export * from "./utils";
export * from "./modules/Store";
export { AppConfigurationSheet as AppConfigureSheet } from "./components/app-configuration-view";
export { AppDetailsForm } from "./components/app-details-view";
export { AppContainer } from "./components/app-container";
export { AppLauncher } from "./components/app-launcher";
export { AppSheet } from "./components/app-sheet";

// Export libs
export * from "./lib/karrio-client";
export * from "./lib/app-client";
export * from "./lib/app-auth";

// Export authentication utilities
export * from "./lib/app-oauth-provider";
export * from "./lib/karrio-client";
export * from "./lib/app-client";
export * from "./lib/app-auth";

// Export specific utils for convenience
export {
  loadAppModule,
  normalizeAppMetadata,
  appSupportsViewport,
  createAppError,
  getAppManifest,
  validateAppManifest
} from "./utils";

// Export the app store as default
export default appStore;
