// BatchesScreen.tsx — Ship › Batches (batch operations; dashboard parity).
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, StatusPill, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useBatches } from "~/lib/karrio/hooks";
import { formatDate } from "~/lib/karrio/display";
import type { BatchOperation } from "~/lib/karrio/types";

export function BatchesScreen() {
  const [preview, setPreview] = useState<BatchOperation | null>(null);
  const { data, isLoading, isError, error } = useBatches();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-batches">
      <PageHeader title="Batches" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> New batch</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Batch ID</th><th>Resource</th><th>Items</th><th>Status</th><th>Created</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={6} kind="loading" message="Loading batches…" />}
            {isError && !isLoading && <StateRow colSpan={6} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={6} kind="empty" message="No batch operations yet." />}
            {rows.map((b) => (
              <tr key={b.id} onClick={() => setPreview(b)} data-testid={`batch-row-${b.id}`}>
                <td className="mono" style={{ fontSize: 12 }}>{b.id}</td>
                <td className="muted">{b.resource_type ?? "—"}</td>
                <td>{b.total ?? "—"}</td>
                <td><StatusPill status={b.status} /></td>
                <td className="muted" style={{ fontSize: 12 }}>{formatDate(b.created_at)}</td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="batches" />
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Batches" title={preview.id} id={preview.id} headRight={<StatusPill status={preview.status} />}>
          <div className="sheet-body-pad" data-testid="batch-sheet-body">
            <Section title="Details">
              <KVGrid>
                <KV label="Resource">{preview.resource_type ?? "—"}</KV>
                <KV label="Items">{preview.total ?? "—"}</KV>
                <KV label="Status">{preview.status ?? "—"}</KV>
                <KV label="Created">{formatDate(preview.created_at)}</KV>
              </KVGrid>
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
