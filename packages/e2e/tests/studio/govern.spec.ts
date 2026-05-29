import { test, expect, type Route } from "@playwright/test";

// E1–E6 · Govern mode (Admin, Tenants, Team, Audit, Security, Settings).
const STUDIO_URL = process.env.KARRIO_STUDIO_URL || "http://localhost:3003";
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};
const json = (route: Route, body: unknown) =>
  route.request().method() === "OPTIONS"
    ? route.fulfill({ status: 204, headers: CORS, body: "" })
    : route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(body) });
const paged = (results: unknown[]) => ({ count: results.length, next: null, previous: null, results });

const DATA: Record<string, unknown> = {
  "/v1/admin/tenants": paged([{ id: "tn_1", name: "Acme", slug: "acme", members: 12, status: "active", created: "2026-01-01" }]),
  "/v1/admin/users": paged([{ id: "usr_1", name: "Daniel K", email: "dan@karrio.io", role: "owner", status: "active" }]),
  "/v1/admin": { version: "2026.5.1", tenants: 3, license: "Enterprise", resources: [{ label: "CPU", used: 40, total: 100 }], runtimes: [{ name: "ups", memory: "48MB", calls: 1284, p99: "84ms" }] },
  "/v1/events": paged([{ id: "ev_1", type: "shipment.purchased", actor: "dan@karrio.io", description: "Purchased label", at: "11:30 AM" }]),
};

test.describe("Govern mode (E)", () => {
  test.beforeEach(async ({ page, context }) => {
    await context.addCookies([
      { name: "karrio-studio-session", value: JSON.stringify({ access: "t", refresh: "r", email: "a@b.c" }), url: STUDIO_URL, httpOnly: true, sameSite: "Lax" },
    ]);
    // /v1/admin/* must be registered before /v1/admin to match correctly; Playwright
    // uses last-registered-first, so register the broad one first.
    await page.route("**/v1/admin**", (route) => json(route, DATA["/v1/admin"]));
    await page.route("**/v1/admin/tenants**", (route) => json(route, DATA["/v1/admin/tenants"]));
    await page.route("**/v1/admin/users**", (route) => json(route, DATA["/v1/admin/users"]));
    await page.route("**/v1/events**", (route) => json(route, DATA["/v1/events"]));
  });

  test("Admin overview renders cards + runtimes", async ({ page }) => {
    await page.goto("/admin");
    await expect(page.getByTestId("admin-cards")).toContainText("Enterprise");
    await expect(page.getByTestId("admin-runtimes")).toContainText("ups");
  });

  test("Tenants table", async ({ page }) => {
    await page.goto("/tenants");
    await expect(page.getByTestId("tenant-row-tn_1")).toContainText("Acme");
  });

  test("Team table", async ({ page }) => {
    await page.goto("/team");
    await expect(page.getByTestId("member-row-usr_1")).toContainText("dan@karrio.io");
  });

  test("Audit log table", async ({ page }) => {
    await page.goto("/audit");
    await expect(page.getByTestId("audit-row-ev_1")).toContainText("shipment.purchased");
  });

  test("Security toggles flip", async ({ page }) => {
    await page.goto("/security");
    await page.waitForLoadState("networkidle");
    const sso = page.getByTestId("sec-sso");
    await expect(sso).toHaveAttribute("aria-checked", "false");
    await sso.click();
    await expect(sso).toHaveAttribute("aria-checked", "true");
  });

  test("Settings toggles flip", async ({ page }) => {
    await page.goto("/settings");
    await page.waitForLoadState("networkidle");
    const ins = page.getByTestId("set-insurance");
    await expect(ins).toHaveAttribute("aria-checked", "false");
    await ins.click();
    await expect(ins).toHaveAttribute("aria-checked", "true");
  });
});
