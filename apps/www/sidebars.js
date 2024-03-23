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
      label: 'PRODUCT',
      collapsed: false,
      link: { type: 'doc', id: 'product' },
      items: [
        'product/quick-start',
        'product/local-development',
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
      items: [
        'product/self-hosting',
        'product/self-hosting/oss',
        'product/self-hosting/enterprise',
        'product/self-hosting/administration',
        'product/self-hosting/environment',
      ],
    },
    {
      type: 'category',
      label: 'ADDITIONAL RESOURCES',
      collapsed: true,
      collapsible: true,
      items: [
        'product/resources/faq',
        'product/resources/support',
        'product/resources/contributing',
        'product/resources/development',
        "product/resources/privacy",
        "product/resources/terms"
      ],
    },
  ],
  reference: [
    {
      type: 'link',
      label: 'OpenAPI',
      href: '/reference/openapi',
    },
    {
      type: 'category',
      label: 'Shipping API',
      link: {
        type: 'generated-index',
        title: 'Shipping API Guides',
        description: 'Learn how to use the Karrio Shipping APIs.',
        slug: '/reference',
        keywords: ['Shipping', 'REST', 'API'],
      },
      items: [
        'reference/api/authentication',
        'reference/api/error-codes',
        'reference/api/pagination',
        'reference/api/metadata',
        'reference/api/carriers',
        'reference/api/shipments',
        'reference/api/trackers',
        'reference/api/orders',
        'reference/api/batches',
      ],
    },
    {
      type: 'category',
      label: 'Management API',
      link: {
        type: 'generated-index',
        title: 'Karrio Management API',
        description: 'Learn how to use the Karrio management GraphQL API.',
        slug: '/reference/management',
        keywords: ['Management', 'Graphql'],
      },
      items: [
        'reference/management/overview',
        'reference/management/organizations',
        'reference/management/users',
        'reference/management/connections',
        'reference/management/data',
      ],
    },
  ],
  carriers: [
    {
      type: 'category',
      label: 'CARRIER INTEGRATIONS',
      link: { type: 'doc', id: 'integrations' },
      collapsed: false,
      collapsible: true,
      items: [
        'carriers/integrations/allied_express',
        'carriers/integrations/allied_express_local',
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
        'carriers/integrations/dhl_parcel_post',
        'carriers/integrations/dhl_express',
        'carriers/integrations/dhl_poland',
        'carriers/integrations/dhl_universal',
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
        'carriers/integrations/usps_international',
        'carriers/integrations/generic',
      ],
    },
    {
      type: 'category',
      label: 'SHIPPING DEV KIT',
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
