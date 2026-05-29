import { type Page, expect } from "@playwright/test";

// Studio nav routes by mode (mirrors apps/studio src/lib/modes.ts).
export const STUDIO_NAV: Record<string, string[]> = {
  ship: ["home", "shipments", "trackers", "orders", "pickups", "connections", "rules", "addresses", "parcels", "products", "documents"],
  build: ["apps", "plugins", "mcp", "editor", "webhooks", "apikeys"],
  govern: ["admin", "tenants", "team", "security", "audit", "settings"],
};

export const ALL_STUDIO_ROUTES = Object.values(STUDIO_NAV).flat();

/** Navigate to a Studio screen by route and wait for the shell to render. */
export async function gotoStudio(page: Page, route = "home"): Promise<void> {
  await page.goto(`/${route}`);
  await expect(page.getByTestId("sidebar")).toBeVisible();
  await expect(page.getByTestId(`screen-${route}`)).toBeVisible();
}

/** Switch mode via the sidebar segmented control. */
export async function switchMode(page: Page, mode: "ship" | "build" | "govern"): Promise<void> {
  await page.getByTestId(`mode-${mode}`).click();
}
