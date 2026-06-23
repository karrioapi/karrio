import { test, expect } from "@playwright/test";

// LIVE integration smoke against a running, seeded Karrio backend (the sandbox).
// Gated behind KARRIO_LIVE so it never runs in the default mocked suite.
//   bin/studio-sandbox            # bring up API + seed sample data
//   npm run dev -w @karrio/studio # studio on :3003
//   KARRIO_LIVE=1 KARRIO_STUDIO_URL=http://localhost:3003 \
//     npx playwright test --project=studio-live
const LIVE = process.env.KARRIO_LIVE === "1";
const EMAIL = process.env.KARRIO_EMAIL || "admin@example.com";
const PASSWORD = process.env.KARRIO_PASSWORD || "demo";

test.skip(!LIVE, "Set KARRIO_LIVE=1 with a running, seeded Karrio sandbox.");

test.describe("Studio live (seeded sandbox)", () => {
  test("real login then Shipments lists seeded data", async ({ page }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");
    await page.getByTestId("login-email").fill(EMAIL);
    await page.locator("#password").fill(PASSWORD);
    await page.getByTestId("login-submit").click();
    await expect(page).toHaveURL(/\/home$/, { timeout: 30_000 });

    await page.getByTestId("nav-shipments").click();
    await expect(page.getByTestId("screen-shipments")).toBeVisible();
    // Seeded data → at least one row, OR a clean empty-state (both valid).
    const rows = page.locator('[data-testid^="shipment-row-"]');
    // Seeded sandbox → expect at least one live shipment row (cold Django + the
    // session→fetch hop can take a few seconds).
    await expect(rows.first()).toBeVisible({ timeout: 20_000 });
  });

  test("trackers and orders screens load against live API", async ({ page }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");
    await page.getByTestId("login-email").fill(EMAIL);
    await page.locator("#password").fill(PASSWORD);
    await page.getByTestId("login-submit").click();
    await expect(page).toHaveURL(/\/home$/, { timeout: 30_000 });

    await page.goto("/trackers");
    await expect(page.getByTestId("screen-trackers")).toBeVisible();
    await page.goto("/orders");
    await expect(page.getByTestId("screen-orders")).toBeVisible();
  });
});
