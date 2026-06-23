import { test, expect } from "@playwright/test";
import { ALL_STUDIO_ROUTES } from "../../helpers/studio";

// Comprehensive responsive + dark/light review across EVERY page.
// Authenticated by default (studio project storageState). Data hooks render
// empty-states without a backend — fine for layout/overflow/theme checks.

async function noHorizontalOverflow(page: import("@playwright/test").Page) {
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow, "horizontal overflow (px)").toBeLessThanOrEqual(2);
}

test.describe("Responsive sweep — mobile (390px), dark", () => {
  test.use({ viewport: { width: 390, height: 844 } });
  for (const route of ALL_STUDIO_ROUTES) {
    test(`/${route} renders without horizontal overflow`, async ({ page }) => {
      await page.goto(`/${route}`);
      await expect(page.getByTestId(`screen-${route}`)).toBeVisible();
      await page.waitForLoadState("networkidle");
      await noHorizontalOverflow(page);
    });
  }
});

test.describe("Responsive sweep — tablet (820px), dark", () => {
  test.use({ viewport: { width: 820, height: 1180 } });
  for (const route of ["home", "shipments", "apps", "mcp", "editor", "admin", "settings"]) {
    test(`/${route} renders without horizontal overflow`, async ({ page }) => {
      await page.goto(`/${route}`);
      await expect(page.getByTestId(`screen-${route}`)).toBeVisible();
      await page.waitForLoadState("networkidle");
      await noHorizontalOverflow(page);
    });
  }
});

test.describe("Theme sweep — light mode across every page", () => {
  test.use({
    // Load each page already in light mode (pre-render init script reads this).
    storageState: {
      cookies: [
        {
          name: "karrio-studio-session",
          value: JSON.stringify({ access: "test-token", refresh: "r", email: "admin@example.com" }),
          domain: "localhost",
          path: "/",
          httpOnly: true,
          secure: false,
          sameSite: "Lax" as const,
          expires: Math.floor(Date.now() / 1000) + 86400,
        },
      ],
      origins: [{ origin: "http://localhost:3003", localStorage: [{ name: "karrio-theme", value: "light" }] }],
    },
  });

  for (const route of ALL_STUDIO_ROUTES) {
    test(`/${route} renders in light theme`, async ({ page }) => {
      await page.goto(`/${route}`);
      await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
      await expect(page.getByTestId(`screen-${route}`)).toBeVisible();
      // Light background is near-white, not the dark canvas.
      const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
      expect(bg).not.toBe("rgb(11, 11, 14)");
    });
  }
});
