// hooks.ts — TanStack Query data hooks over the decoupled Karrio client.
// These replace @karrio/hooks (which is NextAuth/Next-coupled). Each hook reads
// the KarrioCtx (base URL + token + org + test-mode) from the SessionProvider.
import { useQuery } from "@tanstack/react-query";
import { restGet, graphql, type KarrioCtx } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import type {
  CarrierConnection,
  Order,
  Paginated,
  Shipment,
  Tracker,
} from "~/lib/karrio/types";

const keyExtra = (ctx: KarrioCtx) => ({ org: ctx.orgId, test: ctx.testMode });

export function useShipments(params?: Record<string, string | number | undefined>) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["shipments", params, keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Shipment>>(ctx, "/v1/shipments", params),
    enabled: Boolean(ctx.token),
  });
}

export function useShipment(id: string) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["shipment", id, keyExtra(ctx)],
    queryFn: () => restGet<Shipment>(ctx, `/v1/shipments/${id}`),
    enabled: Boolean(ctx.token && id),
  });
}

export function useTrackers(params?: Record<string, string | number | undefined>) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["trackers", params, keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Tracker>>(ctx, "/v1/trackers", params),
    enabled: Boolean(ctx.token),
  });
}

export function useCarrierConnections() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["carrier-connections", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<CarrierConnection>>(ctx, "/v1/connections"),
    enabled: Boolean(ctx.token),
  });
}

const ORDERS_QUERY = `query Orders($filter: OrderFilter) {
  orders(filter: $filter) {
    edges { node { id order_id status source created_at
      line_items { id title quantity }
      shipping_to { city country_code person_name }
    } }
  }
}`;

type OrdersResponse = { orders: { edges: Array<{ node: Order }> } };

export function useOrders(filter?: Record<string, unknown>) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["orders", filter, keyExtra(ctx)],
    queryFn: async () => {
      const data = await graphql<OrdersResponse>(ctx, ORDERS_QUERY, { filter });
      return data.orders.edges.map((e) => e.node);
    },
    enabled: Boolean(ctx.token),
  });
}
