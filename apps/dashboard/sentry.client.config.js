// This file configures the initialization of Sentry on the browser.
// The config you add here will be used whenever a page is visited.
// https://docs.sentry.io/platforms/javascript/guides/nextjs/

import * as Sentry from '@sentry/nextjs';
import getConfig from 'next/config';


const { publicRuntimeConfig } = getConfig();
const SENTRY_DSN = publicRuntimeConfig.SENTRY_DSN;
const API_URL = publicRuntimeConfig.KARRIO_PUBLIC_URL;

Sentry.init({
  dsn: SENTRY_DSN,
  // Adjust this value in production, or use tracesSampler for greater control
  tracesSampleRate: 1.0,
  // ...
  // Note: if you want to override the automatic release value, do not set a
  // `release` value here - use the environment variable `SENTRY_RELEASE`, so
  // that it will also get attached to your source maps
  initialScope: scope => {
    scope.setTags({
      API: API_URL,
    });
    return scope;
  },
});
