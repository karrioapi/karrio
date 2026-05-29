// OrderSheet.tsx — right-drawer detail view for an order (C4).
import { useState } from "react";
import { Sheet } from "~/components/ui/Sheet";
import { AddressCard, KV, KVGrid, Section } from "~/components/ui/detail";
import { StatusPill } from "~/components/ui/primitives";
import { formatDate } from "~/lib/karrio/display";
import type { Order } from "~/lib/karrio/types";

export function OrderSheet({ order, onClose }: { order: Order | null; onClose: () => void }) {
  const [fullscreen, setFullscreen] = useState(false);
  if (!order) return null;

  return (
    <Sheet
      open={!!order}
      onClose={onClose}
      size="md"
      fullscreen={fullscreen}
      onToggleFullscreen={() => setFullscreen((v) => !v)}
      crumb="Orders"
      title={order.order_id ?? order.id}
      id={order.id}
      headRight={<StatusPill status={order.status} />}
      footer={
        <>
          <div style={{ flex: 1 }} />
          <button className="btn">Create shipment</button>
          <button className="btn btn-primary">Open full view</button>
        </>
      }
    >
      <div className="sheet-body-pad" data-testid="order-sheet-body">
        <Section title="Details">
          <KVGrid>
            <KV label="Order" mono>{order.order_id ?? order.id}</KV>
            <KV label="Source">{order.source ?? "—"}</KV>
            <KV label="Status">{order.status}</KV>
            <KV label="Created">{formatDate(order.created_at)}</KV>
          </KVGrid>
        </Section>

        <Section title="Ship to">
          <AddressCard label="Customer" addr={order.shipping_to} />
        </Section>

        <Section title="Line items">
          <div className="card">
            <table className="table">
              <thead>
                <tr><th>Item</th><th style={{ textAlign: "right" }}>Qty</th></tr>
              </thead>
              <tbody>
                {(order.line_items ?? []).length === 0 && (
                  <tr><td colSpan={2}><div className="state-row">No line items.</div></td></tr>
                )}
                {(order.line_items ?? []).map((li) => (
                  <tr key={li.id}>
                    <td>{li.title ?? li.id}</td>
                    <td style={{ textAlign: "right" }} className="mono">{li.quantity ?? 1}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      </div>
    </Sheet>
  );
}
