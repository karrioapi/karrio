import { test, expect, type Route } from "@playwright/test";

// C3 · Trackers
const STUDIO_URL = process.env.KARRIO_STUDIO_URL || "http://localhost:3003";
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,POST,OPTIONS",
  "access-control-allow-headers": "authorization,x-org-id,x-test-mode,content-type",
};

const TRACKERS = {
  count: 2,
  next: null,
  previous: null,
  results: [
    {
      id: "trk_transit",
      tracking_number: "1Z999AA10123456784",
      carrier_name: "ups",
      status: "in_transit",
      estimated_delivery: "2026-06-01",
      events: [{ description: "Departed facility", location: "Newark, NJ", date: "2026-05-28", time: "11:02" }],
    },
    {
      id: "trk_delivered",
      tracking_number: "794651413733",
      carrier_name: "fedex",
      status: "delivered",
      estimated_delivery: "2026-05-27",
      events: [{ description: "Delivered", location: "Vancouver, BC", date: "2026-05-27", time: "15:48" }],
    },
  ],
};

async function fulfill(route: Route) {
  if (route.request().method() === "OPTIONS") return route.fulfill({ status: 204, headers: CORS, body: "" });
  return route.fulfill({ status: 200, headers: { ...CORS, "content-type": "application/json" }, body: JSON.stringify(TRACKERS) });
}

test.describe("Ship · Trackers (C3)", () => {
  test.beforeEach(async ({ page, context }) => {
    await context.addCookies([
      { name: "karrio-studio-session", value: JSON.stringify({ access: "t", refresh: "r", email: "a@b.c" }), url: STUDIO_URL, httpOnly: true, sameSite: "Lax" },
    ]);
    await page.route("**/v1/trackers**", fulfill);
  });

  test("lists trackers with tab counts", async ({ page }) => {
    await page.goto("/trackers");
    await expect(page.getByTestId("screen-trackers")).toBeVisible();
    await expect(page.getByTestId("tracker-row-trk_transit")).toBeVisible();
    await expect(page.getByTestId("tab-all")).toContainText("2");
    await expect(page.getByTestId("tab-delivered")).toContainText("1");
    await page.getByTestId("tab-delivered").click();
    await expect(page.getByTestId("tracker-row-trk_transit")).toHaveCount(0);
    await expect(page.getByTestId("tracker-row-trk_delivered")).toBeVisible();
  });

  test("row opens tracker sheet with timeline", async ({ page }) => {
    await page.goto("/trackers");
    await page.getByTestId("tracker-row-trk_transit").click();
    const sheet = page.getByTestId("tracker-sheet-body");
    await expect(sheet).toBeVisible();
    await expect(sheet).toContainText("1Z999AA10123456784");
    await expect(sheet.getByTestId("timeline")).toContainText("Departed facility");
  });
});
