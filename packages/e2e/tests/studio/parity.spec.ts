import { test, expect, type Route } from "@playwright/test";

// Dashboard-parity screens: Manifests, Batches (REST), Workflows, Rate sheets
// (GraphQL), Usage (REST). List render + row→detail sheet (where applicable).
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
const edges = (field: string, nodes: unknown[]) => ({ data: { [field]: { edges: nodes.map((node) => ({ node })) } } });

const REST: Record<string, unknown> = {
  "/v1/manifests": paged([{ id: "mf_1", carrier_name: "ups", reference: "MAN-1001", shipment_count: 12, created_at: "2026-05-28T10:00:00Z", manifest_url: "http://x/m.pdf" }]),
  "/v1/batches/operations": paged([{ id: "bat_1", status: "completed", resource_type: "shipments", total: 25, created_at: "2026-05-28T09:00:00Z" }]),
};
const GQL: Record<string, unknown> = {
  workflows: edges("workflows", [{ id: "wf_1", name: "Auto-fulfill", description: "Fulfill paid orders", is_active: true, trigger: "order.paid", action_count: 3 }]),
  rate_sheets: edges("rate_sheets", [{ id: "rs_1", name: "UPS Negotiated", carrier_name: "ups", services_count: 8, is_system: false }]),
  // Usage now comes from GraphQL `system_usage` (mapped to plan/metrics by the hook).
  system_usage: { data: { system_usage: { total_shipments: 2143, total_trackers: 1002, total_requests: 142300, total_shipping_spend: 18402, order_volume: 219 } } },
};

test.describe("Dashboard parity screens", () => {
  test.beforeEach(async ({ page }) => {
    for (const [path, body] of Object.entries(REST)) {
      await page.route(`**${path}**`, (route) => json(route, body));
    }
    await page.route("**/graphql", (route) => {
      if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
      const q = route.request().postData() ?? "";
      const field = Object.keys(GQL).find((f) => q.includes(f));
      return json(route, field ? GQL[field] : { data: {} });
    });
  });

  test("Manifests: list + row → sheet", async ({ page }) => {
    await page.goto("/manifests");
    await expect(page.getByTestId("screen-manifests")).toBeVisible();
    await expect(page.getByTestId("manifest-row-mf_1")).toContainText("MAN-1001");
    await page.getByTestId("manifest-row-mf_1").click();
    await expect(page.getByTestId("manifest-sheet-body")).toBeVisible();
  });

  test("Batches: list + row → sheet", async ({ page }) => {
    await page.goto("/batches");
    await expect(page.getByTestId("batch-row-bat_1")).toContainText("shipments");
    await page.getByTestId("batch-row-bat_1").click();
    await expect(page.getByTestId("batch-sheet-body")).toBeVisible();
  });

  test("Workflows: list + row → sheet", async ({ page }) => {
    await page.goto("/workflows");
    await expect(page.getByTestId("workflow-row-wf_1")).toContainText("Auto-fulfill");
    await page.getByTestId("workflow-row-wf_1").click();
    await expect(page.getByTestId("workflow-sheet-body")).toBeVisible();
  });

  test("Rate sheets: list + row → sheet", async ({ page }) => {
    await page.goto("/ratesheets");
    await expect(page.getByTestId("ratesheet-row-rs_1")).toContainText("UPS Negotiated");
    await page.getByTestId("ratesheet-row-rs_1").click();
    await expect(page.getByTestId("ratesheet-sheet-body")).toBeVisible();
  });

  test("Usage: plan + metrics render", async ({ page }) => {
    await page.goto("/usage");
    await expect(page.getByTestId("usage-plan")).toContainText("Open Source");
    await expect(page.getByTestId("usage-metrics")).toContainText("Shipments");
  });
});
