import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    // Main sections
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },

    // Getting Started section
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'getting-started/quick-start',
        'developing/introduction',
        'developing/local-development',
      ],
    },

    // API section
    {
      type: 'category',
      label: 'API Reference',
      collapsed: true,
      items: [
        'api',
        'api/overview',
        'reference/api',
        'reference/management-api',
        'webhooks',
      ],
    },

    // Shipping Integration
    {
      type: 'category',
      label: 'Shipping Integration',
      collapsed: true,
      items: [
        'shipping/overview',
        'carriers',
        'examples',
      ],
    },

    // Self-Hosting section
    {
      type: 'category',
      label: 'Self-Hosting',
      collapsed: true,
      items: [
        'self-hosting/introduction',
        'self-hosting/docker',
      ],
    },

    // Additional resources
    {
      type: 'category',
      label: 'Resources',
      collapsed: true,
      items: [
        'reference/carrier-integration',
      ],
    },
  ],
};

export default sidebars;
