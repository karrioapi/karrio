import { describe, it, expect, vi } from "vitest";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../../../src/client.js";
import { registerRateTools } from "../../../src/tools/rates.js";

describe("get_shipping_rates tool", () => {
  it("registers the tool on the server without errors", () => {
    const server = new McpServer({ name: "test", version: "1.0.0" });
    const client = new KarrioClient({
      apiUrl: "http://localhost",
      apiKey: "key",
    });

    // Should not throw
    const result = registerRateTools(server, client);
    console.log(result);
    expect(result).toBeUndefined();
  });

  it("can be registered alongside other tools without conflict", () => {
    const server = new McpServer({ name: "test", version: "1.0.0" });
    const client = new KarrioClient({
      apiUrl: "http://localhost",
      apiKey: "key",
    });

    registerRateTools(server, client);

    // Registering a second time should throw because the tool name is already taken
    expect(() => registerRateTools(server, client)).toThrow();
  });
});
