// references.ts — Karrio API metadata (`/v1/references`): the carrier registry,
// per-carrier connection field schemas (for dynamic credential forms), and the
// deployment feature flags. This is the same metadata the dashboard's
// useAPIMetadata consumes; it drives dynamic connection forms (EBE-110) and
// feature-flag gating (EBE-109).
import { useQuery } from "@tanstack/react-query";
import { restGet } from "~/lib/karrio/client";
import { useKarrioCtx } from "~/lib/karrio/session";
import { keyExtra } from "~/lib/karrio/hooks/_shared";

export type ConnectionFieldType = "string" | "number" | "boolean" | "object" | string;

export type ConnectionField = {
  name: string;
  label?: string;
  type: ConnectionFieldType;
  required?: boolean;
  sensitive?: boolean;
  default?: unknown;
  enum?: string[];
};

export type References = {
  VERSION?: string;
  APP_NAME?: string;
  /** carrier_name → display name */
  carriers?: Record<string, string>;
  /** carrier_name → { field_name → field schema } */
  connection_fields?: Record<string, Record<string, ConnectionField>>;
  // Feature flags (gate EE / optional modules)
  MULTI_ORGANIZATIONS?: boolean;
  ORDERS_MANAGEMENT?: boolean;
  APPS_MANAGEMENT?: boolean;
  DOCUMENTS_MANAGEMENT?: boolean;
  DATA_IMPORT_EXPORT?: boolean;
  WORKFLOW_MANAGEMENT?: boolean;
  SHIPPING_RULES?: boolean;
  ADMIN_DASHBOARD?: boolean;
  ALLOW_SIGNUP?: boolean;
  AUDIT_LOGGING?: boolean;
  [key: string]: unknown;
};

export function useReferences() {
  const ctx = useKarrioCtx();
  return useQuery({
    queryKey: ["references", keyExtra(ctx)],
    queryFn: () => restGet<References>(ctx, "/v1/references"),
    enabled: Boolean(ctx.token),
    staleTime: 60 * 60_000, // metadata is stable for the session
  });
}

// --- Feature flags (EBE-109) ------------------------------------------------
export type FeatureFlag =
  | "MULTI_ORGANIZATIONS"
  | "ORDERS_MANAGEMENT"
  | "APPS_MANAGEMENT"
  | "DOCUMENTS_MANAGEMENT"
  | "DATA_IMPORT_EXPORT"
  | "WORKFLOW_MANAGEMENT"
  | "SHIPPING_RULES"
  | "ADMIN_DASHBOARD"
  | "AUDIT_LOGGING";

/**
 * Read deployment feature flags from the references payload. Defaults to `true`
 * for unknown flags so a screen never hides itself before metadata loads; gate
 * EE/optional features with an explicit `false`.
 */
export function useFeatureFlags() {
  const { data } = useReferences();
  return {
    flags: data,
    isEnabled: (flag: FeatureFlag): boolean => (data ? data[flag] !== false : true),
  };
}
