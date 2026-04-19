import { defineConfig, devices } from "@playwright/test";
import path from "path";

const AUTH_STATE = path.join(__dirname, "playwright", ".auth", "user.json");

/**
 * Playwright config for the Karrio e2e smoke suite.
 *
 * Environment overrides:
 *   - KARRIO_DASHBOARD_URL  (default http://localhost:3002)
 *   - KARRIO_API_URL        (default http://localhost:5002)
 *   - KARRIO_EMAIL          (default admin@example.com)
 *   - KARRIO_PASSWORD       (default demo)
 */
export default defineConfig({
  testDir: ".",
  testMatch: [
    "tests/**/*.setup.ts",
    "tests/**/*.spec.ts",
    "specs/**/*.spec.ts",
  ],
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  timeout: 60_000,
  expect: { timeout: 15_000 },
  reporter: process.env.CI
    ? [["github"], ["html", { open: "never", outputFolder: "playwright-report" }]]
    : [["list"]],
  outputDir: "test-results",
  use: {
    baseURL: process.env.KARRIO_DASHBOARD_URL || "http://localhost:3002",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  projects: [
    {
      name: "setup",
      testMatch: /auth\.setup\.ts/,
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        storageState: AUTH_STATE,
      },
      dependencies: ["setup"],
    },
    {
      name: "firefox",
      use: {
        ...devices["Desktop Firefox"],
        storageState: AUTH_STATE,
      },
      dependencies: ["setup"],
    },
  ],
});
