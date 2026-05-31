// Chart.tsx — dependency-free inline-SVG charts for usage time-series.
// Renders a smooth area/line series scaled to its container, with a baseline
// and an optional value formatter. Keeps Studio standalone (no chart lib).
import { useId } from "react";
import type { UsagePoint } from "~/lib/karrio/types";

type Fmt = "number" | "currency";

const fmtValue = (n: number, fmt?: Fmt) =>
  fmt === "currency" ? `$${n.toLocaleString(undefined, { maximumFractionDigits: 0 })}` : n.toLocaleString();

export function AreaChart({
  points,
  format,
  height = 64,
  testId,
}: {
  points: UsagePoint[];
  format?: Fmt;
  height?: number;
  testId?: string;
}) {
  const gid = useId().replace(/[:]/g, "");
  const W = 100; // viewBox width units (path uses % via preserveAspectRatio="none")
  const H = height;
  const pad = 4;

  if (points.length === 0) {
    return (
      <div className="chart-empty muted" data-testid={testId} style={{ height, display: "flex", alignItems: "center", fontSize: 12 }}>
        No data for this period.
      </div>
    );
  }

  const vals = points.map((p) => p.count);
  const max = Math.max(...vals, 1);
  const min = Math.min(...vals, 0);
  const span = max - min || 1;
  const n = points.length;
  const x = (i: number) => (n === 1 ? W / 2 : (i / (n - 1)) * W);
  const y = (v: number) => pad + (1 - (v - min) / span) * (H - pad * 2);

  const line = points.map((p, i) => `${i === 0 ? "M" : "L"}${x(i).toFixed(2)},${y(p.count).toFixed(2)}`).join(" ");
  const area = `${line} L${W},${H} L0,${H} Z`;
  const last = points[points.length - 1];

  return (
    <div className="chart" data-testid={testId} style={{ position: "relative" }}>
      <svg viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" width="100%" height={H} role="img" aria-label="usage trend">
        <defs>
          <linearGradient id={`g${gid}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.28" />
            <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d={area} fill={`url(#g${gid})`} />
        <path d={line} fill="none" stroke="var(--accent)" strokeWidth="1.5" vectorEffect="non-scaling-stroke" strokeLinejoin="round" strokeLinecap="round" />
        <circle cx={x(n - 1)} cy={y(last.count)} r="2" fill="var(--accent)" vectorEffect="non-scaling-stroke" />
      </svg>
      <div className="muted" style={{ display: "flex", justifyContent: "space-between", fontSize: 10.5, marginTop: 4 }}>
        <span>{points[0]?.date?.slice(0, 10)}</span>
        <span style={{ color: "var(--fg)", fontWeight: 600 }}>{fmtValue(last.count, format)}</span>
        <span>{last.date?.slice(0, 10)}</span>
      </div>
    </div>
  );
}
