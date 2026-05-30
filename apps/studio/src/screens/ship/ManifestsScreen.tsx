// ManifestsScreen.tsx — Ship › Manifests (dashboard parity).
import { useMemo, useState } from "react";
import { CARRIERS, CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useManifests } from "~/lib/karrio/hooks";
import { carrierKey, formatDate } from "~/lib/karrio/display";
import type { Manifest } from "~/lib/karrio/types";

export function ManifestsScreen() {
  const [preview, setPreview] = useState<Manifest | null>(null);
  const { data, isLoading, isError, error } = useManifests();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-manifests">
      <PageHeader title="Manifests" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Create manifest</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Carrier</th><th>Reference</th><th>Shipments</th><th>Created</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading manifests…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No manifests yet." />}
            {rows.map((mf) => (
              <tr key={mf.id} onClick={() => setPreview(mf)} data-testid={`manifest-row-${mf.id}`}>
                <td>
                  <div className="svc-cell">
                    <CarrierLogo carrier={carrierKey(mf.carrier_name)} />
                    <div className="svc-id">{CARRIERS[carrierKey(mf.carrier_name)]?.name ?? mf.carrier_name ?? "—"}</div>
                  </div>
                </td>
                <td className="mono" style={{ fontSize: 12 }}>{mf.reference ?? "—"}</td>
                <td>{mf.shipment_count ?? "—"}</td>
                <td className="muted" style={{ fontSize: 12 }}>{formatDate(mf.created_at)}</td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="manifests" />
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Manifests" title={preview.reference ?? "Manifest"} id={preview.id}
          footer={preview.manifest_url ? <><div style={{ flex: 1 }} /><button className="btn btn-primary"><Icon.Download size={13} /> Download</button></> : undefined}>
          <div className="sheet-body-pad" data-testid="manifest-sheet-body">
            <Section title="Details">
              <KVGrid>
                <KV label="Carrier">{preview.carrier_name ?? "—"}</KV>
                <KV label="Reference" mono>{preview.reference ?? "—"}</KV>
                <KV label="Shipments">{preview.shipment_count ?? "—"}</KV>
                <KV label="Created">{formatDate(preview.created_at)}</KV>
              </KVGrid>
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
