import { test, expect, type Route } from "@playwright/test";

// C5–C11 · Connections, Pickups, Documents (REST) + Addresses, Parcels,
// Products, Rules (GraphQL). One spec, shared interception.
const STUDIO_URL = process.env.KARRIO_STUDIO_URL || "http://localhost:3003";
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};
const json = (route: Route, body: unknown) =>
  route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(body) });
const paged = (results: unknown[]) => ({ count: results.length, next: null, previous: null, results });
const edges = (field: string, nodes: unknown[]) => ({ data: { [field]: { edges: nodes.map((node) => ({ node })) } } });

const REST: Record<string, unknown> = {
  "/v1/connections": paged([{ id: "conn_1", carrier_name: "ups", carrier_id: "ups_acct", test_mode: false, active: true, capabilities: ["rating", "shipping", "tracking"] }]),
  "/v1/pickups": paged([{ id: "pck_1", carrier_name: "fedex", confirmation_number: "CONF123", pickup_date: "2026-06-01", ready_time: "09:00", closing_time: "17:00", status: "scheduled", address: { person_name: "Acme", city: "Brooklyn", country_code: "US" } }]),
  "/v1/documents/templates": paged([{ id: "doc_1", name: "Packing Slip", slug: "packing_slip", related_object: "shipment", active: true }]),
};

const GQL: Record<string, unknown> = {
  addresses: edges("addresses", [{ id: "adr_1", meta: { label: "HQ", is_default: true }, person_name: "Daniel K", company_name: "Acme", address_line1: "432 Park Ave", city: "Brooklyn", state_code: "NY", country_code: "US", postal_code: "11201", email: "ops@acme.io", phone_number: "+1 555" }]),
  parcels: edges("parcels", [{ id: "pcl_1", meta: { label: "Small Box", is_default: true }, packaging_type: "BOX", width: 15, height: 10, length: 20, dimension_unit: "CM", weight: 0.5, weight_unit: "KG" }]),
  products: edges("products", [{ id: "prd_1", title: "Headphones", label: "Headphones", sku: "ACM-1", hs_code: "8518.30", weight: 0.4, weight_unit: "KG", value_amount: 84, value_currency: "USD", origin_country: "US" }]),
  shipping_rules: edges("shipping_rules", [{ id: "rule_1", name: "Cheapest", priority: 100, is_active: true, description: "Pick cheapest", action_type: "service_selection" }]),
};

test.describe("Ship · resource screens (C5–C11)", () => {
  test.beforeEach(async ({ page, context }) => {
    await context.addCookies([
      { name: "karrio-studio-session", value: JSON.stringify({ access: "t", refresh: "r", email: "a@b.c" }), url: STUDIO_URL, httpOnly: true, sameSite: "Lax" },
    ]);
    for (const [path, body] of Object.entries(REST)) {
      await page.route(`**${path}**`, (route) => (route.request().method() === "OPTIONS" ? route.fulfill({ status: 204, headers: CORS, body: "" }) : json(route, body)));
    }
    await page.route("**/graphql", (route) => {
      if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
      const q = route.request().postData() ?? "";
      const field = Object.keys(GQL).find((f) => q.includes(f));
      return json(route, field ? GQL[field] : { data: {} });
    });
  });

  const cases: { route: string; row: string; sheet: string }[] = [
    { route: "connections", row: "connection-row-conn_1", sheet: "connection-form" },
    { route: "pickups", row: "pickup-row-pck_1", sheet: "pickup-sheet-body" },
    { route: "documents", row: "document-row-doc_1", sheet: "document-sheet-body" },
    { route: "addresses", row: "address-row-adr_1", sheet: "address-form" },
    { route: "parcels", row: "parcel-row-pcl_1", sheet: "parcel-form" },
    { route: "products", row: "product-row-prd_1", sheet: "product-form" },
    { route: "rules", row: "rule-row-rule_1", sheet: "rule-sheet-body" },
  ];

  for (const c of cases) {
    test(`${c.route}: lists rows and opens detail sheet`, async ({ page }) => {
      await page.goto(`/${c.route}`);
      await expect(page.getByTestId(`screen-${c.route}`)).toBeVisible();
      await expect(page.getByTestId(c.row)).toBeVisible();
      await page.getByTestId(c.row).click();
      await expect(page.getByTestId(c.sheet)).toBeVisible();
      await page.getByTestId("sheet-close").click();
      await expect(page.getByTestId(c.sheet)).not.toBeVisible();
    });
  }
});
