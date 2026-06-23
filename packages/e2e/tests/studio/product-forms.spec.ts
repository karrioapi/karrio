import { test, expect, type Route } from "@playwright/test";

// C10 write interactions — product create / edit / delete.
const CORS = { "access-control-allow-origin": "*", "access-control-allow-methods": "GET,POST,OPTIONS", "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type" };
const LIST = { data: { products: { edges: [ { node: { id: "prd_1", title: "Headphones", label: "Headphones", sku: "ACM-1", hs_code: "8518.30", value_amount: 84, value_currency: "USD", weight: 0.4, origin_country: "US" } } ] } } };

async function graphqlRouter(route: Route) {
  if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
  const q = route.request().postData() ?? "";
  let body: unknown = { data: {} };
  if (q.includes("create_product")) body = { data: { create_product: { product: { id: "new" }, errors: [] } } };
  else if (q.includes("update_product")) body = { data: { update_product: { product: { id: "prd_1" }, errors: [] } } };
  else if (q.includes("delete_product")) body = { data: { delete_product: { id: "prd_1" } } };
  else if (q.includes("products")) body = LIST;
  return route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(body) });
}

test.describe("Products · create/edit/delete (C10)", () => {
  test.beforeEach(async ({ page }) => { await page.route("**/graphql", graphqlRouter); });

  test("create: validates then saves and closes", async ({ page }) => {
    await page.goto("/products");
    await expect(page.getByTestId("product-row-prd_1")).toBeVisible();
    await page.getByTestId("product-create").click();
    await expect(page.getByTestId("product-form")).toBeVisible();
    await page.getByTestId("product-save").click();
    await expect(page.getByTestId("product-form-error")).toContainText(/title/i);
    await page.getByTestId("prf-title").fill("USB-C Cable");
    await page.getByTestId("product-save").click();
    await expect(page.getByTestId("product-form")).toHaveCount(0);
  });

  test("edit: prefills and saves", async ({ page }) => {
    await page.goto("/products");
    await page.getByTestId("product-row-prd_1").click();
    await expect(page.getByTestId("prf-title")).toHaveValue("Headphones");
    await page.getByTestId("prf-sku").fill("ACM-2");
    await page.getByTestId("product-save").click();
    await expect(page.getByTestId("product-form")).toHaveCount(0);
  });

  test("delete: removes and closes", async ({ page }) => {
    await page.goto("/products");
    await page.getByTestId("product-row-prd_1").click();
    await page.getByTestId("product-delete").click();
    await expect(page.getByTestId("product-form")).toHaveCount(0);
  });
});
