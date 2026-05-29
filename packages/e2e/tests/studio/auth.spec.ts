import { test, expect } from "@playwright/test";

// B2 · Auth UI (sign in / sign up / forgot). Pre-auth pages; no live backend, so
// server-fn calls to Karrio fail and we assert the error/validation/success UX.

test.describe("Auth UI (B2)", () => {
  test("sign in: renders, validates, shows error, password toggle", async ({ page }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");
    await expect(page.getByTestId("login-form")).toBeVisible();

    // Client validation: invalid email.
    await page.getByTestId("login-email").fill("nope");
    await page.getByTestId("login-submit").click();
    await expect(page.getByTestId("login-error")).toContainText(/valid email/i);

    // Password show/hide toggle flips the input type.
    const pw = page.locator("#password");
    await pw.fill("secret123");
    await expect(pw).toHaveAttribute("type", "password");
    await page.getByRole("button", { name: /show password/i }).click();
    await expect(pw).toHaveAttribute("type", "text");

    // Valid format but no backend → graceful error.
    await page.getByTestId("login-email").fill("admin@example.com");
    await page.getByTestId("login-submit").click();
    await expect(page.getByTestId("login-error")).toBeVisible();
  });

  test("sign in → navigate to signup and forgot", async ({ page }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");
    await page.getByTestId("to-signup").click();
    await expect(page).toHaveURL(/\/signup$/);
    await page.getByTestId("to-login").click();
    await expect(page).toHaveURL(/\/login$/);
    await page.getByTestId("to-forgot").click();
    await expect(page).toHaveURL(/\/forgot$/);
  });

  test("sign up: validation + password strength", async ({ page }) => {
    await page.goto("/signup");
    await page.waitForLoadState("networkidle");
    await page.getByTestId("signup-name").fill("Daniel K");
    await page.getByTestId("signup-email").fill("dan@karrio.io");
    await page.locator("#password").fill("short");
    await expect(page.getByTestId("signup-strength")).toContainText(/8 characters/i);
    await page.getByTestId("signup-submit").click();
    await expect(page.getByTestId("signup-error")).toContainText(/8 characters/i);
    await page.locator("#password").fill("longenough123");
    await expect(page.getByTestId("signup-strength")).toContainText(/strong/i);
  });

  test("forgot: valid email shows success state", async ({ page }) => {
    await page.goto("/forgot");
    await page.waitForLoadState("networkidle");
    await page.getByTestId("forgot-email").fill("dan@karrio.io");
    await page.getByTestId("forgot-submit").click();
    await expect(page.getByTestId("forgot-success")).toBeVisible();
  });
});
