// AdminScreen.tsx — Govern › Overview (E1).
import { useMemo } from "react";
import { PageHeader } from "~/components/ui/primitives";
import { useAdminInfo } from "~/lib/karrio/hooks";

export function AdminScreen() {
  const { data } = useAdminInfo();
  const info = data ?? {};
  const resources = useMemo(() => info.resources ?? [], [info]);
  const runtimes = useMemo(() => info.runtimes ?? [], [info]);

  return (
    <div className="page" data-testid="screen-admin">
      <PageHeader title="Overview" />
      <div className="stat-grid" data-testid="admin-cards">
        <div className="stat-card"><div className="kvstat-label">Version</div><div className="kvstat-value mono">{info.version ?? "—"}</div></div>
        <div className="stat-card"><div className="kvstat-label">Tenants</div><div className="kvstat-value">{info.tenants ?? "—"}</div></div>
        <div className="stat-card"><div className="kvstat-label">License</div><div className="kvstat-value">{info.license ?? "—"}</div></div>
      </div>

      <div className="card" style={{ padding: 16, marginBottom: 16 }}>
        <div style={{ fontWeight: 600, marginBottom: 12 }}>System resources</div>
        {resources.length === 0 && <div className="muted" style={{ fontSize: 12.5 }}>No data.</div>}
        {resources.map((r) => (
          <div key={r.label} style={{ marginBottom: 10 }}>
            <div style={{ display: "flex", fontSize: 12, marginBottom: 4 }}>
              <span className="muted">{r.label}</span>
              <span className="mono" style={{ marginLeft: "auto" }}>{r.used}/{r.total}</span>
            </div>
            <div className="bar"><div className="bar-fill" style={{ width: `${Math.min(100, (r.used / r.total) * 100)}%` }} /></div>
          </div>
        ))}
      </div>

      <div className="card">
        <div style={{ padding: "12px 16px", borderBottom: "1px solid var(--border)", fontWeight: 600 }}>Plugin runtimes</div>
        <table className="table">
          <thead><tr><th>Plugin</th><th style={{ textAlign: "right" }}>Memory</th><th style={{ textAlign: "right" }}>Calls</th><th style={{ textAlign: "right" }}>p99</th></tr></thead>
          <tbody data-testid="admin-runtimes">
            {runtimes.length === 0 && <tr><td colSpan={4}><div className="state-row">No runtimes.</div></td></tr>}
            {runtimes.map((rt) => (
              <tr key={rt.name}><td className="mono">{rt.name}</td><td className="mono" style={{ textAlign: "right" }}>{rt.memory ?? "—"}</td><td className="mono" style={{ textAlign: "right" }}>{rt.calls ?? "—"}</td><td className="mono" style={{ textAlign: "right" }}>{rt.p99 ?? "—"}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
