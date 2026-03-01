import { describe, it, expect } from "vitest";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../../../src/client.js";
import { registerTrackingTools } from "../../../src/tools/tracking.js";

describe("track_package tool", () => {
  it("registers the tool on the server without errors", () => {
    const server = new McpServer({ name: "test", version: "1.0.0" });
    const client = new KarrioClient({
      apiUrl: "http://localhost",
      apiKey: "key",
    });

    const result = registerTrackingTools(server, client);
    console.log(result);
    expect(result).toBeUndefined();
  });

  it("cannot register tracking tools twice (tool names are unique)", () => {
    const server = new McpServer({ name: "test", version: "1.0.0" });
    const client = new KarrioClient({
      apiUrl: "http://localhost",
      apiKey: "key",
    });

    registerTrackingTools(server, client);

    // Registering a second time should throw because the tool name is already taken
    expect(() => registerTrackingTools(server, client)).toThrow();
  });
});
