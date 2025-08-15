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
export function getEffectiveCarrierName(connection: any): string {
  if (connection.carrier_name === "generic" && connection.credentials?.custom_carrier_name) {
    return connection.credentials.custom_carrier_name;
  }
  return connection.carrier_name;
}

/**
 * Check if a carrier connection supports rate sheets
 * Uses both service_levels and custom_carriers from references
 */
export function supportsRateSheets(connection: any, references?: References): boolean {
  if (!references) return false;

  const carrierName = connection.carrier_name;
  const effectiveCarrierName = getEffectiveCarrierName(connection);

  // Check if it's a known carrier with service levels
  if (references.service_levels?.[carrierName]) {
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
 * Get service defaults for a carrier connection
 * Checks both service_levels and custom_carriers
 */
export function getCarrierServiceDefaults(connection: any, references?: References): any[] {
  if (!references) return [];

  const carrierName = connection.carrier_name;
  const effectiveCarrierName = getEffectiveCarrierName(connection);

  // First check service_levels for the main carrier name
  if (references.service_levels?.[carrierName]) {
    return references.service_levels[carrierName];
  }

  // For generic/custom carriers, check custom_carriers
  if (isGenericCarrier(connection) && effectiveCarrierName !== "generic") {
    if ((references.custom_carriers?.[effectiveCarrierName] as any)?.services) {
      return (references.custom_carriers[effectiveCarrierName] as any).services;
    }
  }

  // Return empty array if no defaults found
  return [];
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
