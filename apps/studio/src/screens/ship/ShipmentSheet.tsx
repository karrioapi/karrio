// ShipmentSheet.tsx — right-drawer detail view for a shipment (C2).
import { useState } from "react";
import { Sheet } from "~/components/ui/Sheet";
import { Icon } from "~/components/ui/icons";
import { AddressCard, KV, KVGrid, Section } from "~/components/ui/detail";
import { StatusPill } from "~/components/ui/primitives";
import { CARRIERS } from "~/components/ui/CarrierLogo";
import { carrierKey, formatDate, formatRate } from "~/lib/karrio/display";
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
  const carrier = CARRIERS[carrierKey(shipment.carrier_name)]?.name ?? shipment.carrier_name ?? "—";

  return (
    <Sheet
      open={!!shipment}
      onClose={onClose}
      size="md"
      fullscreen={fullscreen}
      onToggleFullscreen={() => setFullscreen((v) => !v)}
      crumb="Shipments"
      title={`${rate} · ${shipment.service ?? "—"}`}
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
            <KV label="Service">{shipment.service ?? "—"}</KV>
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

        {shipment.selected_rate && (
          <Section title="Charges">
            <div style={{ border: "1px solid var(--border)", borderRadius: "var(--r-md)", overflow: "hidden" }}>
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
            <dd className="mono" style={{ margin: 0, fontSize: 12 }}>{shipment.carrier_id ?? "—"}</dd>
          </dl>
        </Section>
      </div>
    </Sheet>
  );
}
