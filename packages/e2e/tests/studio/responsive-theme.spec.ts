import { test, expect } from "@playwright/test";
import { gotoStudio } from "../../helpers/studio";

// Responsive layout + dark/light theme review.

test.describe("Responsive layout", () => {
  test("desktop shows the sidebar inline", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await gotoStudio(page, "home");
    const sidebar = page.getByTestId("sidebar");
    await expect(sidebar).toBeVisible();
    // Inline (not translated off-canvas): left edge at/near 0.
    const box = await sidebar.boundingBox();
    expect(box?.x ?? -1).toBeGreaterThanOrEqual(0);
  });

  test("mobile hides the sidebar off-canvas and toggles a drawer", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await gotoStudio(page, "home");
    const sidebar = page.getByTestId("sidebar");
    // Off-canvas: translated to negative x.
    const before = await sidebar.boundingBox();
    expect(before === null || before.x < 0).toBeTruthy();

    // Open the drawer via the topbar toggle.
    await page.getByTestId("toggle-sidebar").click();
    await expect(page.getByTestId("nav-backdrop")).toBeVisible();
    // Poll until the slide-in transition settles on-screen.
    await expect.poll(async () => (await sidebar.boundingBox())?.x ?? -1).toBeGreaterThanOrEqual(0);

    // Navigating closes the drawer.
    await page.getByTestId("nav-shipments").click();
    await expect(page).toHaveURL(/\/shipments$/);
    await expect(page.getByTestId("nav-backdrop")).toHaveCount(0);
  });

  test("mobile: page content is usable (no horizontal overflow of the shell)", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await gotoStudio(page, "home");
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow).toBeLessThanOrEqual(2); // allow sub-pixel rounding
  });
});

test.describe("Theme (dark + light)", () => {
  test("dark is the default and renders the shell", async ({ page }) => {
    await gotoStudio(page, "home");
    await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
    await expect(page.getByTestId("home-stats")).toBeVisible();
  });

  test("toggling to light persists across navigation", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("theme-toggle").click();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
    // Background actually changes (light bg is near-white).
    const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    expect(bg).not.toBe("rgb(11, 11, 14)"); // not the dark --bg
    // Persists after navigating.
    await page.getByTestId("nav-shipments").click();
    await expect(page).toHaveURL(/\/shipments$/);
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  });
});
