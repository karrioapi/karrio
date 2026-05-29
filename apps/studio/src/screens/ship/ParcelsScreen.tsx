// ParcelsScreen.tsx — Ship › Parcels (C9) with create / edit / delete.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { Sheet, Field } from "~/components/ui/Sheet";
import { useDeleteParcel, useParcels, useSaveParcel } from "~/lib/karrio/hooks";
import type { ParcelTemplate } from "~/lib/karrio/types";

const dims = (p: ParcelTemplate) =>
  p.length != null ? `${p.length} × ${p.width} × ${p.height} ${p.dimension_unit ?? ""}`.trim() : "—";

type FormState = "closed" | "create" | { edit: ParcelTemplate };

export function ParcelsScreen() {
  const [form, setForm] = useState<FormState>("closed");
  const { data, isLoading, isError, error } = useParcels();
  const rows = useMemo(() => data ?? [], [data]);

  return (
    <div className="page" data-testid="screen-parcels">
      <PageHeader
        title="Parcels"
        actions={
          <button className="btn btn-primary" onClick={() => setForm("create")} data-testid="parcel-create">
            <Icon.Plus size={14} /> Create parcel
          </button>
        }
      />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Label</th><th>Packaging</th><th>Dimensions</th><th>Weight</th><th>Default</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={6} kind="loading" message="Loading parcels…" />}
            {isError && !isLoading && <StateRow colSpan={6} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={6} kind="empty" message="No parcels yet." />}
            {rows.map((p) => (
              <tr key={p.id} onClick={() => setForm({ edit: p })} data-testid={`parcel-row-${p.id}`}>
                <td className="recipient-name">{p.label ?? "—"}</td>
                <td className="muted">{p.packaging_type ?? "—"}</td>
                <td className="mono" style={{ fontSize: 12 }}>{dims(p)}</td>
                <td className="mono" style={{ fontSize: 12 }}>{p.weight != null ? `${p.weight} ${p.weight_unit ?? ""}` : "—"}</td>
                <td>{p.is_default ? <Icon.Check size={14} /> : ""}</td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={rows.length} noun="parcels" />
      </div>

      {form !== "closed" && (
        <ParcelForm key={form === "create" ? "create" : form.edit.id} initial={form === "create" ? undefined : form.edit} onClose={() => setForm("closed")} />
      )}
    </div>
  );
}

function ParcelForm({ initial, onClose }: { initial?: ParcelTemplate; onClose: () => void }) {
  const [label, setLabel] = useState(initial?.label ?? "");
  const [packaging, setPackaging] = useState(initial?.packaging_type ?? "BOX");
  const [length, setLength] = useState(String(initial?.length ?? ""));
  const [width, setWidth] = useState(String(initial?.width ?? ""));
  const [height, setHeight] = useState(String(initial?.height ?? ""));
  const [dimUnit, setDimUnit] = useState(initial?.dimension_unit ?? "CM");
  const [weight, setWeight] = useState(String(initial?.weight ?? ""));
  const [weightUnit, setWeightUnit] = useState(initial?.weight_unit ?? "KG");
  const [isDefault, setIsDefault] = useState(Boolean(initial?.is_default));
  const [err, setErr] = useState<string | null>(null);

  const save = useSaveParcel();
  const del = useDeleteParcel();

  const num = (s: string) => (s.trim() === "" ? undefined : Number(s));

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (!label.trim()) return setErr("Label is required.");
    if (!weight.trim() || Number.isNaN(Number(weight))) return setErr("A numeric weight is required.");
    try {
      await save.mutateAsync({
        id: initial?.id,
        data: {
          label, is_default: isDefault,
          parcel: {
            packaging_type: packaging, dimension_unit: dimUnit, weight_unit: weightUnit,
            length: num(length), width: num(width), height: num(height), weight: num(weight),
          },
        },
      });
      onClose();
    } catch {
      setErr("Could not save the parcel.");
    }
  };

  const onDelete = async () => {
    if (!initial) return;
    try {
      await del.mutateAsync(initial.id);
      onClose();
    } catch {
      setErr("Could not delete the parcel.");
    }
  };

  return (
    <Sheet
      open onClose={onClose} size="md" crumb="Parcels"
      title={initial ? "Edit parcel" : "Create parcel"} id={initial?.id}
      footer={
        <>
          {initial && <button className="btn" onClick={onDelete} disabled={del.isPending} data-testid="parcel-delete">Delete</button>}
          <div style={{ flex: 1 }} />
          <button className="btn" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" form="parcel-form" type="submit" disabled={save.isPending} data-testid="parcel-save">
            {save.isPending ? "Saving…" : "Save"}
          </button>
        </>
      }
    >
      <form id="parcel-form" className="sheet-body-pad" onSubmit={onSubmit} data-testid="parcel-form">
        <Field label="Label"><input className="field-input" value={label} onChange={(e) => setLabel(e.target.value)} data-testid="pf-label" /></Field>
        <Field label="Packaging type">
          <select className="field-input" value={packaging} onChange={(e) => setPackaging(e.target.value)} data-testid="pf-packaging">
            <option value="BOX">Box</option><option value="ENVELOPE">Envelope</option><option value="PAK">Pak</option><option value="TUBE">Tube</option>
          </select>
        </Field>
        <div className="kv-grid">
          <Field label="Length"><input className="field-input" value={length} onChange={(e) => setLength(e.target.value)} data-testid="pf-length" /></Field>
          <Field label="Width"><input className="field-input" value={width} onChange={(e) => setWidth(e.target.value)} /></Field>
          <Field label="Height"><input className="field-input" value={height} onChange={(e) => setHeight(e.target.value)} /></Field>
          <Field label="Dimension unit">
            <select className="field-input" value={dimUnit} onChange={(e) => setDimUnit(e.target.value)}><option>CM</option><option>IN</option></select>
          </Field>
          <Field label="Weight"><input className="field-input" value={weight} onChange={(e) => setWeight(e.target.value)} data-testid="pf-weight" /></Field>
          <Field label="Weight unit">
            <select className="field-input" value={weightUnit} onChange={(e) => setWeightUnit(e.target.value)}><option>KG</option><option>LB</option></select>
          </Field>
        </div>
        <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12.5, marginTop: 6 }}>
          <input type="checkbox" checked={isDefault} onChange={(e) => setIsDefault(e.target.checked)} data-testid="pf-default" />
          Set as default parcel
        </label>
        {err && <div className="auth-error" data-testid="parcel-form-error">{err}</div>}
      </form>
    </Sheet>
  );
}
