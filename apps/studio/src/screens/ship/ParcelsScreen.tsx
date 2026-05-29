// ParcelsScreen.tsx — Ship › Parcels (C9). GraphQL parcel templates.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useParcels } from "~/lib/karrio/hooks";
import type { ParcelTemplate } from "~/lib/karrio/types";

const dims = (p: ParcelTemplate) =>
  p.length != null ? `${p.length} × ${p.width} × ${p.height} ${p.dimension_unit ?? ""}`.trim() : "—";

export function ParcelsScreen() {
  const [preview, setPreview] = useState<ParcelTemplate | null>(null);
  const { data, isLoading, isError, error } = useParcels();
  const rows = useMemo(() => data ?? [], [data]);

  return (
    <div className="page" data-testid="screen-parcels">
      <PageHeader title="Parcels" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Create parcel</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Label</th><th>Packaging</th><th>Dimensions</th><th>Weight</th><th>Default</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={6} kind="loading" message="Loading parcels…" />}
            {isError && !isLoading && <StateRow colSpan={6} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={6} kind="empty" message="No parcels yet." />}
            {rows.map((p) => (
              <tr key={p.id} onClick={() => setPreview(p)} data-testid={`parcel-row-${p.id}`}>
                <td className="recipient-name">{p.label ?? "—"}</td>
                <td className="muted">{p.packaging_type ?? "—"}</td>
                <td className="mono" style={{ fontSize: 12 }}>{dims(p)}</td>
                <td className="mono" style={{ fontSize: 12 }}>{p.weight != null ? `${p.weight} ${p.weight_unit ?? ""}` : "—"}</td>
                <td>{p.is_default ? <Icon.Check size={14} /> : ""}</td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={rows.length} noun="parcels" />
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Parcels" title={preview.label ?? "Parcel"} id={preview.id}>
          <div className="sheet-body-pad" data-testid="parcel-sheet-body">
            <Section title="Specs">
              <KVGrid>
                <KV label="Packaging">{preview.packaging_type ?? "—"}</KV>
                <KV label="Dimensions" mono>{dims(preview)}</KV>
                <KV label="Weight" mono>{preview.weight != null ? `${preview.weight} ${preview.weight_unit ?? ""}` : "—"}</KV>
                <KV label="Default">{preview.is_default ? "Yes" : "No"}</KV>
              </KVGrid>
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
