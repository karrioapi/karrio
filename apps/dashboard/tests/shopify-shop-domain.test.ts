// Regression tests: the Shopify test-connection / OAuth routes only checked
// `shop_domain.endsWith(".myshopify.com")` and then fetched `https://${shop_domain}/...`,
// so a value such as `evil.com#x.myshopify.com` made the server (and the access token it
// was given) call an arbitrary host.
// Run with: npm test --workspace @karrio/dashboard  (Node.js built-in test runner)
import assert from "node:assert/strict";
import test, { afterEach, beforeEach } from "node:test";
import { POST as POST_DASHBOARD } from "../src/app/api/apps/shopify/test-connection/route.ts";
import { POST as POST_APP_STORE } from "../../../packages/app-store/apps/shopify/api/test-connection/route.ts";
import { GET as GET_AUTHORIZE } from "../../../packages/app-store/apps/shopify/api/oauth/authorize/route.ts";

const realFetch = globalThis.fetch;
const realConsole = { log: console.log, error: console.error };
let fetchCalls: { url: string; init?: RequestInit }[] = [];

beforeEach(() => {
  fetchCalls = [];
  console.log = () => {};
  console.error = () => {};
  globalThis.fetch = (async (input: any, init?: RequestInit) => {
    fetchCalls.push({ url: String(input), init });
    return new Response(
      JSON.stringify({ shop: { name: "My Shop", domain: "shop.example.com" } }),
      { status: 200, headers: { "content-type": "application/json" } },
    );
  }) as typeof fetch;
});

afterEach(() => {
  globalThis.fetch = realFetch;
  console.log = realConsole.log;
  console.error = realConsole.error;
});

const BAD_DOMAINS: [string, unknown][] = [
  ["fragment host confusion", "evil.com#x.myshopify.com"],
  ["query host confusion", "evil.com?x.myshopify.com"],
  ["path host confusion", "evil.com/x.myshopify.com"],
  ["backslash host confusion", "evil.com\\.myshopify.com"],
  ["userinfo", "evil.com@shop.myshopify.com"],
  ["userinfo with password", "user:pass@shop.myshopify.com"],
  ["port", "shop.myshopify.com:8443"],
  ["default https port", "shop.myshopify.com:443"],
  ["http scheme", "http://shop.myshopify.com"],
  ["https scheme", "https://shop.myshopify.com"],
  ["uppercase", "Shop.MyShopify.com"],
  ["uppercase label", "SHOP.myshopify.com"],
  ["trailing dot", "shop.myshopify.com."],
  ["path suffix", "shop.myshopify.com/admin"],
  ["subdomain of a shop", "a.shop.myshopify.com"],
  ["empty label", ".myshopify.com"],
  ["bare suffix", "myshopify.com"],
  ["leading hyphen", "-shop.myshopify.com"],
  ["lookalike suffix", "shop.notmyshopify.com"],
  ["suffix only as a label", "shop.myshopify.com.evil.com"],
  ["internal address", "127.0.0.1"],
  ["internal address with the suffix as a path", "127.0.0.1/.myshopify.com"],
  ["ipv6", "[::1]"],
  ["whitespace", "shop.myshopify.com evil"],
  ["trailing newline", "shop.myshopify.com\n"],
  ["embedded tab", "shop.my\tshopify.com"],
  ["percent encoded slash", "evil.com%2f.myshopify.com"],
  ["fullwidth lookalike", "ｓhop.myshopify.com"],
  ["array", ["shop.myshopify.com"]],
  ["object", { endsWith: () => true }],
  ["number", 1234],
];

const JSON_ROUTES: [string, typeof POST_DASHBOARD, Record<string, unknown>][] = [
  ["dashboard test-connection", POST_DASHBOARD, {}],
  ["app-store test-connection", POST_APP_STORE, { installation_id: "inst_1" }],
];

async function postJson(handler: typeof POST_DASHBOARD, body: unknown) {
  const request = new Request("http://localhost:3002/api/apps/shopify/test-connection", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  const response = await handler(request as any);
  return { response, body: (await response.json()) as any };
}

for (const [route, handler, extra] of JSON_ROUTES) {
  for (const [label, domain] of BAD_DOMAINS) {
    test(`${route}: refuses ${label} (${JSON.stringify(domain)}) without making a request`, async () => {
      const { response } = await postJson(handler, {
        ...extra,
        shop_domain: domain,
        access_token: "shpat_secret",
      });
      assert.equal(response.status, 400);
      assert.deepEqual(fetchCalls, [], "no outbound request may be made");
    });
  }

  test(`${route}: still tests a legitimate shop`, async () => {
    const { response, body } = await postJson(handler, {
      ...extra,
      shop_domain: "my-shop-1.myshopify.com",
      access_token: "shpat_secret",
    });
    assert.equal(response.status, 200);
    assert.equal(body.success, true);
    assert.ok(fetchCalls.length >= 1);
    for (const call of fetchCalls) {
      const url = new URL(call.url);
      assert.equal(url.protocol, "https:");
      assert.equal(url.host, "my-shop-1.myshopify.com");
      assert.equal((call.init?.headers as any)["X-Shopify-Access-Token"], "shpat_secret");
      // a redirect must never carry the token to another host
      assert.equal(call.init?.redirect, "manual");
    }
  });
}

test("dashboard test-connection: still reports missing parameters", async () => {
  const { response } = await postJson(POST_DASHBOARD, { shop_domain: "shop.myshopify.com" });
  assert.equal(response.status, 400);
  assert.deepEqual(fetchCalls, []);
});

// --- OAuth authorize: same check, builds a redirect to https://${shop}/admin/oauth/authorize

async function authorize(shop: string) {
  const url = `http://localhost:3002/api/apps/shopify/oauth/authorize?installation_id=inst_1&shop=${encodeURIComponent(shop)}`;
  return GET_AUTHORIZE(Object.assign(new Request(url), { nextUrl: new URL(url) }) as any);
}

for (const [label, domain] of BAD_DOMAINS) {
  if (typeof domain !== "string") continue;
  test(`oauth authorize: refuses ${label} (${JSON.stringify(domain)})`, async () => {
    process.env.SHOPIFY_APP_KEY = "client_id";
    process.env.NEXT_PUBLIC_APP_URL = "http://localhost:3002";
    const response = await authorize(domain);
    assert.equal(response.status, 400);
    assert.equal(response.headers.get("location"), null);
  });
}

test("oauth authorize: redirects a legitimate shop to Shopify", async () => {
  process.env.SHOPIFY_APP_KEY = "client_id";
  process.env.NEXT_PUBLIC_APP_URL = "http://localhost:3002";
  const response = await authorize("my-shop-1.myshopify.com");
  const location = new URL(response.headers.get("location") ?? "");
  assert.equal(location.origin, "https://my-shop-1.myshopify.com");
  assert.equal(location.pathname, "/admin/oauth/authorize");
});
