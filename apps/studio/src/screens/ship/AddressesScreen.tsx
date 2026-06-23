// AddressesScreen.tsx — Ship › Addresses (C8) with create / edit / delete.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { Sheet, Field } from "~/components/ui/Sheet";
import { useAddresses, useDeleteAddress, useSaveAddress } from "~/lib/karrio/hooks";
import type { AddressTemplate } from "~/lib/karrio/types";

type FormState = "closed" | "create" | { edit: AddressTemplate };

export function AddressesScreen() {
  const [form, setForm] = useState<FormState>("closed");
  const { data, isLoading, isError, error } = useAddresses();
  const rows = useMemo(() => data ?? [], [data]);

  return (
    <div className="page" data-testid="screen-addresses">
      <PageHeader
        title="Addresses"
        actions={
          <button className="btn btn-primary" onClick={() => setForm("create")} data-testid="address-create">
            <Icon.Plus size={14} /> Create address
          </button>
        }
      />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Label</th><th>Contact</th><th>Location</th><th>Default</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading addresses…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No addresses yet." />}
            {rows.map((a) => (
              <tr key={a.id} onClick={() => setForm({ edit: a })} data-testid={`address-row-${a.id}`}>
                <td className="recipient-name">{a.label ?? "—"}</td>
                <td>{a.address?.person_name ?? a.address?.company_name ?? "—"}</td>
                <td className="muted" style={{ fontSize: 12 }}>
                  {[a.address?.city, a.address?.state_code, a.address?.country_code].filter(Boolean).join(", ")}
                </td>
                <td>{a.is_default ? <Icon.Check size={14} /> : ""}</td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={rows.length} noun="addresses" />
      </div>

      {form !== "closed" && (
        <AddressForm
          key={form === "create" ? "create" : form.edit.id}
          initial={form === "create" ? undefined : form.edit}
          onClose={() => setForm("closed")}
        />
      )}
    </div>
  );
}

function AddressForm({ initial, onClose }: { initial?: AddressTemplate; onClose: () => void }) {
  const a = initial?.address;
  const [label, setLabel] = useState(initial?.label ?? "");
  const [name, setName] = useState(a?.person_name ?? "");
  const [company, setCompany] = useState(a?.company_name ?? "");
  const [email, setEmail] = useState(a?.email ?? "");
  const [phone, setPhone] = useState(a?.phone_number ?? "");
  const [street, setStreet] = useState(a?.address_line1 ?? "");
  const [city, setCity] = useState(a?.city ?? "");
  const [state, setStateCode] = useState(a?.state_code ?? "");
  const [postal, setPostal] = useState(a?.postal_code ?? "");
  const [country, setCountry] = useState(a?.country_code ?? "");
  const [isDefault, setIsDefault] = useState(Boolean(initial?.is_default));
  const [err, setErr] = useState<string | null>(null);

  const save = useSaveAddress();
  const del = useDeleteAddress();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (!label.trim()) return setErr("Label is required.");
    if (!city.trim() || !country.trim()) return setErr("City and country are required.");
    try {
      await save.mutateAsync({
        id: initial?.id,
        data: {
          label,
          is_default: isDefault,
          address: {
            person_name: name,
            company_name: company,
            email,
            phone_number: phone,
            address_line1: street,
            city,
            state_code: state,
            postal_code: postal,
            country_code: country,
          },
        },
      });
      onClose();
    } catch {
      setErr("Could not save the address. Please try again.");
    }
  };

  const onDelete = async () => {
    if (!initial) return;
    try {
      await del.mutateAsync(initial.id);
      onClose();
    } catch {
      setErr("Could not delete the address.");
    }
  };

  return (
    <Sheet
      open
      onClose={onClose}
      size="md"
      crumb="Addresses"
      title={initial ? "Edit address" : "Create address"}
      id={initial?.id}
      footer={
        <>
          {initial && (
            <button className="btn" onClick={onDelete} disabled={del.isPending} data-testid="address-delete">
              Delete
            </button>
          )}
          <div style={{ flex: 1 }} />
          <button className="btn" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" form="address-form" type="submit" disabled={save.isPending} data-testid="address-save">
            {save.isPending ? "Saving…" : "Save"}
          </button>
        </>
      }
    >
      <form id="address-form" className="sheet-body-pad" onSubmit={onSubmit} data-testid="address-form">
        <Field label="Label"><input className="field-input" value={label} onChange={(e) => setLabel(e.target.value)} data-testid="af-label" /></Field>
        <div className="kv-grid">
          <Field label="Contact name"><input className="field-input" value={name} onChange={(e) => setName(e.target.value)} data-testid="af-name" /></Field>
          <Field label="Company"><input className="field-input" value={company} onChange={(e) => setCompany(e.target.value)} /></Field>
          <Field label="Email"><input className="field-input" value={email} onChange={(e) => setEmail(e.target.value)} /></Field>
          <Field label="Phone"><input className="field-input" value={phone} onChange={(e) => setPhone(e.target.value)} /></Field>
        </div>
        <Field label="Street"><input className="field-input" value={street} onChange={(e) => setStreet(e.target.value)} /></Field>
        <div className="kv-grid">
          <Field label="City"><input className="field-input" value={city} onChange={(e) => setCity(e.target.value)} data-testid="af-city" /></Field>
          <Field label="State / Province"><input className="field-input" value={state} onChange={(e) => setStateCode(e.target.value)} /></Field>
          <Field label="Postal code"><input className="field-input" value={postal} onChange={(e) => setPostal(e.target.value)} /></Field>
          <Field label="Country code"><input className="field-input" value={country} onChange={(e) => setCountry(e.target.value)} data-testid="af-country" /></Field>
        </div>
        <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12.5, marginTop: 6 }}>
          <input type="checkbox" checked={isDefault} onChange={(e) => setIsDefault(e.target.checked)} data-testid="af-default" />
          Set as default address
        </label>
        {err && <div className="auth-error" data-testid="address-form-error">{err}</div>}
      </form>
    </Sheet>
  );
}
