// HomeScreen.tsx — Ship-mode landing. Foundation version shows the page header
// and stat-card layout from the design; metrics wire to shipment/tracker hooks
// in a later phase.
const STATS = [
  { label: "Shipments (30d)", value: "1,284", delta: "+12.4%" },
  { label: "In transit", value: "218", delta: "+3.1%" },
  { label: "Delivered (30d)", value: "1,002", delta: "+9.8%" },
  { label: "Spend (30d)", value: "$18,402", delta: "-2.2%" },
];

export function HomeScreen() {
  return (
    <div className="page" data-testid="screen-home">
      <div className="page-header">
        <h1 className="page-title">Good morning, Daniel</h1>
        <div className="page-actions">
          <button className="btn">Last 30 days</button>
          <button className="btn btn-primary">Refresh</button>
        </div>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "var(--gap)",
        }}
        data-testid="home-stats"
      >
        {STATS.map((s) => (
          <div
            key={s.label}
            style={{
              border: "1px solid var(--border)",
              borderRadius: "var(--r-md)",
              background: "var(--bg-elevated)",
              padding: "14px 16px",
            }}
          >
            <div style={{ fontSize: 11, color: "var(--fg-muted)", marginBottom: 6 }}>
              {s.label}
            </div>
            <div style={{ fontSize: 26, fontWeight: 600, letterSpacing: "-0.02em" }}>
              {s.value}
            </div>
            <div
              style={{
                fontSize: 11,
                marginTop: 4,
                color: s.delta.startsWith("-") ? "var(--red-fg)" : "var(--green-fg)",
              }}
            >
              {s.delta} vs prev. 30 days
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
