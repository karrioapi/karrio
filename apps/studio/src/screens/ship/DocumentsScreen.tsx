// DocumentsScreen.tsx — Ship › Documents (C11). REST document templates.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useDocumentTemplates } from "~/lib/karrio/hooks";
import type { DocumentTemplate } from "~/lib/karrio/types";

export function DocumentsScreen() {
  const [preview, setPreview] = useState<DocumentTemplate | null>(null);
  const { data, isLoading, isError, error } = useDocumentTemplates();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-documents">
      <PageHeader title="Documents" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Create template</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Name</th><th>Slug</th><th>Related to</th><th>Active</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading templates…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No templates yet." />}
            {rows.map((d) => (
              <tr key={d.id} onClick={() => setPreview(d)} data-testid={`document-row-${d.id}`}>
                <td className="recipient-name">{d.name}</td>
                <td className="mono" style={{ fontSize: 12 }}>{d.slug ?? "—"}</td>
                <td className="muted">{d.related_object ?? "—"}</td>
                <td><span className={"pill " + (d.active ? "delivered" : "cancelled")}>{d.active ? "active" : "off"}</span></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="templates" />
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="lg" crumb="Documents" title={preview.name} id={preview.id}>
          <div className="sheet-body-pad" data-testid="document-sheet-body">
            <Section title="Template">
              <KVGrid>
                <KV label="Name">{preview.name}</KV>
                <KV label="Slug" mono>{preview.slug ?? "—"}</KV>
                <KV label="Related object">{preview.related_object ?? "—"}</KV>
                <KV label="Active">{preview.active ? "Yes" : "No"}</KV>
              </KVGrid>
              {preview.description && <p className="muted" style={{ fontSize: 12.5, marginTop: 10 }}>{preview.description}</p>}
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
