import { test, expect } from "@playwright/test";
import { gotoStudio } from "../../helpers/studio";

// D4 Editor + F1 Assistant chat. The assistant server fn returns a stub reply
// (no ANTHROPIC_API_KEY), so the full send→reply interaction is testable.

test.describe("Editor + Assistant (D4/F1)", () => {
  test("renders 3 panes: sessions, chat, files", async ({ page }) => {
    await gotoStudio(page, "editor");
    await expect(page.getByTestId("editor-sessions")).toBeVisible();
    await expect(page.getByTestId("editor-messages")).toBeVisible();
    await expect(page.getByTestId("editor-files")).toBeVisible();
    await expect(page.getByTestId("editor-session-s1")).toBeVisible();
  });

  test("sending a message gets an assistant reply", async ({ page }) => {
    await gotoStudio(page, "editor");
    await page.getByTestId("editor-input").fill("Build a connector for Acme Express");
    await page.getByTestId("editor-send").click();
    // User message appears, then an assistant reply.
    await expect(page.getByTestId("msg-user").last()).toContainText("Acme Express");
    await expect(page.getByTestId("msg-assistant").last()).toContainText(/stub reply|Acme Express/i);
  });

  test("new session resets the chat", async ({ page }) => {
    await gotoStudio(page, "editor");
    await page.getByTestId("editor-new-session").click();
    await expect(page.getByTestId("editor-messages")).toContainText("What should we build");
  });

  test("model and mode selectors are present", async ({ page }) => {
    await gotoStudio(page, "editor");
    await expect(page.getByTestId("editor-model")).toBeVisible();
    await expect(page.getByTestId("editor-mode")).toBeVisible();
  });

  test("scaffold a connector generates the SDK extension file tree (F4)", async ({ page }) => {
    await gotoStudio(page, "editor");
    await page.getByTestId("editor-scaffold-input").fill("acme-express");
    await page.getByTestId("editor-scaffold").click();
    await expect(page.getByTestId("editor-files")).toContainText("karrio/providers/acme_express/rate.py");
    await expect(page.getByTestId("editor-files")).toContainText("tests/acme_express/test_shipment.py");
    await expect(page.getByTestId("editor-messages")).toContainText(/Scaffolded connector/i);
  });
});
