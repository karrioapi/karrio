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
    // visual.spec.ts is excluded here — it only runs via the gated studio-visual project.
    {
      name: "studio",
      testMatch: /studio\/.*\.spec\.ts/,
      testIgnore: /studio\/visual\.spec\.ts/,
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
    // Karrio Studio LIVE — integration specs that drive the real UI against a
    // running, seeded Karrio backend (the sandbox). Real login (no inline auth).
    // Gated: run with KARRIO_LIVE=1 against `bin/studio-sandbox`.
    {
      name: "studio-live",
      testMatch: /studio-live\/.*\.spec\.ts/,
      use: {
        ...devices["Desktop Chrome"],
        baseURL: process.env.KARRIO_STUDIO_URL || "http://localhost:3003",
      },
    },
    // Karrio Studio visual regression — screenshot baselines for key screens.
    // Gated behind KARRIO_VISUAL=1 so CI without committed baselines never fails.
    // Run locally: KARRIO_VISUAL=1 npx playwright test --project=studio-visual
    // Update baselines: KARRIO_VISUAL=1 npx playwright test --project=studio-visual --update-snapshots
    ...(process.env.KARRIO_VISUAL === "1"
      ? [
          {
            name: "studio-visual",
            testMatch: /studio\/visual\.spec\.ts/,
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
                    sameSite: "Lax" as const,
                    expires: Math.floor(Date.now() / 1000) + 86400,
                  },
                ],
                origins: [],
              },
            },
          },
          {
            name: "studio-visual-mobile",
            testMatch: /studio\/visual\.spec\.ts/,
            use: {
              ...devices["Pixel 7"],
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
                    sameSite: "Lax" as const,
                    expires: Math.floor(Date.now() / 1000) + 86400,
                  },
                ],
                origins: [],
              },
            },
          },
        ]
      : []),
  ],
});
