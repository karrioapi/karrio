// This file sets a custom webpack configuration to use your Next.js app
// with Sentry.
// https://nextjs.org/docs/api-reference/next.config.js/introduction
// https://docs.sentry.io/platforms/javascript/guides/nextjs/

const path = require('path');
const { withSentryConfig } = require('@sentry/nextjs');

const BASE_PATH = process.env.BASE_PATH || '';
const KARRIO_PUBLIC_URL = (
  process.env.KARRIO_PUBLIC_URL || process.env.NEXT_PUBLIC_KARRIO_API_URL
);
const KARRIO_URL = (
  process.env.KARRIO_URL || process.env.KARRIO_HOSTNAME || KARRIO_PUBLIC_URL
);
const SENTRY_DSN = (
  process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN
);
const MULTI_TENANT = (
  Boolean(JSON.parse(process.env.MULTI_TENANT || 'false'))
);

const moduleExports = {
  swcMinify: true,
  reactStrictMode: true,
  basePath: BASE_PATH,
  sassOptions: {
    includePaths: [path.join(__dirname, 'src', 'styles')],
  },
  serverRuntimeConfig: {
    KARRIO_URL: KARRIO_URL,
    JWT_SECRET: process.env.JWT_SECRET,
    TENANT_ENV_KEY: process.env.TENANT_ENV_KEY,
    KARRIO_ADMIN_URL: process.env.KARRIO_ADMIN_URL,
    KARRIO_ADMIN_API_KEY: process.env.KARRIO_ADMIN_API_KEY,
  },
  publicRuntimeConfig: {
    BASE_PATH: BASE_PATH,
    SENTRY_DSN: SENTRY_DSN,
    MULTI_TENANT: MULTI_TENANT,
    KARRIO_PUBLIC_URL: KARRIO_PUBLIC_URL,
    NEXTAUTH_URL: process.env.DASHBOARD_URL,
    DASHBOARD_VERSION: process.env.DASHBOARD_VERSION,
  },
  sentry: {
    disableServerWebpackPlugin: true,
    disableClientWebpackPlugin: true,
  },

  async headers() {
    return [
      {
        source: '/api/auth/:slug',
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-store, max-age=0',
          },
          {
            key: 'CDN-Cache-Control',
            value: 'no-store, max-age=0',
          },
        ],
      },
    ];
  },
};

const sentryWebpackPluginOptions = {
  // Additional config options for the Sentry Webpack plugin. Keep in mind that
  // the following options are set automatically, and overriding them is not
  // recommended:
  //   release, url, org, project, authToken, configFile, stripPrefix,
  //   urlPrefix, include, ignore

  silent: true, // Suppresses all logs
  // For all available options, see:
  // https://github.com/getsentry/sentry-webpack-plugin#options.
};

// Make sure adding Sentry options is the last code to run before exporting, to
// ensure that your source maps include changes from all other Webpack plugins
module.exports = withSentryConfig(moduleExports, sentryWebpackPluginOptions);
