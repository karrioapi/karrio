// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Karrio',
  tagline: 'The Open source shipping API for enterprise and platform.',
  url: 'https://karrio.io',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'karrioapi', // Usually your GitHub org/user name.
  projectName: 'karrio', // Usually your repo name.

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  plugins: [
    'tailwind-loader',
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: 'https://github.com/karrioapi/docs/edit/main/apps/www/',
          sidebarCollapsible: false,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
    // Redocusaurus config
    [
      'redocusaurus',
      {
        // Plugin Options for loading OpenAPI files
        specs: [
          {
            spec: 'https://raw.githubusercontent.com/karrioapi/karrio/main/schemas/openapi.yml',
            route: '/api/',
          },
        ],
        // Theme Options for modifying how redoc renders them
        theme: {
          // Change with your site colors
          primaryColor: '#1890ff',
          options: {
            hideHostname: true
          }
        },
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/karrio.png',
      metaImage: 'img/karrio.png',
      navbar: {
        // title: 'Karrio',
        logo: {
          alt: 'Karrio',
          src: 'img/logo.svg',
          srcDark: 'img/logo-inverted.svg',
        },
        items: [
          {
            to: '/product',
            position: 'left',
            label: 'Product',
          },
          {
            to: '/reference',
            position: 'left',
            label: 'Reference',
          },
          {
            to: '/carriers',
            position: 'left',
            label: 'Carriers',
          },
          {
            href: 'https://karrio.io',
            position: 'right',
            label: 'Karrio.io',
          },
          {
            href: 'https://github.com/karrioapi/karrio',
            position: 'right',
            className: 'header-github-link',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Resources',
            items: [
              {
                label: 'Docs',
                to: '/',
              },
              {
                label: 'Product',
                to: '/product',
              },
              {
                label: 'Reference',
                to: '/reference',
              },
              {
                label: 'OpenAPI',
                href: '/api',
              },
              {
                label: 'Carriers',
                to: '/carriers',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Discussions',
                href: 'https://github.com/karrioapi/karrio/discussions',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/karrio',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/karrio',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: 'https://karrio.io/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/karrioapi/karrio',
              },
            ],
          },
          {
            title: 'About Us',
            items: [
              {
                label: 'Join our beta',
                href: 'https://karrio.io/get-started',
              },
              {
                label: 'FAQ',
                href: 'https://karrio.io/get-started#FAQ',
              },
            ],
          },
        ],
        logo: {
          alt: 'Karrio Inc.',
          src: 'img/logo-inverted.svg',
        },
        copyright: `Copyright © ${new Date().getFullYear()} karrio Inc.`,
      },
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 4,
      },
      prism: {
        defaultLanguage: 'js',
        additionalLanguages: ['json'],
        plugins: ['line-numbers', 'show-language'],
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
