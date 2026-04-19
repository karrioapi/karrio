import { test, expect } from "../fixtures/auth";
import { selectors } from "../helpers/selectors";

/**
 * Tracking smoke — the /trackers list loads, and a public tracking
 * lookup surfaces an event stream (or a not-found state if no tracker
 * with that number exists — both are acceptable smoke signals).
 */
test.describe("tracking — dashboard list + public lookup", () => {
  test("trackers page loads the list view", async ({ page }) => {
    await page.goto("/trackers");
    await page.waitForLoadState("domcontentloaded");
    await expect(page).toHaveURL(/\/trackers/);
    await expect(
      selectors.headingMatching(page, /tracker|tracking/i),
    ).toBeVisible({ timeout: 20_000 });
  });

  test("public tracking page renders for an arbitrary tracking number", async ({ page }) => {
    // The public tracking route accepts any tracking number and renders
    // either an event timeline or a "not found" message.  Either
    // response is acceptable for a smoke test.
    await page.goto("/tracking/E2E-SMOKE-12345");
    await page.waitForLoadState("domcontentloaded");
    // Any visible tracking-related content is a pass.
    const body = page.locator("body");
    await expect(body).toContainText(/track|ship|delivery|status|not found/i, {
      timeout: 20_000,
    });
  });
});
