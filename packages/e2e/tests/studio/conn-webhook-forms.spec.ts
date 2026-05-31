import { test, expect, type Route } from "@playwright/test";

// C6 + D6 write interactions — Connections & Webhooks create/edit/delete (REST).
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,PATCH,DELETE,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};
const ok = (route: Route, body: unknown) =>
  route.request().method() === "OPTIONS"
    ? route.fulfill({ status: 204, headers: CORS, body: "" })
    : route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(body) });
const paged = (results: unknown[]) => ({ count: results.length, next: null, previous: null, results });

test.describe("Connections & Webhooks forms (C6/D6)", () => {
  test.beforeEach(async ({ page }) => {
    // Connection LIST is GraphQL (user_connections); create/update/delete stay REST.
    await page.route("**/graphql", (route) =>
      ok(route, (route.request().postData() ?? "").includes("user_connections")
        ? { data: { user_connections: { edges: [{ node: { id: "conn_1", carrier_name: "ups", carrier_id: "ups_acct", display_name: "UPS", test_mode: false, active: true, capabilities: ["rating"] } }] } } }
        : { data: {} }));
    await page.route("**/v1/connections**", (route) => ok(route, { id: "conn_1" }));
    await page.route("**/v1/webhooks**", (route) =>
      ok(route, route.request().method() === "GET"
        ? paged([{ id: "wh_1", url: "https://acme.shop/hooks", enabled: true, events: ["shipment_purchased"], description: "ops" }])
        : { id: "wh_1" }));
  });

  test("connection: validate → create → close", async ({ page }) => {
    await page.goto("/connections");
    await expect(page.getByTestId("connection-row-conn_1")).toBeVisible(); // wait for hydration
    await page.getByTestId("connection-create").click();
    await expect(page.getByTestId("connection-form")).toBeVisible();
    await page.getByTestId("connection-save").click();
    await expect(page.getByTestId("connection-form-error")).toContainText(/account id/i);
    await page.getByTestId("cf-account").fill("ups_main");
    await page.getByTestId("connection-save").click();
    await expect(page.getByTestId("connection-form")).toHaveCount(0);
  });

  test("connection: invalid credentials JSON shows error", async ({ page }) => {
    await page.goto("/connections");
    await expect(page.getByTestId("connection-row-conn_1")).toBeVisible();
    await page.getByTestId("connection-create").click();
    await page.getByTestId("cf-account").fill("ups_main");
    await page.getByTestId("cf-credentials").fill("{not json");
    await page.getByTestId("connection-save").click();
    await expect(page.getByTestId("connection-form-error")).toContainText(/valid json/i);
  });

  test("webhook: validate URL → create → close", async ({ page }) => {
    await page.goto("/webhooks");
    await expect(page.getByTestId("webhook-row-wh_1")).toBeVisible(); // wait for hydration
    await page.getByTestId("webhook-create").click();
    await expect(page.getByTestId("webhook-form")).toBeVisible();
    await page.getByTestId("wf-url").fill("not-a-url");
    await page.getByTestId("webhook-save").click();
    await expect(page.getByTestId("webhook-form-error")).toContainText(/valid https/i);
    await page.getByTestId("wf-url").fill("https://acme.shop/hooks");
    await page.getByTestId("wf-events").fill("shipment_purchased, tracker_updated");
    await page.getByTestId("webhook-save").click();
    await expect(page.getByTestId("webhook-form")).toHaveCount(0);
  });

  test("webhook: edit prefilled then delete", async ({ page }) => {
    await page.goto("/webhooks");
    await page.getByTestId("webhook-row-wh_1").click();
    await expect(page.getByTestId("wf-url")).toHaveValue("https://acme.shop/hooks");
    await page.getByTestId("webhook-delete").click();
    await expect(page.getByTestId("webhook-form")).toHaveCount(0);
  });
});
