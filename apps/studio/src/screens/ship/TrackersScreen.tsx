// TrackersScreen.tsx — Ship › Trackers (C3).
import { useMemo, useState } from "react";
import { CarrierLogo } from "~/components/ui/CarrierLogo";
import { Icon } from "~/components/ui/icons";
import {
  FilterPill,
  FilterToolbar,
  PageHeader,
  StateRow,
  StatusPill,
  TableFooter,
  Tabs,
  type TabDef,
} from "~/components/ui/primitives";
import { useTrackers } from "~/lib/karrio/hooks";
import { carrierKey, formatDate, statusClass } from "~/lib/karrio/display";
import { CARRIERS } from "~/components/ui/CarrierLogo";
import type { Tracker } from "~/lib/karrio/types";
import { TrackerSheet } from "~/screens/ship/TrackerSheet";

const TAB_MATCH: Record<string, (t: Tracker) => boolean> = {
  intransit: (t) => statusClass(t.status) === "intransit",
  pending: (t) => statusClass(t.status) === "pending",
  exception: (t) => statusClass(t.status) === "exception",
  delivered: (t) => statusClass(t.status) === "delivered",
};

export function TrackersScreen() {
  const [tab, setTab] = useState("all");
  const [preview, setPreview] = useState<Tracker | null>(null);
  const { data, isLoading, isError, error } = useTrackers();
  const all = useMemo(() => data?.results ?? [], [data]);

  const rows = useMemo(() => {
    const m = TAB_MATCH[tab];
    return m ? all.filter(m) : all;
  }, [all, tab]);

  const tabs: TabDef[] = useMemo(
    () => [
      { id: "all", label: "All", count: all.length },
      { id: "intransit", label: "In transit", count: all.filter(TAB_MATCH.intransit).length },
      { id: "pending", label: "Pending", count: all.filter(TAB_MATCH.pending).length },
      { id: "exception", label: "Exception", count: all.filter(TAB_MATCH.exception).length },
      { id: "delivered", label: "Delivered", count: all.filter(TAB_MATCH.delivered).length },
    ],
    [all],
  );

  return (
    <div className="page" data-testid="screen-trackers">
      <PageHeader
        title="Trackers"
        actions={
          <>
            <button className="btn"><Icon.Download size={14} /> Export</button>
            <button className="btn btn-primary"><Icon.Plus size={14} /> Track a shipment</button>
          </>
        }
      />
      <Tabs tabs={tabs} value={tab} onChange={setTab} />
      <FilterToolbar>
        <FilterPill><Icon.Filter size={12} /> Filter</FilterPill>
        <FilterPill>Carrier <span className="v">Any</span> <Icon.ChevronD size={12} /></FilterPill>
      </FilterToolbar>

      <div className="card card-scroll">
        <table className="table">
          <thead>
            <tr>
              <th>Carrier service</th>
              <th>Status</th>
              <th>Estimated delivery</th>
              <th>Last event</th>
              <th className="actions-cell" />
            </tr>
          </thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading trackers…" />}
            {isError && !isLoading && (
              <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load trackers"} />
            )}
            {!isLoading && !isError && rows.length === 0 && (
              <StateRow colSpan={5} kind="empty" message="No trackers found." />
            )}
            {rows.map((t) => {
              const last = t.events?.[0];
              return (
                <tr key={t.id} onClick={() => setPreview(t)} data-testid={`tracker-row-${t.id}`}>
                  <td>
                    <div className="svc-cell">
                      <CarrierLogo carrier={carrierKey(t.carrier_name)} />
                      <div>
                        <div className="svc-id">{t.tracking_number}</div>
                        <div className="svc-name">{CARRIERS[carrierKey(t.carrier_name)]?.name ?? t.carrier_name ?? "—"}</div>
                      </div>
                    </div>
                  </td>
                  <td><StatusPill status={t.status} /></td>
                  <td className="muted" style={{ fontSize: 12 }}>{t.estimated_delivery ?? "—"}</td>
                  <td className="muted" style={{ fontSize: 12 }}>
                    {last ? `${last.description ?? ""}${last.date ? ` · ${last.date}` : ""}` : "—"}
                  </td>
                  <td className="actions-cell" onClick={(e) => e.stopPropagation()}>
                    <span className="icon-action"><Icon.Dots size={14} /></span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? all.length} noun="trackers" hasNext={!!data?.next} hasPrev={!!data?.previous} />
      </div>

      <TrackerSheet tracker={preview} onClose={() => setPreview(null)} />
    </div>
  );
}
