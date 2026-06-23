import { test, expect } from "@playwright/test";
import { ALL_STUDIO_ROUTES, gotoStudio } from "../../helpers/studio";

// Every screen in the IA must resolve and render under the app shell.
// As screens graduate from Placeholder to real implementations, these assert
// the shell renders; richer per-screen specs live in their own files.
test.describe("Studio routing", () => {
  for (const route of ALL_STUDIO_ROUTES) {
    test(`/${route} renders within the shell`, async ({ page }) => {
      await gotoStudio(page, route);
      await expect(page.getByTestId("topbar")).toBeVisible();
      await expect(page.getByTestId(`screen-${route}`)).toBeVisible();
    });
  }

  test("unknown route returns not found", async ({ page }) => {
    const res = await page.goto("/not-a-real-screen");
    expect(res?.status()).toBe(404);
  });
});
