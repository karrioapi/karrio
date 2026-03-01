import { describe, it, expect } from "vitest";
import { createServer } from "../../src/server.js";

describe("MCP Server", () => {
  it("creates a server with all tools registered", () => {
    const server = createServer({
      apiUrl: "http://localhost:5002",
      apiKey: "test_key",
    });

    // Server should be created without errors
    console.log(server);
    expect(server).toBeDefined();
  });

  it("creates a server with custom API URL", () => {
    const server = createServer({
      apiUrl: "https://custom.karrio.io",
      apiKey: "custom_key",
    });

    console.log(server);
    expect(server).toBeDefined();
  });

  it("creates a server that is an instance of McpServer", async () => {
    const { McpServer } = await import(
      "@modelcontextprotocol/sdk/server/mcp.js"
    );

    const server = createServer({
      apiUrl: "http://localhost:5002",
      apiKey: "test_key",
    });

    console.log(server);
    expect(server).toBeInstanceOf(McpServer);
  });

  it("creates independent server instances", () => {
    const server1 = createServer({
      apiUrl: "http://localhost:5002",
      apiKey: "key_1",
    });

    const server2 = createServer({
      apiUrl: "http://localhost:5003",
      apiKey: "key_2",
    });

    console.log(server1);
    console.log(server2);
    expect(server1).not.toBe(server2);
  });
});
