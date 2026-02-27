import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerTrackingTools(
  server: McpServer,
  client: KarrioClient,
): void {
  server.tool(
    "track_package",
    "Track a package by tracking number. Returns current status, location, estimated delivery date, and full event history. Supports all major carriers (FedEx, UPS, DHL, USPS, Canada Post, and 50+ more).",
    {
      tracking_number: z.string().describe("The package tracking number"),
      carrier_name: z
        .string()
        .optional()
        .describe(
          "Carrier name (e.g., 'fedex', 'ups'). If omitted, Karrio will attempt auto-detection.",
        ),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
    async (params) => {
      try {
        const payload: Record<string, unknown> = {
          tracking_number: params.tracking_number,
        };

        if (params.carrier_name) {
          payload.carrier_name = params.carrier_name;
        }

        const tracker = await client.createTracker(payload);

        const events = (tracker.events ?? []).map(
          (event: Record<string, unknown>) => ({
            date: event.date ?? null,
            description: event.description ?? null,
            location: event.location ?? null,
          }),
        );

        const result = {
          tracking_number: tracker.tracking_number,
          status: tracker.status,
          carrier: tracker.carrier_name ?? tracker.carrier_id ?? null,
          estimated_delivery: tracker.estimated_delivery ?? null,
          delivered: tracker.delivered ?? false,
          events,
        };

        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error tracking package: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );
}
