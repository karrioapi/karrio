// TenantsScreen.tsx — Govern › Tenants (E2).
import { useMemo } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, StatusPill, TableFooter } from "~/components/ui/primitives";
import { useTenants } from "~/lib/karrio/hooks";

export function TenantsScreen() {
  const { data, isLoading, isError, error } = useTenants();
  const rows = useMemo(() => data?.results ?? [], [data]);
  return (
    <div className="page" data-testid="screen-tenants">
      <PageHeader title="Tenants" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> New tenant</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Name</th><th>Slug</th><th>Members</th><th>Status</th><th>Created</th></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading tenants…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No tenants." />}
            {rows.map((t) => (
              <tr key={t.id} data-testid={`tenant-row-${t.id}`}>
                <td className="recipient-name">{t.name}</td>
                <td className="mono" style={{ fontSize: 12 }}>{t.slug ?? "—"}</td>
                <td>{t.members ?? "—"}</td>
                <td><StatusPill status={t.status} /></td>
                <td className="muted" style={{ fontSize: 12 }}>{t.created ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="tenants" />
      </div>
    </div>
  );
}
