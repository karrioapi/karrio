import { test, expect, type Route } from "@playwright/test";

// D1–D3, D6, D7 · Build mode (Apps, Plugins, MCP, Webhooks, API keys).
const STUDIO_URL = process.env.KARRIO_STUDIO_URL || "http://localhost:3003";
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

const DATA: Record<string, unknown> = {
  "/v1/apps": paged([
    { id: "shopify", name: "Shopify", vendor: "Karrio", description: "Sync orders and rates.", installed: true, status: "connected" },
    { id: "zapier", name: "Zapier", vendor: "Karrio", description: "Automate flows.", installed: false, badge: "new" },
  ]),
  "/v1/plugins": paged([
    { id: "ups", name: "UPS", vendor: "Karrio", description: "Rate, label, track.", installed: true, version: "2026.5.1", tags: ["Carrier"] },
    { id: "smarty", name: "SmartyStreets", vendor: "SmartyStreets", description: "Address validation.", installed: false, tags: ["Address"], badge: "beta" },
  ]),
  "/v1/webhooks": paged([
    { id: "wh_1", url: "https://acme.shop/hooks/karrio", enabled: true, events: ["shipment_purchased", "tracker_updated"], description: "Ops webhook" },
  ]),
  "/v1/api_keys": paged([
    { id: "key_live", label: "Production", key: "sk_live_••••a31f", test_mode: false, created: "2026-05-01" },
    { id: "key_test", label: "Sandbox", key: "sk_test_••••99c1", test_mode: true, created: "2026-05-02" },
  ]),
  "/v1/mcp": {
    status: "running", url: "https://mcp.karrio.io/acme", version: "v2026.5.1",
    stats: { tools: 2, clients: 2, calls_24h: "10.4k", p99: "142ms" },
    tools: [
      { name: "list_shipments", description: "List shipments", requests: 1284, p99: "84ms" },
      { name: "track_shipment", description: "Track a shipment", requests: 2841, p99: "112ms" },
    ],
    clients: [{ id: "claude", name: "Claude Desktop", connected: true, calls: 482 }],
    invocations: [{ id: "iv1", tool: "track_shipment", client: "Claude Desktop", duration_ms: 84 }],
  },
};

test.describe("Build mode (D)", () => {
  test.beforeEach(async ({ page, context }) => {
    await context.addCookies([
      { name: "karrio-studio-session", value: JSON.stringify({ access: "t", refresh: "r", email: "a@b.c" }), url: STUDIO_URL, httpOnly: true, sameSite: "Lax" },
    ]);
    for (const [path, body] of Object.entries(DATA)) {
      await page.route(`**${path}**`, (route) => json(route, body));
    }
  });

  test("Apps: tabs + tile opens config sheet", async ({ page }) => {
    await page.goto("/apps");
    await expect(page.getByTestId("app-tile-shopify")).toBeVisible();
    await expect(page.getByTestId("tab-installed")).toContainText("1");
    await page.getByTestId("tab-available").click();
    await expect(page.getByTestId("app-tile-zapier")).toBeVisible();
    await expect(page.getByTestId("app-tile-shopify")).toHaveCount(0);
    await page.getByTestId("app-tile-zapier").click();
    await expect(page.getByTestId("app-sheet-body")).toBeVisible();
  });

  test("Plugins: category tabs + tile opens sheet", async ({ page }) => {
    await page.goto("/plugins");
    await expect(page.getByTestId("plugin-tile-ups")).toBeVisible();
    await page.getByTestId("tab-address").click();
    await expect(page.getByTestId("plugin-tile-smarty")).toBeVisible();
    await page.getByTestId("plugin-tile-smarty").click();
    await expect(page.getByTestId("plugin-sheet-body")).toBeVisible();
  });

  test("MCP: server card, tools, start/stop toggle, copy snippet", async ({ page }) => {
    await page.goto("/mcp");
    await expect(page.getByTestId("mcp-server-card")).toBeVisible();
    await expect(page.getByTestId("mcp-tool-list_shipments")).toBeVisible();
    await expect(page.getByTestId("mcp-status")).toHaveText("running");
    await page.getByTestId("mcp-toggle").click();
    await expect(page.getByTestId("mcp-status")).toHaveText("stopped");
    await expect(page.getByTestId("mcp-snippet")).toContainText("@karrio/mcp");
    await page.getByTestId("mcp-copy").click(); // should not throw
  });

  test("Webhooks: row opens edit form prefilled with events", async ({ page }) => {
    await page.goto("/webhooks");
    await page.getByTestId("webhook-row-wh_1").click();
    await expect(page.getByTestId("webhook-form")).toBeVisible();
    await expect(page.getByTestId("wf-events")).toHaveValue(/shipment_purchased/);
  });

  test("API keys: live + test rows render", async ({ page }) => {
    await page.goto("/apikeys");
    await expect(page.getByTestId("apikey-row-key_live")).toContainText("Production");
    await expect(page.getByTestId("apikey-row-key_test")).toContainText("Sandbox");
  });
});
