// WebhooksScreen.tsx — Build › Webhooks (D6) with create / edit / delete.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter, Toggle } from "~/components/ui/primitives";
import { Sheet, Field } from "~/components/ui/Sheet";
import { useDeleteWebhook, useSaveWebhook, useWebhooks } from "~/lib/karrio/hooks";
import type { Webhook } from "~/lib/karrio/types";

type FormState = "closed" | "create" | { edit: Webhook };

export function WebhooksScreen() {
  const [form, setForm] = useState<FormState>("closed");
  const { data, isLoading, isError, error } = useWebhooks();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-webhooks">
      <PageHeader
        title="Webhooks"
        actions={
          <button className="btn btn-primary" onClick={() => setForm("create")} data-testid="webhook-create">
            <Icon.Plus size={14} /> Add endpoint
          </button>
        }
      />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Endpoint</th><th>Events</th><th>Status</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={4} kind="loading" message="Loading webhooks…" />}
            {isError && !isLoading && <StateRow colSpan={4} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={4} kind="empty" message="No webhooks yet." />}
            {rows.map((w) => (
              <tr key={w.id} onClick={() => setForm({ edit: w })} data-testid={`webhook-row-${w.id}`}>
                <td className="mono" style={{ fontSize: 12 }}>{w.url}</td>
                <td className="muted">{(w.events ?? []).length} event{(w.events ?? []).length === 1 ? "" : "s"}</td>
                <td><span className={"pill " + (w.enabled ? "delivered" : "cancelled")}>{w.enabled ? "enabled" : "disabled"}</span></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="webhooks" />
      </div>

      {form !== "closed" && (
        <WebhookForm key={form === "create" ? "create" : form.edit.id} initial={form === "create" ? undefined : form.edit} onClose={() => setForm("closed")} />
      )}
    </div>
  );
}

function WebhookForm({ initial, onClose }: { initial?: Webhook; onClose: () => void }) {
  const [url, setUrl] = useState(initial?.url ?? "");
  const [events, setEvents] = useState((initial?.events ?? []).join(", "));
  const [description, setDescription] = useState(initial?.description ?? "");
  const [enabled, setEnabled] = useState(initial?.enabled ?? true);
  const [err, setErr] = useState<string | null>(null);

  const save = useSaveWebhook();
  const del = useDeleteWebhook();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (!/^https?:\/\/.+/.test(url.trim())) return setErr("Enter a valid https URL.");
    try {
      await save.mutateAsync({
        id: initial?.id,
        data: {
          url: url.trim(),
          description,
          enabled,
          events: events.split(",").map((s) => s.trim()).filter(Boolean),
        },
      });
      onClose();
    } catch {
      setErr("Could not save the webhook.");
    }
  };

  const onDelete = async () => {
    if (!initial) return;
    try {
      await del.mutateAsync(initial.id);
      onClose();
    } catch {
      setErr("Could not delete the webhook.");
    }
  };

  return (
    <Sheet
      open onClose={onClose} size="md" crumb="Webhooks"
      title={initial ? "Edit endpoint" : "Add endpoint"} id={initial?.id}
      footer={
        <>
          {initial && <button className="btn" onClick={onDelete} disabled={del.isPending} data-testid="webhook-delete">Delete</button>}
          <div style={{ flex: 1 }} />
          <button className="btn" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" form="webhook-form" type="submit" disabled={save.isPending} data-testid="webhook-save">
            {save.isPending ? "Saving…" : "Save"}
          </button>
        </>
      }
    >
      <form id="webhook-form" className="sheet-body-pad" onSubmit={onSubmit} data-testid="webhook-form">
        <Field label="Endpoint URL"><input className="field-input" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://…" data-testid="wf-url" /></Field>
        <Field label="Events (comma-separated)"><input className="field-input" value={events} onChange={(e) => setEvents(e.target.value)} placeholder="shipment_purchased, tracker_updated" data-testid="wf-events" /></Field>
        <Field label="Description"><input className="field-input" value={description} onChange={(e) => setDescription(e.target.value)} /></Field>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 6 }}>
          <Toggle checked={enabled} onChange={setEnabled} label="Enabled" testid="wf-enabled" />
          <span style={{ fontSize: 12.5 }}>Enabled</span>
        </div>
        {err && <div className="auth-error" data-testid="webhook-form-error">{err}</div>}
      </form>
    </Sheet>
  );
}
