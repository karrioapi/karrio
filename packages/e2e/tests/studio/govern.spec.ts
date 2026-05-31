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

// Team + admin overview now come from the ADMIN GraphQL schema (/admin/graphql),
// audit from the tenant GraphQL `events`. Tenants remains REST (no OSS source yet).
const TENANTS = paged([{ id: "tn_1", name: "Acme", slug: "acme", members: 12, status: "active", created: "2026-01-01" }]);
const GQL_TENANT: Record<string, unknown> = {
  events: { data: { events: { edges: [
    { node: { id: "ev_1", type: "shipment.purchased", created_at: "2026-05-30T11:30:00Z", created_by: { email: "dan@karrio.io" } } },
  ] } } },
};
const GQL_ADMIN: Record<string, unknown> = {
  users: { data: { users: { edges: [
    { node: { id: 1, email: "dan@karrio.io", full_name: "Daniel K", is_active: true, is_staff: true, is_superuser: true } },
  ] } } },
  worker_health: { data: { worker_health: { is_available: true } } },
};

function gqlReply(route: Route, table: Record<string, unknown>) {
  if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
  const q = route.request().postData() ?? "";
  const field = Object.keys(table).find((f) => q.includes(f));
  return json(route, field ? table[field] : { data: {} });
}

test.describe("Govern mode (E)", () => {
  test.beforeEach(async ({ page, context }) => {
    await context.addCookies([
      { name: "karrio-studio-session", value: JSON.stringify({ access: "t", refresh: "r", email: "a@b.c" }), url: STUDIO_URL, httpOnly: true, sameSite: "Lax" },
    ]);
    await page.route("**/v1/admin/tenants**", (route) => json(route, TENANTS));
    // "**/graphql" also matches "/admin/graphql"; register the admin route LAST so
    // it wins for admin URLs (Playwright applies last-registered first).
    await page.route("**/graphql", (route) => gqlReply(route, GQL_TENANT));
    await page.route("**/admin/graphql", (route) => gqlReply(route, GQL_ADMIN));
  });

  test("Admin overview renders cards + runtimes", async ({ page }) => {
    await page.goto("/admin");
    await expect(page.getByTestId("admin-cards")).toContainText("Open Source");
    await expect(page.getByTestId("admin-runtimes")).toContainText("Background worker");
  });

  test("Tenants table", async ({ page }) => {
    await page.goto("/tenants");
    await expect(page.getByTestId("tenant-row-tn_1")).toContainText("Acme");
  });

  test("Team table", async ({ page }) => {
    await page.goto("/team");
    await expect(page.getByTestId("member-row-1")).toContainText("dan@karrio.io");
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
