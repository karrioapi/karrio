import { test, expect } from "../fixtures/auth";
import { selectors } from "../helpers/selectors";
import { env } from "../helpers/env";

/**
 * Auth smoke — golden-path sign-in, session persistence, sign-out.
 * Reuses the storageState seeded by tests/auth.setup.ts.
 */
test.describe("auth — sign-in flow", () => {
  test("signed-in session lands on the dashboard home", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("domcontentloaded");
    // The authenticated home route should never redirect back to /signin.
    await expect(page).not.toHaveURL(/\/signin/);
    await expect(
      selectors.headingMatching(page, /shipments|dashboard|orders|trackers|welcome/i),
    ).toBeVisible();
  });

  test("session survives a full page reload", async ({ page }) => {
    await page.goto("/");
    await page.reload();
    await page.waitForLoadState("domcontentloaded");
    await expect(page).not.toHaveURL(/\/signin/);
  });

  test("unauthenticated context is redirected to /signin", async ({ browser }) => {
    // Fresh context without storageState — must NOT reach /shipments.
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto(`${env.dashboardUrl}/shipments`);
    await page.waitForURL(/\/signin/, { timeout: 15_000 });
    await expect(selectors.emailInput(page)).toBeVisible();
    await ctx.close();
  });
});
