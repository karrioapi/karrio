// RateSheetsScreen.tsx — Govern › Rate sheets. Full management: list + editor
// (name, carrier, services rate table) + CSV import. (EBE-105)
import { useMemo, useState } from "react";
import { CARRIERS, CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { Sheet, Field } from "~/components/ui/Sheet";
import { useRateSheets, useSaveRateSheet, useDeleteRateSheet } from "~/lib/karrio/hooks";
import { useReferences } from "~/lib/karrio/references";
import { carrierKey } from "~/lib/karrio/display";
import type { RateSheet, RateSheetService } from "~/lib/karrio/types";

type EditorState = "closed" | "create" | { edit: RateSheet };

export function RateSheetsScreen() {
  const [editor, setEditor] = useState<EditorState>("closed");
  const { data, isLoading, isError, error } = useRateSheets();
  const rows = useMemo(() => data ?? [], [data]);

  return (
    <div className="page" data-testid="screen-ratesheets">
      <PageHeader
        title="Rate sheets"
        actions={
          <button className="btn btn-primary" onClick={() => setEditor("create")} data-testid="ratesheet-create">
            <Icon.Plus size={14} /> New rate sheet
          </button>
        }
      />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Name</th><th>Carrier</th><th>Services</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={4} kind="loading" message="Loading rate sheets…" />}
            {isError && !isLoading && <StateRow colSpan={4} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={4} kind="empty" message="No rate sheets yet." />}
            {rows.map((rs) => (
              <tr key={rs.id} onClick={() => setEditor({ edit: rs })} data-testid={`ratesheet-row-${rs.id}`}>
                <td className="recipient-name">{rs.name}</td>
                <td>
                  <div className="svc-cell">
                    <CarrierLogo carrier={carrierKey(rs.carrier_name)} size="sm" />
                    <span>{CARRIERS[carrierKey(rs.carrier_name)]?.name ?? rs.carrier_name ?? "—"}</span>
                  </div>
                </td>
                <td>{rs.services?.length ?? rs.services_count ?? 0}</td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={rows.length} noun="rate sheets" />
      </div>

      {editor !== "closed" && (
        <RateSheetEditor
          key={editor === "create" ? "create" : editor.edit.id}
          initial={editor === "create" ? undefined : editor.edit}
          onClose={() => setEditor("closed")}
        />
      )}
    </div>
  );
}

const CSV_COLUMNS = ["service_code", "service_name", "currency", "cost", "min_weight", "max_weight", "transit_days"] as const;
const NUMERIC = new Set(["cost", "min_weight", "max_weight", "transit_days"]);

// Parse a simple CSV (with or without a header row) into service rows.
function parseCsv(text: string): RateSheetService[] {
  const lines = text.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  if (lines.length === 0) return [];
  let header = CSV_COLUMNS as readonly string[];
  let start = 0;
  if (lines[0].toLowerCase().includes("service_code")) {
    header = lines[0].split(",").map((h) => h.trim());
    start = 1;
  }
  const out: RateSheetService[] = [];
  for (let i = start; i < lines.length; i++) {
    const cells = lines[i].split(",").map((c) => c.trim());
    const row: Record<string, unknown> = {};
    header.forEach((h, idx) => {
      const v = cells[idx];
      if (v === undefined || v === "") return;
      row[h] = NUMERIC.has(h) ? Number(v) : v;
    });
    if (row.service_code || row.service_name) {
      out.push({
        service_code: String(row.service_code ?? `svc_${i}`),
        service_name: String(row.service_name ?? row.service_code ?? `Service ${i}`),
        currency: (row.currency as string) ?? "USD",
        cost: row.cost as number | undefined,
        min_weight: row.min_weight as number | undefined,
        max_weight: row.max_weight as number | undefined,
        transit_days: row.transit_days as number | undefined,
      });
    }
  }
  return out;
}

function RateSheetEditor({ initial, onClose }: { initial?: RateSheet; onClose: () => void }) {
  const { data: refs } = useReferences();
  const carriers = useMemo<[string, string][]>(
    () => Object.entries(refs?.carriers ?? {}).sort((a, b) => a[1].localeCompare(b[1])),
    [refs],
  );

  const [name, setName] = useState(initial?.name ?? "");
  const [carrier, setCarrier] = useState(initial?.carrier_name ?? "");
  const [services, setServices] = useState<RateSheetService[]>(initial?.services ?? []);
  const [csv, setCsv] = useState("");
  const [err, setErr] = useState<string | null>(null);

  const save = useSaveRateSheet();
  const del = useDeleteRateSheet();

  const addService = () =>
    setServices((s) => [...s, { service_code: "", service_name: "", currency: "USD" }]);
  const updateService = (i: number, patch: Partial<RateSheetService>) =>
    setServices((s) => s.map((row, idx) => (idx === i ? { ...row, ...patch } : row)));
  const removeService = (i: number) => setServices((s) => s.filter((_, idx) => idx !== i));

  const importCsv = () => {
    const parsed = parseCsv(csv);
    if (parsed.length === 0) return setErr("No service rows found in the CSV.");
    setServices((s) => [...s, ...parsed]);
    setCsv("");
    setErr(null);
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (!name.trim()) return setErr("A name is required.");
    if (!carrier) return setErr("Select a carrier.");
    const valid = services.filter((s) => s.service_code.trim() && s.service_name.trim());
    if (valid.length === 0) return setErr("Add at least one service (code + name).");
    try {
      await save.mutateAsync({
        id: initial?.id,
        data: {
          name: name.trim(),
          carrier_name: carrier,
          services: valid.map((s) => ({
            service_code: s.service_code.trim(),
            service_name: s.service_name.trim(),
            currency: s.currency || "USD",
            cost: s.cost,
            min_weight: s.min_weight,
            max_weight: s.max_weight,
            weight_unit: s.weight_unit || "KG",
            transit_days: s.transit_days,
          })),
        },
      });
      onClose();
    } catch (e2) {
      setErr((e2 as Error)?.message ?? "Could not save the rate sheet.");
    }
  };

  const onDelete = async () => {
    if (!initial) return;
    try {
      await del.mutateAsync(initial.id);
      onClose();
    } catch {
      setErr("Could not delete the rate sheet.");
    }
  };

  return (
    <Sheet
      open onClose={onClose} size="lg" crumb="Rate sheets"
      title={initial ? "Edit rate sheet" : "New rate sheet"} id={initial?.id}
      footer={
        <>
          {initial && <button className="btn" onClick={onDelete} disabled={del.isPending} data-testid="ratesheet-delete">Delete</button>}
          <div style={{ flex: 1 }} />
          <button className="btn" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" form="ratesheet-form" type="submit" disabled={save.isPending} data-testid="ratesheet-save">
            {save.isPending ? "Saving…" : "Save rate sheet"}
          </button>
        </>
      }
    >
      <form id="ratesheet-form" className="sheet-body-pad" onSubmit={onSubmit} data-testid="ratesheet-sheet-body">
        <div className="kv-grid">
          <Field label="Name *"><input className="field-input" value={name} onChange={(e) => setName(e.target.value)} data-testid="rs-name" /></Field>
          <Field label="Carrier *">
            <select className="field-input" value={carrier} onChange={(e) => setCarrier(e.target.value)} disabled={!!initial} data-testid="rs-carrier">
              <option value="">Select a carrier…</option>
              {carriers.map(([id, label]) => <option key={id} value={id}>{label}</option>)}
            </select>
          </Field>
        </div>

        <div className="section-head" style={{ display: "flex", alignItems: "center", marginTop: 14 }}>
          Services &amp; rates
          <button type="button" className="btn btn-sm" style={{ marginLeft: "auto" }} onClick={addService} data-testid="rs-add-service"><Icon.Plus size={12} /> Add service</button>
        </div>
        <table className="table" data-testid="rs-services">
          <thead><tr><th>Code</th><th>Name</th><th>Currency</th><th>Cost</th><th>Transit</th><th /></tr></thead>
          <tbody>
            {services.length === 0 && <tr><td colSpan={6}><div className="state-row" style={{ fontSize: 12 }}>No services yet — add one or import a CSV below.</div></td></tr>}
            {services.map((s, i) => (
              <tr key={i} data-testid={`rs-service-${i}`}>
                <td><input className="field-input mono" style={{ minWidth: 90 }} value={s.service_code} onChange={(e) => updateService(i, { service_code: e.target.value })} data-testid={`rs-service-code-${i}`} /></td>
                <td><input className="field-input" style={{ minWidth: 120 }} value={s.service_name} onChange={(e) => updateService(i, { service_name: e.target.value })} data-testid={`rs-service-name-${i}`} /></td>
                <td><input className="field-input" style={{ width: 64 }} value={s.currency ?? ""} onChange={(e) => updateService(i, { currency: e.target.value })} /></td>
                <td><input className="field-input" style={{ width: 72 }} type="number" step="0.01" value={s.cost ?? ""} onChange={(e) => updateService(i, { cost: e.target.value === "" ? undefined : Number(e.target.value) })} /></td>
                <td><input className="field-input" style={{ width: 56 }} type="number" value={s.transit_days ?? ""} onChange={(e) => updateService(i, { transit_days: e.target.value === "" ? undefined : Number(e.target.value) })} /></td>
                <td><button type="button" className="icon-action" onClick={() => removeService(i)} data-testid={`rs-service-remove-${i}`}><Icon.X size={13} /></button></td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="section-head" style={{ marginTop: 14 }}>Import CSV</div>
        <textarea
          className="field-input mono"
          style={{ width: "100%", height: 90, fontSize: 12 }}
          placeholder="service_code,service_name,currency,cost,min_weight,max_weight,transit_days"
          value={csv}
          onChange={(e) => setCsv(e.target.value)}
          data-testid="rs-csv"
        />
        <button type="button" className="btn btn-sm" style={{ marginTop: 6 }} onClick={importCsv} data-testid="rs-csv-import"><Icon.Download size={12} /> Import services from CSV</button>

        {err && <div className="auth-error" data-testid="ratesheet-form-error">{err}</div>}
      </form>
    </Sheet>
  );
}
