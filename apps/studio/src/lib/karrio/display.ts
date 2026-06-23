// display.ts — map Karrio API entities to display strings for Studio screens.
import { CARRIERS } from "~/components/ui/CarrierLogo";
import type { Address, Shipment } from "~/lib/karrio/types";

const PILL_CLASSES = new Set([
  "created",
  "purchased",
  "delivered",
  "pending",
  "cancelled",
  "exception",
  "failed",
  "draft",
  "intransit",
]);

// Normalize a Karrio status to a pill CSS class.
export function statusClass(status?: string): string {
  if (!status) return "default";
  const s = status.toLowerCase().replace(/[\s_-]+/g, "");
  if (s === "intransit" || s === "transit") return "intransit";
  if (s === "canceled") return "cancelled";
  return PILL_CLASSES.has(s) ? s : "default";
}

export function statusLabel(status?: string): string {
  if (!status) return "unknown";
  return status.replace(/_/g, " ");
}

// Carrier key for the CarrierLogo badge (best-effort match against CARRIERS).
export function carrierKey(carrier?: string): string {
  if (!carrier) return "";
  const c = carrier.toLowerCase().replace(/[\s-]+/g, "_");
  if (CARRIERS[c]) return c;
  if (c.includes("canada") || c.includes("canpost")) return "canpost";
  if (c.includes("fedex")) return "fedex";
  if (c.includes("ups")) return "ups";
  if (c.includes("dhl")) return "dhl";
  if (c.includes("usps") || c.includes("postal")) return "usps";
  if (c.includes("purolator")) return "purolator";
  if (c.includes("royal")) return "royalmail";
  if (c.includes("landmark")) return "landmark";
  if (c.includes("smartkargo")) return "smartkargo";
  if (c.includes("dpd")) return "dpd";
  if (c.includes("australia") || c.includes("aupost")) return "australia";
  if (c.includes("tnt")) return "tnt";
  if (c.includes("aramex")) return "aramex";
  return c;
}

// Carrier display name from any slug/name (humanized fallback for unknowns).
export function carrierName(carrier?: string): string {
  if (!carrier) return "—";
  const key = carrierKey(carrier);
  return CARRIERS[key]?.name ?? carrier.replace(/[_-]+/g, " ").replace(/\b\w/g, (ch) => ch.toUpperCase());
}

// Carrier for a shipment: top-level field, else the selected rate.
export function shipmentCarrier(s: { carrier_name?: string; selected_rate?: { carrier_name?: string } | null }): string {
  return s.carrier_name || s.selected_rate?.carrier_name || "";
}

// Service label for a shipment (rate-first), humanized.
export function shipmentService(s: { service?: string; selected_rate?: { service?: string } | null }): string {
  const svc = s.service || s.selected_rate?.service || "";
  return svc ? svc.replace(/[_-]+/g, " ").replace(/\b\w/g, (ch) => ch.toUpperCase()) : "—";
}

export function formatRate(shipment: Shipment): string {
  const rate = shipment.selected_rate;
  if (!rate || rate.total_charge == null) return "—";
  return `${rate.total_charge.toFixed(2)} ${rate.currency ?? ""}`.trim();
}

export function recipientName(addr?: Address): string {
  return addr?.person_name || addr?.company_name || "—";
}

export function recipientAddr(addr?: Address): string {
  return [addr?.city, addr?.state_code, addr?.country_code].filter(Boolean).join(", ");
}

export function formatDate(iso?: string): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
