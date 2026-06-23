// verify-fixes.mjs — objective DOM verification against running studio + sandbox.
import { chromium } from "playwright";
const S = process.env.KARRIO_STUDIO_URL || "http://localhost:3003";
const b = await chromium.launch();
async function login(ctx) {
  const p = await ctx.newPage();
  await p.goto(S + "/login"); await p.waitForLoadState("networkidle");
  await p.getByTestId("login-email").fill("admin@example.com");
  await p.locator("#password").fill("demo");
  await p.getByTestId("login-submit").click();
  await p.waitForURL(/home$/, { timeout: 30000 });
  return p;
}
{
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  const p = await login(ctx);
  await p.goto(S + "/shipments"); await p.waitForLoadState("networkidle");
  const tb = await p.getByTestId("topbar").boundingBox();
  console.log(`MOBILE h=${Math.round(tb.height)} w=${Math.round(tb.width)} hamburger=${await p.getByTestId("toggle-sidebar").isVisible()} workbench_hidden=${await p.getByTestId("workbench-trigger").isHidden()}`);
  await ctx.close();
}
{
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await login(ctx);
  await p.goto(S + "/shipments"); await p.waitForLoadState("networkidle");
  const rows = await p.locator('[data-testid^="shipment-row-"]').count();
  const badges = await p.locator('.carrier-logo').allInnerTexts();
  console.log(`TABLE rows=${rows} badges=${JSON.stringify(badges)}`);
  await p.locator('[data-testid^="shipment-row-"]').first().click();
  const t = await p.getByTestId("shipment-sheet-body").innerText();
  const has = (s) => t.includes(s);
  console.log(`SHEET from=${has("Brooklyn")} to=${/Romero|Doe|Strauss|Wright/.test(t)} parcels=${has("Parcels")} packaging=${has("BOX")} charges=${has("Base charge")} fuel=${has("Fuel surcharge")}`);
  await ctx.close();
}
await b.close();
