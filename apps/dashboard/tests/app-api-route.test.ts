// Regression tests: /api/apps/[appId]/[...paths] built the module it imports from
// the URL segments (`.../apps/${appId}/api/${paths}/route`) without checking them, so
// `..` segments made it import (and run the handler of) any `route.ts` on the server.
// Run with: npm test --workspace @karrio/dashboard  (Node.js built-in test runner)
import assert from "node:assert/strict";
import test, { after, before } from "node:test";
import { mkdirSync, mkdtempSync, realpathSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { GET, POST } from "../../../packages/app-store/api/api-route.ts";

// A fake checkout the route resolves from process.cwd():
//   <root>/packages/app-store/apps/shopify/api/...   registered app routes
//   <root>/evil/route.ts                             a route.ts that must stay unreachable
const root = realpathSync(mkdtempSync(join(tmpdir(), "app-api-route-")));
const originalCwd = process.cwd();
const realConsole = { log: console.log, error: console.error };

function writeRoute(dir: string, source: string) {
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "route.ts"), source);
}

before(() => {
  const api = join(root, "packages", "app-store", "apps", "shopify", "api");
  writeRoute(join(api, "test-connection"), `export async function POST() { return new Response("legit post"); }`);
  writeRoute(join(api, "oauth", "check-support"), `export async function GET() { return new Response("legit get"); }`);
  writeRoute(
    join(root, "evil"),
    `(globalThis as any).__imported = ((globalThis as any).__imported ?? []).concat(["evil"]);
export async function GET() { return new Response("EVIL HANDLER RAN"); }
export async function POST() { return new Response("EVIL HANDLER RAN"); }`,
  );
  process.chdir(root);
  console.log = () => {};
  console.error = () => {};
});

after(() => {
  process.chdir(originalCwd);
  console.log = realConsole.log;
  console.error = realConsole.error;
  rmSync(root, { recursive: true, force: true });
});

async function call(handler: typeof GET, appId: string, paths: string[]) {
  (globalThis as any).__imported = [];
  const request = Object.assign(new Request("http://localhost:3002/api/apps/x"), {
    nextUrl: new URL("http://localhost:3002/api/apps/x"),
  });
  const response = await handler(request as any, { params: Promise.resolve({ appId, paths }) });
  return { response, body: await response.text(), imported: (globalThis as any).__imported as string[] };
}

test("app routes: a registered app route still works (single and nested path)", async () => {
  const post = await call(POST, "shopify", ["test-connection"]);
  assert.equal(post.response.status, 200);
  assert.equal(post.body, "legit post");

  const get = await call(GET, "shopify", ["oauth", "check-support"]);
  assert.equal(get.response.status, 200);
  assert.equal(get.body, "legit get");
});

test("app routes: unknown routes are 404 and unsupported methods 405", async () => {
  assert.equal((await call(GET, "shopify", ["nothing-here"])).response.status, 404);
  assert.equal((await call(GET, "unknown-app", ["x"])).response.status, 404);
  assert.equal((await call(GET, "shopify", ["test-connection"])).response.status, 405);
});

// Every way of climbing out of packages/app-store/apps/<app>/api/ with 1..8 levels.
const CLIMBS = Array.from({ length: 8 }, (_, i) => i + 1);
const ATTACKS: [string, (up: string[]) => [string, string[]]][] = [
  ["appId '..' and separate '..' segments", (up) => ["..", [...up, "evil"]]],
  ["registered appId and separate '..' segments", (up) => ["shopify", [...up, "evil"]]],
  ["registered appId and one segment containing slashes", (up) => ["shopify", [`${up.join("/")}/evil`]]],
  ["slashes inside the appId", (up) => [`shopify/${up.join("/")}/evil`, ["x"]]],
  ["backslash separators", (up) => ["shopify", [`${up.join("\\")}\\evil`]]],
];

for (const [label, build] of ATTACKS) {
  test(`app routes: refuses ${label} at every depth`, async () => {
    for (const depth of CLIMBS) {
      const [appId, paths] = build(Array(depth).fill(".."));
      for (const handler of [GET, POST]) {
        const { response, body, imported } = await call(handler, appId, paths);
        const where = `${appId} / ${JSON.stringify(paths)}`;
        assert.equal(response.status, 404, where);
        assert.equal(body.includes("EVIL"), false, where);
        assert.deepEqual(imported, [], `module outside the app directory was imported: ${where}`);
      }
    }
  });
}

const BAD_SEGMENTS: [string, string, string[]][] = [
  ["a dot in a path segment", "shopify", ["test.connection"]],
  ["an uppercase path segment", "shopify", ["Test-Connection"]],
  ["an absolute-looking path segment", "shopify", [join(root, "evil")]],
  ["an empty path segment", "shopify", ["", "test-connection"]],
  ["a NUL byte", "shopify", ["test-connection\0"]],
  ["a percent-encoded dot segment left undecoded", "shopify", ["%2e%2e", "%2e%2e", "evil"]],
  ["an uppercase appId", "Shopify", ["test-connection"]],
  ["a dotted appId", "karrio.app.shopify", ["test-connection"]],
  ["an empty appId", "", ["test-connection"]],
  ["no path at all", "shopify", []],
];

for (const [label, appId, paths] of BAD_SEGMENTS) {
  test(`app routes: refuses ${label}`, async () => {
    const { response, imported } = await call(POST, appId, paths);
    assert.equal(response.status, 404);
    assert.deepEqual(imported, []);
  });
}
