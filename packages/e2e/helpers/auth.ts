import { type Page } from "@playwright/test";

const EMAIL = process.env.KARRIO_EMAIL || "admin@example.com";
const PASSWORD = process.env.KARRIO_PASSWORD || "demo";

/**
 * Log in to the Karrio dashboard.
 *
 * The dashboard uses NextAuth with a credentials provider.
 * The sign-in form is at `/signin` and uses `name="email"` / `name="password"` inputs.
 *
 * After calling this helper, the browser context will hold the NextAuth
 * session cookies.  Persist them with:
 *
 *   await page.context().storageState({ path: 'playwright/.auth/user.json' })
 */
export async function loginToDashboard(page: Page): Promise<void> {
  await page.goto("/signin");
  await page.waitForLoadState("networkidle");

  // Fill in credentials — the form uses `name` attributes
  const emailInput = page.locator('input[name="email"]');
  const passwordInput = page.locator('input[name="password"]');

  await emailInput.waitFor({ timeout: 15_000 });
  await emailInput.fill(EMAIL);
  await passwordInput.fill(PASSWORD);

  // Submit the form
  await page.getByRole("button", { name: /sign in|log in/i }).click();

  // Wait for redirect away from /signin
  await page.waitForURL((url) => !url.pathname.includes("signin"), {
    timeout: 30_000,
  });
  await page.waitForLoadState("networkidle");
}
