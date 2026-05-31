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

// Per-carrier connection field schema served by /v1/references (drives the
// dynamic credential form).
const REFERENCES = {
  carriers: { ups: "UPS", canadapost: "Canada Post" },
  connection_fields: {
    ups: {
      api_key: { name: "api_key", label: "API Key", type: "string", required: true, sensitive: true },
      account_number: { name: "account_number", label: "Account Number", type: "string", required: false, sensitive: false },
    },
    canadapost: {
      username: { name: "username", label: "Username", type: "string", required: true, sensitive: false },
      password: { name: "password", label: "Password", type: "string", required: true, sensitive: true },
      language: { name: "language", label: "Language", type: "string", required: false, sensitive: false, default: "en", enum: ["en", "fr"] },
    },
  },
};

test.describe("Connections & Webhooks forms (C6/D6)", () => {
  test.beforeEach(async ({ page }) => {
    // Lists + connection mutations are GraphQL; webhook mutations stay REST.
    await page.route("**/graphql", (route) => {
      const q = route.request().postData() ?? "";
      if (q.includes("user_connections")) return ok(route, { data: { user_connections: { edges: [{ node: { id: "conn_1", carrier_name: "ups", carrier_id: "ups_acct", display_name: "UPS", test_mode: false, active: true, capabilities: ["rating"] } }] } } });
      if (q.includes("webhooks")) return ok(route, { data: { webhooks: { edges: [{ node: { id: "wh_1", url: "https://acme.shop/hooks", disabled: false, description: "ops", enabled_events: ["shipment_purchased"] } }] } } });
      if (q.includes("create_carrier_connection")) return ok(route, { data: { create_carrier_connection: { connection: { id: "conn_new", carrier_name: "ups", carrier_id: "ups_main" }, errors: null } } });
      if (q.includes("update_carrier_connection")) return ok(route, { data: { update_carrier_connection: { connection: { id: "conn_1" }, errors: null } } });
      if (q.includes("delete_carrier_connection")) return ok(route, { data: { delete_carrier_connection: { id: "conn_1" } } });
      return ok(route, { data: {} });
    });
    await page.route("**/v1/references**", (route) => ok(route, REFERENCES));
    await page.route("**/v1/webhooks**", (route) =>
      ok(route, route.request().method() === "GET"
        ? paged([{ id: "wh_1", url: "https://acme.shop/hooks", enabled: true, events: ["shipment_purchased"], description: "ops" }])
        : { id: "wh_1" }));
  });

  test("connection: dynamic per-carrier form — validate → create → close", async ({ page }) => {
    await page.goto("/connections");
    await expect(page.getByTestId("connection-row-conn_1")).toBeVisible(); // wait for hydration
    await page.getByTestId("connection-create").click();
    await expect(page.getByTestId("connection-form")).toBeVisible();
    // Carrier required first.
    await page.getByTestId("connection-save").click();
    await expect(page.getByTestId("connection-form-error")).toContainText(/carrier/i);
    // Pick a carrier → its dynamic credential fields appear.
    await page.getByTestId("cf-carrier").selectOption("ups");
    await expect(page.getByTestId("cf-field-api_key")).toBeVisible();
    await page.getByTestId("connection-save").click();
    await expect(page.getByTestId("connection-form-error")).toContainText(/account id/i);
    await page.getByTestId("cf-account").fill("ups_main");
    await page.getByTestId("connection-save").click();
    await expect(page.getByTestId("connection-form-error")).toContainText(/api key/i); // required dynamic field
    await page.getByTestId("cf-field-api_key").fill("secret-key");
    await page.getByTestId("connection-save").click();
    await expect(page.getByTestId("connection-form")).toHaveCount(0);
  });

  test("connection: credential fields are carrier-specific (dynamic from references)", async ({ page }) => {
    await page.goto("/connections");
    await expect(page.getByTestId("connection-row-conn_1")).toBeVisible(); // wait for hydration
    await page.getByTestId("connection-create").click();
    await expect(page.getByTestId("connection-form")).toBeVisible();
    // Canada Post exposes username/password/language (enum) — not UPS's api_key.
    await page.getByTestId("cf-carrier").selectOption("canadapost");
    await expect(page.getByTestId("cf-field-username")).toBeVisible();
    await expect(page.getByTestId("cf-field-password")).toHaveAttribute("type", "password");
    await expect(page.getByTestId("cf-field-language")).toBeVisible(); // enum → select, default en
    await expect(page.getByTestId("cf-field-api_key")).toHaveCount(0);
    // Switching carrier swaps the field set.
    await page.getByTestId("cf-carrier").selectOption("ups");
    await expect(page.getByTestId("cf-field-api_key")).toBeVisible();
    await expect(page.getByTestId("cf-field-username")).toHaveCount(0);
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
