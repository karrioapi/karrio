import { test, expect, type Route } from "@playwright/test";

// C4 · Orders (GraphQL-backed)
const STUDIO_URL = process.env.KARRIO_STUDIO_URL || "http://localhost:3003";
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};

const ORDERS = {
  data: {
    orders: {
      edges: [
        { node: { id: "ord_1", order_id: "#11335", status: "unfulfilled", source: "Shopify", created_at: "2026-05-28T10:00:00Z", line_items: [{ id: "li1", title: "Widget", quantity: 2 }], shipping_to: { person_name: "Alicia Romero", city: "Brooklyn", country_code: "US" } } },
        { node: { id: "ord_2", order_id: "#11334", status: "fulfilled", source: "Medusa", created_at: "2026-05-28T09:00:00Z", line_items: [{ id: "li2", title: "Cable", quantity: 1 }], shipping_to: { person_name: "Jane Doe", city: "Vancouver", country_code: "CA" } } },
      ],
    },
  },
};

async function fulfillGraphql(route: Route) {
  if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
  return route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(ORDERS) });
}

test.describe("Ship · Orders (C4)", () => {
  test.beforeEach(async ({ page, context }) => {
    await context.addCookies([
      { name: "karrio-studio-session", value: JSON.stringify({ access: "t", refresh: "r", email: "a@b.c" }), url: STUDIO_URL, httpOnly: true, sameSite: "Lax" },
    ]);
    await page.route("**/graphql", fulfillGraphql);
  });

  test("lists orders from GraphQL with tab counts", async ({ page }) => {
    await page.goto("/orders");
    await expect(page.getByTestId("screen-orders")).toBeVisible();
    await expect(page.getByTestId("order-row-ord_1")).toBeVisible();
    await expect(page.getByTestId("tab-all")).toContainText("2");
    await expect(page.getByTestId("tab-fulfilled")).toContainText("1");
  });

  test("row opens order sheet with line items", async ({ page }) => {
    await page.goto("/orders");
    await page.getByTestId("order-row-ord_1").click();
    const sheet = page.getByTestId("order-sheet-body");
    await expect(sheet).toBeVisible();
    await expect(sheet).toContainText("#11335");
    await expect(sheet).toContainText("Widget");
  });
});
