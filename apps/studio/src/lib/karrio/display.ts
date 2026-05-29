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
  const c = carrier.toLowerCase();
  if (CARRIERS[c]) return c;
  if (c.includes("canada")) return "canpost";
  if (c.includes("fedex")) return "fedex";
  if (c.includes("ups")) return "ups";
  if (c.includes("dhl")) return "dhl";
  if (c.includes("usps")) return "usps";
  return c;
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
