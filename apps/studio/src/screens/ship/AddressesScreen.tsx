// AddressesScreen.tsx — Ship › Addresses (C8). GraphQL address templates.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useAddresses } from "~/lib/karrio/hooks";
import type { AddressTemplate } from "~/lib/karrio/types";

export function AddressesScreen() {
  const [preview, setPreview] = useState<AddressTemplate | null>(null);
  const { data, isLoading, isError, error } = useAddresses();
  const rows = useMemo(() => data ?? [], [data]);

  return (
    <div className="page" data-testid="screen-addresses">
      <PageHeader title="Addresses" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Create address</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Label</th><th>Contact</th><th>Location</th><th>Default</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading addresses…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No addresses yet." />}
            {rows.map((a) => (
              <tr key={a.id} onClick={() => setPreview(a)} data-testid={`address-row-${a.id}`}>
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

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Addresses" title={preview.label ?? "Address"} id={preview.id}>
          <div className="sheet-body-pad" data-testid="address-sheet-body">
            <Section title="Contact">
              <KVGrid>
                <KV label="Name">{preview.address?.person_name ?? "—"}</KV>
                <KV label="Company">{preview.address?.company_name ?? "—"}</KV>
                <KV label="Email">{preview.address?.email ?? "—"}</KV>
                <KV label="Phone">{preview.address?.phone_number ?? "—"}</KV>
              </KVGrid>
            </Section>
            <Section title="Location">
              <KVGrid>
                <KV label="Street">{preview.address?.address_line1 ?? "—"}</KV>
                <KV label="City">{preview.address?.city ?? "—"}</KV>
                <KV label="State">{preview.address?.state_code ?? "—"}</KV>
                <KV label="Postal">{preview.address?.postal_code ?? "—"}</KV>
                <KV label="Country">{preview.address?.country_code ?? "—"}</KV>
                <KV label="Residential">{preview.address?.residential ? "Yes" : "No"}</KV>
              </KVGrid>
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
