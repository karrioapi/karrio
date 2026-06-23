// RulesScreen.tsx — Ship › Shipping rules (C7). GraphQL shipping_rules.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useShippingRules } from "~/lib/karrio/hooks";
import type { ShippingRule } from "~/lib/karrio/types";

export function RulesScreen() {
  const [preview, setPreview] = useState<ShippingRule | null>(null);
  const { data, isLoading, isError, error } = useShippingRules();
  const rows = useMemo(() => [...(data ?? [])].sort((a, b) => (b.priority ?? 0) - (a.priority ?? 0)), [data]);

  return (
    <div className="page" data-testid="screen-rules">
      <PageHeader title="Shipping rules" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Create rule</button>} />
      <div
        style={{ border: "1px solid var(--green-bg)", background: "var(--green-bg)", color: "var(--green-fg)", borderRadius: "var(--r-md)", padding: "10px 14px", fontSize: 12.5, marginBottom: 14 }}
        data-testid="rules-banner"
      >
        Rules run top-to-bottom by priority. The first matching rule applies its action.
      </div>
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Priority</th><th>Name</th><th>Action</th><th>Active</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading rules…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No rules yet." />}
            {rows.map((r) => (
              <tr key={r.id} onClick={() => setPreview(r)} data-testid={`rule-row-${r.id}`}>
                <td className="mono">{r.priority ?? "—"}</td>
                <td className="recipient-name">{r.name}</td>
                <td className="muted">{r.action_type ?? "—"}</td>
                <td><span className={"pill " + (r.is_active ? "delivered" : "cancelled")}>{r.is_active ? "active" : "off"}</span></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={rows.length} noun="rules" />
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Shipping rules" title={preview.name} id={preview.id}>
          <div className="sheet-body-pad" data-testid="rule-sheet-body">
            <Section title="Basics">
              <KVGrid>
                <KV label="Name">{preview.name}</KV>
                <KV label="Priority" mono>{preview.priority ?? "—"}</KV>
                <KV label="Action">{preview.action_type ?? "—"}</KV>
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
