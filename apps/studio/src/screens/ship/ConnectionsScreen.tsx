// ConnectionsScreen.tsx — Ship › Connections (C6) with add / edit / delete.
import { useMemo, useState } from "react";
import { CARRIERS, CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter, Toggle } from "~/components/ui/primitives";
import { Sheet, Field } from "~/components/ui/Sheet";
import { useCarrierConnections, useDeleteConnection, useSaveConnection } from "~/lib/karrio/hooks";
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

const COMMON_CARRIERS = ["ups", "fedex", "dhl_express", "canadapost", "usps", "purolator", "dpd"];

function ConnectionForm({ initial, onClose }: { initial?: CarrierConnection; onClose: () => void }) {
  const [carrier, setCarrier] = useState(initial?.carrier_name ?? "ups");
  const [accountId, setAccountId] = useState(initial?.carrier_id ?? "");
  const [credentials, setCredentials] = useState("{\n  \"api_key\": \"\"\n}");
  const [testMode, setTestMode] = useState(initial?.test_mode ?? true);
  const [active, setActive] = useState(initial?.active ?? true);
  const [err, setErr] = useState<string | null>(null);

  const save = useSaveConnection();
  const del = useDeleteConnection();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (!accountId.trim()) return setErr("An account ID is required.");
    let creds: Record<string, unknown> = {};
    if (!initial) {
      try {
        creds = JSON.parse(credentials);
      } catch {
        return setErr("Credentials must be valid JSON.");
      }
    }
    try {
      await save.mutateAsync({
        id: initial?.id,
        data: { carrier_name: carrier, carrier_id: accountId.trim(), test_mode: testMode, active, ...creds },
      });
      onClose();
    } catch {
      setErr("Could not save the connection.");
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
        <Field label="Carrier">
          <select className="field-input" value={carrier} onChange={(e) => setCarrier(e.target.value)} disabled={!!initial} data-testid="cf-carrier">
            {COMMON_CARRIERS.map((c) => <option key={c} value={c}>{CARRIERS[carrierKey(c)]?.name ?? c}</option>)}
          </select>
        </Field>
        <Field label="Account ID"><input className="field-input" value={accountId} onChange={(e) => setAccountId(e.target.value)} data-testid="cf-account" /></Field>
        {!initial && (
          <Field label="Credentials (JSON)">
            <textarea className="field-input" style={{ height: 90, fontFamily: "var(--font-mono)" }} value={credentials} onChange={(e) => setCredentials(e.target.value)} data-testid="cf-credentials" />
          </Field>
        )}
        <div style={{ display: "flex", gap: 18, marginTop: 6 }}>
          <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12.5 }}>
            <Toggle checked={testMode} onChange={setTestMode} label="Test mode" testid="cf-test" /> Test mode
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12.5 }}>
            <Toggle checked={active} onChange={setActive} label="Active" testid="cf-active" /> Active
          </label>
        </div>
        {err && <div className="auth-error" data-testid="connection-form-error">{err}</div>}
      </form>
    </Sheet>
  );
}
