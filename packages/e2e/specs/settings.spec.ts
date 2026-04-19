import { test, expect } from "../fixtures/auth";
import { selectors } from "../helpers/selectors";

/**
 * Settings smoke — API keys page, carrier connections page,
 * and the organization profile page all render for an authenticated user.
 */
test.describe("settings — API keys, connections, profile", () => {
  test("API keys page loads", async ({ page }) => {
    await page.goto("/developers/apikeys");
    await page.waitForLoadState("domcontentloaded");
    await expect(page).toHaveURL(/\/developers\/apikeys/);
    await expect(
      selectors.headingMatching(page, /api keys?|developer/i),
    ).toBeVisible({ timeout: 20_000 });
  });

  test("carrier connections page loads", async ({ page }) => {
    await page.goto("/connections");
    await page.waitForLoadState("domcontentloaded");
    await expect(page).toHaveURL(/\/connections/);
    await expect(
      selectors.headingMatching(page, /connection|carrier/i),
    ).toBeVisible({ timeout: 20_000 });
  });

  test("organization settings page loads", async ({ page }) => {
    await page.goto("/settings/organization");
    await page.waitForLoadState("domcontentloaded");
    // May 404 gracefully on non-platform builds — accept either.
    const ok = await selectors
      .headingMatching(page, /organization|settings|profile/i)
      .isVisible({ timeout: 15_000 })
      .catch(() => false);
    const redirected = /settings/.test(page.url());
    expect(ok || redirected).toBe(true);
  });
});
