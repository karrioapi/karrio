import * as Sentry from '@sentry/nextjs';

const SENTRY_DSN = process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN;
const API_URL = process.env.KARRIO_PUBLIC_URL;

export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    Sentry.init({
      dsn: SENTRY_DSN,
      tracesSampleRate: 1.0,
      initialScope: scope => {
        scope.setTags({
          API: API_URL,
        });
        return scope;
      },
    });
  }

  if (process.env.NEXT_RUNTIME === 'edge') {
    Sentry.init({
      dsn: SENTRY_DSN,
      tracesSampleRate: 1.0,
    });
  }
}

export function onRequestError(error: Error) {
  Sentry.captureException(error);
}
