// Regression tests: the Google Places proxy routes logged the Google API key and
// were callable without a session.
// Run with: npm test --workspace @karrio/dashboard  (Node.js built-in test runner)
import assert from "node:assert/strict";
import test, { afterEach, beforeEach } from "node:test";
import axios from "axios";
import { GET as AUTOCOMPLETE } from "../src/app/api/places/autocomplete/route.ts";
import { GET as DETAILS } from "../src/app/api/places/details/route.ts";
import { configureAutocomplete } from "./support/karrio-lib-stub.mjs";
import { setSession } from "./support/karrio-core-auth-stub.mjs";

const KEY = "AIzaSy-test-key-must-never-be-logged";
const realGet = axios.get;
const realConsole = { ...console };
let output: string[] = [];
let upstream: { url: string; params: Record<string, string> }[] = [];

beforeEach(() => {
  output = [];
  upstream = [];
  for (const level of ["log", "info", "warn", "error", "debug"] as const) {
    (console as any)[level] = (...args: unknown[]) =>
      output.push(args.map((a) => (typeof a === "string" ? a : JSON.stringify(a))).join(" "));
  }
  (axios as any).get = async (url: string, config: { params: Record<string, string> }) => {
    upstream.push({ url, params: config.params });
    return { data: { status: "OK", predictions: [], result: {} } };
  };
  configureAutocomplete("google", KEY);
  setSession({ accessToken: "jwt", orgId: null, testMode: false });
});

afterEach(() => {
  Object.assign(console, realConsole);
  (axios as any).get = realGet;
  configureAutocomplete(undefined, undefined);
  setSession(null);
});

const ROUTES: [string, typeof AUTOCOMPLETE, string][] = [
  ["autocomplete", AUTOCOMPLETE, "input=12%20main&country=US&sessiontoken=tok-1"],
  ["details", DETAILS, "place_id=abc123&sessiontoken=tok-1"],
];

function call(handler: typeof AUTOCOMPLETE, query: string) {
  const url = `http://localhost:3002/api/places/x?${query}`;
  return handler(Object.assign(new Request(url), { nextUrl: new URL(url) }) as any);
}

for (const [name, handler, query] of ROUTES) {
  test(`places/${name}: never writes the API key to the log`, async () => {
    const response = await call(handler, query);
    assert.equal(response.status, 200);
    assert.equal(upstream.length, 1);
    assert.equal(upstream[0].params.key, KEY, "the key must still be sent to Google");
    assert.equal(output.some((line) => line.includes(KEY)), false, output.join("\n"));
  });

  test(`places/${name}: a failing upstream call does not leak the key either`, async () => {
    (axios as any).get = async () => {
      throw new Error("Request failed with status code 403");
    };
    const response = await call(handler, query);
    assert.equal(response.status, 500);
    assert.equal(JSON.stringify(await response.json()).includes(KEY), false);
    assert.equal(output.some((line) => line.includes(KEY)), false);
  });

  test(`places/${name}: still answers 400 when the key is not configured`, async () => {
    configureAutocomplete("canadapost", KEY);
    const response = await call(handler, query);
    assert.equal(response.status, 400);
    assert.deepEqual(upstream, []);
    assert.equal(output.some((line) => line.includes(KEY)), false);
  });
}

// --- the proxies spend the deployment's Google quota, so they need a signed-in user

const SESSIONS: [string, unknown][] = [
  ["no session", null],
  ["an expired session (refresh error)", { error: "RefreshAccessTokenError" }],
];

for (const [name, handler, query] of ROUTES) {
  for (const [label, session] of SESSIONS) {
    test(`places/${name}: refuses ${label} without calling Google`, async () => {
      setSession(session);
      const response = await call(handler, query);
      assert.equal(response.status, 401);
      assert.deepEqual(upstream, []);
      assert.equal(JSON.stringify(await response.json()).includes(KEY), false);
    });
  }
}
