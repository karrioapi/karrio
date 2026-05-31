// ConnectionsScreen.tsx — Ship › Connections (C6). Carrier connections with a
// DYNAMIC, per-carrier credential form driven by the API references
// (connection_fields), plus create/edit/delete via GraphQL. (EBE-110)
import { useEffect, useMemo, useState } from "react";
import { CARRIERS, CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter, Toggle } from "~/components/ui/primitives";
import { Sheet, Field } from "~/components/ui/Sheet";
import { useCarrierConnections, useDeleteConnection, useSaveConnection } from "~/lib/karrio/hooks";
import { useReferences, type ConnectionField } from "~/lib/karrio/references";
import { carrierKey } from "~/lib/karrio/display";
import type { CarrierConnection } from "~/lib/karrio/types";

type FormState = "closed" | "create" | { edit: CarrierConnection };

export function ConnectionsScreen() {
  const [form, setForm] = useState<FormState>("closed");
  const { data, isLoading, isError, error } = useCarrierConnections();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-connections">
      <PageHeader
        title="Connections"
        actions={
          <button className="btn btn-primary" onClick={() => setForm("create")} data-testid="connection-create">
            <Icon.Plus size={14} /> Add connection
          </button>
        }
      />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Carrier</th><th>Account ID</th><th>Mode</th><th>Status</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading connections…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No connections yet." />}
            {rows.map((c) => (
              <tr key={c.id} onClick={() => setForm({ edit: c })} data-testid={`connection-row-${c.id}`}>
                <td>
                  <div className="svc-cell">
                    <CarrierLogo carrier={carrierKey(c.carrier_name)} />
                    <div className="svc-id">{CARRIERS[carrierKey(c.carrier_name)]?.name ?? c.carrier_name}</div>
                  </div>
                </td>
                <td className="mono" style={{ fontSize: 12 }}>{c.carrier_id}</td>
                <td><span className={"pill " + (c.test_mode ? "draft" : "purchased")}>{c.test_mode ? "test" : "live"}</span></td>
                <td><span className={"pill " + (c.active === false ? "cancelled" : "delivered")}>{c.active === false ? "inactive" : "active"}</span></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="connections" />
      </div>

      {form !== "closed" && (
        <ConnectionForm key={form === "create" ? "create" : form.edit.id} initial={form === "create" ? undefined : form.edit} onClose={() => setForm("closed")} />
      )}
    </div>
  );
}

function ConnectionForm({ initial, onClose }: { initial?: CarrierConnection; onClose: () => void }) {
  const { data: refs, isLoading: refsLoading } = useReferences();
  const carriers = useMemo<[string, string][]>(
    () => Object.entries(refs?.carriers ?? {}).sort((a, b) => a[1].localeCompare(b[1])),
    [refs],
  );
  const fieldsByCarrier = refs?.connection_fields ?? {};

  const [carrier, setCarrier] = useState(initial?.carrier_name ?? "");
  const [carrierId, setCarrierId] = useState(initial?.carrier_id ?? "");
  const [values, setValues] = useState<Record<string, string>>({});
  const [active, setActive] = useState(initial?.active ?? true);
  const [err, setErr] = useState<string | null>(null);

  // Credential fields for the selected carrier (object fields like metadata/config
  // are handled separately, so they're excluded from the credential inputs).
  const fields = useMemo<ConnectionField[]>(
    () => Object.values(fieldsByCarrier[carrier] ?? {}).filter((f) => f.type !== "object"),
    [fieldsByCarrier, carrier],
  );

  // Seed default values when the carrier changes (e.g. language=en, country=CA).
  useEffect(() => {
    const schema = fieldsByCarrier[carrier] ?? {};
    const seed: Record<string, string> = {};
    for (const [name, f] of Object.entries(schema)) {
      if (f.type !== "object" && f.default != null) seed[name] = String(f.default);
    }
    setValues(seed);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [carrier]);

  const save = useSaveConnection();
  const del = useDeleteConnection();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (!carrier) return setErr("Select a carrier.");
    if (!carrierId.trim()) return setErr("An account ID is required.");
    const missing = fields.find((f) => f.required && !values[f.name]?.trim());
    if (missing) return setErr(`${missing.label ?? missing.name} is required.`);

    const credentials: Record<string, unknown> = {};
    for (const f of fields) {
      const v = values[f.name];
      if (v !== undefined && v !== "") credentials[f.name] = v;
    }

    try {
      await save.mutateAsync({
        id: initial?.id,
        data: initial
          ? { carrier_id: carrierId.trim(), active, credentials }
          : { carrier_name: carrier, carrier_id: carrierId.trim(), active, credentials },
      });
      onClose();
    } catch (e2) {
      setErr((e2 as Error)?.message ?? "Could not save the connection.");
    }
  };

  const onDelete = async () => {
    if (!initial) return;
    try {
      await del.mutateAsync(initial.id);
      onClose();
    } catch {
      setErr("Could not delete the connection.");
    }
  };

  return (
    <Sheet
      open onClose={onClose} size="md" crumb="Connections"
      title={initial ? "Edit connection" : "Add connection"} id={initial?.id}
      footer={
        <>
          {initial && <button className="btn" onClick={onDelete} disabled={del.isPending} data-testid="connection-delete">Delete</button>}
          <div style={{ flex: 1 }} />
          <button className="btn" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" form="connection-form" type="submit" disabled={save.isPending} data-testid="connection-save">
            {save.isPending ? "Saving…" : "Save"}
          </button>
        </>
      }
    >
      <form id="connection-form" className="sheet-body-pad" onSubmit={onSubmit} data-testid="connection-form">
        <Field label="Carrier *">
          <select className="field-input" value={carrier} onChange={(e) => setCarrier(e.target.value)} disabled={!!initial} data-testid="cf-carrier">
            <option value="">{refsLoading ? "Loading carriers…" : "Select a carrier…"}</option>
            {carriers.map(([id, name]) => <option key={id} value={id}>{name}</option>)}
          </select>
        </Field>

        <Field label="Account ID *">
          <input className="field-input" value={carrierId} onChange={(e) => setCarrierId(e.target.value)} placeholder="A label for this account" data-testid="cf-account" />
        </Field>

        {carrier && fields.length === 0 && !refsLoading && (
          <div className="muted" style={{ fontSize: 12, margin: "8px 0" }} data-testid="cf-no-fields">
            No credential fields are defined for this carrier.
          </div>
        )}

        {/* Per-carrier dynamic credential fields, driven by /v1/references. */}
        {fields.map((f) => (
          <Field key={f.name} label={(f.label ?? f.name) + (f.required ? " *" : "")}>
            {f.enum ? (
              <select className="field-input" value={values[f.name] ?? ""} onChange={(e) => setValues((v) => ({ ...v, [f.name]: e.target.value }))} data-testid={`cf-field-${f.name}`}>
                {!f.required && <option value="">—</option>}
                {f.enum.map((o) => <option key={o} value={o}>{o}</option>)}
              </select>
            ) : (
              <input
                className="field-input"
                type={f.sensitive ? "password" : "text"}
                value={values[f.name] ?? ""}
                onChange={(e) => setValues((v) => ({ ...v, [f.name]: e.target.value }))}
                placeholder={initial && f.sensitive ? "•••••• (unchanged)" : undefined}
                autoComplete={f.sensitive ? "new-password" : "off"}
                data-testid={`cf-field-${f.name}`}
              />
            )}
          </Field>
        ))}

        <div style={{ display: "flex", gap: 18, marginTop: 6 }}>
          <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12.5 }}>
            <Toggle checked={active} onChange={setActive} label="Active" testid="cf-active" /> Active
          </label>
        </div>
        {err && <div className="auth-error" data-testid="connection-form-error">{err}</div>}
      </form>
    </Sheet>
  );
}
