import { test, expect, type Page, type Route } from "@playwright/test";
import { ALL_STUDIO_ROUTES, STUDIO_NAV } from "../../helpers/studio";

// Render-smoke: for EVERY studio route, navigate authenticated and assert:
//   (a) no `pageerror` was emitted during load, and
//   (b) the route's screen testid renders.
//
// This catches "build-green-but-broken" runtime crashes that tsc/vite miss.
// Example: display.ts crashed with "Cannot read properties of undefined
// (reading 'split')" on Trackers/Shipments even though the build was green.
//
// All API calls are mocked so this spec is self-contained (no Django backend).

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};

function jsonReply(route: Route, body: unknown): Promise<void> {
  if (route.request().method() === "OPTIONS") {
    return route.fulfill({ status: 204, headers: CORS, body: "" });
  }
  return route.fulfill({
    status: 200,
    headers: { ...CORS, "content-type": "application/json" },
    body: JSON.stringify(body),
  });
}

const paged = (results: unknown[]) => ({ count: results.length, next: null, previous: null, results });
const edges = (field: string, nodes: unknown[]) => ({
  data: { [field]: { edges: nodes.map((node) => ({ node })) } },
});

// Minimal fixture data — just enough for each screen to render without crashing.
// Lists need at least one item so data-path code (map/filter/split) is exercised.
const MOCK_DATA: Record<string, unknown> = {
  // Ship mode
  "/v1/shipments": paged([
    {
      id: "shp_smoke",
      status: "purchased",
      tracking_number: "SMOKE001",
      selected_rate: { carrier_name: "ups", service: "ups_ground", total_charge: 9.99, currency: "USD", extra_charges: [] },
      recipient: { person_name: "Test User", city: "New York", state_code: "NY", country_code: "US" },
      shipper: { person_name: "Shipper", city: "LA", state_code: "CA", country_code: "US" },
      reference: "SMOKE-REF",
      created_at: "2026-05-01T10:00:00Z",
    },
  ]),
  "/v1/trackers": paged([
    {
      id: "trk_smoke",
      tracking_number: "SMOKE_TRK001",
      carrier_name: "ups",
      status: "in_transit",
      estimated_delivery: "2026-06-01",
      events: [{ description: "Departed", location: "Newark, NJ", date: "2026-05-28", time: "11:00" }],
    },
  ]),
  "/v1/orders": paged([
    { id: "ord_smoke", order_id: "ORD-001", source: "shopify", status: "unfulfilled", created_at: "2026-05-01T10:00:00Z",
      shipping_to: { person_name: "Test", city: "NYC", country_code: "US" },
      line_items: [{ id: "li_1", title: "Widget", quantity: 1, sku: "WGT-1", unfulfilled_quantity: 1 }] },
  ]),
  "/v1/pickups": paged([
    { id: "pck_smoke", carrier_name: "ups", confirmation_number: "PU123", pickup_date: "2026-06-01",
      ready_time: "09:00", closing_time: "17:00", address: { city: "Brooklyn", country_code: "US" } },
  ]),
  "/v1/connections": paged([
    { id: "con_smoke", carrier_name: "ups", carrier_id: "ups_prod", display_name: "UPS Production",
      enabled: true, test_mode: false, capabilities: ["rating", "shipping", "tracking"] },
  ]),
  "/v1/carrier_connections": paged([]),
  "/v1/rules": paged([
    { id: "rl_smoke", name: "Default rule", status: "active", priority: 1 },
  ]),
  "/v1/addresses": paged([
    { id: "adr_smoke", person_name: "Test User", city: "Brooklyn", state_code: "NY", country_code: "US",
      address_line1: "123 Main St", postal_code: "11201", residential: false },
  ]),
  "/v1/parcels": paged([
    { id: "pcl_smoke", packaging_type: "BOX", weight: 2, weight_unit: "KG",
      length: 20, width: 15, height: 10, dimension_unit: "CM" },
  ]),
  "/v1/products": paged([
    { id: "prod_smoke", sku: "SKU-001", title: "Test Product", description: "A widget",
      weight: 0.5, weight_unit: "KG", quantity: 100, variant_id: "v1" },
  ]),
  "/v1/documents": paged([
    { id: "doc_smoke", template_name: "invoice", carrier_name: "ups",
      related_object_id: "shp_smoke", document_format: "PDF", created_at: "2026-05-01T10:00:00Z" },
  ]),
  "/v1/manifests": paged([
    { id: "mf_smoke", carrier_name: "ups", reference: "MAN-001", shipment_count: 3,
      created_at: "2026-05-01T10:00:00Z", manifest_url: "http://example.com/m.pdf" },
  ]),
  "/v1/batches/operations": paged([
    { id: "bat_smoke", status: "completed", resource_type: "shipments", total: 5,
      created_at: "2026-05-01T10:00:00Z" },
  ]),
  // Build mode
  "/v1/apps": paged([
    { id: "shopify", name: "Shopify", vendor: "Karrio", description: "Sync orders.", installed: true, status: "connected" },
  ]),
  "/v1/plugins": paged([
    { id: "ups", name: "UPS", vendor: "Karrio", description: "Rate, label, track.", installed: true, version: "2026.5.1", tags: ["Carrier"] },
  ]),
  "/v1/mcp": {
    status: "running", url: "https://mcp.karrio.io/test", version: "v2026.5.1",
    stats: { tools: 1, clients: 1, calls_24h: "1k", p99: "100ms" },
    tools: [{ name: "list_shipments", description: "List shipments", requests: 100, p99: "80ms" }],
    clients: [{ id: "claude", name: "Claude Desktop", connected: true, calls: 10 }],
    invocations: [],
  },
  "/v1/webhooks": paged([
    { id: "wh_smoke", url: "https://example.com/hook", enabled: true,
      events: ["shipment_purchased"], description: "Test webhook" },
  ]),
  "/v1/api_keys": paged([
    { id: "key_smoke", label: "Test Key", key: "sk_test_••••smoke", test_mode: true, created: "2026-05-01" },
  ]),
  // Govern mode
  "/v1/admin": {
    version: "2026.5.1", tenants: 1, license: "Enterprise",
    resources: [{ label: "CPU", used: 30, total: 100 }],
    runtimes: [{ name: "ups", memory: "32MB", calls: 100, p99: "80ms" }],
  },
  "/v1/admin/tenants": paged([
    { id: "tn_smoke", name: "Smoke Tenant", slug: "smoke", members: 1, status: "active", created: "2026-05-01" },
  ]),
  "/v1/admin/users": paged([
    { id: "usr_smoke", name: "Smoke User", email: "smoke@test.io", role: "owner", status: "active" },
  ]),
  "/v1/events": paged([
    { id: "ev_smoke", type: "shipment.purchased", actor: "smoke@test.io", description: "Purchased label", at: "10:00 AM" },
  ]),
  "/v1/usage": {
    plan: "Enterprise", period: "May 2026",
    metrics: [{ label: "API calls", value: "1k", delta: "+5%" }],
  },
};

// GraphQL mock data for screens that use GQL queries.
const GQL_DATA: Record<string, unknown> = {
  workflows: edges("workflows", [
    { id: "wf_smoke", name: "Auto-fulfill", description: "Fulfill paid orders", is_active: true,
      trigger: "order.paid", action_count: 1 },
  ]),
  rate_sheets: edges("rate_sheets", [
    { id: "rs_smoke", name: "UPS Negotiated", carrier_name: "ups", services_count: 3, is_system: false },
  ]),
};

/**
 * Register all REST and GraphQL mocks on a page so every API call is satisfied
 * without a live backend. Mocks use route glob patterns; Playwright applies the
 * last-registered route first, so specific patterns are registered last.
 */
async function mockAllApis(page: Page): Promise<void> {
  // Broad fallback: any unmatched /v1/ call returns an empty paged response.
  await page.route("**/v1/**", (route) => jsonReply(route, paged([])));

  // GraphQL (workflows / rate sheets)
  await page.route("**/graphql", (route) => {
    if (route.request().method() === "OPTIONS") {
      return route.fulfill({ status: 204, headers: CORS, body: "" });
    }
    const q = route.request().postData() ?? "";
    const field = Object.keys(GQL_DATA).find((f) => q.includes(f));
    return jsonReply(route, field ? GQL_DATA[field] : { data: {} });
  });

  // Register specific REST routes (more specific = registered last = wins).
  // Admin sub-routes must come after the broad /admin match.
  await page.route("**/v1/admin**", (route) => jsonReply(route, MOCK_DATA["/v1/admin"]));
  await page.route("**/v1/admin/tenants**", (route) => jsonReply(route, MOCK_DATA["/v1/admin/tenants"]));
  await page.route("**/v1/admin/users**", (route) => jsonReply(route, MOCK_DATA["/v1/admin/users"]));

  for (const [path, body] of Object.entries(MOCK_DATA)) {
    // Skip admin paths — already registered above with correct specificity.
    if (path.startsWith("/v1/admin")) continue;
    await page.route(`**${path}**`, (route) => jsonReply(route, body));
  }
}

// Routes that require extra patience (lazy-loaded chunks or heavier data fetch)
const SLOW_ROUTES = new Set(["editor", "admin"]);

test.describe("Studio render-smoke", () => {
  // Iterate ALL routes and assert:
  //   1. No JS errors emitted via `pageerror`
  //   2. The route's `screen-<route>` testid becomes visible
  for (const route of ALL_STUDIO_ROUTES) {
    test(`/${route} — no crash + screen renders`, async ({ page }) => {
      const errors: string[] = [];
      page.on("pageerror", (err) => errors.push(err.message));

      await mockAllApis(page);

      await page.goto(`/${route}`, { waitUntil: "domcontentloaded" });

      // Wait for the screen testid (generous timeout for lazy chunks).
      const timeout = SLOW_ROUTES.has(route) ? 15_000 : 10_000;
      await expect(page.getByTestId(`screen-${route}`)).toBeVisible({ timeout });

      // Fail the test if any JS error fired during load.
      if (errors.length > 0) {
        throw new Error(`Page errors on /${route}:\n${errors.join("\n")}`);
      }
    });
  }
});

// Sanity: verify ALL_STUDIO_ROUTES covers every known mode.
test.describe("Studio render-smoke — route coverage", () => {
  const expectedModes = Object.keys(STUDIO_NAV);

  test("STUDIO_NAV covers ship, build, govern modes", () => {
    expect(expectedModes).toContain("ship");
    expect(expectedModes).toContain("build");
    expect(expectedModes).toContain("govern");
  });

  test("ALL_STUDIO_ROUTES is non-empty and matches STUDIO_NAV union", () => {
    const union = Object.values(STUDIO_NAV).flat();
    expect(ALL_STUDIO_ROUTES).toEqual(union);
    expect(ALL_STUDIO_ROUTES.length).toBeGreaterThan(0);
  });
});
