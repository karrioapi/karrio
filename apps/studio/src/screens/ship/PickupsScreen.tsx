// PickupsScreen.tsx — Ship › Pickups (C5). REST /v1/pickups.
import { useMemo, useState } from "react";
import { CARRIERS, CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, StatusPill, TableFooter } from "~/components/ui/primitives";
import { AddressCard, KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { usePickups } from "~/lib/karrio/hooks";
import { carrierKey } from "~/lib/karrio/display";
import type { Pickup } from "~/lib/karrio/types";

export function PickupsScreen() {
  const [preview, setPreview] = useState<Pickup | null>(null);
  const { data, isLoading, isError, error } = usePickups();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-pickups">
      <PageHeader title="Pickups" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Schedule pickup</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Carrier</th><th>Confirmation</th><th>Date</th><th>Window</th><th>Status</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={6} kind="loading" message="Loading pickups…" />}
            {isError && !isLoading && <StateRow colSpan={6} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={6} kind="empty" message="No pickups scheduled." />}
            {rows.map((p) => (
              <tr key={p.id} onClick={() => setPreview(p)} data-testid={`pickup-row-${p.id}`}>
                <td>
                  <div className="svc-cell">
                    <CarrierLogo carrier={carrierKey(p.carrier_name)} />
                    <div className="svc-id">{CARRIERS[carrierKey(p.carrier_name)]?.name ?? p.carrier_name ?? "—"}</div>
                  </div>
                </td>
                <td className="mono" style={{ fontSize: 12 }}>{p.confirmation_number ?? "—"}</td>
                <td className="muted" style={{ fontSize: 12 }}>{p.pickup_date ?? "—"}</td>
                <td className="muted" style={{ fontSize: 12 }}>{[p.ready_time, p.closing_time].filter(Boolean).join("–") || "—"}</td>
                <td><StatusPill status={p.status} /></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="pickups" />
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Pickups" title={preview.confirmation_number ?? "Pickup"} id={preview.id} headRight={<StatusPill status={preview.status} />}>
          <div className="sheet-body-pad" data-testid="pickup-sheet-body">
            <Section title="Details">
              <KVGrid>
                <KV label="Carrier">{preview.carrier_name ?? "—"}</KV>
                <KV label="Confirmation" mono>{preview.confirmation_number ?? "—"}</KV>
                <KV label="Date">{preview.pickup_date ?? "—"}</KV>
                <KV label="Window">{[preview.ready_time, preview.closing_time].filter(Boolean).join(" – ") || "—"}</KV>
              </KVGrid>
            </Section>
            <Section title="Pickup address">
              <AddressCard label="Address" addr={preview.address} />
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
