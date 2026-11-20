// Regression tests for reflected XSS in /api/images/[name].
// Run with: npm test --workspace @karrio/dashboard  (Node.js built-in test runner, no extra dependencies)
import assert from "node:assert/strict";
import test from "node:test";
import { GET as GET_ROOT } from "../src/app/api/images/[name]/route.ts";
import { readFileSync } from "node:fs";

type Handler = typeof GET_ROOT;

async function call(handler: Handler, name: string, query = "") {
  const url = `http://localhost:3002/api/images/${encodeURIComponent(name)}${query}`;
  // emulate NextRequest (a Request that also exposes nextUrl)
  const request = Object.assign(new Request(url), { nextUrl: new URL(url) });
  const response = await handler(request as any, { params: Promise.resolve({ name }) });
  return { response, body: await response.text() };
}

const HANDLERS: [string, Handler][] = [["api/images", GET_ROOT]];

test("(base)/[domain]/api/images only re-exports the hardened handler", () => {
  // Node cannot resolve the extension-less re-export, so check the source instead.
  const source = readFileSync(
    new URL("../src/app/(base)/[domain]/api/images/[name]/route.ts", import.meta.url),
    "utf8",
  );
  assert.equal(
    source.trim(),
    'export { GET } from "../../../../../api/images/[name]/route";',
  );
});

const NAME_PAYLOADS = [
  "<script>alert(1)</script>_logo.svg",
  '"><svg onload=alert(1)>_icon.svg',
  "x</text><script>alert(document.domain)</script><text>_logo.svg",
  "<img src=x onerror=alert(1)>",
  "ups_logo.svg<script>alert(1)</script>",
  "../../etc/passwd_logo.svg",
  "ups logo.svg",
  "ups_logo.html",
  "ups",
  "",
  `${"a".repeat(200)}_logo.svg`,
];

const COLOR_PAYLOADS = [
  '"/><script>alert(1)</script>',
  '#fff" onload="alert(1)',
  "red;}</style><script>alert(1)</script>",
  "url(javascript:alert(1))",
  "#fff'/><script>alert(1)</script>",
  "%E0%A4%A", // malformed percent-encoding
];

for (const [label, GET] of HANDLERS) {
  test(`${label}: renders logo and icon for a legitimate carrier name`, async () => {
    const logo = await call(GET, "dhl_express_logo.svg");
    assert.equal(logo.response.status, 200);
    assert.match(logo.response.headers.get("content-type") ?? "", /^image\/svg\+xml/);
    assert.match(logo.body, /viewBox="0 0 125 25"/);
    assert.match(logo.body, />\s*DHL_EXPRE\.\s*</); // 10+ chars are shortened
    assert.match(logo.body, /fill:#7e51e1;/);
    assert.match(logo.body, /fill="#ddd"/);

    const icon = await call(GET, "dhl_express_icon.svg");
    assert.equal(icon.response.status, 200);
    assert.match(icon.body, /viewBox="0 0 512 512"/);
    assert.match(icon.body, />\s*de\s*</);
  });

  test(`${label}: honours valid colours (including the UI's double encoding)`, async () => {
    const { response, body } = await call(
      GET,
      "ups_logo.svg",
      `?text_color=${encodeURIComponent(encodeURIComponent("#112233"))}&background=rgb(1%2C2%2C3)`,
    );
    assert.equal(response.status, 200);
    assert.match(body, /fill="#112233"/);
    assert.match(body, /fill:rgb\(1,2,3\);/);
  });

  test(`${label}: sends nosniff and a script-blocking CSP`, async () => {
    const { response } = await call(GET, "ups_logo.svg");
    assert.equal(response.headers.get("x-content-type-options"), "nosniff");
    const csp = response.headers.get("content-security-policy") ?? "";
    assert.match(csp, /default-src 'none'/);
    assert.match(csp, /\bsandbox\b/);
  });

  for (const payload of NAME_PAYLOADS) {
    test(`${label}: rejects name ${JSON.stringify(payload.slice(0, 40))}`, async () => {
      const { response, body } = await call(GET, payload);
      assert.equal(response.status, 404);
      assert.doesNotMatch(response.headers.get("content-type") ?? "", /svg|html|xml/);
      assert.equal(body.includes("<"), false);
      assert.equal(body.includes(payload) && payload !== "", false);
      assert.equal(response.headers.get("x-content-type-options"), "nosniff");
    });
  }

  for (const payload of COLOR_PAYLOADS) {
    test(`${label}: ignores colour ${JSON.stringify(payload.slice(0, 40))}`, async () => {
      for (const key of ["text_color", "background"]) {
        const { response, body } = await call(GET, "ups_logo.svg", `?${key}=${encodeURIComponent(payload)}`);
        assert.equal(response.status, 200);
        assert.doesNotMatch(body, /<script|onload|onerror|javascript:|alert\(/i);
        assert.match(body, /fill="#ddd"/);
        assert.match(body, /fill:#7e51e1;/);
      }
    });
  }
}
