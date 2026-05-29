// TeamScreen.tsx — Govern › Team & roles (E3).
import { useMemo } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, StatusPill, TableFooter } from "~/components/ui/primitives";
import { useTeam } from "~/lib/karrio/hooks";

export function TeamScreen() {
  const { data, isLoading, isError, error } = useTeam();
  const rows = useMemo(() => data?.results ?? [], [data]);
  return (
    <div className="page" data-testid="screen-team">
      <PageHeader title="Team & roles" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Invite member</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Member</th><th>Email</th><th>Role</th><th>Status</th></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={4} kind="loading" message="Loading team…" />}
            {isError && !isLoading && <StateRow colSpan={4} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={4} kind="empty" message="No members." />}
            {rows.map((m) => (
              <tr key={m.id} data-testid={`member-row-${m.id}`}>
                <td className="recipient-name">{m.name ?? "—"}</td>
                <td className="mono" style={{ fontSize: 12 }}>{m.email}</td>
                <td><span className="tag">{m.role ?? "member"}</span></td>
                <td><StatusPill status={m.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="members" />
      </div>
    </div>
  );
}
