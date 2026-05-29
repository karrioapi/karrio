// ConnectionsScreen.tsx — Ship › Connections (C6).
import { useMemo, useState } from "react";
import { CARRIERS, CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useCarrierConnections } from "~/lib/karrio/hooks";
import { carrierKey } from "~/lib/karrio/display";
import type { CarrierConnection } from "~/lib/karrio/types";

export function ConnectionsScreen() {
  const [preview, setPreview] = useState<CarrierConnection | null>(null);
  const { data, isLoading, isError, error } = useCarrierConnections();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-connections">
      <PageHeader
        title="Connections"
        actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Add connection</button>}
      />
      <div className="card card-scroll">
        <table className="table">
          <thead>
            <tr><th>Carrier</th><th>Account ID</th><th>Mode</th><th>Status</th><th className="actions-cell" /></tr>
          </thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading connections…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No connections yet." />}
            {rows.map((c) => (
              <tr key={c.id} onClick={() => setPreview(c)} data-testid={`connection-row-${c.id}`}>
                <td>
                  <div className="svc-cell">
                    <CarrierLogo carrier={carrierKey(c.carrier_name)} />
                    <div className="svc-id">{CARRIERS[carrierKey(c.carrier_name)]?.name ?? c.carrier_name}</div>
                  </div>
                </td>
                <td className="mono" style={{ fontSize: 12 }}>{c.carrier_id}</td>
                <td><span className={"pill " + (c.test_mode ? "draft" : "purchased")}>{c.test_mode ? "test" : "live"}</span></td>
                <td><span className={"pill " + (c.active === false ? "cancelled" : "delivered")}>{c.active === false ? "inactive" : "active"}</span></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="connections" />
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Connections"
          title={CARRIERS[carrierKey(preview.carrier_name)]?.name ?? preview.carrier_name} id={preview.id}>
          <div className="sheet-body-pad" data-testid="connection-sheet-body">
            <Section title="Account">
              <KVGrid>
                <KV label="Carrier">{preview.carrier_name}</KV>
                <KV label="Account ID" mono>{preview.carrier_id}</KV>
                <KV label="Mode">{preview.test_mode ? "Test" : "Live"}</KV>
                <KV label="Status">{preview.active === false ? "Inactive" : "Active"}</KV>
              </KVGrid>
            </Section>
            {preview.capabilities && preview.capabilities.length > 0 && (
              <Section title="Capabilities">
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {preview.capabilities.map((cap) => <span key={cap} className="tag">{cap}</span>)}
                </div>
              </Section>
            )}
          </div>
        </Sheet>
      )}
    </div>
  );
}
