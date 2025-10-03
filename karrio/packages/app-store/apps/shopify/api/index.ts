// Shopify app API route registration
// This file registers all API routes for the Shopify app

import { registerAppRoutes } from '../../../lib/app-routes';
import * as testConnection from './test-connection/route';
import * as oauthCheckSupport from './oauth/check-support/route';
import * as oauthAuthorize from './oauth/authorize/route';
import * as oauthCallback from './oauth/callback/route';

// Register all Shopify API routes
registerAppRoutes('shopify', {
  'test-connection': testConnection,
  'oauth/check-support': oauthCheckSupport,
  'oauth/authorize': oauthAuthorize,
  'oauth/callback': oauthCallback,
});

// Export for potential direct usage
export {
  testConnection,
  oauthCheckSupport,
  oauthAuthorize,
  oauthCallback,
};
