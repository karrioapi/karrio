// CarrierLogo.tsx — square carrier badge (ported from the design handoff)

export const CARRIERS: Record<string, { name: string; bg: string; fg: string; abbr: string }> = {
  ups: { name: "UPS", bg: "#351B0E", fg: "#FFB81C", abbr: "UPS" },
  fedex: { name: "FedEx", bg: "#4D148C", fg: "#FF6600", abbr: "FDX" },
  dhl: { name: "DHL", bg: "#FFCC00", fg: "#D40511", abbr: "DHL" },
  usps: { name: "USPS", bg: "#004B87", fg: "#fff", abbr: "USPS" },
  canpost: { name: "Canada Post", bg: "#EE2D24", fg: "#fff", abbr: "CP" },
  purolator: { name: "Purolator", bg: "#1C3F94", fg: "#fff", abbr: "PUR" },
  royalmail: { name: "Royal Mail", bg: "#E60000", fg: "#fff", abbr: "RM" },
  landmark: { name: "Landmark", bg: "#E0153A", fg: "#fff", abbr: "LM" },
  smartkargo: { name: "SmartKargo", bg: "#FFFFFF", fg: "#1A66B5", abbr: "SK" },
  dpd: { name: "DPD", bg: "#DC0032", fg: "#fff", abbr: "DPD" },
  australia: { name: "Australia Post", bg: "#D70000", fg: "#fff", abbr: "AUS" },
  tnt: { name: "TNT", bg: "#FF6600", fg: "#fff", abbr: "TNT" },
  aramex: { name: "Aramex", bg: "#E10A17", fg: "#fff", abbr: "ARX" },
};

export function CarrierLogo({
  carrier,
  size = "md",
}: {
  carrier: string;
  size?: "sm" | "md" | "lg";
}) {
  const meta = CARRIERS[carrier] || { bg: "#52525B", fg: "#fff", abbr: "?" };
  return (
    <div
      className={"carrier-logo " + (size === "sm" ? "sm" : size === "lg" ? "lg" : "")}
      style={{
        background: meta.bg,
        color: meta.fg,
        border: meta.bg === "#FFFFFF" ? "1px solid var(--border)" : "none",
      }}
    >
      {meta.abbr}
    </div>
  );
}
