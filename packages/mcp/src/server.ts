import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "./client.js";
import { registerRateTools } from "./tools/rates.js";
import { registerShipmentTools } from "./tools/shipments.js";
import { registerTrackingTools } from "./tools/tracking.js";
import { registerCarrierTools } from "./tools/carriers.js";
import { registerPickupTools } from "./tools/pickups.js";
import { registerManifestTools } from "./tools/manifests.js";
import { registerCarrierResources } from "./resources/carriers.js";

export interface ServerConfig {
  apiUrl: string;
  apiKey: string;
}

export function createServer(config: ServerConfig): McpServer {
  const server = new McpServer({
    name: "karrio",
    version: "1.0.0",
  });

  const client = new KarrioClient({
    apiUrl: config.apiUrl,
    apiKey: config.apiKey,
  });

  // Register all tools
  registerRateTools(server, client);
  registerShipmentTools(server, client);
  registerTrackingTools(server, client);
  registerCarrierTools(server, client);
  registerPickupTools(server, client);
  registerManifestTools(server, client);

  // Register resources
  registerCarrierResources(server, client);

  return server;
}
