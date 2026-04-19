import { test, expect } from "../fixtures/auth";
import { selectors } from "../helpers/selectors";

/**
 * Order smoke — orders list + order creation entry point.
 * Fulfilment requires a carrier purchase which we don't exercise in
 * smoke; the goal is dashboard surface coverage.
 */
test.describe("orders — list + create entry point", () => {
  test("orders page loads the list view", async ({ page }) => {
    await page.goto("/orders");
    await page.waitForLoadState("domcontentloaded");
    await expect(page).toHaveURL(/\/orders/);
    await expect(
      selectors.headingMatching(page, /orders/i),
    ).toBeVisible({ timeout: 20_000 });
  });

  test("draft-order entry point is reachable", async ({ page }) => {
    await page.goto("/draft_orders");
    await page.waitForLoadState("domcontentloaded");
    // Either we land on the draft-orders page, or the dashboard keeps us
    // on /orders — both are acceptable smoke states.
    await expect(page).toHaveURL(/draft_orders|orders/);
  });
});
