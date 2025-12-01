import { useMutation } from "@tanstack/react-query";
import { useSyncedSession } from "./session";
import { useAPIMetadata } from "./api-metadata";

export type ResourceType = "shipment" | "manifest" | "order" | "template" | "document";
export type AccessType = "label" | "invoice" | "manifest" | "render" | "batch_labels" | "batch_invoices" | "batch_manifests";
export type FormatType = "pdf" | "png" | "zpl" | "gif";

export interface ResourceTokenRequest {
  resource_type: ResourceType;
  resource_ids: string[];
  access: AccessType[];
  format?: FormatType;
  expires_in?: number;
}

export interface ResourceTokenResponse {
  token: string;
  expires_at: string;
  resource_urls: Record<string, string>;
}

export function useResourceToken() {
  const { getHost } = useAPIMetadata();
  const { query: sessionQuery } = useSyncedSession();
  const session = sessionQuery.data as { accessToken?: string; orgId?: string };

  return useMutation({
    mutationFn: async (request: ResourceTokenRequest): Promise<ResourceTokenResponse> => {
      const host = getHost?.() || "";
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(session?.accessToken && { Authorization: `Bearer ${session.accessToken}` }),
        ...(session?.orgId && { "x-org-id": session.orgId }),
      };

      const response = await fetch(`${host}/api/tokens`, {
        method: "POST",
        headers,
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || error.message || "Failed to generate token");
      }

      return response.json();
    },
  });
}

export function useDocumentPrinter() {
  const { getHost } = useAPIMetadata();
  const tokenMutation = useResourceToken();

  // Helper to build clean URLs without double slashes
  const buildUrl = (resourceUrl: string) => {
    const host = (getHost?.() || "").replace(/\/$/, ""); // Remove trailing slash
    return `${host}${resourceUrl}`;
  };

  const openShipmentLabel = async (
    shipmentId: string,
    opts: { format?: FormatType; doc?: "label" | "invoice" } = {},
  ) => {
    const { format = "pdf", doc = "label" } = opts;

    const result = await tokenMutation.mutateAsync({
      resource_type: "shipment",
      resource_ids: [shipmentId],
      access: [doc],
      format,
    });

    const url = buildUrl(result.resource_urls[shipmentId]);
    window.open(url, "_blank");
  };

  const openBatchLabels = async (
    shipmentIds: string[],
    opts: { format?: FormatType; doc?: "label" | "invoice" } = {},
  ) => {
    const { format = "pdf", doc = "label" } = opts;

    const accessType = doc === "label" ? "batch_labels" : "batch_invoices";
    const result = await tokenMutation.mutateAsync({
      resource_type: "document",
      resource_ids: shipmentIds,
      access: [accessType],
      format,
    });

    const url = buildUrl(result.resource_urls.batch);
    window.open(url, "_blank");
  };

  const openManifest = async (
    manifestId: string,
    opts: { format?: FormatType } = {},
  ) => {
    const { format = "pdf" } = opts;

    const result = await tokenMutation.mutateAsync({
      resource_type: "manifest",
      resource_ids: [manifestId],
      access: ["manifest"],
      format,
    });

    const url = buildUrl(result.resource_urls[manifestId]);
    window.open(url, "_blank");
  };

  const openBatchManifests = async (
    manifestIds: string[],
    opts: { format?: FormatType } = {},
  ) => {
    const { format = "pdf" } = opts;

    const result = await tokenMutation.mutateAsync({
      resource_type: "document",
      resource_ids: manifestIds,
      access: ["batch_manifests"],
      format,
    });

    const url = buildUrl(result.resource_urls.batch);
    window.open(url, "_blank");
  };

  const openOrderLabels = async (
    orderIds: string[],
    opts: { format?: FormatType; doc?: "label" | "invoice" } = {},
  ) => {
    const { format = "pdf", doc = "label" } = opts;

    const accessType = doc === "label" ? "batch_labels" : "batch_invoices";
    const result = await tokenMutation.mutateAsync({
      resource_type: "order",
      resource_ids: orderIds,
      access: [accessType],
      format,
    });

    const url = buildUrl(result.resource_urls.batch);
    window.open(url, "_blank");
  };

  const openTemplate = async (
    templateId: string,
    params?: Record<string, string>,
  ) => {
    const result = await tokenMutation.mutateAsync({
      resource_type: "template",
      resource_ids: [templateId],
      access: ["render"],
    });

    const baseUrl = buildUrl(result.resource_urls[templateId]);
    const url = params
      ? `${baseUrl}&${new URLSearchParams(params).toString()}`
      : baseUrl;
    window.open(url, "_blank");
  };

  return {
    openShipmentLabel,
    openBatchLabels,
    openManifest,
    openBatchManifests,
    openOrderLabels,
    openTemplate,
    isLoading: tokenMutation.isPending,
    error: tokenMutation.error,
  };
}
