import { test, expect, type Route } from "@playwright/test";

// C9 write interactions — parcel create / edit / delete (forms + mutations).
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};
// Live schema: `parcels` connection with flat ParcelTemplate nodes;
// label/is_default live under `meta` (the hook normalises them out).
const LIST = {
  data: {
    parcels: {
      edges: [
        { node: { id: "pcl_1", meta: { label: "Small Box", is_default: true }, packaging_type: "BOX", width: 15, height: 10, length: 20, dimension_unit: "CM", weight: 0.5, weight_unit: "KG" } },
      ],
    },
  },
};

async function graphqlRouter(route: Route) {
  if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
  const q = route.request().postData() ?? "";
  let body: unknown = { data: {} };
  if (q.includes("create_parcel")) body = { data: { create_parcel: { parcel: { id: "new" }, errors: [] } } };
  else if (q.includes("update_parcel")) body = { data: { update_parcel: { parcel: { id: "pcl_1" }, errors: [] } } };
  else if (q.includes("delete_parcel")) body = { data: { delete_parcel: { id: "pcl_1" } } };
  else if (q.includes("parcels")) body = LIST;
  return route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(body) });
}

test.describe("Parcels · create/edit/delete (C9)", () => {
  test.beforeEach(async ({ page }) => {
    await page.route("**/graphql", graphqlRouter);
  });

  test("create: validates then saves and closes", async ({ page }) => {
    await page.goto("/parcels");
    await expect(page.getByTestId("parcel-row-pcl_1")).toBeVisible();
    await page.getByTestId("parcel-create").click();
    await expect(page.getByTestId("parcel-form")).toBeVisible();
    await page.getByTestId("parcel-save").click();
    await expect(page.getByTestId("parcel-form-error")).toContainText(/label/i);
    await page.getByTestId("pf-label").fill("Large Box");
    await page.getByTestId("pf-weight").fill("5");
    await page.getByTestId("parcel-save").click();
    await expect(page.getByTestId("parcel-form")).toHaveCount(0);
  });

  test("edit: prefills and saves", async ({ page }) => {
    await page.goto("/parcels");
    await page.getByTestId("parcel-row-pcl_1").click();
    await expect(page.getByTestId("pf-label")).toHaveValue("Small Box");
    await page.getByTestId("pf-label").fill("Small Box v2");
    await page.getByTestId("parcel-save").click();
    await expect(page.getByTestId("parcel-form")).toHaveCount(0);
  });

  test("delete: removes and closes", async ({ page }) => {
    await page.goto("/parcels");
    await page.getByTestId("parcel-row-pcl_1").click();
    await page.getByTestId("parcel-delete").click();
    await expect(page.getByTestId("parcel-form")).toHaveCount(0);
  });
});
