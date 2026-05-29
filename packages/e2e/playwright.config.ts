import { defineConfig, devices } from "@playwright/test";
import path from "path";

const AUTH_STATE = path.join(__dirname, "playwright", ".auth", "user.json");

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: process.env.CI ? "github" : "list",
  use: {
    baseURL: process.env.KARRIO_DASHBOARD_URL || "http://localhost:3002",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "off",
  },
  projects: [
    {
      name: "setup",
      testMatch: /auth\.setup\.ts/,
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "chromium",
      testIgnore: /studio\//,
      use: {
        ...devices["Desktop Chrome"],
        storageState: AUTH_STATE,
      },
      dependencies: ["setup"],
    },
    // Karrio Studio (TanStack Start app, apps/studio). Authenticated by default
    // via an inline session cookie (the _app routes are guarded); the auth/guard
    // specs override storageState to test the unauthenticated paths.
    {
      name: "studio",
      testMatch: /studio\/.*\.spec\.ts/,
      use: {
        ...devices["Desktop Chrome"],
        baseURL: process.env.KARRIO_STUDIO_URL || "http://localhost:3003",
        storageState: {
          cookies: [
            {
              name: "karrio-studio-session",
              value: JSON.stringify({ access: "test-token", refresh: "r", email: "admin@example.com" }),
              domain: "localhost",
              path: "/",
              httpOnly: true,
              secure: false,
              sameSite: "Lax",
              expires: Math.floor(Date.now() / 1000) + 86400,
            },
          ],
          origins: [],
        },
      },
    },
  ],
});
