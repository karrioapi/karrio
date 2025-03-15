// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import path from 'path';

const config: Config = {
  title: 'Karrio - Programmable Shipping APIs for Platforms',
  tagline: 'The most flexible way to integrate shipping into your platform',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://karrio.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'karrioapi', // Usually your GitHub org/user name.
  projectName: 'karrio', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/karrioapi/karrio/tree/main/apps/web/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/karrioapi/karrio/tree/main/apps/web/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/karrio-social-card.png',
    navbar: {
      // title: '',
      logo: {
        alt: 'Karrio Logo',
        src: 'img/logo.svg',
      },
      hideOnScroll: false,
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        { to: '/blog', label: 'Blog', position: 'left' },
        { to: '/platform', label: 'Platform', position: 'left' },
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
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Getting Started',
              to: '/docs/getting-started/quick-start',
            },
            {
              label: 'API Reference',
              to: '/docs/api/overview',
            },
            {
              label: 'Self-Hosting',
              to: '/docs/self-hosting/introduction',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Discord',
              href: 'https://discord.gg/karrio',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/karrioapi',
            },
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/company/karrioapi',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/karrioapi/karrio',
            },
            {
              label: 'Platform',
              to: '/platform',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Karrio, Inc.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
  } satisfies Preset.ThemeConfig,
  plugins: [
    [
      async function tailwindPlugin(_context, _options) {
        return {
          name: 'docusaurus-tailwindcss',
          configurePostCss(postcssOptions) {
            // Clear existing plugins array to avoid duplicates
            postcssOptions.plugins = [];

            // Add tailwind and autoprefixer
            postcssOptions.plugins.push(
              require('tailwindcss'),
              require('autoprefixer')
            );

            return postcssOptions;
          },
        };
      },
      // Optional configuration options
      {
        // Any options here
      }
    ],
  ],
};

export default config;
