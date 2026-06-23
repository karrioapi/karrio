// ProductsScreen.tsx — Ship › Products (C10) with create / edit / delete.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { Sheet, Field } from "~/components/ui/Sheet";
import { useDeleteProduct, useProducts, useSaveProduct } from "~/lib/karrio/hooks";
import type { ProductTemplate } from "~/lib/karrio/types";

type FormState = "closed" | "create" | { edit: ProductTemplate };

export function ProductsScreen() {
  const [form, setForm] = useState<FormState>("closed");
  const { data, isLoading, isError, error } = useProducts();
  const rows = useMemo(() => data ?? [], [data]);

  return (
    <div className="page" data-testid="screen-products">
      <PageHeader
        title="Products"
        actions={
          <button className="btn btn-primary" onClick={() => setForm("create")} data-testid="product-create">
            <Icon.Plus size={14} /> Create product
          </button>
        }
      />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Product</th><th>SKU</th><th>HS code</th><th>Value</th><th>Origin</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={6} kind="loading" message="Loading products…" />}
            {isError && !isLoading && <StateRow colSpan={6} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={6} kind="empty" message="No products yet." />}
            {rows.map((p) => (
              <tr key={p.id} onClick={() => setForm({ edit: p })} data-testid={`product-row-${p.id}`}>
                <td className="recipient-name">{p.title ?? p.label ?? "—"}</td>
                <td className="mono" style={{ fontSize: 12 }}>{p.sku ?? "—"}</td>
                <td className="mono" style={{ fontSize: 12 }}>{p.hs_code ?? "—"}</td>
                <td className="mono" style={{ fontSize: 12 }}>{p.value_amount != null ? `${p.value_amount} ${p.value_currency ?? ""}` : "—"}</td>
                <td className="muted">{p.origin_country ?? "—"}</td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={rows.length} noun="products" />
      </div>

      {form !== "closed" && (
        <ProductForm key={form === "create" ? "create" : form.edit.id} initial={form === "create" ? undefined : form.edit} onClose={() => setForm("closed")} />
      )}
    </div>
  );
}

function ProductForm({ initial, onClose }: { initial?: ProductTemplate; onClose: () => void }) {
  const [title, setTitle] = useState(initial?.title ?? "");
  const [sku, setSku] = useState(initial?.sku ?? "");
  const [hs, setHs] = useState(initial?.hs_code ?? "");
  const [value, setValue] = useState(String(initial?.value_amount ?? ""));
  const [currency, setCurrency] = useState(initial?.value_currency ?? "USD");
  const [weight, setWeight] = useState(String(initial?.weight ?? ""));
  const [origin, setOrigin] = useState(initial?.origin_country ?? "");
  const [err, setErr] = useState<string | null>(null);

  const save = useSaveProduct();
  const del = useDeleteProduct();
  const num = (s: string) => (s.trim() === "" ? undefined : Number(s));

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (!title.trim()) return setErr("Title is required.");
    try {
      await save.mutateAsync({
        id: initial?.id,
        data: {
          title, label: title, sku, hs_code: hs, origin_country: origin,
          value_amount: num(value), value_currency: currency, weight: num(weight),
        },
      });
      onClose();
    } catch {
      setErr("Could not save the product.");
    }
  };

  const onDelete = async () => {
    if (!initial) return;
    try {
      await del.mutateAsync(initial.id);
      onClose();
    } catch {
      setErr("Could not delete the product.");
    }
  };

  return (
    <Sheet
      open onClose={onClose} size="md" crumb="Products"
      title={initial ? "Edit product" : "Create product"} id={initial?.id}
      footer={
        <>
          {initial && <button className="btn" onClick={onDelete} disabled={del.isPending} data-testid="product-delete">Delete</button>}
          <div style={{ flex: 1 }} />
          <button className="btn" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" form="product-form" type="submit" disabled={save.isPending} data-testid="product-save">
            {save.isPending ? "Saving…" : "Save"}
          </button>
        </>
      }
    >
      <form id="product-form" className="sheet-body-pad" onSubmit={onSubmit} data-testid="product-form">
        <Field label="Title"><input className="field-input" value={title} onChange={(e) => setTitle(e.target.value)} data-testid="prf-title" /></Field>
        <div className="kv-grid">
          <Field label="SKU"><input className="field-input" value={sku} onChange={(e) => setSku(e.target.value)} data-testid="prf-sku" /></Field>
          <Field label="HS code"><input className="field-input" value={hs} onChange={(e) => setHs(e.target.value)} /></Field>
          <Field label="Value"><input className="field-input" value={value} onChange={(e) => setValue(e.target.value)} data-testid="prf-value" /></Field>
          <Field label="Currency">
            <select className="field-input" value={currency} onChange={(e) => setCurrency(e.target.value)}><option>USD</option><option>EUR</option><option>GBP</option><option>CAD</option></select>
          </Field>
          <Field label="Weight (kg)"><input className="field-input" value={weight} onChange={(e) => setWeight(e.target.value)} /></Field>
          <Field label="Origin country"><input className="field-input" value={origin} onChange={(e) => setOrigin(e.target.value)} /></Field>
        </div>
        {err && <div className="auth-error" data-testid="product-form-error">{err}</div>}
      </form>
    </Sheet>
  );
}
