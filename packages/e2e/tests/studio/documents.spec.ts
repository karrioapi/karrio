import { test, expect, type Route } from "@playwright/test";

// C11 · Document template editor — list + two-pane editor (code + live preview)
// + create via GraphQL.
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

const DOC = {
  id: "doc_1", name: "Packing slip", slug: "packing_slip", related_object: "shipment",
  description: "Default packing slip", active: true,
  template: "<h1>Slip {{ shipment.tracking_number }}</h1>", preview_url: "/documents/templates/doc_1.packing_slip?shipments=sample",
};

test.describe("Documents · template editor (C11)", () => {
  test.beforeEach(async ({ page, context }) => {
    await context.addCookies([
      { name: "karrio-studio-session", value: JSON.stringify({ access: "t", refresh: "r", email: "a@b.c" }), url: STUDIO_URL, httpOnly: true, sameSite: "Lax" },
    ]);
    await page.route("**/graphql", (route) => {
      const q = route.request().postData() ?? "";
      if (q.includes("document_templates")) return json(route, { data: { document_templates: { edges: [{ node: DOC }] } } });
      if (q.includes("create_document_template")) return json(route, { data: { create_document_template: { template: { id: "doc_new", slug: "invoice", preview_url: null }, errors: null } } });
      if (q.includes("update_document_template")) return json(route, { data: { update_document_template: { template: { id: "doc_1" }, errors: null } } });
      return json(route, { data: {} });
    });
  });

  test("lists templates and opens the editor", async ({ page }) => {
    await page.goto("/documents");
    await expect(page.getByTestId("screen-documents")).toBeVisible();
    await expect(page.getByTestId("document-row-doc_1")).toContainText("Packing slip");
    await page.getByTestId("document-row-doc_1").click();
    await expect(page.getByTestId("document-sheet-body")).toBeVisible();
    await expect(page.getByTestId("dt-template")).toHaveValue(/tracking_number/);
    await expect(page.getByTestId("dt-server-preview")).toBeVisible(); // saved → server preview link
  });

  test("live preview tab renders the template HTML in a sandboxed frame", async ({ page }) => {
    await page.goto("/documents");
    await expect(page.getByTestId("document-row-doc_1")).toBeVisible();
    await page.getByTestId("document-create").click();
    await expect(page.getByTestId("document-sheet-body")).toBeVisible();
    await page.getByTestId("dt-tab-preview").click();
    await expect(page.getByTestId("dt-preview-frame")).toBeVisible();
  });

  test("create: validates then saves and closes", async ({ page }) => {
    await page.goto("/documents");
    await expect(page.getByTestId("document-row-doc_1")).toBeVisible();
    await page.getByTestId("document-create").click();
    await expect(page.getByTestId("document-sheet-body")).toBeVisible();
    await page.getByTestId("dt-name").fill("");
    await page.getByTestId("document-save").click();
    await expect(page.getByTestId("document-form-error")).toContainText(/name/i);
    await page.getByTestId("dt-name").fill("Commercial invoice");
    await page.getByTestId("dt-related").selectOption("order");
    await page.getByTestId("document-save").click();
    await expect(page.getByTestId("document-sheet-body")).toHaveCount(0);
  });
});
