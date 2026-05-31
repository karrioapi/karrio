// hooks/ship.ts — Ship-mode read hooks. UNIT A migrates these REST calls to
// the tenant GraphQL schema (shipments/trackers/user_connections/pickups/
// document_templates/manifests/batch_operations) mirroring the dashboard GET_*
// selections. See STUDIO_GRAPHQL_REBUILD.md.
import { useQuery } from "@tanstack/react-query";
import { restGet } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import { keyExtra } from "~/lib/karrio/hooks/_shared";
import type {
  BatchOperation,
  CarrierConnection,
  DocumentTemplate,
  Manifest,
  Paginated,
  Pickup,
  Shipment,
  Tracker,
} from "~/lib/karrio/types";

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
    queryFn: async () => {
      const data = await restGet<Paginated<Tracker>>(ctx, "/v1/trackers", params);
      // Karrio stores the carrier under meta on tracking records; surface it.
      data.results = data.results.map((t) => ({
        ...t,
        carrier_name: t.carrier_name || (t.meta as { carrier_name?: string } | undefined)?.carrier_name,
      }));
      return data;
    },
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

export function usePickups() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["pickups", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Pickup>>(ctx, "/v1/pickups"),
    enabled: Boolean(ctx.token),
  });
}

export function useDocumentTemplates() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["document-templates", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<DocumentTemplate>>(ctx, "/v1/documents/templates"),
    enabled: Boolean(ctx.token),
  });
}

export function useManifests() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["manifests", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<Manifest>>(ctx, "/v1/manifests"),
    enabled: Boolean(ctx.token),
  });
}

export function useBatches() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["batches", keyExtra(ctx)],
    queryFn: () => restGet<Paginated<BatchOperation>>(ctx, "/v1/batches/operations"),
    enabled: Boolean(ctx.token),
  });
}
