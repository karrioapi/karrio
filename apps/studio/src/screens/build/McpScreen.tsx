// McpScreen.tsx — Build › MCP (D3). Manage the Karrio MCP server.
import { useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader } from "~/components/ui/primitives";
import { useMcp } from "~/lib/karrio/hooks";

function KvStat({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div>
      <div className="kvstat-label">{label}</div>
      <div className="kvstat-value">{value}</div>
    </div>
  );
}

const CLAUDE_SNIPPET = `{
  "mcpServers": {
    "karrio": {
      "command": "npx",
      "args": ["-y", "@karrio/mcp"],
      "env": { "KARRIO_API_KEY": "sk_live_•••••" }
    }
  }
}`;

export function McpScreen() {
  const { data, isLoading } = useMcp();
  // null = follow server state; true/false = user override (optimistic toggle).
  const [override, setOverride] = useState<boolean | null>(null);
  const info = data ?? {};
  const tools = info.tools ?? [];
  const clients = info.clients ?? [];
  const invocations = info.invocations ?? [];
  const on = override ?? (info.status ? info.status === "running" : true);

  const copy = (text: string) => {
    try {
      void navigator.clipboard?.writeText(text);
    } catch {
      /* clipboard may be unavailable in some contexts */
    }
  };

  return (
    <div className="page" data-testid="screen-mcp">
      <PageHeader
        title="Karrio MCP"
        actions={<><button className="btn"><Icon.Doc size={14} /> Docs</button><button className="btn btn-primary"><Icon.Plus size={14} /> New client</button></>}
      />

      <div className="card" style={{ padding: 16, marginBottom: 16, display: "flex", alignItems: "center", gap: 16, flexWrap: "wrap" }} data-testid="mcp-server-card">
        <div style={{ flex: 1, minWidth: 200 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{ fontWeight: 600 }}>MCP server</span>
            <span className={"pill " + (on ? "delivered" : "cancelled")} data-testid="mcp-status">{on ? "running" : "stopped"}</span>
            <span className="muted mono" style={{ fontSize: 11.5 }}>{info.version ?? "v2026.5.1"}</span>
          </div>
          <div className="mono muted" style={{ fontSize: 12, marginTop: 3 }}>{info.url ?? "https://mcp.karrio.io/acme-shipping"}</div>
        </div>
        <div style={{ display: "flex", gap: 18 }}>
          <KvStat label="Tools" value={info.stats?.tools ?? tools.length} />
          <KvStat label="Clients" value={info.stats?.clients ?? clients.length} />
          <KvStat label="Calls 24h" value={info.stats?.calls_24h ?? "—"} />
          <KvStat label="p99" value={info.stats?.p99 ?? "—"} />
        </div>
        <button className="btn" onClick={() => setOverride(!on)} data-testid="mcp-toggle">
          {on ? <><Icon.X size={13} /> Stop</> : <><Icon.Plus size={13} /> Start</>}
        </button>
      </div>

      <div className="card card-scroll" style={{ marginBottom: 16 }}>
        <div style={{ padding: "12px 16px", borderBottom: "1px solid var(--border)", fontWeight: 600 }}>Exposed tools</div>
        <table className="table">
          <thead><tr><th>Tool</th><th>Description</th><th style={{ textAlign: "right" }}>Requests</th><th style={{ textAlign: "right" }}>p99</th></tr></thead>
          <tbody data-testid="mcp-tools">
            {isLoading && <tr><td colSpan={4}><div className="state-row">Loading…</div></td></tr>}
            {!isLoading && tools.length === 0 && <tr><td colSpan={4}><div className="state-row">No tools exposed.</div></td></tr>}
            {tools.map((t) => (
              <tr key={t.name} data-testid={`mcp-tool-${t.name}`}>
                <td className="mono" style={{ fontWeight: 500 }}>{t.name}</td>
                <td className="muted" style={{ fontSize: 12 }}>{t.description}</td>
                <td className="mono" style={{ textAlign: "right" }}>{t.requests ?? "—"}</td>
                <td className="mono" style={{ textAlign: "right" }}>{t.p99 ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="two-col">
        <div className="card" style={{ padding: 16 }}>
          <div style={{ fontWeight: 600, marginBottom: 8 }}>Install — Claude Desktop</div>
          <pre className="snippet" data-testid="mcp-snippet">{CLAUDE_SNIPPET}</pre>
          <button className="btn btn-sm" style={{ marginTop: 8 }} onClick={() => copy(CLAUDE_SNIPPET)} data-testid="mcp-copy"><Icon.Copy size={12} /> Copy</button>
        </div>
        <div className="card card-scroll">
          <div style={{ padding: "12px 16px", borderBottom: "1px solid var(--border)", fontWeight: 600 }}>Recent invocations</div>
          <table className="table">
            <thead><tr><th>Tool</th><th>Client</th><th style={{ textAlign: "right" }}>ms</th></tr></thead>
            <tbody data-testid="mcp-invocations">
              {invocations.length === 0 && <tr><td colSpan={3}><div className="state-row">No recent invocations.</div></td></tr>}
              {invocations.map((iv) => (
                <tr key={iv.id}><td className="mono">{iv.tool}</td><td className="muted">{iv.client ?? "—"}</td><td className="mono" style={{ textAlign: "right" }}>{iv.duration_ms ?? "—"}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
