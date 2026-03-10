import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { KarrioClient } from "../client.js";

/** Remove keys with undefined or null values from an object. */
function cleanObject<T extends Record<string, unknown>>(obj: T): Partial<T> {
  return Object.fromEntries(
    Object.entries(obj).filter(([, v]) => v !== undefined && v !== null),
  ) as Partial<T>;
}

export function registerShipmentTools(
  server: McpServer,
  client: KarrioClient,
): void {
  // ── Tool 1: create_shipment ──────────────────────────────────────────
  server.tool(
    "create_shipment",
    "Create a shipment and purchase a shipping label. This generates a label you can print. IMPORTANT: This action purchases a label and incurs a charge. Make sure the user has confirmed the shipment details before calling this tool.",
    {
      shipper_name: z.string().describe("Shipper person or company name"),
      shipper_address_line1: z.string().describe("Shipper street address"),
      shipper_address_line2: z
        .string()
        .optional()
        .describe("Shipper address line 2"),
      shipper_city: z.string().optional().describe("Shipper city"),
      shipper_state: z
        .string()
        .optional()
        .describe("Shipper state/province code"),
      shipper_postal_code: z.string().describe("Shipper postal/zip code"),
      shipper_country_code: z
        .string()
        .describe("Shipper ISO 2-letter country code"),
      shipper_phone: z.string().optional().describe("Shipper phone number"),
      shipper_email: z.string().optional().describe("Shipper email"),

      recipient_name: z.string().describe("Recipient person or company name"),
      recipient_address_line1: z
        .string()
        .describe("Recipient street address"),
      recipient_address_line2: z
        .string()
        .optional()
        .describe("Recipient address line 2"),
      recipient_city: z.string().optional().describe("Recipient city"),
      recipient_state: z
        .string()
        .optional()
        .describe("Recipient state/province code"),
      recipient_postal_code: z
        .string()
        .describe("Recipient postal/zip code"),
      recipient_country_code: z
        .string()
        .describe("Recipient ISO 2-letter country code"),
      recipient_phone: z
        .string()
        .optional()
        .describe("Recipient phone number"),
      recipient_email: z.string().optional().describe("Recipient email"),

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

      carrier_name: z
        .string()
        .describe("Carrier to ship with (e.g., 'fedex', 'ups')"),
      service: z
        .string()
        .describe(
          "Service code (e.g., 'fedex_ground'). Use list_carriers to find codes.",
        ),
      label_type: z
        .enum(["PDF", "ZPL", "PNG"])
        .default("PDF")
        .describe("Label format"),
      reference: z.string().optional().describe("Shipment reference number"),
    },
    {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: true,
    },
    async (params) => {
      try {
        const shipper = cleanObject({
          person_name: params.shipper_name,
          address_line1: params.shipper_address_line1,
          address_line2: params.shipper_address_line2,
          city: params.shipper_city,
          state_code: params.shipper_state,
          postal_code: params.shipper_postal_code,
          country_code: params.shipper_country_code,
          phone_number: params.shipper_phone,
          email: params.shipper_email,
        });

        const recipient = cleanObject({
          person_name: params.recipient_name,
          address_line1: params.recipient_address_line1,
          address_line2: params.recipient_address_line2,
          city: params.recipient_city,
          state_code: params.recipient_state,
          postal_code: params.recipient_postal_code,
          country_code: params.recipient_country_code,
          phone_number: params.recipient_phone,
          email: params.recipient_email,
        });

        const parcel = cleanObject({
          weight: params.weight,
          weight_unit: params.weight_unit,
          length: params.length,
          width: params.width,
          height: params.height,
          dimension_unit: params.dimension_unit,
        });

        const shipmentPayload: Record<string, unknown> = {
          shipper,
          recipient,
          parcels: [parcel],
          service: params.service,
          carrier_ids: [params.carrier_name],
          label_type: params.label_type,
        };

        if (params.reference) {
          shipmentPayload.reference = params.reference;
        }

        // Step 1: Create the shipment
        const shipment = await client.createShipment(shipmentPayload);

        // Step 2: Purchase the label
        const selectedRateId = shipment.rates?.[0]?.id;
        if (!selectedRateId) {
          return {
            content: [
              {
                type: "text" as const,
                text: JSON.stringify(
                  {
                    error:
                      "No rates returned for this shipment. Verify the carrier, service, and addresses are correct.",
                    shipment_id: shipment.id,
                    shipment,
                  },
                  null,
                  2,
                ),
              },
            ],
            isError: true,
          };
        }

        const purchased = await client.purchaseShipment(shipment.id, {
          selected_rate_id: selectedRateId,
        });

        const result = {
          shipment_id: purchased.id,
          status: purchased.status,
          tracking_number: purchased.tracking_number,
          label_url: purchased.label_url,
          carrier_name: purchased.carrier_name,
          service: purchased.service,
          cost: purchased.selected_rate?.total_charge,
          currency: purchased.selected_rate?.currency,
          estimated_delivery: purchased.selected_rate?.estimated_delivery,
        };

        return {
          content: [
            { type: "text" as const, text: JSON.stringify(result, null, 2) },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error creating shipment: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    },
  );

  // ── Tool 2: get_shipment ─────────────────────────────────────────────
  server.tool(
    "get_shipment",
    "Get details of an existing shipment by ID. Returns shipment status, tracking number, carrier, service, addresses, and label information.",
    {
      shipment_id: z.string().describe("The shipment ID to retrieve"),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async (params) => {
      try {
        const shipment = await client.getShipment(params.shipment_id);

        const result = {
          shipment_id: shipment.id,
          status: shipment.status,
          tracking_number: shipment.tracking_number,
          carrier_name: shipment.carrier_name,
          service: shipment.service,
          label_url: shipment.label_url,
          label_type: shipment.label_type,
          cost: shipment.selected_rate?.total_charge,
          currency: shipment.selected_rate?.currency,
          shipper: shipment.shipper,
          recipient: shipment.recipient,
          parcels: shipment.parcels,
          reference: shipment.reference,
          created_at: shipment.created_at,
          updated_at: shipment.updated_at,
        };

        return {
          content: [
            { type: "text" as const, text: JSON.stringify(result, null, 2) },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error retrieving shipment: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    },
  );

  // ── Tool 3: list_shipments ───────────────────────────────────────────
  server.tool(
    "list_shipments",
    "List shipments with optional filters. Returns a paginated list of shipments with status, tracking number, carrier, and creation date.",
    {
      status: z
        .enum([
          "draft",
          "created",
          "cancelled",
          "shipped",
          "in_transit",
          "delivered",
        ])
        .optional()
        .describe("Filter by status"),
      carrier_name: z
        .string()
        .optional()
        .describe("Filter by carrier name"),
      created_after: z
        .string()
        .optional()
        .describe("Filter shipments created after this date (ISO format)"),
      created_before: z
        .string()
        .optional()
        .describe("Filter shipments created before this date (ISO format)"),
      limit: z.number().default(20).describe("Max results to return"),
      offset: z.number().default(0).describe("Pagination offset"),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async (params) => {
      try {
        const queryParams = cleanObject({
          status: params.status,
          carrier_name: params.carrier_name,
          created_after: params.created_after,
          created_before: params.created_before,
          limit: String(params.limit),
          offset: String(params.offset),
        }) as Record<string, string>;

        const response = await client.listShipments(queryParams);

        const shipments = (response.results ?? []).map((s: any) => ({
          shipment_id: s.id,
          status: s.status,
          tracking_number: s.tracking_number,
          carrier_name: s.carrier_name,
          service: s.service,
          reference: s.reference,
          created_at: s.created_at,
        }));

        const result = {
          count: response.count,
          next: response.next,
          previous: response.previous,
          shipments,
        };

        return {
          content: [
            { type: "text" as const, text: JSON.stringify(result, null, 2) },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error listing shipments: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    },
  );

  // ── Tool 4: cancel_shipment ──────────────────────────────────────────
  server.tool(
    "cancel_shipment",
    "Cancel a shipment and void its label. This reverses a label purchase. The shipment must be in a cancellable state (not yet picked up by carrier).",
    {
      shipment_id: z.string().describe("The shipment ID to cancel"),
    },
    {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: true,
    },
    async (params) => {
      try {
        const result = await client.cancelShipment(params.shipment_id);

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(
                {
                  shipment_id: params.shipment_id,
                  status: "cancelled",
                  message: "Shipment has been cancelled and label voided.",
                  details: result,
                },
                null,
                2,
              ),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error cancelling shipment: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    },
  );
}
