import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerOrderTools(
  server: McpServer,
  client: KarrioClient,
): void {
  server.tool(
    "list_orders",
    "List orders and their fulfillment status. Returns order details including items, shipping status, and tracking information.",
    {
      status: z
        .enum(["unfulfilled", "fulfilled", "cancelled", "partial"])
        .optional()
        .describe("Filter by order status"),
      order_id: z
        .string()
        .optional()
        .describe("Filter by specific order ID"),
      limit: z
        .number()
        .int()
        .default(20)
        .describe("Max results"),
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
        // If a specific order ID is provided, fetch it directly
        if (params.order_id) {
          const order = await client.getOrder(params.order_id);

          const result = {
            order_id: order.id ?? params.order_id,
            order_number: order.order_id ?? null,
            status: order.status ?? null,
            source: order.source ?? null,
            created_at: order.created_at ?? null,
            updated_at: order.updated_at ?? null,
            shipping_to: order.shipping_to ?? null,
            line_items: order.line_items ?? [],
            shipments: order.shipments ?? [],
            meta: order.meta ?? {},
          };

          return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
          };
        }

        // Otherwise, list orders with optional filters
        const queryParams: Record<string, string> = {
          limit: String(params.limit),
          offset: String(params.offset),
        };
        if (params.status) queryParams.status = params.status;

        const response = await client.listOrders(queryParams);

        const orders = (response.results ?? []).map((order: any) => ({
          order_id: order.id ?? null,
          order_number: order.order_id ?? null,
          status: order.status ?? null,
          source: order.source ?? null,
          created_at: order.created_at ?? null,
          line_items_count: order.line_items?.length ?? 0,
          shipments_count: order.shipments?.length ?? 0,
        }));

        const result = {
          orders,
          total: response.count ?? orders.length,
          limit: params.limit,
          offset: params.offset,
        };

        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error listing orders: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );
}
