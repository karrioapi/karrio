// Regression tests: /api/dev-assets/[...path] joined the URL path onto the app
// directory without checking where it ended up, so `..` segments (or a symlink) could read
// any file the dashboard process can read (development mode only).
// Run with: npm test --workspace @karrio/dashboard  (Node.js built-in test runner)
import assert from "node:assert/strict";
import test, { after, before } from "node:test";
import { mkdirSync, mkdtempSync, realpathSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { GET } from "../src/app/api/dev-assets/[...path]/route.ts";

const SECRET = "TOP-SECRET-OUTSIDE-THE-ASSETS-ROOT";
const OTHER_APP = "OTHER-APP-ASSET";

// <root>/apps/dashboard is the cwd, like the real repo layout the route expects:
//   <root>/packages/app-store/apps/demo/{README.md,assets/...}
const root = realpathSync(mkdtempSync(join(tmpdir(), "dev-assets-")));
const cwd = join(root, "apps", "dashboard");
const appsDir = join(root, "packages", "app-store", "apps");
const outsideDir = join(root, "outside");
const secretFile = join(root, "secret.txt");
const originalCwd = process.cwd();
const originalEnv = process.env.NODE_ENV;

before(() => {
  mkdirSync(cwd, { recursive: true });
  mkdirSync(join(appsDir, "demo", "assets", "img"), { recursive: true });
  mkdirSync(join(appsDir, "other", "assets"), { recursive: true });
  mkdirSync(outsideDir, { recursive: true });
  writeFileSync(secretFile, SECRET);
  writeFileSync(join(outsideDir, "secret.txt"), SECRET);
  writeFileSync(join(appsDir, "other", "assets", "other.txt"), OTHER_APP);
  writeFileSync(join(appsDir, "demo", "README.md"), "# demo");
  writeFileSync(join(appsDir, "demo", "assets", "logo.svg"), "<svg/>");
  writeFileSync(join(appsDir, "demo", "assets", "img", "a.png"), "png");
  symlinkSync(secretFile, join(appsDir, "demo", "assets", "link.txt"));
  symlinkSync(outsideDir, join(appsDir, "demo", "assets", "dirlink"));
  // An app whose assets/ directory itself is a symlink pointing outside the app.
  mkdirSync(join(appsDir, "linked"), { recursive: true });
  symlinkSync(outsideDir, join(appsDir, "linked", "assets"));
  process.chdir(cwd);
  (process.env as any).NODE_ENV = "development";
});

after(() => {
  process.chdir(originalCwd);
  (process.env as any).NODE_ENV = originalEnv;
  rmSync(root, { recursive: true, force: true });
});

async function get(path: string[]) {
  const request = new Request(`http://localhost:3002/api/dev-assets/${path.join("/")}`);
  const response = await GET(request as any, { params: Promise.resolve({ path }) });
  return { response, body: await response.text() };
}

const TRAVERSAL: [string, string[]][] = [
  ["../ segments to a file outside", ["demo", "..", "..", "..", "..", "..", "secret.txt"]],
  ["../ segments from a nested directory", ["demo", "img", "..", "..", "..", "..", "..", "..", "secret.txt"]],
  ["../ inside one decoded segment (%2f)", ["demo", "../../../../../secret.txt"]],
  ["backslash separators", ["demo", "..\\..\\..\\..\\..\\secret.txt"]],
  ["an absolute path", ["demo", secretFile]],
  ["an absolute path to a system file", ["demo", "/etc/hosts"]],
  ["a leading slash segment", ["demo", "", secretFile]],
  ["the app root directory itself escaping to a sibling app", ["demo", "..", "..", "other", "assets", "other.txt"]],
  ["traversal in the app slug", ["..", "..", "..", "..", "secret.txt"]],
  ["a slash inside the app slug", ["demo/../other", "assets", "other.txt"]],
  ["a dot slug", [".", "..", "secret.txt"]],
  ["a NUL byte", ["demo", "logo.svg\0.png"]],
  ["a symlink to a file outside", ["demo", "link.txt"]],
  ["a symlink to a directory outside", ["demo", "dirlink", "secret.txt"]],
  ["an assets/ directory that is itself a symlink outside the app", ["linked", "secret.txt"]],
];

for (const [label, path] of TRAVERSAL) {
  test(`dev-assets: refuses ${label}`, async () => {
    const { response, body } = await get(path);
    assert.ok([400, 404].includes(response.status), `status ${response.status}`);
    assert.equal(body.includes(SECRET), false, "file content must not be served");
    assert.equal(body.includes(OTHER_APP), false, "another app's files must not be served");
  });
}

test("dev-assets: serves an asset from the assets directory", async () => {
  const { response, body } = await get(["demo", "logo.svg"]);
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("content-type"), "image/svg+xml");
  assert.equal(body, "<svg/>");
});

test("dev-assets: serves a nested asset", async () => {
  const { response } = await get(["demo", "img", "a.png"]);
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("content-type"), "image/png");
});

test("dev-assets: still serves README.md from the app root", async () => {
  const { response, body } = await get(["demo", "README.md"]);
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("content-type"), "text/markdown");
  assert.equal(body, "# demo");
});

test("dev-assets: a path that stays inside but normalises (./ and a/..) still works", async () => {
  const { response } = await get(["demo", "img", "..", "logo.svg"]);
  assert.equal(response.status, 200);
});

test("dev-assets: unknown asset is 404, a too short path is 400", async () => {
  assert.equal((await get(["demo", "missing.svg"])).response.status, 404);
  assert.equal((await get(["demo"])).response.status, 400);
});

test("dev-assets: is disabled outside development", async () => {
  (process.env as any).NODE_ENV = "production";
  try {
    assert.equal((await get(["demo", "logo.svg"])).response.status, 404);
  } finally {
    (process.env as any).NODE_ENV = "development";
  }
});
