import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerCarrierTools(
  server: McpServer,
  client: KarrioClient,
): void {
  server.tool(
    "list_carriers",
    "List all supported carrier integrations in the Karrio catalog with their capabilities. Use this to discover what carriers can be connected. For carriers already connected to your account, use list_carrier_connections instead.",
    {
      carrier_name: z
        .string()
        .optional()
        .describe("Filter by carrier name (e.g., 'fedex', 'ups')"),
      limit: z
        .number()
        .int()
        .default(50)
        .describe("Maximum results"),
      offset: z
        .number()
        .int()
        .default(0)
        .describe("Pagination offset"),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async (params) => {
      try {
        const queryParams: Record<string, string> = {
          limit: String(params.limit),
          offset: String(params.offset),
        };
        if (params.carrier_name) {
          queryParams.carrier_name = params.carrier_name;
        }

        const response = await client.listCarriers(queryParams);

        const carriers = (response.results ?? response ?? []).map(
          (carrier: any) => ({
            id: carrier.id,
            carrier_name: carrier.carrier_name,
            display_name: carrier.display_name ?? null,
            capabilities: carrier.capabilities ?? [],
          }),
        );

        const result = {
          carriers,
          count: response.count ?? carriers.length,
          limit: params.limit,
          offset: params.offset,
        };

        return {
          content: [
            { type: "text", text: JSON.stringify(result, null, 2) },
          ],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error listing carriers: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );

  server.tool(
    "list_carrier_connections",
    "List carrier accounts connected to your Karrio instance. These are the carriers configured with credentials that you can use for rating, shipping, and tracking. Returns carrier_id, display_name, capabilities, and connection status.",
    {
      carrier_name: z
        .string()
        .optional()
        .describe("Filter by carrier name (e.g., 'fedex', 'ups')"),
      limit: z
        .number()
        .int()
        .default(20)
        .describe("Maximum results"),
      offset: z
        .number()
        .int()
        .default(0)
        .describe("Pagination offset"),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async (params) => {
      try {
        const queryParams: Record<string, string> = {
          limit: String(params.limit),
          offset: String(params.offset),
        };
        if (params.carrier_name) {
          queryParams.carrier_name = params.carrier_name;
        }

        const response = await client.listConnections(queryParams);

        const connections = (response.results ?? []).map(
          (conn: any) => ({
            id: conn.id,
            carrier_name: conn.carrier_name,
            carrier_id: conn.carrier_id,
            display_name: conn.display_name ?? null,
            capabilities: conn.capabilities ?? [],
            active: conn.active ?? conn.is_active ?? null,
            test_mode: conn.test_mode ?? null,
          }),
        );

        const result = {
          connections,
          count: response.count ?? connections.length,
          limit: params.limit,
          offset: params.offset,
        };

        return {
          content: [
            { type: "text", text: JSON.stringify(result, null, 2) },
          ],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error listing carrier connections: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );
}
