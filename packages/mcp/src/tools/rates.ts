import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerRateTools(
  server: McpServer,
  client: KarrioClient,
): void {
  server.tool(
    "get_shipping_rates",
    "Get shipping rate quotes from multiple carriers for a package. Returns ranked rates with carrier name, service, price, and estimated delivery. Use this when a user wants to compare shipping options or find the cheapest/fastest way to ship something.",
    {
      origin_city: z.string().optional().describe("Origin city name"),
      origin_state: z
        .string()
        .optional()
        .describe("Origin state/province code (e.g., 'CA', 'ON')"),
      origin_postal_code: z.string().describe("Origin postal/zip code"),
      origin_country_code: z
        .string()
        .describe("Origin ISO 2-letter country code (e.g., 'US', 'CA')"),
      dest_city: z.string().optional().describe("Destination city name"),
      dest_state: z
        .string()
        .optional()
        .describe("Destination state/province code"),
      dest_postal_code: z.string().describe("Destination postal/zip code"),
      dest_country_code: z
        .string()
        .describe("Destination ISO 2-letter country code"),
      weight: z.number().describe("Package weight"),
      weight_unit: z
        .enum(["LB", "KG", "OZ", "G"])
        .default("LB")
        .describe("Weight unit"),
      length: z.number().optional().describe("Package length"),
      width: z.number().optional().describe("Package width"),
      height: z.number().optional().describe("Package height"),
      dimension_unit: z
        .enum(["IN", "CM"])
        .default("IN")
        .describe("Dimension unit"),
      carrier_names: z
        .string()
        .optional()
        .describe(
          "Comma-separated carrier names to query (e.g., 'fedex,ups'). Omit to query all.",
        ),
      max_results: z
        .number()
        .int()
        .default(10)
        .describe("Maximum number of rates to return"),
      sort_by: z
        .enum(["price", "delivery_time"])
        .default("price")
        .describe("Sort order"),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
    async (params) => {
      try {
        const shipper: Record<string, string> = {
          postal_code: params.origin_postal_code,
          country_code: params.origin_country_code,
        };
        if (params.origin_city) shipper.city = params.origin_city;
        if (params.origin_state) shipper.state_code = params.origin_state;

        const recipient: Record<string, string> = {
          postal_code: params.dest_postal_code,
          country_code: params.dest_country_code,
        };
        if (params.dest_city) recipient.city = params.dest_city;
        if (params.dest_state) recipient.state_code = params.dest_state;

        const parcel: Record<string, unknown> = {
          weight: params.weight,
          weight_unit: params.weight_unit,
          dimension_unit: params.dimension_unit,
        };
        if (params.length !== undefined) parcel.length = params.length;
        if (params.width !== undefined) parcel.width = params.width;
        if (params.height !== undefined) parcel.height = params.height;

        const payload: Record<string, unknown> = {
          shipper,
          recipient,
          parcels: [parcel],
        };

        if (params.carrier_names) {
          const carrierIds = params.carrier_names
            .split(",")
            .map((name) => name.trim())
            .filter(Boolean);
          if (carrierIds.length > 0) {
            payload.carrier_ids = carrierIds;
          }
        }

        const response = await client.fetchRates(payload);

        let rates: any[] = response.rates ?? [];

        rates.sort((a: any, b: any) => {
          if (params.sort_by === "delivery_time") {
            const daysA = a.estimated_delivery
              ? parseInt(a.estimated_delivery, 10)
              : Infinity;
            const daysB = b.estimated_delivery
              ? parseInt(b.estimated_delivery, 10)
              : Infinity;
            return daysA - daysB;
          }
          const priceA = a.total_charge ?? Infinity;
          const priceB = b.total_charge ?? Infinity;
          return priceA - priceB;
        });

        rates = rates.slice(0, params.max_results);

        const formattedRates = rates.map((rate: any, index: number) => ({
          rank: index + 1,
          carrier: rate.carrier_name ?? rate.carrier_id ?? "unknown",
          service: rate.service ?? "unknown",
          total_charge: rate.total_charge,
          currency: rate.currency,
          estimated_delivery: rate.estimated_delivery ?? null,
          transit_days: rate.transit_days ?? null,
          extra_charges: rate.extra_charges ?? [],
          meta: rate.meta ?? {},
        }));

        const result = {
          rates: formattedRates,
          total_carriers_queried: response.rates?.length ?? 0,
          results_returned: formattedRates.length,
          sorted_by: params.sort_by,
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
              text: `Error fetching shipping rates: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );
}
