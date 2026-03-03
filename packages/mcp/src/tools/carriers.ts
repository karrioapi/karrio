import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerCarrierTools(
  server: McpServer,
  client: KarrioClient,
): void {
  server.tool(
    "list_carriers",
    "List all carrier accounts connected to your Karrio instance with their capabilities (tracking, rating, shipping, pickup). Use this to discover available carriers and their service codes before creating shipments or fetching rates.",
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
            carrier_id: carrier.carrier_id,
            active: carrier.active ?? carrier.is_active ?? null,
            capabilities: carrier.capabilities ?? [],
            test_mode: carrier.test_mode ?? null,
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
}
