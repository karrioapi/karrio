// TeamScreen.tsx — Govern › Team & roles (E3). Real admin user management:
// invite (create_user), edit role/active (update_user), remove (remove_user)
// via the ADMIN GraphQL schema. (EBE-108)
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, StatusPill, TableFooter } from "~/components/ui/primitives";
import { Sheet, Field } from "~/components/ui/Sheet";
import { useInviteUser, useRemoveUser, useTeam, useUpdateUser } from "~/lib/karrio/hooks";
import type { TeamMember } from "~/lib/karrio/types";

type Role = "owner" | "admin" | "member";
const ROLES: Role[] = ["owner", "admin", "member"];
const asRole = (r?: string): Role => (r === "owner" || r === "admin" ? r : "member");

type EditorState = "closed" | "invite" | { edit: TeamMember };

export function TeamScreen() {
  const [editor, setEditor] = useState<EditorState>("closed");
  const { data, isLoading, isError, error } = useTeam();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-team">
      <PageHeader
        title="Team & roles"
        actions={
          <button className="btn btn-primary" onClick={() => setEditor("invite")} data-testid="team-invite">
            <Icon.Plus size={14} /> Invite member
          </button>
        }
      />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Member</th><th>Email</th><th>Role</th><th>Status</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading team…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No members." />}
            {rows.map((m) => (
              <tr key={m.id} onClick={() => setEditor({ edit: m })} data-testid={`member-row-${m.id}`}>
                <td className="recipient-name">{m.name ?? "—"}</td>
                <td className="mono" style={{ fontSize: 12 }}>{m.email}</td>
                <td><span className="tag">{m.role ?? "member"}</span></td>
                <td><StatusPill status={m.status} /></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="members" />
      </div>

      {editor !== "closed" && (
        <MemberEditor
          key={editor === "invite" ? "invite" : editor.edit.id}
          member={editor === "invite" ? undefined : editor.edit}
          onClose={() => setEditor("closed")}
        />
      )}
    </div>
  );
}

function MemberEditor({ member, onClose }: { member?: TeamMember; onClose: () => void }) {
  const invite = useInviteUser();
  const update = useUpdateUser();
  const remove = useRemoveUser();

  const [email, setEmail] = useState(member?.email ?? "");
  const [name, setName] = useState(member?.name ?? "");
  const [role, setRole] = useState<Role>(asRole(member?.role));
  const [active, setActive] = useState(member ? member.status !== "inactive" : true);
  const [err, setErr] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    try {
      if (member) {
        await update.mutateAsync({ id: member.id, role, is_active: active, full_name: name });
      } else {
        if (!email.trim()) return setErr("An email address is required.");
        await invite.mutateAsync({ email: email.trim(), full_name: name.trim() || undefined, role });
      }
      onClose();
    } catch (e2) {
      setErr((e2 as Error)?.message ?? "Could not save the member.");
    }
  };

  const onRemove = async () => {
    if (!member) return;
    setErr(null);
    try {
      await remove.mutateAsync(member.id);
      onClose();
    } catch (e2) {
      setErr((e2 as Error)?.message ?? "Could not remove the member.");
    }
  };

  const pending = invite.isPending || update.isPending;

  return (
    <Sheet
      open onClose={onClose} size="sm" crumb="Team & roles"
      title={member ? "Edit member" : "Invite member"} id={member?.id}
      footer={
        <>
          {member && (
            <button className="btn" onClick={onRemove} disabled={remove.isPending} data-testid="member-remove">
              {remove.isPending ? "Removing…" : "Remove"}
            </button>
          )}
          <div style={{ flex: 1 }} />
          <button className="btn" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" form="member-form" type="submit" disabled={pending} data-testid="member-save">
            {pending ? "Saving…" : member ? "Save changes" : "Send invite"}
          </button>
        </>
      }
    >
      <form id="member-form" className="sheet-body-pad" onSubmit={onSubmit} data-testid="member-sheet-body">
        <Field label="Email *">
          <input
            className="field-input" type="email" value={email} disabled={!!member}
            onChange={(e) => setEmail(e.target.value)} data-testid="member-email"
          />
        </Field>
        <Field label="Full name">
          <input className="field-input" value={name} onChange={(e) => setName(e.target.value)} data-testid="member-name" />
        </Field>
        <Field label="Role">
          <select className="field-input" value={role} onChange={(e) => setRole(e.target.value as Role)} data-testid="member-role">
            {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
          </select>
        </Field>
        {member && (
          <Field label="Status">
            <select className="field-input" value={active ? "active" : "inactive"} onChange={(e) => setActive(e.target.value === "active")} data-testid="member-status">
              <option value="active">active</option>
              <option value="inactive">inactive</option>
            </select>
          </Field>
        )}
        {!member && (
          <p className="muted" style={{ fontSize: 12, marginTop: 8 }}>
            An invitation email is sent to set up the account. Roles map to access:
            owner (full), admin (staff), member (standard).
          </p>
        )}
        {err && <div className="auth-error" data-testid="member-form-error">{err}</div>}
      </form>
    </Sheet>
  );
}
