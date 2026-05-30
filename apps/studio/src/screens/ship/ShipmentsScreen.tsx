// ShipmentsScreen.tsx — Ship › Shipments (C2). Wired to useShipments via the
// decoupled Karrio client; built on shared primitives.
import { useMemo, useState } from "react";
import { CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import {
  Checkbox,
  FilterPill,
  FilterToolbar,
  PageHeader,
  StateRow,
  StatusPill,
  TableFooter,
  Tabs,
  type TabDef,
} from "~/components/ui/primitives";
import { useShipments } from "~/lib/karrio/hooks";
import {
  carrierKey,
  formatDate,
  formatRate,
  recipientAddr,
  recipientName,
  shipmentCarrier,
  shipmentService,
  statusClass,
} from "~/lib/karrio/display";
import type { Shipment } from "~/lib/karrio/types";
import { ShipmentSheet } from "~/screens/ship/ShipmentSheet";

const TAB_MATCH: Record<string, (s: Shipment) => boolean> = {
  purchased: (s) => statusClass(s.status) === "purchased",
  intransit: (s) => statusClass(s.status) === "intransit",
  delivered: (s) => statusClass(s.status) === "delivered",
  exception: (s) => statusClass(s.status) === "exception",
  cancelled: (s) => statusClass(s.status) === "cancelled",
  draft: (s) => statusClass(s.status) === "draft",
};

export function ShipmentsScreen() {
  const [tab, setTab] = useState("all");
  const [selected, setSelected] = useState<string[]>([]);
  const [preview, setPreview] = useState<Shipment | null>(null);

  const { data, isLoading, isError, error } = useShipments();
  const all = useMemo(() => data?.results ?? [], [data]);

  const rows = useMemo(() => {
    const m = TAB_MATCH[tab];
    return m ? all.filter(m) : all;
  }, [all, tab]);

  const tabs: TabDef[] = useMemo(
    () => [
      { id: "all", label: "All", count: all.length },
      { id: "purchased", label: "Purchased", count: all.filter(TAB_MATCH.purchased).length },
      { id: "intransit", label: "In transit", count: all.filter(TAB_MATCH.intransit).length },
      { id: "delivered", label: "Delivered", count: all.filter(TAB_MATCH.delivered).length },
      { id: "exception", label: "Exception", count: all.filter(TAB_MATCH.exception).length },
      { id: "cancelled", label: "Cancelled", count: all.filter(TAB_MATCH.cancelled).length },
      { id: "draft", label: "Draft", count: all.filter(TAB_MATCH.draft).length },
    ],
    [all],
  );

  const toggle = (id: string) =>
    setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));
  const allSelected = rows.length > 0 && selected.length === rows.length;
  const toggleAll = () => setSelected(allSelected ? [] : rows.map((r) => r.id));

  return (
    <div className="page" data-testid="screen-shipments">
      <PageHeader
        title="Shipments"
        actions={
          selected.length > 0 ? (
            <>
              <span className="muted" style={{ fontSize: 12 }} data-testid="selection-count">
                {selected.length} selected
              </span>
              <button className="btn"><Icon.Print size={14} /> Print labels</button>
              <button className="btn"><Icon.Download size={14} /> Export</button>
              <button className="btn">Manifest</button>
            </>
          ) : (
            <>
              <button className="btn"><Icon.Download size={14} /> Export</button>
              <button className="btn btn-primary"><Icon.Plus size={14} /> Create label</button>
            </>
          )
        }
      />

      <Tabs tabs={tabs} value={tab} onChange={setTab} />

      <FilterToolbar>
        <FilterPill><Icon.Filter size={12} /> Filter</FilterPill>
        <FilterPill>Carrier <span className="v">Any</span> <Icon.ChevronD size={12} /></FilterPill>
        <FilterPill>Date <span className="v">Last 30 days</span> <Icon.ChevronD size={12} /></FilterPill>
        <div style={{ flex: 1 }} />
        <FilterPill><Icon.Sliders size={12} /> View</FilterPill>
      </FilterToolbar>

      <div className="card card-scroll">
        <table className="table">
          <thead>
            <tr>
              <th className="checkbox-cell">
                <Checkbox checked={allSelected} onChange={toggleAll} testid="select-all" />
              </th>
              <th>Shipping service</th>
              <th>Status</th>
              <th>Recipient</th>
              <th style={{ textAlign: "right" }}>Rate</th>
              <th>Reference</th>
              <th>Date</th>
              <th className="actions-cell" />
            </tr>
          </thead>
          <tbody>
            {isLoading && <StateRow colSpan={8} kind="loading" message="Loading shipments…" />}
            {isError && !isLoading && (
              <StateRow colSpan={8} kind="error" message={(error as Error)?.message ?? "Failed to load shipments"} />
            )}
            {!isLoading && !isError && rows.length === 0 && (
              <StateRow colSpan={8} kind="empty" message="No shipments found." />
            )}
            {rows.map((s) => (
              <tr
                key={s.id}
                className={selected.includes(s.id) ? "selected" : ""}
                onClick={() => setPreview(s)}
                data-testid={`shipment-row-${s.id}`}
              >
                <td className="checkbox-cell">
                  <Checkbox checked={selected.includes(s.id)} onChange={() => toggle(s.id)} />
                </td>
                <td>
                  <div className="svc-cell">
                    <CarrierLogo carrier={carrierKey(shipmentCarrier(s))} />
                    <div>
                      <div className="svc-id">{s.tracking_number ?? s.id}</div>
                      <div className="svc-name">{shipmentService(s)}</div>
                    </div>
                  </div>
                </td>
                <td><StatusPill status={s.status} /></td>
                <td>
                  <div className="recipient-name">{recipientName(s.recipient)}</div>
                  <div className="recipient-addr">{recipientAddr(s.recipient)}</div>
                </td>
                <td style={{ textAlign: "right", fontWeight: 500 }}>{formatRate(s)}</td>
                <td className="mono" style={{ fontSize: 12, color: "var(--fg-onsubtle)" }}>{s.reference ?? "—"}</td>
                <td className="muted" style={{ fontSize: 12, whiteSpace: "nowrap" }}>{formatDate(s.created_at)}</td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}>
                  <span className="icon-action"><Icon.Dots size={14} /></span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? all.length} noun="shipments" hasNext={!!data?.next} hasPrev={!!data?.previous} />
      </div>

      <ShipmentSheet shipment={preview} onClose={() => setPreview(null)} />
    </div>
  );
}
