import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../../src/client.js";
import { registerLogTools } from "../../src/tools/logs.js";

describe("log tools", () => {
  let client: KarrioClient;
  let originalFetch: typeof global.fetch;

  beforeEach(() => {
    originalFetch = global.fetch;
    client = new KarrioClient({
      apiUrl: "https://api.karrio.io",
      apiKey: "test_key",
    });
  });

  afterEach(() => {
    global.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  describe("registration", () => {
    it("registers all three tools without errors", () => {
      const server = new McpServer({ name: "test", version: "1.0.0" });
      const result = registerLogTools(server, client);
      expect(result).toBeUndefined();
    });

    it("cannot register log tools twice (tool names are unique)", () => {
      const server = new McpServer({ name: "test", version: "1.0.0" });
      registerLogTools(server, client);
      expect(() => registerLogTools(server, client)).toThrow();
    });
  });

  describe("list_api_logs", () => {
    it("returns logs on success", async () => {
      const mockGraphQLResponse = {
        data: {
          logs: {
            page_info: { count: 2 },
            edges: [
              {
                node: {
                  id: 1,
                  path: "/v1/shipments",
                  method: "POST",
                  status_code: 200,
                  response_ms: 150,
                  requested_at: "2026-03-01T10:00:00Z",
                  remote_addr: "127.0.0.1",
                  response: '{"id": "shp_1"}',
                  records: [],
                },
              },
              {
                node: {
                  id: 2,
                  path: "/v1/trackers",
                  method: "GET",
                  status_code: 404,
                  response_ms: 50,
                  requested_at: "2026-03-01T10:01:00Z",
                  remote_addr: "127.0.0.1",
                  response: '{"detail": "Not found"}',
                  records: [{ id: "rec_1" }],
                },
              },
            ],
          },
        },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockGraphQLResponse),
      });

      const result = await client.listLogs();

      expect(result).toBeDefined();
      expect(result.page_info.count).toBe(2);
      expect(result.edges).toHaveLength(2);
    });

    it("passes filter params to GraphQL query", async () => {
      const mockGraphQLResponse = {
        data: {
          logs: {
            page_info: { count: 0 },
            edges: [],
          },
        },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockGraphQLResponse),
      });

      const filter = {
        api_endpoint: "/v1/shipments",
        method: ["POST"],
        status: "failed",
      };

      await client.listLogs(filter);

      const fetchCall = (fetch as any).mock.calls[0];
      const body = JSON.parse(fetchCall[1].body);
      expect(body.variables.filter).toEqual(filter);
      expect(body.query).toContain("get_logs");
    });

    it("handles API errors gracefully", async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        statusText: "Internal Server Error",
        json: () => Promise.resolve({ detail: "Server error" }),
      });

      await expect(client.listLogs()).rejects.toThrow(/500/);
    });
  });

  describe("get_api_log", () => {
    it("returns full log details on success", async () => {
      const mockGraphQLResponse = {
        data: {
          log: {
            id: 1,
            path: "/v1/shipments",
            host: "api.karrio.io",
            method: "POST",
            status_code: 200,
            response_ms: 150,
            requested_at: "2026-03-01T10:00:00Z",
            remote_addr: "127.0.0.1",
            query_params: "{}",
            data: '{"shipper": {}}',
            response: '{"id": "shp_1"}',
            records: [
              {
                id: "rec_1",
                key: "fedex_create_shipment",
                timestamp: 1709290800,
                test_mode: false,
                created_at: "2026-03-01T10:00:00Z",
                meta: {},
                record: '{"request": {}, "response": {}}',
              },
            ],
          },
        },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockGraphQLResponse),
      });

      const result = await client.getLog(1);

      expect(result).toBeDefined();
      expect(result.id).toBe(1);
      expect(result.records).toHaveLength(1);
      expect(result.records[0].key).toBe("fedex_create_shipment");
    });

    it("passes log ID to GraphQL query", async () => {
      const mockGraphQLResponse = {
        data: { log: { id: 42 } },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockGraphQLResponse),
      });

      await client.getLog(42);

      const fetchCall = (fetch as any).mock.calls[0];
      const body = JSON.parse(fetchCall[1].body);
      expect(body.variables.id).toBe(42);
      expect(body.query).toContain("get_log");
    });

    it("handles API errors gracefully", async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 404,
        statusText: "Not Found",
        json: () => Promise.resolve({ detail: "Not found" }),
      });

      await expect(client.getLog(999)).rejects.toThrow(/404/);
    });
  });

  describe("list_tracing_records", () => {
    it("returns tracing records on success", async () => {
      const mockGraphQLResponse = {
        data: {
          tracing_records: {
            page_info: { count: 1 },
            edges: [
              {
                node: {
                  id: "rec_1",
                  key: "fedex_create_shipment",
                  timestamp: 1709290800,
                  test_mode: false,
                  created_at: "2026-03-01T10:00:00Z",
                  meta: {},
                  record: '{"request": {}, "response": {}}',
                },
              },
            ],
          },
        },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockGraphQLResponse),
      });

      const result = await client.listTracingRecords();

      expect(result).toBeDefined();
      expect(result.page_info.count).toBe(1);
      expect(result.edges).toHaveLength(1);
      expect(result.edges[0].node.key).toBe("fedex_create_shipment");
    });

    it("passes filter params to GraphQL query", async () => {
      const mockGraphQLResponse = {
        data: {
          tracing_records: {
            page_info: { count: 0 },
            edges: [],
          },
        },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockGraphQLResponse),
      });

      const filter = {
        key: "fedex",
        request_log_id: 42,
      };

      await client.listTracingRecords(filter);

      const fetchCall = (fetch as any).mock.calls[0];
      const body = JSON.parse(fetchCall[1].body);
      expect(body.variables.filter).toEqual(filter);
      expect(body.query).toContain("get_tracing_records");
    });

    it("handles API errors gracefully", async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        statusText: "Internal Server Error",
        json: () => Promise.resolve({ detail: "Server error" }),
      });

      await expect(client.listTracingRecords()).rejects.toThrow(/500/);
    });
  });

  describe("queryGraphQL", () => {
    it("sends query to /graphql endpoint with POST", async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ data: {} }),
      });

      await client.queryGraphQL("query { test }", { foo: "bar" });

      const fetchCall = (fetch as any).mock.calls[0];
      expect(fetchCall[0]).toBe("https://api.karrio.io/graphql");
      expect(fetchCall[1].method).toBe("POST");
      const body = JSON.parse(fetchCall[1].body);
      expect(body.query).toBe("query { test }");
      expect(body.variables).toEqual({ foo: "bar" });
    });
  });
});
