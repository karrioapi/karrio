// OrdersScreen.tsx — Ship › Orders (C4). GraphQL-backed via useOrders.
import { useMemo, useState } from "react";
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
import { useOrders } from "~/lib/karrio/hooks";
import { formatDate, recipientAddr, recipientName } from "~/lib/karrio/display";
import type { Order } from "~/lib/karrio/types";
import { OrderSheet } from "~/screens/ship/OrderSheet";

const norm = (s?: string) => (s ?? "").toLowerCase();
const TAB_MATCH: Record<string, (o: Order) => boolean> = {
  unfulfilled: (o) => norm(o.status) === "unfulfilled",
  partial: (o) => norm(o.status) === "partial",
  fulfilled: (o) => norm(o.status) === "fulfilled",
  cancelled: (o) => norm(o.status) === "cancelled",
};

export function OrdersScreen() {
  const [tab, setTab] = useState("all");
  const [preview, setPreview] = useState<Order | null>(null);
  const { data, isLoading, isError, error } = useOrders();
  const all = useMemo(() => data ?? [], [data]);

  const rows = useMemo(() => {
    const m = TAB_MATCH[tab];
    return m ? all.filter(m) : all;
  }, [all, tab]);

  const tabs: TabDef[] = useMemo(
    () => [
      { id: "all", label: "All", count: all.length },
      { id: "unfulfilled", label: "Unfulfilled", count: all.filter(TAB_MATCH.unfulfilled).length },
      { id: "partial", label: "Partial", count: all.filter(TAB_MATCH.partial).length },
      { id: "fulfilled", label: "Fulfilled", count: all.filter(TAB_MATCH.fulfilled).length },
      { id: "cancelled", label: "Cancelled", count: all.filter(TAB_MATCH.cancelled).length },
    ],
    [all],
  );

  return (
    <div className="page" data-testid="screen-orders">
      <PageHeader
        title="Orders"
        actions={
          <>
            <button className="btn"><Icon.Download size={14} /> Export</button>
            <button className="btn btn-primary"><Icon.Plus size={14} /> Create order</button>
          </>
        }
      />
      <Tabs tabs={tabs} value={tab} onChange={setTab} />
      <FilterToolbar>
        <FilterPill><Icon.Filter size={12} /> Filter</FilterPill>
        <FilterPill>Source <span className="v">Any</span> <Icon.ChevronD size={12} /></FilterPill>
      </FilterToolbar>

      <div className="card card-scroll">
        <table className="table">
          <thead>
            <tr>
              <th>Order</th>
              <th>Customer</th>
              <th>Items</th>
              <th>Status</th>
              <th>Source</th>
              <th>Date</th>
              <th className="actions-cell" />
            </tr>
          </thead>
          <tbody>
            {isLoading && <StateRow colSpan={7} kind="loading" message="Loading orders…" />}
            {isError && !isLoading && (
              <StateRow colSpan={7} kind="error" message={(error as Error)?.message ?? "Failed to load orders"} />
            )}
            {!isLoading && !isError && rows.length === 0 && (
              <StateRow colSpan={7} kind="empty" message="No orders found." />
            )}
            {rows.map((o) => (
              <tr key={o.id} onClick={() => setPreview(o)} data-testid={`order-row-${o.id}`}>
                <td className="mono" style={{ fontWeight: 500 }}>{o.order_id ?? o.id}</td>
                <td>
                  <div className="recipient-name">{recipientName(o.shipping_to)}</div>
                  <div className="recipient-addr">{recipientAddr(o.shipping_to)}</div>
                </td>
                <td>{o.line_items?.length ?? 0}</td>
                <td><StatusPill status={o.status} /></td>
                <td className="muted" style={{ fontSize: 12 }}>{o.source ?? "—"}</td>
                <td className="muted" style={{ fontSize: 12, whiteSpace: "nowrap" }}>{formatDate(o.created_at)}</td>
                <td className="actions-cell" onClick={(e) => e.stopPropagation()}>
                  <span className="icon-action"><Icon.Dots size={14} /></span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={all.length} noun="orders" />
      </div>

      <OrderSheet order={preview} onClose={() => setPreview(null)} />
    </div>
  );
}
