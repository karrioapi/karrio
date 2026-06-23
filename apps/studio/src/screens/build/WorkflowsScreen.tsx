// WorkflowsScreen.tsx — Build › Workflows (automation; dashboard parity).
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useWorkflows } from "~/lib/karrio/hooks";
import type { Workflow } from "~/lib/karrio/types";

export function WorkflowsScreen() {
  const [preview, setPreview] = useState<Workflow | null>(null);
  const { data, isLoading, isError, error } = useWorkflows();
  const rows = useMemo(() => data ?? [], [data]);

  return (
    <div className="page" data-testid="screen-workflows">
      <PageHeader title="Workflows" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Create workflow</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Name</th><th>Trigger</th><th>Actions</th><th>Status</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading workflows…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No workflows yet." />}
            {rows.map((w) => (
              <tr key={w.id} onClick={() => setPreview(w)} data-testid={`workflow-row-${w.id}`}>
                <td className="recipient-name">{w.name}</td>
                <td className="muted">{w.trigger ?? "—"}</td>
                <td>{w.action_count ?? 0}</td>
                <td><span className={"pill " + (w.is_active ? "delivered" : "cancelled")}>{w.is_active ? "active" : "off"}</span></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={rows.length} noun="workflows" />
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Workflows" title={preview.name} id={preview.id}>
          <div className="sheet-body-pad" data-testid="workflow-sheet-body">
            <Section title="Basics">
              <KVGrid>
                <KV label="Name">{preview.name}</KV>
                <KV label="Trigger">{preview.trigger ?? "—"}</KV>
                <KV label="Actions">{preview.action_count ?? 0}</KV>
                <KV label="Active">{preview.is_active ? "Yes" : "No"}</KV>
              </KVGrid>
              {preview.description && <p className="muted" style={{ fontSize: 12.5, marginTop: 10 }}>{preview.description}</p>}
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
