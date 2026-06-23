// McpScreen.tsx — Build › MCP (D3). Manage the Karrio MCP server + user-defined
// MCP server configurations (F3). The Karrio server card reflects live API data.
// User-managed server configs are persisted to localStorage via ~/lib/karrio/agents.
//
// IMPORTANT: Actual MCP execution (connecting, invoking tools) is NOT supported
// in OSS Karrio — there is no backend proxy. All user-added servers show status
// "config only". Never display a fabricated "connected" or "healthy" status.
import { useEffect, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader } from "~/components/ui/primitives";
import { NotAvailableNotice } from "~/components/ui/NotAvailable";
import { useMcp } from "~/lib/karrio/hooks";
import { mcpServers, type McpServerConfig, type McpTransport } from "~/lib/karrio/agents";

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

// ---------------------------------------------------------------------------
// MCP server form (add / edit user-managed servers)
// ---------------------------------------------------------------------------

type McpServerFormProps = {
  initial?: McpServerConfig;
  onSave: (server: McpServerConfig) => void;
  onCancel: () => void;
};

function McpServerForm({ initial, onSave, onCancel }: McpServerFormProps) {
  const [name, setName] = useState(initial?.name ?? "");
  const [transport, setTransport] = useState<McpTransport>(initial?.transport ?? "stdio");
  const [endpoint, setEndpoint] = useState(initial?.endpoint ?? "");
  const [envRaw, setEnvRaw] = useState(
    initial?.env ? Object.entries(initial.env).map(([k, v]) => `${k}=${v}`).join("\n") : "",
  );
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const parseEnv = (raw: string): Record<string, string> =>
    Object.fromEntries(
      raw
        .split("\n")
        .map((line) => line.trim())
        .filter(Boolean)
        .map((line) => {
          const eq = line.indexOf("=");
          return eq > 0 ? [line.slice(0, eq).trim(), line.slice(eq + 1).trim()] : null;
        })
        .filter((pair): pair is [string, string] => pair !== null),
    );

  const handleSave = async () => {
    if (!name.trim()) { setError("Name is required."); return; }
    if (!endpoint.trim()) { setError("Endpoint / command is required."); return; }
    setSaving(true);
    setError(null);
    try {
      const env = parseEnv(envRaw);
      const saved = initial
        ? await mcpServers.update(initial.id, { name, transport, endpoint, env })
        : await mcpServers.create({ name, transport, endpoint, env });
      onSave(saved);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to save.");
    } finally {
      setSaving(false);
    }
  };

  const endpointLabel = transport === "stdio" ? "Command" : "URL";
  const endpointPlaceholder =
    transport === "stdio" ? "e.g. npx @my/mcp-server" : "e.g. https://mcp.example.com/events";

  return (
    <div className="card" style={{ padding: 16, display: "flex", flexDirection: "column", gap: 10 }} data-testid="mcp-server-form">
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{initial ? "Edit MCP server" : "Add MCP server"}</div>
      {error && <div style={{ color: "var(--danger, #e53)", fontSize: 12 }}>{error}</div>}

      <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12, fontWeight: 500 }}>
        Name *
        <input className="field-input" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. My MCP server" data-testid="mcp-form-name" />
      </label>

      <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12, fontWeight: 500 }}>
        Transport
        <select className="select-sm" style={{ height: 30 }} value={transport} onChange={(e) => setTransport(e.target.value as McpTransport)} data-testid="mcp-form-transport">
          <option value="stdio">stdio (local process)</option>
          <option value="sse">SSE (server-sent events)</option>
          <option value="http">HTTP (streamable)</option>
        </select>
      </label>

      <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12, fontWeight: 500 }}>
        {endpointLabel} *
        <input className="field-input" value={endpoint} onChange={(e) => setEndpoint(e.target.value)} placeholder={endpointPlaceholder} data-testid="mcp-form-endpoint" />
      </label>

      {transport === "stdio" && (
        <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12, fontWeight: 500 }}>
          Environment variables <span className="muted" style={{ fontWeight: 400 }}>(one KEY=value per line)</span>
          <textarea
            className="field-input"
            style={{ minHeight: 60, resize: "vertical", fontFamily: "var(--font-mono, monospace)", fontSize: 11 }}
            value={envRaw}
            onChange={(e) => setEnvRaw(e.target.value)}
            placeholder={"API_KEY=sk_live_...\nSECRET=..."}
            data-testid="mcp-form-env"
          />
        </label>
      )}

      <div style={{ padding: "8px 10px", background: "var(--surface-muted, #f5f5f5)", borderRadius: 6, fontSize: 11, color: "var(--muted-fg, #888)" }} data-testid="mcp-form-notice">
        Configuration only — OSS Karrio does not include an MCP execution proxy. Actual connection and tool invocation require a backend proxy (not yet implemented).
      </div>

      <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
        <button className="btn btn-primary btn-sm" onClick={() => void handleSave()} disabled={saving} data-testid="mcp-form-save">
          {saving ? "Saving…" : "Save"}
        </button>
        <button className="btn btn-sm" onClick={onCancel} data-testid="mcp-form-cancel">Cancel</button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// User-managed MCP servers section
// ---------------------------------------------------------------------------

function UserMcpServers() {
  const [serverList, setServerList] = useState<McpServerConfig[]>([]);
  const [editing, setEditing] = useState<McpServerConfig | "new" | null>(null);

  const load = () =>
    mcpServers
      .list()
      .then(setServerList)
      .catch(() => undefined);

  useEffect(() => { void load(); }, []);

  const handleSaved = (server: McpServerConfig) => {
    setEditing(null);
    void load();
  };

  const handleDelete = async (id: string) => {
    await mcpServers.remove(id);
    await load();
  };

  if (editing !== null) {
    return (
      <McpServerForm
        initial={editing === "new" ? undefined : editing}
        onSave={handleSaved}
        onCancel={() => setEditing(null)}
      />
    );
  }

  return (
    <div className="card card-scroll" data-testid="mcp-user-servers">
      <div style={{ padding: "12px 16px", borderBottom: "1px solid var(--border)", display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{ fontWeight: 600, flex: 1 }}>Your MCP servers</span>
        <button className="btn btn-sm" onClick={() => setEditing("new")} data-testid="mcp-add-server">
          <Icon.Plus size={12} /> Add
        </button>
      </div>
      {serverList.length === 0 ? (
        <div className="state-row" style={{ padding: "16px", fontSize: 12 }}>
          No MCP servers configured. Add one to store its connection details.
        </div>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Transport</th>
              <th>Endpoint</th>
              <th>Status</th>
              <th style={{ textAlign: "right" }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {serverList.map((s) => (
              <tr key={s.id} data-testid={`mcp-server-row-${s.id}`}>
                <td style={{ fontWeight: 500 }}>{s.name}</td>
                <td><span className="pill" style={{ background: "var(--surface-muted, #eee)", color: "inherit", fontSize: 10 }}>{s.transport}</span></td>
                <td className="mono muted" style={{ fontSize: 11, maxWidth: 240, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{s.endpoint}</td>
                <td>
                  {/* Honest status: never claim "connected" — no backend proxy in OSS */}
                  <span className="pill" style={{ background: "var(--surface-muted, #eee)", color: "var(--muted-fg, #888)", fontSize: 10 }} data-testid={`mcp-server-status-${s.id}`}>
                    config only
                  </span>
                </td>
                <td style={{ textAlign: "right" }}>
                  <div style={{ display: "flex", gap: 4, justifyContent: "flex-end" }}>
                    <button
                      className="btn btn-sm"
                      style={{ padding: "2px 6px", fontSize: 11 }}
                      onClick={() => setEditing(s)}
                      data-testid={`mcp-server-edit-${s.id}`}
                    >
                      <Icon.Settings size={11} />
                    </button>
                    <button
                      className="btn btn-sm"
                      style={{ padding: "2px 6px", fontSize: 11 }}
                      onClick={() => void handleDelete(s.id)}
                      data-testid={`mcp-server-delete-${s.id}`}
                    >
                      <Icon.X size={11} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// McpScreen — top-level
// ---------------------------------------------------------------------------

export function McpScreen() {
  useMcp(); // resolves "not_available" on OSS — no hosted MCP proxy

  return (
    <div className="page" data-testid="screen-mcp">
      <PageHeader
        title="Karrio MCP"
        actions={<button className="btn"><Icon.Doc size={14} /> Docs</button>}
      />

      <NotAvailableNotice
        feature="A hosted Karrio MCP server"
        detail="The open-source Karrio API doesn’t run an MCP server proxy, so there’s no live server status, tool catalog, or invocation history to show. You can still register and manage your own MCP servers below."
      />

      {/* User-managed MCP server configurations (F3) — real, persisted locally. */}
      <div style={{ marginTop: 16 }}>
        <UserMcpServers />
      </div>
    </div>
  );
}
