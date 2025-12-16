import { References } from "@karrio/types";

/**
 * Utility functions for carrier detection and compatibility checks
 */

/**
 * Check if a carrier connection is a generic/custom carrier
 */
export function isGenericCarrier(connection: any): boolean {
  return connection.carrier_name === "generic" || !!connection.credentials?.custom_carrier_name;
}

/**
 * Get the effective carrier name for service lookups
 * For generic carriers, returns the custom_carrier_name if available, otherwise "generic"
 */
export function getEffectiveCarrierName(connection: any) {
  return isGenericCarrier(connection) ? "generic" : connection.carrier_name;
}

/**
 * Get the canonical carrier name for rate sheets linkage.
 * For generic/custom carriers we always use the base "generic" so
 * rate sheets attach to the shared generic carrier namespace and
 * default data loads correctly.
 */
export function getRateSheetCarrierName(connection: any): string {
  return isGenericCarrier(connection) ? "generic" : connection.carrier_name;
}

/**
 * Normalize a carrier name against references; if it's not a known enum, fallback to "generic".
 */
export function normalizeCarrierEnumName(name: string, references?: References): string {
  if (!references) return name;
  const known = references.ratesheets?.[name] || (references as any).carriers?.[name];
  return known ? name : "generic";
}

/**
 * Check if a carrier connection supports rate sheets
 * Uses both ratesheets and custom_carriers from references
 */
export function supportsRateSheets(connection: any, references?: References): boolean {
  if (!references) return false;

  const carrierName = getRateSheetCarrierName(connection);
  const effectiveCarrierName = getEffectiveCarrierName(connection);

  // Check if it's a known carrier with ratesheets
  if (references.ratesheets?.[carrierName]) {
    return true;
  }

  // Check if it's a custom carrier defined in references
  if (isGenericCarrier(connection)) {
    // For generic carriers, check if the custom carrier name is in custom_carriers
    if (effectiveCarrierName !== "generic" && references.custom_carriers?.[effectiveCarrierName]) {
      return true;
    }

    // Always allow rate sheets for generic carriers (they can define their own services)
    return true;
  }

  return false;
}

/**
 * Rate sheet defaults structure with shared zones format
 */
export interface RateSheetDefaults {
  zones: Array<{
    id: string;
    label?: string;
    country_codes?: string[];
    postal_codes?: string[];
    cities?: string[];
    transit_days?: number;
    transit_time?: number;
    radius?: number;
    latitude?: number;
    longitude?: number;
  }>;
  services: Array<any & { zone_ids: string[]; surcharge_ids: string[] }>;
  service_rates: Array<{
    service_id: string;
    zone_id: string;
    rate: number;
    cost?: number;
    min_weight?: number;
    max_weight?: number;
    transit_days?: number;
    transit_time?: number;
  }>;
}

/**
 * Get rate sheet defaults for a carrier connection
 * Returns the new shared zones format (zones, services, service_rates)
 */
export function getCarrierRateSheetDefaults(connection: any, references?: References): RateSheetDefaults | null {
  if (!references) return null;

  const carrierName = getRateSheetCarrierName(connection);
  const effectiveCarrierName = getEffectiveCarrierName(connection);

  // First check ratesheets for the main carrier name
  if (references.ratesheets?.[carrierName]) {
    return references.ratesheets[carrierName] as unknown as RateSheetDefaults;
  }

  // For generic/custom carriers, check custom_carriers
  if (isGenericCarrier(connection) && effectiveCarrierName !== "generic") {
    if (references.custom_carriers?.[effectiveCarrierName]) {
      return references.custom_carriers[effectiveCarrierName] as unknown as RateSheetDefaults;
    }
  }

  // Return null if no defaults found
  return null;
}

/**
 * Get service defaults for a carrier connection (legacy - returns services array)
 * @deprecated Use getCarrierRateSheetDefaults instead for the full rate sheet format
 */
export function getCarrierServiceDefaults(connection: any, references?: References): any[] {
  const defaults = getCarrierRateSheetDefaults(connection, references);
  return defaults?.services || [];
}

/**
 * Get the display name for a carrier connection
 */
export function getCarrierDisplayName(connection: any): string {
  if (connection.display_name) {
    return connection.display_name;
  }

  if (isGenericCarrier(connection)) {
    return connection.credentials?.custom_carrier_name || "Custom Carrier";
  }

  return connection.carrier_name || "Unknown Carrier";
}

/**
 * Check if two connections are for the same effective carrier
 * Useful for rate sheet matching
 */
export function isSameCarrier(connection1: any, connection2: any): boolean {
  return getEffectiveCarrierName(connection1) === getEffectiveCarrierName(connection2);
}
