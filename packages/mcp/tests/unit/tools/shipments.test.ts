import { describe, it, expect } from "vitest";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../../../src/client.js";
import { registerShipmentTools } from "../../../src/tools/shipments.js";

describe("shipment tools", () => {
  it("registers all shipment tools on the server without errors", () => {
    const server = new McpServer({ name: "test", version: "1.0.0" });
    const client = new KarrioClient({
      apiUrl: "http://localhost",
      apiKey: "key",
    });

    const result = registerShipmentTools(server, client);
    console.log(result);
    expect(result).toBeUndefined();
  });

  it("cannot register shipment tools twice (tool names are unique)", () => {
    const server = new McpServer({ name: "test", version: "1.0.0" });
    const client = new KarrioClient({
      apiUrl: "http://localhost",
      apiKey: "key",
    });

    registerShipmentTools(server, client);

    // Registering a second time should throw because tool names collide
    expect(() => registerShipmentTools(server, client)).toThrow();
  });
});
