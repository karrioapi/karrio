// ProductsScreen.tsx — Ship › Products (C10). GraphQL products/commodities.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useProducts } from "~/lib/karrio/hooks";
import type { ProductTemplate } from "~/lib/karrio/types";

export function ProductsScreen() {
  const [preview, setPreview] = useState<ProductTemplate | null>(null);
  const { data, isLoading, isError, error } = useProducts();
  const rows = useMemo(() => data ?? [], [data]);

  return (
    <div className="page" data-testid="screen-products">
      <PageHeader title="Products" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Create product</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Product</th><th>SKU</th><th>HS code</th><th>Value</th><th>Origin</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={6} kind="loading" message="Loading products…" />}
            {isError && !isLoading && <StateRow colSpan={6} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={6} kind="empty" message="No products yet." />}
            {rows.map((p) => (
              <tr key={p.id} onClick={() => setPreview(p)} data-testid={`product-row-${p.id}`}>
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

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Products" title={preview.title ?? preview.label ?? "Product"} id={preview.id}>
          <div className="sheet-body-pad" data-testid="product-sheet-body">
            <Section title="Details">
              <KVGrid>
                <KV label="Title">{preview.title ?? "—"}</KV>
                <KV label="SKU" mono>{preview.sku ?? "—"}</KV>
                <KV label="HS code" mono>{preview.hs_code ?? "—"}</KV>
                <KV label="Value" mono>{preview.value_amount != null ? `${preview.value_amount} ${preview.value_currency ?? ""}` : "—"}</KV>
                <KV label="Weight" mono>{preview.weight != null ? `${preview.weight} ${preview.weight_unit ?? ""}` : "—"}</KV>
                <KV label="Origin">{preview.origin_country ?? "—"}</KV>
              </KVGrid>
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
