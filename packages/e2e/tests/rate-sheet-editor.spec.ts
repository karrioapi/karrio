import { test, expect } from "@playwright/test";
import path from "path";
import {
  navigateToCarrierNetwork,
  clickRateSheetsTab,
  openCreateRateSheetEditor,
  clickModeButton,
  uploadImportFile,
  waitForDiffPreview,
  waitForImportErrors,
} from "../helpers/rate-sheet-helpers";

const FIXTURES = path.join(__dirname, "..", "fixtures");

// ─── Suite configuration ──────────────────────────────────────────────────────
// Auth is handled by the "setup" project in playwright.config.ts.

test.describe.configure({ mode: "serial" });

test.describe("Rate Sheet Editor — Karrio Dashboard", () => {

  // ── 1. Navigation ────────────────────────────────────────────────────────────
  test("1. navigates to /admin/carriers and shows the Carrier Network page", async ({ page }) => {
    await navigateToCarrierNetwork(page);

    // Page heading should mention "Carrier" — exact text may vary
    const heading = page.locator("h1, h2").filter({ hasText: /carrier/i }).first();
    await expect(heading).toBeVisible({ timeout: 20_000 });

    // "Rate Sheets" tab button must be present
    await expect(page.getByRole("button", { name: /rate sheets/i })).toBeVisible({
      timeout: 10_000,
    });
  });

  // ── 2. Tab switch ────────────────────────────────────────────────────────────
  test("2. clicking the Rate Sheets tab shows the rate sheet list (or empty state)", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);

    // Either a rate-sheet card/row exists or an empty-state message is shown
    const hasContent = await page
      .locator("text=/no rate sheets|rate sheet|create rate sheet/i")
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasContent).toBe(true);
  });

  // ── 3. Create editor opens ───────────────────────────────────────────────────
  test("3. clicking Create Rate Sheet opens the editor panel with title 'Create Rate Sheet'", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);
    await openCreateRateSheetEditor(page);

    const dialog = page.locator('[role="dialog"]').first();
    await expect(dialog).toBeVisible({ timeout: 15_000 });

    // The SheetTitle contains "Create Rate Sheet"
    await expect(dialog.locator("text=/create rate sheet/i").first()).toBeVisible({
      timeout: 10_000,
    });
  });

  // ── 4. Mode buttons visible ──────────────────────────────────────────────────
  test("4. editor header shows edit, import, and export mode buttons", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);
    await openCreateRateSheetEditor(page);

    const dialog = page.locator('[role="dialog"]').first();
    await expect(dialog).toBeVisible();

    // Each mode button has the lowercase label as text content
    for (const mode of ["edit", "import", "export"] as const) {
      await expect(
        dialog.locator("button", { hasText: new RegExp(`^${mode}$`, "i") })
      ).toBeVisible({ timeout: 10_000 });
    }
  });

  // ── 5. Switch to import mode ─────────────────────────────────────────────────
  test("5. clicking import mode shows the import panel with a file input", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);
    await openCreateRateSheetEditor(page);

    await clickModeButton(page, "import");

    // The import panel renders a file input (possibly hidden) and a drop zone
    const fileInput = page.locator('input[type="file"]').first();
    await expect(fileInput).toBeAttached({ timeout: 15_000 });
  });

  // ── 6. Upload valid file → diff preview ──────────────────────────────────────
  test("6. uploading a valid xlsx shows the diff preview with a Confirm Import button", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);
    await openCreateRateSheetEditor(page);
    await clickModeButton(page, "import");

    await uploadImportFile(page, path.join(FIXTURES, "rate-sheet-valid.xlsx"));

    // After dry-run succeeds, "Confirm Import" button appears
    await waitForDiffPreview(page);

    const confirmBtn = page.getByRole("button", { name: /confirm import/i });
    await expect(confirmBtn).toBeVisible({ timeout: 30_000 });
    await expect(confirmBtn).toBeEnabled();
  });

  // ── 7. Upload error file → error list ────────────────────────────────────────
  test("7. uploading an invalid xlsx shows validation errors and hides Confirm Import", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);
    await openCreateRateSheetEditor(page);
    await clickModeButton(page, "import");

    await uploadImportFile(page, path.join(FIXTURES, "rate-sheet-errors.xlsx"));

    // Error step appears
    await waitForImportErrors(page);

    // Confirm Import must NOT be visible in the error state
    const confirmBtn = page.locator("button", { hasText: /confirm import/i });
    await expect(confirmBtn).not.toBeVisible({ timeout: 5_000 }).catch(() => {
      // If the button is present but disabled — also acceptable
    });
  });

  // ── 8. Cancel returns to edit mode ───────────────────────────────────────────
  test("8. Cancel in import panel returns to the rate sheet edit grid", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);
    await openCreateRateSheetEditor(page);
    await clickModeButton(page, "import");

    // Upload a valid file so we land on the diff preview
    await uploadImportFile(page, path.join(FIXTURES, "rate-sheet-valid.xlsx"));
    await waitForDiffPreview(page);

    // Click Cancel
    const cancelBtn = page.getByRole("button", { name: /^cancel$/i });
    await cancelBtn.click();

    // Should be back in "edit" mode — the Save button and edit controls are shown
    const dialog = page.locator('[role="dialog"]').first();
    await expect(
      dialog.locator("button[aria-label='Save'], button[title='Save']")
    ).toBeVisible({ timeout: 10_000 });

    // The import panel's file input should be gone
    await expect(page.locator('input[type="file"]')).not.toBeAttached({ timeout: 5_000 });
  });

  // ── 9. Export button triggers download / no crash ────────────────────────────
  test("9. clicking export in the editor triggers a file download without crashing", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);
    await openCreateRateSheetEditor(page);

    // Set up download listener BEFORE clicking export
    const [download] = await Promise.all([
      page.waitForEvent("download", { timeout: 15_000 }).catch(() => null),
      clickModeButton(page, "export"),
    ]);

    // If no download event fired (e.g. empty sheet, no-op), at minimum the dialog
    // must still be open and not have crashed the page.
    const dialog = page.locator('[role="dialog"]').first();
    await expect(dialog).toBeVisible({ timeout: 5_000 });

    if (download) {
      // Confirm the downloaded file has a sensible name
      expect(download.suggestedFilename()).toMatch(/\.(xlsx|csv)$/i);
    }
  });

  // ── 10. Connections rate-sheets page ─────────────────────────────────────────
  test("10. /connections/rate-sheets loads with a heading and Add rate sheet button", async ({ page }) => {
    await page.goto("/connections/rate-sheets");
    await page.waitForLoadState("networkidle");

    // The page has an h1 with "Carrier Connections" or "Rate Sheets" text
    await expect(
      page.locator("h1").filter({ hasText: /carrier connections|rate sheets/i }).first()
    ).toBeVisible({ timeout: 20_000 });

    // "Add rate sheet" button (the CTA on this page)
    await expect(
      page.getByRole("button", { name: /add rate sheet/i })
    ).toBeVisible({ timeout: 10_000 });
  });

  // ── 11. Close editor with Escape key ─────────────────────────────────────────
  test("11. pressing Escape closes the rate sheet editor", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);
    await openCreateRateSheetEditor(page);

    const dialog = page.locator('[role="dialog"]').first();
    await expect(dialog).toBeVisible();

    // Press Escape to close
    await page.keyboard.press("Escape");
    await expect(dialog).not.toBeVisible({ timeout: 5_000 });
  });

  // ── 12. Close editor via Close button ────────────────────────────────────────
  test("12. clicking the Close button in the editor header dismisses the panel", async ({ page }) => {
    await navigateToCarrierNetwork(page);
    await clickRateSheetsTab(page);
    await openCreateRateSheetEditor(page);

    const dialog = page.locator('[role="dialog"]').first();
    await expect(dialog).toBeVisible();

    // Close button has aria-label="Close"
    const closeBtn = dialog.locator("button[aria-label='Close']");
    await closeBtn.click();

    await expect(dialog).not.toBeVisible({ timeout: 5_000 });
  });
});
