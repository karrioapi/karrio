import { test, expect, type Route } from "@playwright/test";

// C1 · Home — verifies the landing page renders REAL metrics computed from the
// shipment / tracker / order hooks (no hardcoded numbers), plus the recent
// shipments list and the actionable "things to do" panel.
const STUDIO_URL = process.env.KARRIO_STUDIO_URL || "http://localhost:3003";
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};
const json = (route: Route, body: unknown) =>
  route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(body) });
const paged = (results: unknown[]) => ({ count: results.length, next: null, previous: null, results });

const SHIPMENTS = paged([
  { id: "shp_1", status: "purchased", tracking_number: "1Z999AA10123456784",
    selected_rate: { carrier_name: "ups", service: "ups_ground", total_charge: 12.4, currency: "USD", extra_charges: [] },
    recipient: { person_name: "Alicia Romero", city: "Brooklyn", country_code: "US" } },
  { id: "shp_2", status: "delivered", tracking_number: "CP123456789CA",
    selected_rate: { carrier_name: "canadapost", service: "expedited", total_charge: 9.8, currency: "CAD", extra_charges: [] },
    recipient: { person_name: "Jane Doe", city: "Vancouver", country_code: "CA" } },
]);
const TRACKERS = paged([
  { id: "trk_1", tracking_number: "1Z999AA10123456784", carrier_name: "ups", status: "in_transit", estimated_delivery: "2026-06-01" },
  { id: "trk_2", tracking_number: "CP123456789CA", carrier_name: "canadapost", status: "delivered", estimated_delivery: "2026-05-27" },
]);
const ORDERS = {
  data: {
    orders: {
      edges: [
        { node: { id: "ord_1", order_id: "#11335", status: "unfulfilled", source: "shopify", line_items: [{ id: "li_1", title: "Headphones", quantity: 1 }], shipping_to: { person_name: "Alicia", city: "Brooklyn", country_code: "US" } } },
      ],
    },
  },
};

test.describe("Home · landing (C1)", () => {
  test.beforeEach(async ({ page, context }) => {
    await context.addCookies([
      { name: "karrio-studio-session", value: JSON.stringify({ access: "t", refresh: "r", email: "a@b.c" }), url: STUDIO_URL, httpOnly: true, sameSite: "Lax" },
    ]);
    await page.route("**/v1/shipments**", (route) => (route.request().method() === "OPTIONS" ? route.fulfill({ status: 204, headers: CORS, body: "" }) : json(route, SHIPMENTS)));
    await page.route("**/v1/trackers**", (route) => (route.request().method() === "OPTIONS" ? route.fulfill({ status: 204, headers: CORS, body: "" }) : json(route, TRACKERS)));
    await page.route("**/graphql", (route) => {
      if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
      const q = route.request().postData() ?? "";
      return json(route, q.includes("orders") ? ORDERS : { data: {} });
    });
  });

  test("stats reflect real data", async ({ page }) => {
    await page.goto("/home");
    await expect(page.getByTestId("screen-home")).toBeVisible();
    // Shipments count = 2; In transit = 1; Delivered = 1; Orders to fulfill = 1.
    await expect(page.getByTestId("home-stat-shipments")).toContainText("2");
    await expect(page.getByTestId("home-stat-in-transit")).toContainText("1");
    await expect(page.getByTestId("home-stat-delivered")).toContainText("1");
    await expect(page.getByTestId("home-stat-orders-to-fulfill")).toContainText("1");
  });

  test("recent shipments list shows rows", async ({ page }) => {
    await page.goto("/home");
    await expect(page.getByTestId("home-recent-shp_1")).toContainText("1Z999AA10123456784");
    await expect(page.getByTestId("home-recent-shp_1")).toContainText("Alicia Romero");
    await expect(page.getByTestId("home-recent-shp_2")).toContainText("CP123456789CA");
    await expect(page.getByTestId("home-recent-shp_2")).toContainText("Jane Doe");
  });

  test("things-to-do lists actionable items linking to their screens", async ({ page }) => {
    await page.goto("/home");
    const todo = page.getByTestId("home-todo");
    await expect(todo).toContainText(/order.*fulfill/i);
    await expect(todo).toContainText(/in transit/i);
    // First to-do links to the orders screen.
    await expect(page.getByTestId("home-todo-0")).toHaveAttribute("href", "/orders");
  });

  test("stat cards navigate client-side to their screen", async ({ page }) => {
    await page.goto("/home");
    await expect(page.getByTestId("home-stat-shipments")).toBeVisible();
    await page.getByTestId("home-stat-shipments").click();
    await expect(page).toHaveURL(/\/shipments$/);
    await expect(page.getByTestId("screen-shipments")).toBeVisible();
  });

  test("empty state shows 'all caught up' when nothing is pending", async ({ page }) => {
    // Override with no in-transit/unfulfilled work.
    await page.route("**/v1/trackers**", (route) => json(route, paged([{ id: "trk_x", tracking_number: "X", carrier_name: "ups", status: "delivered" }])));
    await page.route("**/graphql", (route) => {
      const q = route.request().postData() ?? "";
      return json(route, q.includes("orders") ? { data: { orders: { edges: [] } } } : { data: {} });
    });
    await page.goto("/home");
    await expect(page.getByTestId("home-todo-empty")).toBeVisible();
  });
});
