import {
  McpServer,
  ResourceTemplate,
} from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerCarrierResources(
  server: McpServer,
  client: KarrioClient,
): void {
  // Resource 1: karrio://carriers — Full carrier catalog
  server.resource(
    "carrier-catalog",
    "karrio://carriers",
    {
      description:
        "Complete multi-carrier capability catalog. Lists all connected carriers " +
        "with their capabilities (tracking, rating, shipping, pickup, manifest). " +
        "Use this to understand what carriers are available before fetching rates " +
        "or creating shipments.",
      mimeType: "application/json",
    },
    async (uri) => {
      try {
        const response = await client.listCarriers();
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

        return {
          contents: [
            {
              uri: "karrio://carriers",
              mimeType: "application/json",
              text: JSON.stringify(
                { carriers, count: carriers.length },
                null,
                2,
              ),
            },
          ],
        };
      } catch (error: any) {
        return {
          contents: [
            {
              uri: "karrio://carriers",
              mimeType: "application/json",
              text: JSON.stringify({ error: error.message, carriers: [] }),
            },
          ],
        };
      }
    },
  );

  // Resource 2: karrio://carriers/{carrier_id} — Individual carrier details
  server.resource(
    "carrier-detail",
    new ResourceTemplate("karrio://carriers/{carrier_id}", {
      list: async () => {
        try {
          const response = await client.listCarriers();
          const carriers = response.results ?? response ?? [];
          return {
            resources: carriers.map((carrier: any) => ({
              uri: `karrio://carriers/${carrier.carrier_id ?? carrier.id}`,
              name: carrier.carrier_name ?? carrier.id,
              description: `Carrier connection details for ${carrier.carrier_name ?? carrier.id}`,
              mimeType: "application/json",
            })),
          };
        } catch {
          return { resources: [] };
        }
      },
    }),
    {
      description:
        "Detailed information for a specific carrier connection including " +
        "services and capabilities.",
      mimeType: "application/json",
    },
    async (uri, params) => {
      try {
        const carrierId = String(params.carrier_id);
        const response = await client.listCarriers({
          carrier_name: carrierId,
        });
        const carriers = response.results ?? response ?? [];
        const carrier = carriers[0] ?? null;

        const data = carrier
          ? {
              id: carrier.id,
              carrier_name: carrier.carrier_name,
              carrier_id: carrier.carrier_id,
              active: carrier.active ?? carrier.is_active ?? null,
              capabilities: carrier.capabilities ?? [],
              test_mode: carrier.test_mode ?? null,
            }
          : { error: `Carrier '${carrierId}' not found` };

        return {
          contents: [
            {
              uri: uri.href,
              mimeType: "application/json",
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      } catch (error: any) {
        return {
          contents: [
            {
              uri: uri.href,
              mimeType: "application/json",
              text: JSON.stringify({ error: error.message }),
            },
          ],
        };
      }
    },
  );
}
