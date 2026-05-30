// capture.mjs — screenshot key Studio screens (dark + light + mobile) against
// the seeded sandbox. Run from packages/e2e so `playwright` resolves.
import { chromium } from "playwright";

const STUDIO = process.env.KARRIO_STUDIO_URL || "http://localhost:3003";
const OUT = process.env.OUT || "../../apps/studio/docs/screenshots";
const EMAIL = "admin@example.com";
const PASSWORD = "demo";

const shots = [
  { route: "home", name: "01-home" },
  { route: "shipments", name: "02-shipments" },
  { route: "trackers", name: "03-trackers" },
  { route: "orders", name: "04-orders" },
  { route: "connections", name: "05-connections" },
  { route: "mcp", name: "06-mcp" },
  { route: "editor", name: "07-editor" },
  { route: "plugins", name: "08-plugins" },
  { route: "admin", name: "09-admin" },
  { route: "ratesheets", name: "10-ratesheets" },
];

const browser = await chromium.launch();

async function login(ctx, theme) {
  const page = await ctx.newPage();
  await page.goto(`${STUDIO}/login`);
  await page.waitForLoadState("networkidle");
  await page.getByTestId("login-email").fill(EMAIL);
  await page.locator("#password").fill(PASSWORD);
  await page.getByTestId("login-submit").click();
  await page.waitForURL(/\/home$/, { timeout: 30000 });
  if (theme === "light") {
    await page.getByTestId("theme-toggle").click();
    await page.waitForTimeout(300);
  }
  return page;
}

// Dark set (full).
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  const page = await login(ctx, "dark");
  for (const s of shots) {
    await page.goto(`${STUDIO}/${s.route}`);
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(700);
    await page.screenshot({ path: `${OUT}/${s.name}.png` });
    console.log("shot", s.name);
  }
  await page.goto(`${STUDIO}/shipments`);
  await page.waitForLoadState("networkidle");
  const row = page.locator('[data-testid^="shipment-row-"]').first();
  if (await row.count()) {
    await row.click();
    await page.waitForTimeout(600);
    await page.screenshot({ path: `${OUT}/11-shipment-sheet.png` });
    console.log("shot 11-shipment-sheet");
  }
  await ctx.close();
}

// Light set (representative screens).
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  const page = await login(ctx, "light");
  for (const s of [shots[0], shots[1], shots[5]]) {
    await page.goto(`${STUDIO}/${s.route}`);
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(700);
    await page.screenshot({ path: `${OUT}/light-${s.name}.png` });
    console.log("shot light", s.name);
  }
  await ctx.close();
}

// Login (no auth).
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto(`${STUDIO}/login`);
  await page.waitForLoadState("networkidle");
  await page.screenshot({ path: `${OUT}/00-login.png` });
  console.log("shot 00-login");
  await ctx.close();
}

// Mobile (off-canvas nav).
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const page = await login(ctx, "dark");
  await page.goto(`${STUDIO}/shipments`);
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(700);
  await page.screenshot({ path: `${OUT}/12-mobile-shipments.png` });
  console.log("shot 12-mobile-shipments");
  await ctx.close();
}

await browser.close();
console.log("done");
