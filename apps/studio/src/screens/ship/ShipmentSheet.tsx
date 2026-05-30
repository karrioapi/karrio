// ShipmentSheet.tsx — right-drawer detail view for a shipment (C2).
import { useState } from "react";
import { Sheet } from "~/components/ui/Sheet";
import { Icon } from "~/components/ui/icons";
import { AddressCard, KV, KVGrid, Section } from "~/components/ui/detail";
import { StatusPill } from "~/components/ui/primitives";
import { carrierName, formatDate, formatRate, shipmentCarrier, shipmentService } from "~/lib/karrio/display";
import type { Shipment } from "~/lib/karrio/types";

export function ShipmentSheet({
  shipment,
  onClose,
}: {
  shipment: Shipment | null;
  onClose: () => void;
}) {
  const [fullscreen, setFullscreen] = useState(false);
  if (!shipment) return null;

  const rate = formatRate(shipment);
  const [amount, currency] = rate.split(" ");
  const carrier = carrierName(shipmentCarrier(shipment));
  const service = shipmentService(shipment);
  const charges = shipment.selected_rate?.extra_charges ?? [];
  const cur = shipment.selected_rate?.currency ?? "";
  const parcels = shipment.parcels ?? [];

  return (
    <Sheet
      open={!!shipment}
      onClose={onClose}
      size="md"
      fullscreen={fullscreen}
      onToggleFullscreen={() => setFullscreen((v) => !v)}
      crumb="Shipments"
      title={`${rate} · ${service}`}
      id={shipment.id}
      headRight={<StatusPill status={shipment.status} />}
      footer={
        <>
          <button className="btn"><Icon.Print size={13} /> Print label</button>
          <button className="btn"><Icon.Refresh size={13} /> Refresh tracking</button>
          <div style={{ flex: 1 }} />
          <button className="btn">Cancel shipment</button>
          <button className="btn btn-primary">Open full view</button>
        </>
      }
    >
      <div className="sheet-body-pad" data-testid="shipment-sheet-body">
        <div style={{ display: "flex", alignItems: "baseline", gap: 10, marginBottom: 8 }}>
          <div style={{ fontSize: 28, fontWeight: 600, letterSpacing: "-0.02em", fontVariantNumeric: "tabular-nums" }}>
            {amount}
          </div>
          <div className="muted" style={{ fontSize: 13 }}>{currency}</div>
        </div>

        <Section title="Details">
          <KVGrid>
            <KV label="Shipment ID" mono>{shipment.id}</KV>
            <KV label="Tracking #" mono>{shipment.tracking_number ?? "—"}</KV>
            <KV label="Service">{service}</KV>
            <KV label="Carrier">{carrier}</KV>
            <KV label="Reference" mono>{shipment.reference ?? "—"}</KV>
            <KV label="Created">{formatDate(shipment.created_at)}</KV>
          </KVGrid>
        </Section>

        <Section title="Addresses">
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <AddressCard label="Shipped from" addr={shipment.shipper} />
            <AddressCard label="Shipped to" addr={shipment.recipient} />
          </div>
        </Section>

        {parcels.length > 0 && (
          <Section title="Parcels">
            <div className="card">
              <table className="table">
                <thead><tr><th>Packaging</th><th>Dimensions</th><th style={{ textAlign: "right" }}>Weight</th></tr></thead>
                <tbody>
                  {parcels.map((p, i) => (
                    <tr key={p.id ?? i}>
                      <td>{p.packaging_type ?? "—"}</td>
                      <td className="mono" style={{ fontSize: 12 }}>
                        {p.length != null ? `${p.length} × ${p.width} × ${p.height} ${p.dimension_unit ?? ""}`.trim() : "—"}
                      </td>
                      <td className="mono" style={{ textAlign: "right", fontSize: 12 }}>
                        {p.weight != null ? `${p.weight} ${p.weight_unit ?? ""}` : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Section>
        )}

        {shipment.selected_rate && (
          <Section title="Charges">
            <div style={{ border: "1px solid var(--border)", borderRadius: "var(--r-md)", overflow: "hidden" }}>
              {charges.map((c, i) => (
                <div key={i} style={{ display: "flex", padding: "9px 14px", borderBottom: "1px solid var(--border)", fontSize: 12.5 }}>
                  <span className="muted">{c.name ?? "Charge"}</span>
                  <span className="mono" style={{ marginLeft: "auto" }}>{c.amount != null ? `${c.amount.toFixed(2)} ${c.currency ?? cur}` : "—"}</span>
                </div>
              ))}
              <div style={{ display: "flex", padding: "10px 14px", fontWeight: 600, fontSize: 13 }}>
                <span>Total</span>
                <span className="mono" style={{ marginLeft: "auto" }}>{rate}</span>
              </div>
            </div>
          </Section>
        )}

        <Section title="Connection">
          <dl style={{ display: "grid", gridTemplateColumns: "120px 1fr", gap: "6px 14px", margin: 0 }}>
            <dt className="muted" style={{ fontSize: 12 }}>Carrier</dt>
            <dd style={{ margin: 0, fontSize: 12 }}>{carrier}</dd>
            <dt className="muted" style={{ fontSize: 12 }}>Connection ID</dt>
            <dd className="mono" style={{ margin: 0, fontSize: 12 }}>{shipment.selected_rate?.carrier_id ?? shipment.carrier_id ?? "—"}</dd>
          </dl>
        </Section>
      </div>
    </Sheet>
  );
}
