// RateSheetsScreen.tsx — Govern › Rate sheets (dashboard parity).
import { useMemo, useState } from "react";
import { CARRIERS, CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useRateSheets } from "~/lib/karrio/hooks";
import { carrierKey } from "~/lib/karrio/display";
import type { RateSheet } from "~/lib/karrio/types";

export function RateSheetsScreen() {
  const [preview, setPreview] = useState<RateSheet | null>(null);
  const { data, isLoading, isError, error } = useRateSheets();
  const rows = useMemo(() => data ?? [], [data]);

  return (
    <div className="page" data-testid="screen-ratesheets">
      <PageHeader title="Rate sheets" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> New rate sheet</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Name</th><th>Carrier</th><th>Services</th><th>Type</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading rate sheets…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No rate sheets yet." />}
            {rows.map((rs) => (
              <tr key={rs.id} onClick={() => setPreview(rs)} data-testid={`ratesheet-row-${rs.id}`}>
                <td className="recipient-name">{rs.name}</td>
                <td>
                  <div className="svc-cell">
                    <CarrierLogo carrier={carrierKey(rs.carrier_name)} size="sm" />
                    <span>{CARRIERS[carrierKey(rs.carrier_name)]?.name ?? rs.carrier_name ?? "—"}</span>
                  </div>
                </td>
                <td>{rs.services_count ?? "—"}</td>
                <td><span className="tag">{rs.is_system ? "system" : "custom"}</span></td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={rows.length} noun="rate sheets" />
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Rate sheets" title={preview.name} id={preview.id}>
          <div className="sheet-body-pad" data-testid="ratesheet-sheet-body">
            <Section title="Details">
              <KVGrid>
                <KV label="Name">{preview.name}</KV>
                <KV label="Carrier">{preview.carrier_name ?? "—"}</KV>
                <KV label="Services">{preview.services_count ?? "—"}</KV>
                <KV label="Type">{preview.is_system ? "System" : "Custom"}</KV>
              </KVGrid>
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
