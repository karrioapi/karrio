// ShipmentsScreen.tsx — Ship › Shipments (C2). Wired to the decoupled Karrio
// client via useShipments. Tabs + filter toolbar + selectable table + bulk
// actions + row→ShipmentSheet, faithful to the design handoff.
import { useMemo, useState } from "react";
import { CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import { useShipments } from "~/lib/karrio/hooks";
import {
  carrierKey,
  formatDate,
  formatRate,
  recipientAddr,
  recipientName,
  statusClass,
  statusLabel,
} from "~/lib/karrio/display";
import type { Shipment } from "~/lib/karrio/types";
import { ShipmentSheet } from "~/screens/ship/ShipmentSheet";

const TABS: { id: string; label: string; match?: (s: Shipment) => boolean }[] = [
  { id: "all", label: "All" },
  { id: "purchased", label: "Purchased", match: (s) => statusClass(s.status) === "purchased" },
  { id: "intransit", label: "In transit", match: (s) => statusClass(s.status) === "intransit" },
  { id: "delivered", label: "Delivered", match: (s) => statusClass(s.status) === "delivered" },
  { id: "exception", label: "Exception", match: (s) => statusClass(s.status) === "exception" },
  { id: "cancelled", label: "Cancelled", match: (s) => statusClass(s.status) === "cancelled" },
  { id: "draft", label: "Draft", match: (s) => statusClass(s.status) === "draft" },
];

export function ShipmentsScreen() {
  const [tab, setTab] = useState("all");
  const [selected, setSelected] = useState<string[]>([]);
  const [preview, setPreview] = useState<Shipment | null>(null);

  const { data, isLoading, isError, error } = useShipments();
  const all = useMemo(() => data?.results ?? [], [data]);

  const counts = useMemo(() => {
    const c: Record<string, number> = { all: all.length };
    for (const t of TABS) if (t.match) c[t.id] = all.filter(t.match).length;
    return c;
  }, [all]);

  const rows = useMemo(() => {
    const t = TABS.find((x) => x.id === tab);
    return t?.match ? all.filter(t.match) : all;
  }, [all, tab]);

  const toggle = (id: string) =>
    setSelected((sel) => (sel.includes(id) ? sel.filter((x) => x !== id) : [...sel, id]));
  const allSelected = rows.length > 0 && selected.length === rows.length;
  const toggleAll = () => setSelected(allSelected ? [] : rows.map((r) => r.id));

  return (
    <div className="page" data-testid="screen-shipments">
      <div className="page-header">
        <h1 className="page-title">Shipments</h1>
        <div className="page-actions">
          {selected.length > 0 ? (
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
          )}
        </div>
      </div>

      <div className="tabs" role="tablist">
        {TABS.map((t) => (
          <button
            key={t.id}
            role="tab"
            aria-selected={tab === t.id}
            className={"tab" + (tab === t.id ? " active" : "")}
            onClick={() => setTab(t.id)}
            data-testid={`tab-${t.id}`}
          >
            {t.label}
            <span className="count">{counts[t.id] ?? 0}</span>
          </button>
        ))}
      </div>

      <div className="table-toolbar">
        <button className="filter-pill"><Icon.Filter size={12} /> Filter</button>
        <button className="filter-pill">Carrier <span className="v">Any</span> <Icon.ChevronD size={12} /></button>
        <button className="filter-pill">Date <span className="v">Last 30 days</span> <Icon.ChevronD size={12} /></button>
        <div style={{ flex: 1 }} />
        <button className="filter-pill"><Icon.Sliders size={12} /> View</button>
      </div>

      <div className="card card-scroll">
        <table className="table">
          <thead>
            <tr>
              <th className="checkbox-cell">
                <span
                  className={"checkbox" + (allSelected ? " checked" : "")}
                  onClick={toggleAll}
                  data-testid="select-all"
                >
                  {allSelected && <Icon.Check size={12} style={{ color: "white" }} />}
                </span>
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
            {isLoading && (
              <tr><td colSpan={8}><div className="state-row" data-testid="shipments-loading">Loading shipments…</div></td></tr>
            )}
            {isError && !isLoading && (
              <tr><td colSpan={8}><div className="state-row" data-testid="shipments-error">{(error as Error)?.message ?? "Failed to load shipments"}</div></td></tr>
            )}
            {!isLoading && !isError && rows.length === 0 && (
              <tr><td colSpan={8}><div className="state-row" data-testid="shipments-empty">No shipments found.</div></td></tr>
            )}
            {rows.map((s) => (
              <tr
                key={s.id}
                className={selected.includes(s.id) ? "selected" : ""}
                onClick={() => setPreview(s)}
                data-testid={`shipment-row-${s.id}`}
              >
                <td className="checkbox-cell" onClick={(e) => { e.stopPropagation(); toggle(s.id); }}>
                  <span className={"checkbox" + (selected.includes(s.id) ? " checked" : "")}>
                    {selected.includes(s.id) && <Icon.Check size={12} style={{ color: "white" }} />}
                  </span>
                </td>
                <td>
                  <div className="svc-cell">
                    <CarrierLogo carrier={carrierKey(s.carrier_name)} />
                    <div>
                      <div className="svc-id">{s.tracking_number ?? s.id}</div>
                      <div className="svc-name">{s.service ?? "—"}</div>
                    </div>
                  </div>
                </td>
                <td><span className={"pill " + statusClass(s.status)}>{statusLabel(s.status)}</span></td>
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
        <div className="table-footer">
          <span>Viewing 1–{rows.length} of {data?.count ?? all.length} shipments</span>
          <div className="right">
            <button className="btn btn-sm"><Icon.ChevronL size={12} /> Previous</button>
            <button className="btn btn-sm">Next <Icon.ChevronR size={12} /></button>
          </div>
        </div>
      </div>

      <ShipmentSheet shipment={preview} onClose={() => setPreview(null)} />
    </div>
  );
}
