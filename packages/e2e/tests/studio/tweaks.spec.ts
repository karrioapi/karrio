import { test, expect } from "@playwright/test";
import { gotoStudio } from "../../helpers/studio";

// G1–G3 · Customization (Tweaks panel): accent, density, font, theme — applied
// live via CSS variables and persisted.

test.describe("Customization (G)", () => {
  test("topbar opens the tweaks panel", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("tweaks-trigger").click();
    await expect(page.getByTestId("tweaks-panel")).toBeVisible();
  });

  test("changing accent updates the --accent CSS variable", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("tweaks-trigger").click();
    await page.getByTestId("tweak-accent-10B981").click();
    const accent = await page.evaluate(() =>
      getComputedStyle(document.documentElement).getPropertyValue("--accent").trim(),
    );
    expect(accent.toLowerCase()).toBe("#10b981");
  });

  test("changing density updates data-density and persists", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("tweaks-trigger").click();
    await page.getByTestId("tweak-density").selectOption("compact");
    await expect(page.locator("html")).toHaveAttribute("data-density", "compact");
    // Close the panel, then verify it persists across navigation.
    await page.getByTestId("sheet-close").click();
    await page.getByTestId("nav-shipments").click();
    await expect(page).toHaveURL(/\/shipments$/);
    await expect(page.locator("html")).toHaveAttribute("data-density", "compact");
  });

  test("appearance is reachable from the command palette", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.keyboard.press("Meta+k");
    await page.getByTestId("cp-input").fill("appearance");
    await page.getByTestId("cp-item-appearance").click();
    await expect(page.getByTestId("tweaks-panel")).toBeVisible();
  });
});
