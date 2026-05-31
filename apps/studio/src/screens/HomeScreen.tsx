// HomeScreen.tsx — Ship-mode landing. Real metrics computed from the shipment,
// tracker, and order hooks (no hardcoded numbers): summary stats, a recent
// shipments list, and an actionable "things to do" panel.
import { PageHeader, StatusPill } from "~/components/ui/primitives";
import { CarrierLogo } from "~/components/ui/CarrierLogo";
import { useOrders, useShipments, useTrackers } from "~/lib/karrio/hooks";
import {
  carrierKey,
  formatRate,
  recipientName,
  shipmentCarrier,
  shipmentService,
} from "~/lib/karrio/display";

const has = (status: string | undefined, re: RegExp) => re.test(status ?? "");
const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? "" : "s"}`;

export function HomeScreen() {
  const shipmentsQ = useShipments();
  const trackersQ = useTrackers();
  const ordersQ = useOrders();

  const shipments = shipmentsQ.data?.results ?? [];
  const trackers = trackersQ.data?.results ?? [];
  const orders = ordersQ.data ?? [];

  const inTransit = trackers.filter((t) => has(t.status, /transit|out_for|pickup/i)).length;
  const delivered = trackers.filter((t) => has(t.status, /deliver/i)).length;
  const exceptions = trackers.filter((t) => has(t.status, /exception|failed|return/i)).length;
  const toFulfill = orders.filter((o) => has(o.status, /unfulfilled|partial/i)).length;

  const stats = [
    { label: "Shipments", value: shipmentsQ.data?.count ?? shipments.length, href: "/shipments" },
    { label: "In transit", value: inTransit, href: "/trackers" },
    { label: "Delivered", value: delivered, href: "/trackers" },
    { label: "Orders to fulfill", value: toFulfill, href: "/orders" },
  ];

  const recent = shipments.slice(0, 6);
  const loading = shipmentsQ.isLoading;

  const todos: Array<{ label: string; href: string }> = [];
  if (toFulfill > 0) todos.push({ label: `${plural(toFulfill, "order")} waiting to be fulfilled`, href: "/orders" });
  if (inTransit > 0) todos.push({ label: `${plural(inTransit, "shipment")} in transit to track`, href: "/trackers" });
  if (exceptions > 0) todos.push({ label: `${plural(exceptions, "shipment")} with a delivery exception`, href: "/trackers" });

  return (
    <div className="page" data-testid="screen-home">
      <PageHeader
        title="Home"
        actions={
          <>
            <button className="btn">Last 30 days</button>
            <a className="btn btn-primary" href="/shipments">Create label</a>
          </>
        }
      />

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "var(--gap)",
        }}
        data-testid="home-stats"
      >
        {stats.map((s) => (
          <a
            key={s.label}
            href={s.href}
            data-testid={`home-stat-${s.label.toLowerCase().replace(/\s+/g, "-")}`}
            style={{
              border: "1px solid var(--border)",
              borderRadius: "var(--r-md)",
              background: "var(--bg-elevated)",
              padding: "14px 16px",
              textDecoration: "none",
              color: "inherit",
              display: "block",
            }}
          >
            <div style={{ fontSize: 11, color: "var(--fg-muted)", marginBottom: 6 }}>{s.label}</div>
            <div style={{ fontSize: 26, fontWeight: 600, letterSpacing: "-0.02em", fontVariantNumeric: "tabular-nums" }}>
              {loading ? "—" : s.value.toLocaleString()}
            </div>
          </a>
        ))}
      </div>

      <div className="two-col" style={{ marginTop: "var(--gap)", gap: "var(--gap)" }}>
        <section className="card" data-testid="home-recent">
          <div className="section-head" style={{ display: "flex", alignItems: "center" }}>
            Recent shipments
            <a href="/shipments" className="muted" style={{ marginLeft: "auto", fontSize: 12 }}>View all →</a>
          </div>
          <table className="table">
            <tbody>
              {loading && (
                <tr><td className="muted" style={{ padding: "14px" }}>Loading…</td></tr>
              )}
              {!loading && recent.length === 0 && (
                <tr><td className="muted" style={{ padding: "14px" }} data-testid="home-recent-empty">No shipments yet.</td></tr>
              )}
              {recent.map((s) => (
                <tr key={s.id} data-testid={`home-recent-${s.id}`}>
                  <td>
                    <div className="svc-cell">
                      <CarrierLogo carrier={carrierKey(shipmentCarrier(s))} />
                      <div>
                        <div className="svc-id">{s.tracking_number ?? s.id}</div>
                        <div className="svc-name">{shipmentService(s)}</div>
                      </div>
                    </div>
                  </td>
                  <td className="muted" style={{ fontSize: 12 }}>{recipientName(s.recipient)}</td>
                  <td className="mono" style={{ fontSize: 12, textAlign: "right" }}>{formatRate(s)}</td>
                  <td style={{ textAlign: "right" }}><StatusPill status={s.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="card" data-testid="home-todo">
          <div className="section-head">Things to do</div>
          <div style={{ padding: "4px 0" }}>
            {todos.length === 0 ? (
              <div className="muted" style={{ padding: "10px 14px", fontSize: 13 }} data-testid="home-todo-empty">
                You're all caught up. 🎉
              </div>
            ) : (
              todos.map((t, i) => (
                <a
                  key={i}
                  href={t.href}
                  data-testid={`home-todo-${i}`}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 10,
                    padding: "10px 14px",
                    borderBottom: i < todos.length - 1 ? "1px solid var(--border)" : "none",
                    textDecoration: "none",
                    color: "inherit",
                    fontSize: 13,
                  }}
                >
                  <span style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--accent)" }} />
                  {t.label}
                  <span className="muted" style={{ marginLeft: "auto" }}>→</span>
                </a>
              ))
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
