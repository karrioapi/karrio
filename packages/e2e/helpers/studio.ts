import { type Page, expect } from "@playwright/test";

// Studio nav routes by mode (mirrors apps/studio src/lib/modes.ts).
export const STUDIO_NAV: Record<string, string[]> = {
  ship: ["home", "shipments", "trackers", "orders", "pickups", "connections", "rules", "addresses", "parcels", "products", "documents", "manifests", "batches"],
  build: ["apps", "plugins", "mcp", "editor", "webhooks", "apikeys", "workflows"],
  govern: ["admin", "tenants", "team", "security", "audit", "settings", "ratesheets", "usage"],
};

export const ALL_STUDIO_ROUTES = Object.values(STUDIO_NAV).flat();

/**
 * Navigate to a Studio screen by route and wait for the shell to render AND for
 * the client to hydrate (SSR markup is interactive-looking before React attaches
 * handlers, so we must wait before clicking). `networkidle` lets Vite connect and
 * hydration settle.
 */
export async function gotoStudio(page: Page, route = "home"): Promise<void> {
  await page.goto(`/${route}`);
  await expect(page.getByTestId("sidebar")).toBeVisible();
  await expect(page.getByTestId(`screen-${route}`)).toBeVisible();
  await page.waitForLoadState("networkidle");
}

/** Switch mode via the sidebar segmented control. */
export async function switchMode(page: Page, mode: "ship" | "build" | "govern"): Promise<void> {
  await page.getByTestId(`mode-${mode}`).click();
}
