import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerPickupTools(
  server: McpServer,
  client: KarrioClient,
): void {
  server.tool(
    "schedule_pickup",
    "Schedule a carrier pickup for one or more shipments. The carrier will come to the specified location to collect packages.",
    {
      carrier_name: z
        .string()
        .describe("Carrier name (e.g., 'fedex', 'ups')"),
      pickup_date: z
        .string()
        .describe("Pickup date in YYYY-MM-DD format"),
      ready_time: z
        .string()
        .describe("Earliest ready time in HH:MM format"),
      closing_time: z
        .string()
        .describe("Latest closing time in HH:MM format"),
      address_line1: z
        .string()
        .describe("Pickup street address"),
      city: z
        .string()
        .optional()
        .describe("Pickup city"),
      state: z
        .string()
        .optional()
        .describe("Pickup state/province code"),
      postal_code: z
        .string()
        .describe("Pickup postal/zip code"),
      country_code: z
        .string()
        .describe("Pickup country code"),
      person_name: z
        .string()
        .optional()
        .describe("Contact person name"),
      phone: z
        .string()
        .optional()
        .describe("Contact phone number"),
      instruction: z
        .string()
        .optional()
        .describe("Special instructions for the driver"),
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
        if (params.person_name) address.person_name = params.person_name;
        if (params.phone) address.phone_number = params.phone;

        const payload: Record<string, unknown> = {
          carrier_name: params.carrier_name,
          pickup_date: params.pickup_date,
          ready_time: params.ready_time,
          closing_time: params.closing_time,
          address,
        };

        if (params.instruction) {
          payload.instruction = params.instruction;
        }

        if (params.shipment_ids) {
          const ids = params.shipment_ids
            .split(",")
            .map((id) => id.trim())
            .filter(Boolean);
          if (ids.length > 0) {
            payload.tracking_numbers = ids;
          }
        }

        const response = await client.schedulePickup(payload);

        const result = {
          pickup_id: response.id ?? null,
          confirmation_number: response.confirmation_number ?? null,
          carrier: response.carrier_name ?? params.carrier_name,
          pickup_date: response.pickup_date ?? params.pickup_date,
          ready_time: response.ready_time ?? params.ready_time,
          closing_time: response.closing_time ?? params.closing_time,
          address: response.address ?? address,
          messages: response.messages ?? [],
        };

        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error scheduling pickup: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );
}
