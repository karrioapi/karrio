import { type Page, type Locator } from "@playwright/test";

/**
 * Shared locators for the Karrio dashboard.
 *
 * Prefer getByRole / getByTestId.  Do NOT depend on generated Tailwind
 * class names — they change between builds and make specs brittle.
 */
export const selectors = {
  // ── Sign-in form ──────────────────────────────────────────────────────────
  emailInput: (page: Page): Locator => page.locator('input[name="email"]'),
  passwordInput: (page: Page): Locator => page.locator('input[name="password"]'),
  signInSubmit: (page: Page): Locator =>
    page.getByRole("button", { name: /sign in|log in/i }),

  // ── Top-level navigation ──────────────────────────────────────────────────
  sidebarNav: (page: Page): Locator => page.getByRole("navigation").first(),
  userMenu: (page: Page): Locator =>
    page.getByRole("button", { name: /account|profile|user menu/i }),
  signOutButton: (page: Page): Locator =>
    page.getByRole("menuitem", { name: /sign out|log out/i }).or(
      page.getByRole("button", { name: /sign out|log out/i }),
    ),

  // ── Heading by page ───────────────────────────────────────────────────────
  headingMatching: (page: Page, pattern: RegExp): Locator =>
    page.locator("h1, h2").filter({ hasText: pattern }).first(),

  // ── Table / list rows ─────────────────────────────────────────────────────
  tableRows: (page: Page): Locator =>
    page.locator('table tr, [role="row"]'),

  // ── Dialog / sheet ────────────────────────────────────────────────────────
  dialog: (page: Page): Locator => page.locator('[role="dialog"]').first(),

  // ── Generic button-by-label factory ───────────────────────────────────────
  buttonByName: (page: Page, pattern: RegExp | string): Locator =>
    page.getByRole("button", {
      name: typeof pattern === "string" ? new RegExp(pattern, "i") : pattern,
    }),

  // ── Link-by-label factory ─────────────────────────────────────────────────
  linkByName: (page: Page, pattern: RegExp | string): Locator =>
    page.getByRole("link", {
      name: typeof pattern === "string" ? new RegExp(pattern, "i") : pattern,
    }),
};
