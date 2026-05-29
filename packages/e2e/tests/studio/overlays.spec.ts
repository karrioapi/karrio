import { test, expect } from "@playwright/test";
import { gotoStudio } from "../../helpers/studio";

// H1 Command palette + D5 Workbench overlay (cross-cutting shell features).

test.describe("Command palette (H1)", () => {
  test("⌘K opens, filters, and navigates", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.keyboard.press("Meta+k");
    await expect(page.getByTestId("command-palette")).toBeVisible();
    await page.getByTestId("cp-input").fill("track");
    await expect(page.getByTestId("cp-item-nav:trackers")).toBeVisible();
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(/\/trackers$/);
    await expect(page.getByTestId("command-palette")).toHaveCount(0);
  });

  test("topbar search trigger opens the palette; ESC closes", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("palette-trigger").click();
    await expect(page.getByTestId("command-palette")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("command-palette")).toHaveCount(0);
  });

  test("palette can run the theme action", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("palette-trigger").click();
    await page.getByTestId("cp-input").fill("theme");
    await page.getByTestId("cp-item-toggle-theme").click();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  });
});

test.describe("Workbench (D5)", () => {
  test("⌘` opens the workbench; logs render; ESC closes", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("workbench-trigger").click();
    const wb = page.getByTestId("workbench");
    await expect(wb).toHaveClass(/open/);
    await expect(page.getByTestId("wb-logs")).toBeVisible();
    await expect(page.getByTestId("wb-log-l1")).toContainText("/v1/shipments");
    await page.getByTestId("wb-nav-events").click();
    await expect(page.getByTestId("wb-body")).toContainText("Events view");
    await page.getByTestId("wb-close").click();
    await expect(wb).not.toHaveClass(/open/);
  });
});
