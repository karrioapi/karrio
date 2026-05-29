// AuditScreen.tsx — Govern › Audit log (E5).
import { useMemo } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { useAuditLog } from "~/lib/karrio/hooks";

export function AuditScreen() {
  const { data, isLoading, isError, error } = useAuditLog();
  const rows = useMemo(() => data?.results ?? [], [data]);
  return (
    <div className="page" data-testid="screen-audit">
      <PageHeader title="Audit log" actions={<button className="btn"><Icon.Download size={14} /> Export</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Event</th><th>Actor</th><th>Description</th><th>When</th></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={4} kind="loading" message="Loading audit log…" />}
            {isError && !isLoading && <StateRow colSpan={4} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={4} kind="empty" message="No events." />}
            {rows.map((e) => (
              <tr key={e.id} data-testid={`audit-row-${e.id}`}>
                <td className="mono" style={{ fontSize: 12 }}>{e.type ?? "—"}</td>
                <td>{e.actor ?? "—"}</td>
                <td className="muted" style={{ fontSize: 12 }}>{e.description ?? "—"}</td>
                <td className="muted" style={{ fontSize: 12, whiteSpace: "nowrap" }}>{e.at ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="events" />
      </div>
    </div>
  );
}
