import { type Page, expect } from "@playwright/test";

// ─── Navigation ───────────────────────────────────────────────────────────────

/**
 * Navigate to the Carrier Network admin page (/admin/carriers).
 * Waits until the page heading is visible.
 */
export async function navigateToCarrierNetwork(page: Page): Promise<void> {
  await page.goto("/admin/carriers");
  await page.waitForLoadState("networkidle");
  // The page renders either an h1 or h2 with "Carrier" in the title
  await expect(
    page.locator("h1, h2").filter({ hasText: /carrier/i }).first()
  ).toBeVisible({ timeout: 20_000 });
}

/**
 * Click the "Rate Sheets" tab on the Carrier Network page.
 * After clicking, waits for the Rate Sheets sub-section to appear.
 */
export async function clickRateSheetsTab(page: Page): Promise<void> {
  const tab = page.getByRole("button", { name: /rate sheets/i });
  await tab.waitFor({ timeout: 10_000 });
  await tab.click();
  // Wait for the Rate Sheets heading or empty state to appear
  await expect(
    page.locator("h2, h3, [data-testid]").filter({ hasText: /rate sheets/i }).first()
  ).toBeVisible({ timeout: 15_000 });
}

/**
 * Click "Create Rate Sheet" to open the rate sheet editor panel.
 * Waits for the Sheet/dialog to appear.
 */
export async function openCreateRateSheetEditor(page: Page): Promise<void> {
  const btn = page.getByRole("button", { name: /create rate sheet/i });
  await btn.waitFor({ timeout: 10_000 });
  await btn.click();
  // The editor opens as a shadcn Sheet (role="dialog" or aside)
  await expect(page.locator('[role="dialog"]').first()).toBeVisible({
    timeout: 15_000,
  });
}

/**
 * Open the editor for an existing rate sheet by name.
 * Finds the row/card with the given name, opens its dropdown, and clicks "Edit Rate Sheet".
 */
export async function openExistingRateSheetEditor(
  page: Page,
  name: string
): Promise<void> {
  // Find the row or card that contains the rate sheet name
  const row = page.locator("tr, [data-testid], .border-l-4, li").filter({
    hasText: name,
  }).first();
  await row.waitFor({ timeout: 10_000 });

  // Click the MoreHorizontal / three-dot dropdown trigger inside the row
  const menuBtn = row.getByRole("button").last();
  await menuBtn.click();

  // Click "Edit Rate Sheet" in the dropdown
  const editItem = page.getByRole("menuitem", { name: /edit rate sheet/i });
  await editItem.waitFor({ timeout: 5_000 });
  await editItem.click();

  // Wait for the editor panel
  await expect(page.locator('[role="dialog"]').first()).toBeVisible({
    timeout: 15_000,
  });
}

// ─── Editor interactions ──────────────────────────────────────────────────────

/**
 * Click one of the mode toggle buttons ("edit" | "import" | "export") in the
 * rate sheet editor header.
 *
 * Note: For "export" the click triggers a download immediately (no mode switch).
 */
export async function clickModeButton(
  page: Page,
  mode: "edit" | "import" | "export"
): Promise<void> {
  // The buttons are plain <button> elements with text "edit", "import", or "export"
  // and have `title` attributes describing their purpose.
  const btn = page.locator('[role="dialog"]').first().locator("button", {
    hasText: new RegExp(`^${mode}$`, "i"),
  });
  await btn.waitFor({ timeout: 10_000 });
  await btn.click();
}

/**
 * Upload a file to the rate sheet import panel.
 *
 * The file input may be visually hidden; we use setInputFiles() directly.
 */
export async function uploadImportFile(
  page: Page,
  filePath: string
): Promise<void> {
  const fileInput = page.locator('input[type="file"]').first();
  await fileInput.setInputFiles(filePath);
}

/**
 * Wait for the diff preview table to appear after a successful dry-run import.
 * The preview step shows a table with change rows and a "Confirm Import" button.
 */
export async function waitForDiffPreview(page: Page): Promise<void> {
  await expect(
    page.getByRole("button", { name: /confirm import/i })
  ).toBeVisible({ timeout: 30_000 });
}

/**
 * Wait for the validation error list to appear after a failed dry-run import.
 */
export async function waitForImportErrors(page: Page): Promise<void> {
  // The errors step renders a list of error messages
  await expect(
    page.locator("text=/validation error|error|invalid/i").first()
  ).toBeVisible({ timeout: 30_000 });
}
