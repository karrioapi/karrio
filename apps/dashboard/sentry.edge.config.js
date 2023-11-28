// sentry.edge.config.js or sentry.edge.config.ts

import * as Sentry from "@sentry/nextjs";
import getConfig from 'next/config';


const { publicRuntimeConfig } = getConfig();
const SENTRY_DSN = publicRuntimeConfig.SENTRY_DSN;

Sentry.init({
    dsn: SENTRY_DSN,
    tracesSampleRate: 1.0,
});
