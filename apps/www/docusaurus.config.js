// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import { themes as prismThemes } from 'prism-react-renderer';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const posthogPlugins = (
  process.env.POSTHOG_KEY ? [[
    "posthog-docusaurus",
    {
      apiKey: process.env.POSTHOG_KEY, // required
      appUrl: process.env.POSTHOG_HOST || "https://app.posthog.com", // optional
      enableInDevelopment: false, // optional
    },
  ]] : []
)

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

  markdown: {
    mermaid: true,
  },

  plugins: [
    'tailwind-loader',
    // 'content-pages',
    ...posthogPlugins,
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: [
          {
            to: '/product/quick-start',
            from: '/quick-start',
          },
          {
            to: '/product/local-development',
            from: '/local-development',
          },
          {
            to: '/product/resources/faq',
            from: '/faq',
          },
          {
            to: '/product/resources/support',
            from: '/support',
          },
          {
            to: '/product/resources/privacy',
            from: '/privacy',
          },
          {
            to: '/product/resources/terms',
            from: '/terms',
          },
          {
            to: '/product/resources/contributing',
            from: '/contributing/guidlines',
          },
          {
            to: '/product/resources/development',
            from: '/contributing/development',
          },
          {
            to: '/product/self-hosting',
            from: '/guides/self-hosting',
          },
          {
            to: '/product/self-hosting/oss',
            from: '/self-hosting/oss',
          },
          {
            to: '/product/self-hosting/pla',
            from: '/self-hosting/enterprise',
          },
          {
            to: '/product/self-hosting/administration',
            from: '/self-hosting/administration',
          },
          {
            to: '/product/self-hosting/environment',
            from: '/self-hosting/environment',
          },
        ],
      },
    ],
    [
      'docusaurus-plugin-openapi-docs',
      {
        id: "api",
        docsPluginId: "openapi",
        config: {
          api: {
            specPath: "./openapi.yml",
            outputDir: "docs/reference/api",
            sidebarOptions: {
              groupPathsBy: "tag",
              categoryLinkSource: "tag",
              sidebarCollapsible: true,
              sidebarCollapsed: true,
            },
            downloadUrl: "./openapi.yml",
            // showSchemas: true,
          },
        }
      },
    ],
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/karrioapi/docs/edit/main/apps/www/',
          sidebarCollapsible: false,
          docItemComponent: "@theme/ApiItem",
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
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
            spec: '../../schemas/openapi.yml',
            route: '/reference/openapi/',
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
            href: 'https://platform.karrio.io',
            position: 'left',
            label: 'Platform',
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
                label: 'Carriers',
                href: 'https://docs.karrio.io/carriers/',
              },
              {
                label: 'Product',
                href: 'https://docs.karrio.io/product',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Launch week X',
                href: 'https://www.karrio.io/launch-week-x',
              },
              {
                label: 'Discussions',
                href: 'https://github.com/karrioapi/karrio/discussions',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/karrio',
              },
            ],
          },
          {
            title: 'Company',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/karrioapi/karrio',
              },
              {
                label: 'Blog',
                href: 'https://www.karrio.io/blog',
              },
              {
                label: 'API Reference',
                href: '/reference/openapi',
              },
            ],
          },
          {
            title: 'Get Started',
            items: [
              {
                label: 'Platform',
                href: 'https://platform.karrio.io'
              },
              {
                label: 'Download',
                to: '/product/self-hosting',
              },
            ],
          },
        ],
        logo: {
          alt: 'Karrio Inc.',
          src: 'img/logo-inverted.svg',
          href: 'https://www.karrio.io',
          width: 180,
          height: 'auto',
        },
        copyright: `Copyright © ${new Date().getFullYear()} karrio Inc. - the modern shipping infrastructure for global commerce`,
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

  themes: [
    '@docusaurus/theme-mermaid',
    'docusaurus-theme-openapi-docs',
  ],
};

export default config;
