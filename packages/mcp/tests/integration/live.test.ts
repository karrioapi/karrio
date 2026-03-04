/**
 * Live integration tests for the Karrio MCP server.
 *
 * These tests run against a real Karrio server and are skipped automatically
 * in CI when the environment variables are not set.
 *
 * To run locally:
 *   KARRIO_API_URL=http://127.0.0.1:5002 KARRIO_API_KEY=<key> npm test
 */
import { describe, it, expect, beforeAll } from "vitest";
import { KarrioClient } from "../../src/client.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { createServer } from "../../src/server.js";

const LIVE =
  process.env.KARRIO_API_URL && process.env.KARRIO_API_KEY
    ? true
    : false;

describe.skipIf(!LIVE)("Live MCP integration", () => {
  let client: KarrioClient;
  let server: McpServer;

  beforeAll(() => {
    client = new KarrioClient({
      apiUrl: process.env.KARRIO_API_URL!,
      apiKey: process.env.KARRIO_API_KEY!,
    });
    server = createServer({
      apiUrl: process.env.KARRIO_API_URL!,
      apiKey: process.env.KARRIO_API_KEY!,
    });
  });

  // ── list_carrier_connections ────────────────────────────────────────
  it("list_carrier_connections — returns connected carriers", async () => {
    const response = await client.listConnections({ limit: "10", offset: "0" });

    expect(response).toBeDefined();
    expect(typeof response.count).toBe("number");
    expect(Array.isArray(response.results)).toBe(true);

    // We created DHL + UPS in setup, so at least 2 should exist
    expect(response.count).toBeGreaterThanOrEqual(2);

    const first = response.results[0];
    expect(first).toHaveProperty("id");
    expect(first).toHaveProperty("carrier_name");
    expect(first).toHaveProperty("carrier_id");
  });

  // ── list_shipments ──────────────────────────────────────────────────
  it("list_shipments — returns paginated shipment list", async () => {
    const response = await client.listShipments({ limit: "10", offset: "0" });

    expect(response).toBeDefined();
    expect(typeof response.count).toBe("number");
    expect(Array.isArray(response.results)).toBe(true);
  });

  // ── list_trackers ───────────────────────────────────────────────────
  it("list_trackers — returns paginated tracker list", async () => {
    const response = await client.listTrackers({ limit: "10", offset: "0" });

    expect(response).toBeDefined();
    expect(typeof response.count).toBe("number");
    expect(Array.isArray(response.results)).toBe(true);
  });

  // ── list_api_logs ───────────────────────────────────────────────────
  it("list_api_logs — returns API logs via GraphQL", async () => {
    const response = await client.listLogs();

    expect(response).toBeDefined();
    expect(response).toHaveProperty("edges");
    expect(response).toHaveProperty("page_info");
    expect(Array.isArray(response.edges)).toBe(true);
    expect(typeof response.page_info.count).toBe("number");

    // We've made requests to set up carrier connections, so count > 0
    expect(response.page_info.count).toBeGreaterThan(0);

    if (response.edges.length > 0) {
      const node = response.edges[0].node;
      expect(node).toHaveProperty("id");
      expect(node).toHaveProperty("path");
      expect(node).toHaveProperty("method");
      expect(node).toHaveProperty("status_code");
      expect(node).toHaveProperty("requested_at");
    }
  });

  // ── list_tracing_records ────────────────────────────────────────────
  it("list_tracing_records — returns carrier tracing records", async () => {
    const response = await client.listTracingRecords();

    expect(response).toBeDefined();
    expect(response).toHaveProperty("edges");
    expect(response).toHaveProperty("page_info");
    expect(Array.isArray(response.edges)).toBe(true);
    expect(typeof response.page_info.count).toBe("number");
  });

  // ── get_api_log ─────────────────────────────────────────────────────
  it("get_api_log — fetches a specific log by ID", async () => {
    // First get the ID of a real log
    const logs = await client.listLogs();
    expect(logs.edges.length).toBeGreaterThan(0);

    const logId: number = logs.edges[0].node.id;
    const log = await client.getLog(logId);

    expect(log).toBeDefined();
    expect(log.id).toBe(logId);
    expect(log).toHaveProperty("path");
    expect(log).toHaveProperty("method");
    expect(log).toHaveProperty("status_code");
    expect(log).toHaveProperty("requested_at");
    expect(Array.isArray(log.records)).toBe(true);
  });

  // ── list_carriers (catalog) ─────────────────────────────────────────
  it("list_carriers — returns carrier catalog", async () => {
    const response = await client.listCarriers({ limit: "10", offset: "0" });

    expect(response).toBeDefined();
    // carrier catalog can be array or paginated object
    const items = response.results ?? response ?? [];
    expect(Array.isArray(items)).toBe(true);
    expect(items.length).toBeGreaterThan(0);
  });

  // ── error handling ──────────────────────────────────────────────────
  it("bad API key returns an auth error (not a crash)", async () => {
    const badClient = new KarrioClient({
      apiUrl: process.env.KARRIO_API_URL!,
      apiKey: "bad_key_00000000000000000000000000000000",
    });

    await expect(
      badClient.listShipments({ limit: "1" }),
    ).rejects.toThrow(/Karrio API error (401|403)/);
  });

  // ── server creation ─────────────────────────────────────────────────
  it("createServer returns a valid McpServer instance", () => {
    expect(server).toBeDefined();
    // McpServer is registered with tools — it has a _registeredTools or similar
    // We just assert it's an object with expected shape
    expect(typeof server).toBe("object");
  });
});
