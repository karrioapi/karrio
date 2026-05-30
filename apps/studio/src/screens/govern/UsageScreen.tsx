// UsageScreen.tsx — Govern › Usage & billing (dashboard parity).
import { useMemo } from "react";
import { PageHeader } from "~/components/ui/primitives";
import { useUsage } from "~/lib/karrio/hooks";

export function UsageScreen() {
  const { data, isLoading } = useUsage();
  const metrics = useMemo(() => data?.metrics ?? [], [data]);

  return (
    <div className="page" data-testid="screen-usage">
      <PageHeader title="Usage & billing" actions={<button className="btn">Manage plan</button>} />

      <div className="card" style={{ padding: 16, marginBottom: 16 }} data-testid="usage-plan">
        <div className="kvstat-label">Current plan</div>
        <div className="kvstat-value">{data?.plan ?? (isLoading ? "…" : "Free")}</div>
        <div className="muted" style={{ fontSize: 12, marginTop: 4 }}>{data?.period ?? "Current billing period"}</div>
      </div>

      <div className="stat-grid" data-testid="usage-metrics">
        {metrics.length === 0 && !isLoading && (
          <div className="state-row" data-testid="usage-empty">No usage data for this period.</div>
        )}
        {metrics.map((m) => (
          <div key={m.label} className="stat-card">
            <div className="kvstat-label">{m.label}</div>
            <div className="kvstat-value">{m.value}</div>
            {m.delta && <div className="stat-card-meta"><span className={m.delta.startsWith("-") ? "down" : "up"}>{m.delta}</span> vs last period</div>}
          </div>
        ))}
      </div>
    </div>
  );
}
