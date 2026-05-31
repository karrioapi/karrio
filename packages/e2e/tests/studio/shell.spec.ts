import { test, expect } from "@playwright/test";
import { gotoStudio, switchMode } from "../../helpers/studio";

// Foundation coverage for the Karrio Studio app shell: routing, mode IA,
// theme toggle, and sidebar collapse. Feature-screen specs are added per
// Linear issue as each screen is implemented.

test.describe("Studio shell", () => {
  test("root redirects to Ship home", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveURL(/\/home$/);
    await expect(page.getByTestId("screen-home")).toBeVisible();
    await expect(page.getByTestId("home-stats")).toBeVisible();
  });

  test("mode switch swaps nav and jumps to mode default", async ({ page }) => {
    await gotoStudio(page, "home");

    await switchMode(page, "build");
    await expect(page).toHaveURL(/\/apps$/);
    await expect(page.getByTestId("nav-plugins")).toBeVisible();
    await expect(page.getByTestId("nav-mcp")).toBeVisible();

    await switchMode(page, "govern");
    await expect(page).toHaveURL(/\/admin$/);
    // Assert an ungated govern item: `tenants` is gated behind the
    // MULTI_ORGANIZATIONS feature flag (off on OSS), so `team` is the stable
    // signal that the govern nav rendered.
    await expect(page.getByTestId("nav-team")).toBeVisible();

    await switchMode(page, "ship");
    await expect(page).toHaveURL(/\/home$/);
    await expect(page.getByTestId("nav-shipments")).toBeVisible();
  });

  test("deep link lands in the correct mode", async ({ page }) => {
    await gotoStudio(page, "mcp");
    // Build-mode nav should be present for a Build deep link.
    await expect(page.getByTestId("nav-editor")).toBeVisible();
    await expect(page.getByTestId("mode-build")).toHaveAttribute("aria-selected", "true");
  });

  test("theme toggle flips the data-theme attribute", async ({ page }) => {
    await gotoStudio(page, "home");
    const html = page.locator("html");
    await expect(html).toHaveAttribute("data-theme", "dark");
    await page.getByTestId("theme-toggle").click();
    await expect(html).toHaveAttribute("data-theme", "light");
  });

  test("sidebar collapses and expands", async ({ page }) => {
    await gotoStudio(page, "home");
    const app = page.locator(".app");
    await expect(app).not.toHaveClass(/sidebar-collapsed/);
    await page.getByTestId("toggle-sidebar").click();
    await expect(app).toHaveClass(/sidebar-collapsed/);
  });

  test("create menu opens with quick-create actions", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("create-btn").click();
    const menu = page.getByTestId("create-menu");
    await expect(menu).toBeVisible();
    await expect(menu.getByText("New shipment")).toBeVisible();
    await expect(menu.getByText("Generate API key")).toBeVisible();
  });

  test("user menu opens and signs out to /login", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("user-menu-trigger").click();
    await expect(page.getByTestId("user-menu")).toBeVisible();
    await expect(page.getByTestId("user-menu-settings")).toBeVisible();
    await page.getByTestId("user-menu-logout").click();
    await expect(page).toHaveURL(/\/login$/);
  });

  test("workspace menu opens with settings + honest org state", async ({ page }) => {
    await gotoStudio(page, "home");
    await page.getByTestId("workspace-switcher").click();
    const menu = page.getByTestId("workspace-menu");
    await expect(menu).toBeVisible();
    await expect(page.getByTestId("workspace-menu-settings")).toBeVisible();
    await expect(page.getByTestId("workspace-menu-orgs")).toContainText(/Enterprise/i);
  });

  test("nav hides items gated by a disabled deployment feature flag", async ({ page }) => {
    // /v1/references drives feature-flag gating; default-on until it loads.
    await page.route("**/v1/references**", (route) =>
      route.fulfill({
        status: 200,
        headers: { "content-type": "application/json", "access-control-allow-origin": "*" },
        body: JSON.stringify({ ORDERS_MANAGEMENT: false, DOCUMENTS_MANAGEMENT: true, carriers: {}, connection_fields: {} }),
      }));
    await gotoStudio(page, "home");
    await expect(page.getByTestId("nav-shipments")).toBeVisible();
    await expect(page.getByTestId("nav-documents")).toBeVisible(); // flag true
    await expect(page.getByTestId("nav-orders")).toHaveCount(0); // flag false → gated out
  });

  test("test mode toggles a banner and persists across reload", async ({ page }) => {
    await gotoStudio(page, "home");
    await expect(page.getByTestId("test-mode-banner")).toHaveCount(0);
    await page.getByTestId("test-mode").click();
    await expect(page.getByTestId("test-mode-banner")).toBeVisible();
    await page.reload();
    await expect(page.getByTestId("test-mode-banner")).toBeVisible(); // persisted
  });
});
