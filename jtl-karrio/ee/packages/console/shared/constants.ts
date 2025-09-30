import { env } from "next-runtime-env";

// Public environment variables
export const TENANT_API_DOMAIN = (
  env("NEXT_PUBLIC_KARRIO_PLATFORM_TENANT_API_DOMAIN") ||
  env("KARRIO_PLATFORM_TENANT_API_DOMAIN")
);
export const TENANT_DASHBOARD_DOMAIN = (
  env("NEXT_PUBLIC_KARRIO_PLATFORM_TENANT_DASHBOARD_DOMAIN") ||
  env("KARRIO_PLATFORM_TENANT_DASHBOARD_DOMAIN")
);
export const STRIPE_PUBLISHABLE_KEY = env("NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY");
export const STRIPE_PRICING_TABLE_ID = env(
  "NEXT_PUBLIC_STRIPE_PRICING_TABLE_ID",
);

// Server-only environment variables
let PLATFORM_API_URL: string | undefined;
let PLATFORM_API_KEY: string | undefined;
let DATABASE_URL: string | undefined;
let DIRECT_URL: string | undefined;
let AUTH_SECRET: string | undefined;
let GITHUB_CLIENT_ID: string | undefined;
let GITHUB_CLIENT_SECRET: string | undefined;
let STRIPE_SECRET_KEY: string | undefined;

if (typeof window === "undefined") {
  PLATFORM_API_URL = env("KARRIO_PLATFORM_API_URL");
  PLATFORM_API_KEY = env("KARRIO_PLATFORM_API_KEY");
  DATABASE_URL = env("DATABASE_URL");
  DIRECT_URL = env("DIRECT_URL");
  AUTH_SECRET = env("AUTH_SECRET") || env("NEXTAUTH_SECRET");
  GITHUB_CLIENT_ID = env("GITHUB_CLIENT_ID");
  GITHUB_CLIENT_SECRET = env("GITHUB_CLIENT_SECRET");
  STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY");
}

export {
  PLATFORM_API_URL,
  PLATFORM_API_KEY,
  DATABASE_URL,
  DIRECT_URL,
  AUTH_SECRET,
  GITHUB_CLIENT_ID,
  GITHUB_CLIENT_SECRET,
  STRIPE_SECRET_KEY,
};
