import { test, expect, type Route } from "@playwright/test";

// C2 · Shipments — exercises the decoupled data path end to end:
// session cookie → getSession server fn → useShipments → fetch client → render.
// The Karrio API is intercepted so the spec runs without a live backend; the
// live-backend variant is covered by EPIC I3 (seeded fixtures).

const STUDIO_URL = process.env.KARRIO_STUDIO_URL || "http://localhost:3003";

const SHIPMENTS = {
  count: 3,
  next: null,
  previous: null,
  results: [
    {
      id: "shp_purch",
      status: "purchased",
      tracking_number: "1Z999AA10123456784",
      selected_rate: { carrier_name: "ups", carrier_id: "ups_prod", service: "ups_2nd_day_air", total_charge: 12.4, currency: "USD",
        extra_charges: [{ name: "Base charge", amount: 9.92, currency: "USD" }, { name: "Fuel surcharge", amount: 1.86, currency: "USD" }] },
      parcels: [{ id: "pcl_1", packaging_type: "BOX", length: 25, width: 30, height: 20, dimension_unit: "CM", weight: 2, weight_unit: "KG" }],
      recipient: { person_name: "Alicia Romero", city: "Brooklyn", state_code: "NY", country_code: "US", postal_code: "11201", address_line1: "55 Water St" },
      shipper: { company_name: "Acme Inc.", person_name: "Daniel Kovic", city: "Brooklyn", state_code: "NY", country_code: "US", postal_code: "11201", address_line1: "432 Park Ave" },
      reference: "ORDER-11335",
      created_at: "2026-05-28T10:02:00Z",
    },
    {
      id: "shp_transit",
      status: "in_transit",
      carrier_name: "dhl",
      tracking_number: "1231006943",
      service: "DHL Express Worldwide",
      selected_rate: { total_charge: 42.8, currency: "USD" },
      recipient: { person_name: "Helmut Strauss", city: "Berlin", country_code: "DE" },
      reference: "ORDER-11334",
      created_at: "2026-05-28T07:48:00Z",
    },
    {
      id: "shp_delivered",
      status: "delivered",
      carrier_name: "fedex",
      tracking_number: "794651413733",
      service: "FedEx Priority Overnight",
      selected_rate: { total_charge: 28.1, currency: "USD" },
      recipient: { person_name: "Jane Doe", city: "Vancouver", state_code: "BC", country_code: "CA" },
      reference: "REF-1112",
      created_at: "2026-05-28T09:58:00Z",
    },
  ],
};

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};

// Shipments now load via GraphQL `shipments { edges { node } }`.
async function fulfillShipments(route: Route) {
  if (route.request().method() === "OPTIONS") {
    return route.fulfill({ status: 204, headers: CORS, body: "" });
  }
  const q = route.request().postData() ?? "";
  const body = q.includes("shipments")
    ? { data: { shipments: { edges: SHIPMENTS.results.map((node) => ({ node })) } } }
    : { data: {} };
  return route.fulfill({
    status: 200,
    headers: { ...CORS, "content-type": "application/json" },
    contentType: "application/json",
    body: JSON.stringify(body),
  });
}

test.describe("Ship · Shipments (C2)", () => {
  test.beforeEach(async ({ page, context }) => {
    // Seed an authenticated Studio session so useShipments is enabled.
    await context.addCookies([
      {
        name: "karrio-studio-session",
        value: JSON.stringify({ access: "test-token", refresh: "r", email: "admin@example.com" }),
        url: STUDIO_URL,
        httpOnly: true,
        sameSite: "Lax",
      },
    ]);
    await page.route("**/graphql", fulfillShipments);
  });

  test("renders header, tabs and filter toolbar", async ({ page }) => {
    await page.goto("/shipments");
    await expect(page.getByTestId("screen-shipments")).toBeVisible();
    await expect(page.getByRole("heading", { name: "Shipments" })).toBeVisible();
    await expect(page.getByTestId("tab-all")).toBeVisible();
    await expect(page.getByTestId("tab-intransit")).toBeVisible();
    await expect(page.getByText("Filter")).toBeVisible();
  });

  test("lists shipments from the API with tab counts", async ({ page }) => {
    await page.goto("/shipments");
    await expect(page.getByTestId("shipment-row-shp_purch")).toBeVisible();
    await expect(page.getByTestId("shipment-row-shp_transit")).toBeVisible();
    await expect(page.getByTestId("shipment-row-shp_delivered")).toBeVisible();

    // tab counts derived from the loaded page
    await expect(page.getByTestId("tab-all")).toContainText("3");
    await expect(page.getByTestId("tab-delivered")).toContainText("1");

    // filter by tab
    await page.getByTestId("tab-delivered").click();
    await expect(page.getByTestId("shipment-row-shp_delivered")).toBeVisible();
    await expect(page.getByTestId("shipment-row-shp_purch")).toHaveCount(0);
  });

  test("row opens the shipment sheet with details", async ({ page }) => {
    await page.goto("/shipments");
    await page.getByTestId("shipment-row-shp_purch").click();
    const sheet = page.getByTestId("shipment-sheet-body");
    await expect(sheet).toBeVisible();
    await expect(sheet).toContainText("1Z999AA10123456784");
    await expect(sheet).toContainText("Ups 2nd Day Air"); // humanized service from rate
    await expect(sheet).toContainText("Daniel Kovic"); // shipped-from
    await expect(sheet).toContainText("Alicia Romero"); // shipped-to
    await expect(sheet).toContainText("BOX"); // parcels section
    await expect(sheet).toContainText("25 × 30 × 20 CM");
    await expect(sheet).toContainText("Base charge"); // itemized charges
    await expect(sheet).toContainText("Fuel surcharge");
    await page.getByTestId("sheet-close").click();
    await expect(sheet).not.toBeVisible();
  });

  test("selecting rows reveals bulk actions", async ({ page }) => {
    await page.goto("/shipments");
    // Wait for fetched rows (implies the client has hydrated) before interacting
    // with the static select-all control.
    await expect(page.getByTestId("shipment-row-shp_purch")).toBeVisible();
    await page.getByTestId("select-all").click();
    await expect(page.getByTestId("selection-count")).toContainText("3 selected");
    await expect(page.getByRole("button", { name: /print labels/i })).toBeVisible();
  });
});
