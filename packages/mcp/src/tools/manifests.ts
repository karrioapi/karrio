import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerManifestTools(
  server: McpServer,
  client: KarrioClient,
): void {
  server.tool(
    "create_manifest",
    "Create an end-of-day manifest (SCAN form) for a carrier. This consolidates all shipments into a single document for carrier pickup.",
    {
      carrier_name: z
        .string()
        .describe("Carrier name (e.g., 'fedex', 'ups')"),
      address_line1: z
        .string()
        .describe("Pickup/origin address line"),
      city: z
        .string()
        .optional()
        .describe("City"),
      state: z
        .string()
        .optional()
        .describe("State code"),
      postal_code: z
        .string()
        .describe("Postal code"),
      country_code: z
        .string()
        .describe("Country code"),
      shipment_ids: z
        .string()
        .optional()
        .describe("Comma-separated shipment IDs to include"),
    },
    {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: true,
    },
    async (params) => {
      try {
        const address: Record<string, string> = {
          address_line1: params.address_line1,
          postal_code: params.postal_code,
          country_code: params.country_code,
        };
        if (params.city) address.city = params.city;
        if (params.state) address.state_code = params.state;

        const payload: Record<string, unknown> = {
          carrier_name: params.carrier_name,
          address,
        };

        if (params.shipment_ids) {
          const ids = params.shipment_ids
            .split(",")
            .map((id) => id.trim())
            .filter(Boolean);
          if (ids.length > 0) {
            payload.shipment_ids = ids;
          }
        }

        const response = await client.createManifest(payload);

        const result = {
          manifest_id: response.id ?? null,
          carrier: response.carrier_name ?? params.carrier_name,
          document_url: response.manifest_url ?? response.doc?.manifest_url ?? null,
          shipment_count: response.shipment_ids?.length ?? null,
          address: response.address ?? address,
          messages: response.messages ?? [],
          meta: response.meta ?? {},
        };

        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error creating manifest: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );
}
