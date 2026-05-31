import { test, expect, type Page, type Route } from "@playwright/test";

// Visual regression baselines for Karrio Studio key screens.
//
// Gated: only runs when KARRIO_VISUAL=1 via the `studio-visual` / `studio-visual-mobile`
// Playwright projects defined in playwright.config.ts.
//
// First run (no committed baselines): run with --update-snapshots to create them.
//   KARRIO_VISUAL=1 npx playwright test --project=studio-visual --update-snapshots
//
// Subsequent CI runs without baselines: the studio-visual project is excluded from
// the config entirely (conditional spread), so these tests are never discovered.
//
// Screenshots are committed to packages/e2e/tests/studio/__snapshots__/ and
// compared pixel-by-pixel on future runs (threshold: 0.2%).

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};

function ok(route: Route, body: unknown): Promise<void> {
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

async function setupMocks(page: Page): Promise<void> {
  await page.route("**/v1/**", (route) => ok(route, paged([])));
  const SHIPMENTS = [
    {
      id: "shp_1", status: "shipped", tracking_number: "1Z999AA10123456784",
      selected_rate: { carrier_name: "ups", service: "ups_ground", total_charge: 12.4, currency: "USD", extra_charges: [] },
      recipient: { person_name: "Alicia Romero", city: "Brooklyn", state_code: "NY", country_code: "US" },
      shipper: { person_name: "Daniel K", city: "LA", state_code: "CA", country_code: "US" },
      reference: "ORDER-001", created_at: "2026-05-01T10:00:00Z",
    },
    {
      id: "shp_2", status: "in_transit", tracking_number: "1231006943",
      selected_rate: { carrier_name: "dhl", service: "dhl_express", total_charge: 42.8, currency: "USD", extra_charges: [] },
      recipient: { person_name: "Helmut Strauss", city: "Berlin", country_code: "DE" },
      reference: "ORDER-002", created_at: "2026-05-02T08:00:00Z",
    },
  ];
  const TRACKERS = [
    { id: "trk_1", tracking_number: "1Z999AA10123456784", carrier_name: "ups",
      status: "in_transit", estimated_delivery: "2026-06-01",
      events: [{ description: "Departed facility", location: "Newark, NJ", date: "2026-05-28", time: "11:00" }] },
  ];
  // Shipments + trackers load via GraphQL.
  await page.route("**/graphql", (route) => {
    if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
    const q = route.request().postData() ?? "";
    if (q.includes("shipments")) return ok(route, { data: { shipments: { edges: SHIPMENTS.map((node) => ({ node })) } } });
    if (q.includes("trackers")) return ok(route, { data: { trackers: { edges: TRACKERS.map((node) => ({ node })) } } });
    return ok(route, { data: {} });
  });
}

// Screens chosen for visual coverage: Home (dashboard summary), Shipments
// (data-rich list), and the Build/Apps tile grid. These cover distinct layout
// archetypes (stats cards, tabbed list, tile grid) while keeping the suite small.
test.describe("Studio visual baselines", () => {
  test.beforeEach(async ({ page }) => {
    await setupMocks(page);
  });

  test("Home dashboard", async ({ page }) => {
    await page.goto("/home", { waitUntil: "domcontentloaded" });
    await expect(page.getByTestId("screen-home")).toBeVisible();
    await page.waitForLoadState("networkidle");
    // Mask dynamic values (dates, counts) to avoid flake.
    await expect(page).toHaveScreenshot("home.png", {
      maxDiffPixelRatio: 0.002,
      mask: [page.locator("[data-testid='home-stats']")],
    });
  });

  test("Shipments list", async ({ page }) => {
    await page.goto("/shipments", { waitUntil: "domcontentloaded" });
    await expect(page.getByTestId("screen-shipments")).toBeVisible();
    await page.waitForLoadState("networkidle");
    await expect(page).toHaveScreenshot("shipments.png", {
      maxDiffPixelRatio: 0.002,
    });
  });

  test("Apps tile grid", async ({ page }) => {
    await page.route("**/v1/apps**", (route) =>
      ok(route, paged([
        { id: "shopify", name: "Shopify", vendor: "Karrio", description: "Sync orders.", installed: true, status: "connected" },
        { id: "zapier", name: "Zapier", vendor: "Karrio", description: "Automate flows.", installed: false, badge: "new" },
      ]))
    );
    await page.goto("/apps", { waitUntil: "domcontentloaded" });
    await expect(page.getByTestId("screen-apps")).toBeVisible();
    await page.waitForLoadState("networkidle");
    await expect(page).toHaveScreenshot("apps.png", {
      maxDiffPixelRatio: 0.002,
    });
  });
});
