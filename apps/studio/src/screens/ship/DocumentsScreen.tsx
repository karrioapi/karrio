// DocumentsScreen.tsx — Ship › Documents (C11). Document template management
// with a real two-pane editor (Liquid/HTML code + live preview), parity with the
// dashboard template editor. (EBE-104)
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, StatusPill, TableFooter } from "~/components/ui/primitives";
import { Sheet, Field } from "~/components/ui/Sheet";
import { useDocumentTemplates, useSaveDocumentTemplate, useDeleteDocumentTemplate } from "~/lib/karrio/hooks";
import { useKarrioCtx } from "~/lib/karrio/session";
import { joinUrl } from "~/lib/karrio/env";
import type { DocumentTemplate } from "~/lib/karrio/types";

type EditorState = "closed" | "create" | { edit: DocumentTemplate };

const STARTER = `<!-- Liquid + HTML. Variables render on the server with sample data. -->
<div style="font-family: sans-serif; padding: 24px">
  <h1>Packing slip</h1>
  <p>Tracking: {{ shipment.tracking_number }}</p>
  <p>To: {{ shipment.recipient.person_name }}</p>
</div>`;

export function DocumentsScreen() {
  const [editor, setEditor] = useState<EditorState>("closed");
  const { data, isLoading, isError, error } = useDocumentTemplates();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-documents">
      <PageHeader
        title="Documents"
        actions={
          <button className="btn btn-primary" onClick={() => setEditor("create")} data-testid="document-create">
            <Icon.Plus size={14} /> New template
          </button>
        }
      />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Name</th><th>Slug</th><th>Related</th><th>Status</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading templates…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No templates yet." />}
            {rows.map((t) => (
              <tr key={t.id} onClick={() => setEditor({ edit: t })} data-testid={`document-row-${t.id}`}>
                <td className="recipient-name">{t.name}</td>
                <td className="mono" style={{ fontSize: 12 }}>{t.slug ?? "—"}</td>
                <td><span className="tag">{t.related_object ?? "other"}</span></td>
                <td><StatusPill status={t.active === false ? "cancelled" : "delivered"} /></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="templates" />
      </div>

      {editor !== "closed" && (
        <DocumentEditor
          key={editor === "create" ? "create" : editor.edit.id}
          initial={editor === "create" ? undefined : editor.edit}
          onClose={() => setEditor("closed")}
        />
      )}
    </div>
  );
}

function DocumentEditor({ initial, onClose }: { initial?: DocumentTemplate; onClose: () => void }) {
  const ctx = useKarrioCtx();
  const [name, setName] = useState(initial?.name ?? "");
  const [slug, setSlug] = useState(initial?.slug ?? "");
  const [related, setRelated] = useState(initial?.related_object ?? "shipment");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [active, setActive] = useState(initial?.active ?? true);
  const [template, setTemplate] = useState(initial?.template ?? STARTER);
  const [tab, setTab] = useState<"code" | "preview">("code");
  const [err, setErr] = useState<string | null>(null);

  const save = useSaveDocumentTemplate();
  const del = useDeleteDocumentTemplate();

  // Server-rendered preview (real sample data) once the template is saved.
  const serverPreview = initial?.preview_url ? joinUrl(ctx.baseUrl, initial.preview_url) : null;

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (!name.trim()) return setErr("A name is required.");
    if (!template.trim()) return setErr("The template body can’t be empty.");
    try {
      await save.mutateAsync({
        id: initial?.id,
        data: {
          name: name.trim(),
          slug: slug.trim() || name.trim().toLowerCase().replace(/[^a-z0-9]+/g, "_"),
          related_object: related,
          description: description.trim(),
          active,
          template,
        },
      });
      onClose();
    } catch (e2) {
      setErr((e2 as Error)?.message ?? "Could not save the template.");
    }
  };

  const onDelete = async () => {
    if (!initial) return;
    try {
      await del.mutateAsync(initial.id);
      onClose();
    } catch {
      setErr("Could not delete the template.");
    }
  };

  return (
    <Sheet
      open onClose={onClose} size="lg" crumb="Documents"
      title={initial ? "Edit template" : "New template"} id={initial?.id}
      footer={
        <>
          {initial && <button className="btn" onClick={onDelete} disabled={del.isPending} data-testid="document-delete">Delete</button>}
          <div style={{ flex: 1 }} />
          <button className="btn" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" form="document-form" type="submit" disabled={save.isPending} data-testid="document-save">
            {save.isPending ? "Saving…" : "Save template"}
          </button>
        </>
      }
    >
      <form id="document-form" className="sheet-body-pad" onSubmit={onSubmit} data-testid="document-sheet-body">
        <div className="kv-grid">
          <Field label="Name *"><input className="field-input" value={name} onChange={(e) => setName(e.target.value)} data-testid="dt-name" /></Field>
          <Field label="Slug"><input className="field-input mono" value={slug} onChange={(e) => setSlug(e.target.value)} placeholder="auto from name" data-testid="dt-slug" /></Field>
          <Field label="Related object">
            <select className="field-input" value={related} onChange={(e) => setRelated(e.target.value)} data-testid="dt-related">
              <option value="shipment">Shipment</option>
              <option value="order">Order</option>
              <option value="other">Other</option>
            </select>
          </Field>
          <Field label="Description"><input className="field-input" value={description} onChange={(e) => setDescription(e.target.value)} data-testid="dt-description" /></Field>
        </div>

        {/* Editor / live-preview tabs */}
        <div className="seg" role="tablist" style={{ display: "flex", gap: 4, margin: "12px 0 8px" }}>
          <button type="button" role="tab" aria-selected={tab === "code"} className={"btn btn-sm" + (tab === "code" ? " btn-primary" : "")} onClick={() => setTab("code")} data-testid="dt-tab-code">Template</button>
          <button type="button" role="tab" aria-selected={tab === "preview"} className={"btn btn-sm" + (tab === "preview" ? " btn-primary" : "")} onClick={() => setTab("preview")} data-testid="dt-tab-preview">Preview</button>
        </div>

        {tab === "code" ? (
          <textarea
            className="field-input mono"
            style={{ width: "100%", minHeight: 320, lineHeight: 1.5, tabSize: 2, resize: "vertical" }}
            value={template}
            onChange={(e) => setTemplate(e.target.value)}
            spellCheck={false}
            data-testid="dt-template"
          />
        ) : (
          <div data-testid="dt-preview" style={{ border: "1px solid var(--border)", borderRadius: "var(--r-md)", overflow: "hidden", background: "#fff", minHeight: 320 }}>
            {/* Live raw HTML preview (sandboxed). Liquid variables render with real
                sample data on the server — the saved server preview is linked below. */}
            <iframe title="template preview" srcDoc={template} sandbox="" style={{ width: "100%", height: 320, border: 0, background: "#fff" }} data-testid="dt-preview-frame" />
          </div>
        )}

        <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 10, fontSize: 12 }}>
          <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} data-testid="dt-active" /> Active
          </label>
          {serverPreview && (
            <a className="muted" href={serverPreview} target="_blank" rel="noreferrer" data-testid="dt-server-preview" style={{ marginLeft: "auto" }}>
              Open rendered preview (sample data) →
            </a>
          )}
        </div>
        {err && <div className="auth-error" data-testid="document-form-error">{err}</div>}
      </form>
    </Sheet>
  );
}
