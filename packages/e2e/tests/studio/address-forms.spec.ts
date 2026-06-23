import { test, expect, type Route } from "@playwright/test";

// C8 write interactions — create / edit / delete (forms + mutations).
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};

// Live schema: `addresses` connection with flat AddressTemplate nodes;
// label/is_default live under `meta` (the hook normalises them out).
const LIST = {
  data: {
    addresses: {
      edges: [
        { node: { id: "adr_1", meta: { label: "HQ", is_default: true }, person_name: "Daniel K", company_name: "Acme", address_line1: "432 Park Ave", city: "Brooklyn", state_code: "NY", country_code: "US", postal_code: "11201", email: "ops@acme.io", phone_number: "+1 555" } },
      ],
    },
  },
};

async function graphqlRouter(route: Route) {
  if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
  const q = route.request().postData() ?? "";
  let body: unknown = { data: {} };
  if (q.includes("create_address")) body = { data: { create_address: { address: { id: "new" }, errors: [] } } };
  else if (q.includes("update_address")) body = { data: { update_address: { address: { id: "adr_1" }, errors: [] } } };
  else if (q.includes("delete_address")) body = { data: { delete_address: { id: "adr_1" } } };
  else if (q.includes("addresses")) body = LIST;
  return route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(body) });
}

test.describe("Addresses · create/edit/delete (C8)", () => {
  test.beforeEach(async ({ page }) => {
    await page.route("**/graphql", graphqlRouter);
  });

  test("create: validates then saves and closes", async ({ page }) => {
    await page.goto("/addresses");
    await expect(page.getByTestId("address-row-adr_1")).toBeVisible();
    await page.getByTestId("address-create").click();
    await expect(page.getByTestId("address-form")).toBeVisible();

    // Validation: empty label.
    await page.getByTestId("address-save").click();
    await expect(page.getByTestId("address-form-error")).toContainText(/label/i);

    // Fill required fields and save.
    await page.getByTestId("af-label").fill("Warehouse");
    await page.getByTestId("af-city").fill("Newark");
    await page.getByTestId("af-country").fill("US");
    await page.getByTestId("address-save").click();
    await expect(page.getByTestId("address-form")).toHaveCount(0);
  });

  test("edit: prefills and saves", async ({ page }) => {
    await page.goto("/addresses");
    await page.getByTestId("address-row-adr_1").click();
    await expect(page.getByTestId("af-label")).toHaveValue("HQ");
    await page.getByTestId("af-label").fill("HQ (updated)");
    await page.getByTestId("address-save").click();
    await expect(page.getByTestId("address-form")).toHaveCount(0);
  });

  test("delete: removes and closes", async ({ page }) => {
    await page.goto("/addresses");
    await page.getByTestId("address-row-adr_1").click();
    await page.getByTestId("address-delete").click();
    await expect(page.getByTestId("address-form")).toHaveCount(0);
  });
});
