// AdminScreen.tsx — Govern › Overview (E1). Real admin data via /admin/graphql
// (worker health, users, system connections) + version from references.
import { useMemo } from "react";
import { PageHeader } from "~/components/ui/primitives";
import { useAdminInfo } from "~/lib/karrio/hooks";
import { useReferences } from "~/lib/karrio/references";

export function AdminScreen() {
  const { data } = useAdminInfo();
  const { data: refs } = useReferences();
  const info = data ?? {};
  const resources = useMemo(() => info.resources ?? [], [info]);
  const runtimes = useMemo(() => info.runtimes ?? [], [info]);
  const version = (refs?.VERSION as string) ?? info.version;

  return (
    <div className="page" data-testid="screen-admin">
      <PageHeader title="Overview" />
      <div className="stat-grid" data-testid="admin-cards">
        <div className="stat-card"><div className="kvstat-label">Version</div><div className="kvstat-value mono">{version ?? "—"}</div></div>
        <div className="stat-card"><div className="kvstat-label">License</div><div className="kvstat-value">{info.license ?? "—"}</div></div>
        <div className="stat-card" data-testid="admin-users"><div className="kvstat-label">Users</div><div className="kvstat-value">{info.users ?? "—"}</div></div>
        <div className="stat-card" data-testid="admin-system-connections"><div className="kvstat-label">System connections</div><div className="kvstat-value">{info.system_connections ?? "—"}</div></div>
        <div className="stat-card" data-testid="admin-worker">
          <div className="kvstat-label">Background worker</div>
          <div className="kvstat-value">
            <span className={"pill " + (info.worker_available ? "delivered" : info.worker_available === false ? "cancelled" : "draft")}>
              {info.worker_available ? "available" : info.worker_available === false ? "down" : "—"}
            </span>
          </div>
        </div>
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

      <div className="card card-scroll">
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
