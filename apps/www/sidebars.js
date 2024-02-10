/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  product: [
    {
      type: 'category',
      label: 'INTRODUCTION',
      collapsed: false,
      items: [
        'quick-start',
        'local-development',
      ],
    },
    {
      type: 'category',
      label: 'PRODUCT',
      collapsed: false,
      link: { type: 'doc', id: 'product' },
      items: [
        'product/connections',
        'product/shipments',
        'product/trackers',
        'product/orders',
        'product/workflows',
        'product/webhooks',
        'product/events',
        'product/api-logs',
        'product/document-templates',
      ],
    },
    {
      type: 'category',
      label: 'SELF-HOSTING',
      collapsed: true,
      collapsible: true,
      link: { type: 'doc', id: 'self-hosting' },
      items: [
        'self-hosting/oss',
        'self-hosting/enterprise',
        {
          type: 'category',
          label: 'Configure',
          collapsed: true,
          collapsible: true,
          items: [
            'self-hosting/administration',
            'self-hosting/environment',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'SEE ALSO',
      collapsed: true,
      collapsible: true,
      link: { type: 'doc', id: 'faq' },
      items: [
        'faq',
        'support',
        {
          type: 'category',
          label: 'Contributing',
          collapsed: true,
          collapsible: true,
          items: [
            'contributing/guidlines',
            'contributing/development',
          ],
        },
        "privacy",
        "terms"
      ],
    },
  ],
  reference: [
    {
      type: 'link',
      label: 'API Reference',
      href: '/api'
    },
    {
      type: 'category',
      label: 'Shipping API',
      link: {
        type: 'generated-index',
        title: 'Shipping API Guides',
        description: 'Learn how to use the Karrio Shipping APIs.',
        slug: '/reference',
        keywords: ['guides'],
      },
      items: [
        'api/authentication',
        'api/error-codes',
        'api/pagination',
        'api/metadata',
        'api/carriers',
        'api/shipments',
        'api/trackers',
        // 'api/addresses',
        // 'api/parcels',
        'api/orders',
        'api/batches',
      ],
    },
    {
      type: 'category',
      label: 'Management API',
      link: {
        type: 'generated-index',
        title: 'Karrio Management API',
        description: 'Learn how to use the Karrio management GraphQL API.',
        slug: '/management',
        keywords: ['management', 'graphql'],
      },
      items: [
        'management/overview',
        'management/organizations',
        'management/users',
        'management/connections',
        'management/data',
      ],
    },
  ],
  carriers: [
    {
      type: 'category',
      label: 'CARRIER INTEGRATIONS',
      link: { type: 'doc', id: 'integrations' },
      collapsed: false,
      items: [
        'carriers/integrations/allied_express',
        'carriers/integrations/amazon_shipping',
        'carriers/integrations/aramex',
        'carriers/integrations/asendia_us',
        'carriers/integrations/australiapost',
        'carriers/integrations/boxknight',
        'carriers/integrations/bpost',
        'carriers/integrations/canadapost',
        'carriers/integrations/canpar',
        'carriers/integrations/chronopost',
        'carriers/integrations/colissimo',
        'carriers/integrations/dhl-express',
        'carriers/integrations/dhl-poland',
        'carriers/integrations/dhl-universal',
        'carriers/integrations/dicom',
        'carriers/integrations/dpdhl',
        'carriers/integrations/fedex',
        'carriers/integrations/geodis',
        'carriers/integrations/laposte',
        'carriers/integrations/nationex',
        'carriers/integrations/purolator',
        'carriers/integrations/roadie',
        'carriers/integrations/royalmail',
        'carriers/integrations/sendle',
        'carriers/integrations/tnt',
        'carriers/integrations/ups',
        'carriers/integrations/usps',
        'carriers/integrations/usps-international',
        'carriers/integrations/generic-carrier',
      ],
    },
    {
      type: 'category',
      label: 'SDK',
      collapsed: true,
      collapsible: true,
      link: { type: 'doc', id: 'sdk' },
      items: [
        'carriers/sdk/architecture',
        'carriers/sdk/gateways',
        'carriers/sdk/rating',
        'carriers/sdk/shipping',
        'carriers/sdk/tracking',
        'carriers/sdk/pickup',
        'carriers/sdk/debugging',
        'carriers/sdk/extension',
      ],
    },
  ]
};

export default sidebars;
