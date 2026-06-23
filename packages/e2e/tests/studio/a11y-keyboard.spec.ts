import { test, expect, type Route } from "@playwright/test";
import { gotoStudio } from "../../helpers/studio";

// Accessibility / keyboard-navigation coverage: Sheet focus management + trap,
// keyboard-operable Checkbox, and global keyboard shortcuts.
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};
const SHIPMENTS = {
  count: 1, next: null, previous: null,
  results: [{ id: "shp_a", status: "purchased", carrier_name: "ups", tracking_number: "1Z1", service: "UPS Ground",
    selected_rate: { total_charge: 10, currency: "USD" }, recipient: { person_name: "A", city: "NYC", country_code: "US" }, reference: "R1", created_at: "2026-05-28T10:00:00Z" }],
};

test.describe("Accessibility & keyboard", () => {
  test.beforeEach(async ({ page }) => {
    await page.route("**/graphql", (route) =>
      route.request().method() === "OPTIONS"
        ? route.fulfill({ status: 204, headers: CORS, body: "" })
        : route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(
            (route.request().postData() ?? "").includes("shipments")
              ? { data: { shipments: { edges: SHIPMENTS.results.map((node) => ({ node })) } } }
              : { data: {} },
          ) }));
  });

  test("Sheet: focus moves in on open, traps Tab, Escape closes", async ({ page }) => {
    await page.goto("/shipments");
    await page.getByTestId("shipment-row-shp_a").click();
    await expect(page.getByTestId("sheet")).toBeVisible();
    // Focus is inside the dialog.
    const focusInside = await page.evaluate(() =>
      document.querySelector('[data-testid="sheet"]')?.contains(document.activeElement) ?? false);
    expect(focusInside).toBeTruthy();
    // Tab several times — focus stays trapped within the sheet.
    for (let i = 0; i < 12; i++) await page.keyboard.press("Tab");
    const stillInside = await page.evaluate(() =>
      document.querySelector('[data-testid="sheet"]')?.contains(document.activeElement) ?? false);
    expect(stillInside).toBeTruthy();
    // Escape closes.
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("sheet")).toHaveCount(0);
  });

  test("Checkbox is keyboard-operable (Space toggles)", async ({ page }) => {
    await page.goto("/shipments");
    await expect(page.getByTestId("shipment-row-shp_a")).toBeVisible(); // hydrate
    const selectAll = page.getByTestId("select-all");
    await expect(selectAll).toHaveAttribute("role", "checkbox");
    await selectAll.focus();
    await page.keyboard.press("Space");
    await expect(page.getByTestId("selection-count")).toBeVisible();
    await expect(selectAll).toHaveAttribute("aria-checked", "true");
  });

  test("global keyboard shortcuts: ⌘\\ theme, ⌘B sidebar", async ({ page }) => {
    await gotoStudio(page, "home");
    const html = page.locator("html");
    await expect(html).toHaveAttribute("data-theme", "dark");
    await page.keyboard.press("Meta+\\");
    await expect(html).toHaveAttribute("data-theme", "light");
    const app = page.locator(".app");
    await expect(app).not.toHaveClass(/sidebar-collapsed/);
    await page.keyboard.press("Meta+b");
    await expect(app).toHaveClass(/sidebar-collapsed/);
  });

  test("command palette is fully keyboard-driven", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.keyboard.press("Meta+k");
    await expect(page.getByTestId("command-palette")).toBeVisible();
    await page.keyboard.type("orders");
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(/\/orders$/);
  });
});
