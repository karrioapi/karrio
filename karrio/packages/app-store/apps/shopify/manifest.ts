import { AppManifest } from '@karrio/app-store/types';

export const manifest: AppManifest = {
  // Basic App Information
  id: 'shopify',
  name: 'Shopify',
  slug: 'shopify',
  description: 'Connect your Shopify store to Karrio for automated shipping rate calculations and label generation',
  version: '1.0.0',
  type: 'builtin',
  category: 'ecommerce',

  // Static assets
  assets: {
    logo: './assets/logo.svg',
    screenshots: [
      './assets/screenshots/configuration.png',
      './assets/screenshots/oauth-setup.png',
      './assets/screenshots/rate-calculation.png',
    ],
    readme: './README.md',
  },

  // Developer Information
  developer: {
    name: 'Karrio',
    email: 'support@karrio.io',
    website: 'https://karrio.io',
  },

  // App Configuration
  ui: {
    viewports: ['dashboard'],
    settings: true,
  },

  // Features
  features: ['shipments', 'webhooks'],

  // Essential Configuration Fields
  metafields: [
    // Shopify Store Connection
    {
      key: 'shopify_shop_domain',
      label: 'Shop Domain',
      type: 'text',
      description: 'Your Shopify store domain (e.g., mystore.myshopify.com)',
      is_required: true,
      validation: {
        format: '^[a-zA-Z0-9][a-zA-Z0-9-]*\\.myshopify\\.com$',
      },
    },
    {
      key: 'shopify_access_token',
      label: 'Access Token',
      type: 'password',
      description: 'Shopify private app access token',
      is_required: true,
      sensitive: true,
    },

    // Carrier Service Configuration
    {
      key: 'carrier_service_name',
      label: 'Carrier Service Name',
      type: 'text',
      description: 'Name displayed in Shopify checkout',
      default_value: 'Karrio Shipping',
      is_required: false,
    },
    {
      key: 'enable_rate_calculation',
      label: 'Enable Rate Calculation',
      type: 'boolean',
      description: 'Allow Shopify to request shipping rates from Karrio',
      default_value: true,
      is_required: false,
    },

    // Operational Settings
    {
      key: 'default_package_weight',
      label: 'Default Package Weight (kg)',
      type: 'number',
      description: 'Default weight for items without weight specified',
      default_value: 0.5,
      is_required: false,
    },
    {
      key: 'rate_markup_percentage',
      label: 'Rate Markup (%)',
      type: 'number',
      description: 'Percentage markup to add to shipping rates',
      default_value: 0,
      is_required: false,
    },
  ],

  // OAuth Configuration
  oauth: {
    required: true,
    scopes: ['read_orders', 'write_shipping'],
  },

  // Webhook Configuration
  webhooks: {
    events: ['shipment.created'],
    endpoint: '/api/apps/shopify/webhooks',
  },

  // API Configuration
  api: {
    // Public endpoints that don't require authentication
    publicEndpoints: [
      'test-connection',
      'oauth/check-support',
      'oauth/authorize',
      'oauth/callback',
      'assets/*'
    ],
  },
};
