import { test as base, expect } from "@playwright/test";
import { KarrioApi } from "../helpers/api";

/**
 * Extended Playwright test that provides a shared KarrioApi REST client
 * authenticated as the default admin.
 *
 * Browser-side auth (NextAuth session cookies) is handled by the
 * `setup` project in playwright.config.ts — this fixture is for
 * REST-backed seeding (addresses, parcels, carrier connections, etc.).
 */
type Fixtures = {
  api: KarrioApi;
};

export const test = base.extend<Fixtures>({
  api: async ({}, use) => {
    const api = new KarrioApi();
    await api.login();
    await use(api);
    await api.dispose();
  },
});

export { expect };
