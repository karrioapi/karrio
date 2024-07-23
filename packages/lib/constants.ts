// environment variables and constants

export const BASE_PATH = (process.env.NEXT_PUBLIC_BASE_PATH || "/").replace(
  "//",
  "/",
);
export const TEST_BASE_PATH = (BASE_PATH + "/test").replace("//", "/");

export const KARRIO_PUBLIC_URL =
  process.env.KARRIO_PUBLIC_URL || process.env.NEXT_PUBLIC_KARRIO_PUBLIC_URL;
export const KARRIO_URL =
  process.env.KARRIO_URL || process.env.KARRIO_HOSTNAME || KARRIO_PUBLIC_URL;
export const KARRIO_API =
  typeof window === "undefined" ? KARRIO_URL : KARRIO_PUBLIC_URL;

export const SENTRY_DSN =
  process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN;
export const POSTHOG_KEY =
  process.env.POSTHOG_KEY || process.env.NEXT_PUBLIC_POSTHOG_KEY;
export const POSTHOG_HOST =
  process.env.POSTHOG_HOST || process.env.NEXT_PUBLIC_POSTHOG_HOST;
export const NEXTAUTH_SECRET =
  process.env.NEXTAUTH_SECRET || process.env.JWT_SECRET;

export const TENANT_ENV_KEY = process.env.TENANT_ENV_KEY;
export const KARRIO_ADMIN_URL = process.env.KARRIO_ADMIN_URL;
export const KARRIO_ADMIN_API_KEY = process.env.KARRIO_ADMIN_API_KEY;
export const MULTI_TENANT = Boolean(
  JSON.parse(process.env.NEXT_PUBLIC_MULTI_TENANT || "false"),
);

export const DASHBOARD_VERSION = process.env.NEXT_PUBLIC_DASHBOARD_VERSION;
export const DASHBOARD_URL = process.env.NEXT_PUBLIC_DASHBOARD_URL;
