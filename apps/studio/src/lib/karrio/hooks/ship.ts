// hooks/ship.ts — Ship-mode read hooks (UNIT A), all on the tenant GraphQL
// schema, mirroring the dashboard GET_* selections. Connection results are
// flattened to the Paginated<T> shape the screens already consume.
// See STUDIO_GRAPHQL_REBUILD.md.
import { useQuery } from "@tanstack/react-query";
import { graphql } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import { graphqlEdges, keyExtra } from "~/lib/karrio/hooks/_shared";
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

const page = <T>(results: T[]): Paginated<T> => ({ count: results.length, next: null, previous: null, results });

// --- Shipments --------------------------------------------------------------
const SHIPMENTS_QUERY = `query { shipments { edges { node {
  id status tracking_number reference created_at carrier_name carrier_id service
  selected_rate { carrier_name service total_charge currency transit_days
    extra_charges { name amount currency } }
  recipient { person_name company_name city state_code country_code postal_code address_line1 email phone_number residential }
  shipper { person_name company_name city state_code country_code postal_code address_line1 }
  parcels { weight weight_unit width height length dimension_unit packaging_type reference_number }
} } } }`;

export function useShipments(params?: Record<string, string | number | undefined>) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["shipments", params, keyExtra(ctx)],
    queryFn: async () => page(await graphqlEdges<Shipment>(ctx, SHIPMENTS_QUERY, "shipments")),
    enabled: Boolean(ctx.token),
  });
}

const SHIPMENT_QUERY = `query($id: String!) { shipment(id: $id) {
  id status tracking_number reference created_at carrier_name carrier_id service
  selected_rate { carrier_name service total_charge currency transit_days
    extra_charges { name amount currency } }
  recipient { person_name company_name city state_code country_code postal_code address_line1 email phone_number residential }
  shipper { person_name company_name city state_code country_code postal_code address_line1 }
  parcels { weight weight_unit width height length dimension_unit packaging_type reference_number }
} }`;

export function useShipment(id: string) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["shipment", id, keyExtra(ctx)],
    queryFn: async () => {
      const data = await graphql<{ shipment: Shipment }>(ctx, SHIPMENT_QUERY, { id });
      return data.shipment;
    },
    enabled: Boolean(ctx.token && id),
  });
}

// --- Trackers (carrier surfaced from meta when null, as before) -------------
const TRACKERS_QUERY = `query { trackers { edges { node {
  id tracking_number carrier_name status estimated_delivery meta
  events { description location code date time }
} } } }`;

export function useTrackers(params?: Record<string, string | number | undefined>) {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["trackers", params, keyExtra(ctx)],
    queryFn: async () => {
      const raws = await graphqlEdges<Tracker>(ctx, TRACKERS_QUERY, "trackers");
      return page(
        raws.map((t) => ({
          ...t,
          carrier_name: t.carrier_name || (t.meta as { carrier_name?: string } | undefined)?.carrier_name,
        })),
      );
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Carrier connections (GraphQL `user_connections`) -----------------------
const USER_CONNECTIONS_QUERY = `query { user_connections { edges { node {
  id carrier_name carrier_id display_name active test_mode capabilities
} } } }`;

export function useCarrierConnections() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["carrier-connections", keyExtra(ctx)],
    queryFn: async () => page(await graphqlEdges<CarrierConnection>(ctx, USER_CONNECTIONS_QUERY, "user_connections")),
    enabled: Boolean(ctx.token),
  });
}

// --- Pickups ----------------------------------------------------------------
const PICKUPS_QUERY = `query { pickups { edges { node {
  id confirmation_number carrier_name pickup_date ready_time closing_time status
  address { person_name city country_code }
} } } }`;

export function usePickups() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["pickups", keyExtra(ctx)],
    queryFn: async () => page(await graphqlEdges<Pickup>(ctx, PICKUPS_QUERY, "pickups")),
    enabled: Boolean(ctx.token),
  });
}

// --- Document templates -----------------------------------------------------
const DOCUMENT_TEMPLATES_QUERY = `query { document_templates { edges { node {
  id name slug description related_object active
} } } }`;

export function useDocumentTemplates() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["document-templates", keyExtra(ctx)],
    queryFn: async () => page(await graphqlEdges<DocumentTemplate>(ctx, DOCUMENT_TEMPLATES_QUERY, "document_templates")),
    enabled: Boolean(ctx.token),
  });
}

// --- Manifests (shipment_count derived from shipment_identifiers) -----------
const MANIFESTS_QUERY = `query { manifests { edges { node {
  id carrier_name reference created_at manifest_url shipment_identifiers
} } } }`;

type RawManifest = Omit<Manifest, "shipment_count"> & { shipment_identifiers?: string[] };

export function useManifests() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["manifests", keyExtra(ctx)],
    queryFn: async () => {
      const raws = await graphqlEdges<RawManifest>(ctx, MANIFESTS_QUERY, "manifests");
      return page(raws.map((m) => ({ ...m, shipment_count: m.shipment_identifiers?.length ?? 0 })));
    },
    enabled: Boolean(ctx.token),
  });
}

// --- Batch operations (total derived from resources) ------------------------
const BATCHES_QUERY = `query { batch_operations { edges { node {
  id status resource_type created_at resources { id }
} } } }`;

type RawBatch = Omit<BatchOperation, "total"> & { resources?: Array<{ id: string }> };

export function useBatches() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["batches", keyExtra(ctx)],
    queryFn: async () => {
      const raws = await graphqlEdges<RawBatch>(ctx, BATCHES_QUERY, "batch_operations");
      return page(raws.map((b) => ({ ...b, total: b.resources?.length ?? 0 })));
    },
    enabled: Boolean(ctx.token),
  });
}
