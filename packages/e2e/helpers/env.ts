/**
 * Centralised env-var resolution for the e2e smoke suite.
 *
 * Every spec/helper should import from here rather than reading
 * process.env directly so defaults stay in one place.
 */
export const env = {
  dashboardUrl: process.env.KARRIO_DASHBOARD_URL || "http://localhost:3002",
  apiUrl: process.env.KARRIO_API_URL || "http://localhost:5002",
  email: process.env.KARRIO_EMAIL || "admin@example.com",
  password: process.env.KARRIO_PASSWORD || "demo",
  // Optional tenant/org slug — smoke suite runs against the bootstrapped admin
  // org by default.  Override per-test if you need a specific org.
  orgSlug: process.env.KARRIO_ORG_SLUG || undefined,
};
