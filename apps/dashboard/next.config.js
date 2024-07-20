// This file sets a custom webpack configuration to use your Next.js app
// with Sentry.
// https://nextjs.org/docs/api-reference/next.config.js/introduction
// https://docs.sentry.io/platforms/javascript/guides/nextjs/

const path = require('path');
const { withSentryConfig } = require('@sentry/nextjs');

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || '';

const moduleExports = {
  swcMinify: true,
  reactStrictMode: true,
  transpilePackages: ['@karrio/hooks', '@karrio/ui', '@karrio/lib', '@karrio/types'],
  basePath: BASE_PATH,
  sassOptions: {
    includePaths: [path.join(__dirname, 'src', 'styles')],
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
