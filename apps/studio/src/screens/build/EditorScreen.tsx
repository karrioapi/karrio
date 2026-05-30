// EditorScreen.tsx — Build › Editor (D4). Agent-first plugin IDE: sessions ·
// assistant chat · files. The chat is wired to the assistant server fn (F1).
// Agent definitions are persisted via ~/lib/karrio/agents (F2).
import { useEffect, useRef, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { sendAssistantMessage } from "~/server/assistant";
import { agents, seedDefaultAgents, type AgentDef, type AgentModel } from "~/lib/karrio/agents";

type Msg = { id: string; role: "user" | "assistant"; content: string };
type Sess = { id: string; title: string; plugin: string; agentId?: string };

// Standard Karrio connector extension layout (mirrors `bin/cli sdk add-extension`).
function connectorFiles(slug: string): string[] {
  return [
    `karrio/mappers/${slug}/__init__.py`,
    `karrio/mappers/${slug}/mapper.py`,
    `karrio/mappers/${slug}/proxy.py`,
    `karrio/mappers/${slug}/settings.py`,
    `karrio/providers/${slug}/__init__.py`,
    `karrio/providers/${slug}/rate.py`,
    `karrio/providers/${slug}/shipment/create.py`,
    `karrio/providers/${slug}/shipment/cancel.py`,
    `karrio/providers/${slug}/tracking.py`,
    `karrio/providers/${slug}/error.py`,
    `karrio/providers/${slug}/units.py`,
    `karrio/schemas/${slug}/`,
    `tests/${slug}/test_rate.py`,
    `tests/${slug}/test_shipment.py`,
    `tests/${slug}/test_tracking.py`,
  ];
}

const FILES = ["__init__.py", "settings.py", "mapper.py", "providers/rate.py", "providers/tracking.py", "units.py"];

// ---------------------------------------------------------------------------
// Agent form (create / edit)
// ---------------------------------------------------------------------------

type AgentFormProps = {
  initial?: AgentDef;
  onSave: (agent: AgentDef) => void;
  onCancel: () => void;
};

function AgentForm({ initial, onSave, onCancel }: AgentFormProps) {
  const [name, setName] = useState(initial?.name ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [systemPrompt, setSystemPrompt] = useState(initial?.systemPrompt ?? "");
  const [model, setModel] = useState<AgentModel>(initial?.model ?? "claude-sonnet-4-6");
  const [enabled, setEnabled] = useState(initial?.enabled ?? true);
  const [toolsRaw, setToolsRaw] = useState((initial?.enabledTools ?? []).join(", "));
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSave = async () => {
    if (!name.trim()) {
      setError("Name is required.");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const enabledTools = toolsRaw
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean);
      const saved = initial
        ? await agents.update(initial.id, { name, description, systemPrompt, model, enabled, enabledTools })
        : await agents.create({ name, description, systemPrompt, model, enabled, enabledTools });
      onSave(saved);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to save agent.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="card" style={{ padding: 16, display: "flex", flexDirection: "column", gap: 10 }} data-testid="agent-form">
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{initial ? "Edit agent" : "New agent"}</div>
      {error && <div style={{ color: "var(--danger, #e53)", fontSize: 12 }}>{error}</div>}

      <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12, fontWeight: 500 }}>
        Name *
        <input
          className="field-input"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g. Carrier Connector Builder"
          data-testid="agent-form-name"
        />
      </label>

      <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12, fontWeight: 500 }}>
        Description
        <input
          className="field-input"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Short description shown in the sidebar"
          data-testid="agent-form-description"
        />
      </label>

      <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12, fontWeight: 500 }}>
        System prompt
        <textarea
          className="field-input"
          style={{ minHeight: 80, resize: "vertical" }}
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          placeholder="Instructions prepended before every user message…"
          data-testid="agent-form-prompt"
        />
      </label>

      <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12, fontWeight: 500 }}>
        Model
        <select
          className="select-sm"
          style={{ height: 30 }}
          value={model}
          onChange={(e) => setModel(e.target.value as AgentModel)}
          data-testid="agent-form-model"
        >
          <option value="claude-opus-4-8">Opus 4.8</option>
          <option value="claude-sonnet-4-6">Sonnet 4.6</option>
          <option value="claude-haiku-3-5">Haiku 3.5</option>
        </select>
      </label>

      <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12, fontWeight: 500 }}>
        Enabled tools <span className="muted" style={{ fontWeight: 400 }}>(comma-separated IDs)</span>
        <input
          className="field-input"
          value={toolsRaw}
          onChange={(e) => setToolsRaw(e.target.value)}
          placeholder="e.g. scaffold_connector, read_file, run_tests"
          data-testid="agent-form-tools"
        />
      </label>

      <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12, fontWeight: 500, cursor: "pointer" }}>
        <input
          type="checkbox"
          checked={enabled}
          onChange={(e) => setEnabled(e.target.checked)}
          data-testid="agent-form-enabled"
        />
        Enabled
      </label>

      <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
        <button
          className="btn btn-primary btn-sm"
          onClick={() => void handleSave()}
          disabled={saving}
          data-testid="agent-form-save"
        >
          {saving ? "Saving…" : "Save"}
        </button>
        <button className="btn btn-sm" onClick={onCancel} data-testid="agent-form-cancel">
          Cancel
        </button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Agents panel (list + add/edit/delete)
// ---------------------------------------------------------------------------

type AgentsPanelProps = {
  onSelectAgent: (agent: AgentDef) => void;
  selectedAgentId?: string;
};

function AgentsPanel({ onSelectAgent, selectedAgentId }: AgentsPanelProps) {
  const [agentList, setAgentList] = useState<AgentDef[]>([]);
  const [editing, setEditing] = useState<AgentDef | "new" | null>(null);

  const load = () =>
    agents
      .list()
      .then(setAgentList)
      .catch(() => undefined);

  useEffect(() => {
    void seedDefaultAgents().then(load);
  }, []);

  const handleSaved = (agent: AgentDef) => {
    setEditing(null);
    void load();
    onSelectAgent(agent);
  };

  const handleDelete = async (id: string) => {
    await agents.remove(id);
    await load();
  };

  if (editing !== null) {
    return (
      <AgentForm
        initial={editing === "new" ? undefined : editing}
        onSave={handleSaved}
        onCancel={() => setEditing(null)}
      />
    );
  }

  return (
    <>
      <div className="editor-pane-head">
        <span>Agents</span>
        <button
          className="btn btn-sm"
          style={{ marginLeft: "auto" }}
          onClick={() => setEditing("new")}
          data-testid="agent-add"
        >
          <Icon.Plus size={12} /> New
        </button>
      </div>
      <div className="editor-pane-body" data-testid="agent-list">
        {agentList.length === 0 && (
          <div className="state-row" style={{ padding: "12px 16px", fontSize: 12 }}>No agents yet.</div>
        )}
        {agentList.map((a) => (
          <div
            key={a.id}
            className={"session-item" + (a.id === selectedAgentId ? " active" : "")}
            style={{ position: "relative" }}
            data-testid={`agent-item-${a.id}`}
          >
            <span
              className="session-dot"
              style={{ background: a.enabled ? "var(--green, #16a34a)" : "var(--muted-fg, #aaa)" }}
            />
            <button
              style={{
                flex: 1,
                textAlign: "left",
                background: "none",
                border: "none",
                cursor: "pointer",
                minWidth: 0,
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                padding: 0,
                fontSize: "inherit",
              }}
              onClick={() => onSelectAgent(a)}
              title={a.description || a.name}
            >
              {a.name}
            </button>
            <div style={{ display: "flex", gap: 4, flexShrink: 0 }}>
              <button
                className="btn btn-sm"
                style={{ padding: "1px 5px", fontSize: 10 }}
                onClick={(e) => { e.stopPropagation(); setEditing(a); }}
                data-testid={`agent-edit-${a.id}`}
                title="Edit agent"
              >
                <Icon.Settings size={11} />
              </button>
              <button
                className="btn btn-sm"
                style={{ padding: "1px 5px", fontSize: 10 }}
                onClick={(e) => { e.stopPropagation(); void handleDelete(a.id); }}
                data-testid={`agent-delete-${a.id}`}
                title="Delete agent"
              >
                <Icon.X size={11} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

// ---------------------------------------------------------------------------
// Main EditorScreen
// ---------------------------------------------------------------------------

export function EditorScreen() {
  const [sessions, setSessions] = useState<Sess[]>([{ id: "s1", title: "New carrier: Acme Express", plugin: "acme" }]);
  const [activeSession, setActiveSession] = useState("s1");
  const [messages, setMessages] = useState<Msg[]>([
    { id: "m0", role: "assistant", content: "Hi! Describe the carrier or plugin you want to build and I'll scaffold it." },
  ]);
  const [draft, setDraft] = useState("");
  const [model, setModel] = useState<AgentModel>("claude-opus-4-8");
  const [mode, setMode] = useState("agent");
  const [sending, setSending] = useState(false);
  const [files, setFiles] = useState<string[]>(FILES);
  const [scaffoldSlug, setScaffoldSlug] = useState("");
  const [selectedAgentId, setSelectedAgentId] = useState<string | undefined>();
  const [leftTab, setLeftTab] = useState<"sessions" | "agents">("sessions");
  const streamRef = useRef<HTMLDivElement>(null);

  const scaffold = () => {
    const slug = scaffoldSlug.trim().toLowerCase().replace(/[^a-z0-9_]+/g, "_");
    if (!slug) return;
    const generated = connectorFiles(slug);
    setFiles(generated);
    setSessions((s) => s.map((x) => (x.id === activeSession ? { ...x, title: `New carrier: ${slug}`, plugin: slug } : x)));
    setMessages((m) => [
      ...m,
      { id: `s${Date.now()}`, role: "assistant", content: `Scaffolded connector **${slug}** — ${generated.length} files created from the Karrio SDK extension template (mappers, providers, schemas, tests). Describe ${slug}'s rate/label/tracking API and I'll fill them in.` },
    ]);
    setScaffoldSlug("");
  };

  const send = async () => {
    const text = draft.trim();
    if (!text || sending) return;
    const userMsg: Msg = { id: `u${Date.now()}`, role: "user", content: text };
    setMessages((m) => [...m, userMsg]);
    setDraft("");
    setSending(true);
    try {
      const res = await sendAssistantMessage({ data: { message: text, model, mode } });
      setMessages((m) => [...m, { id: `a${Date.now()}`, role: "assistant", content: res.reply }]);
    } catch {
      setMessages((m) => [...m, { id: `e${Date.now()}`, role: "assistant", content: "Something went wrong." }]);
    } finally {
      setSending(false);
      requestAnimationFrame(() => streamRef.current?.scrollTo({ top: streamRef.current.scrollHeight }));
    }
  };

  const newSession = () => {
    const id = `s${Date.now()}`;
    setSessions((s) => [{ id, title: "Untitled session", plugin: "—" }, ...s]);
    setActiveSession(id);
    setMessages([{ id: "m0", role: "assistant", content: "New session. What should we build?" }]);
  };

  const handleSelectAgent = (agent: AgentDef) => {
    setSelectedAgentId(agent.id);
    setModel(agent.model as AgentModel);
    setLeftTab("sessions");
  };

  return (
    <div className="editor" data-testid="screen-editor">
      {/* Left pane: tabbed Sessions / Agents */}
      <div className="editor-pane">
        <div style={{ display: "flex", borderBottom: "1px solid var(--border)" }}>
          <button
            className={"tab" + (leftTab === "sessions" ? " active" : "")}
            style={{ flex: 1, borderRadius: 0, border: "none", fontSize: 12 }}
            onClick={() => setLeftTab("sessions")}
            data-testid="left-tab-sessions"
          >
            Sessions
          </button>
          <button
            className={"tab" + (leftTab === "agents" ? " active" : "")}
            style={{ flex: 1, borderRadius: 0, border: "none", fontSize: 12 }}
            onClick={() => setLeftTab("agents")}
            data-testid="left-tab-agents"
          >
            Agents
          </button>
        </div>

        {leftTab === "sessions" && (
          <>
            <div className="editor-pane-head">
              <span>Sessions</span>
              <button className="btn btn-sm" style={{ marginLeft: "auto" }} onClick={newSession} data-testid="editor-new-session">
                <Icon.Plus size={12} /> New
              </button>
            </div>
            <div className="editor-pane-body" data-testid="editor-sessions">
              {sessions.map((s) => (
                <div
                  key={s.id}
                  className={"session-item" + (s.id === activeSession ? " active" : "")}
                  onClick={() => setActiveSession(s.id)}
                  data-testid={`editor-session-${s.id}`}
                >
                  <span className="session-dot" />
                  <span style={{ minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{s.title}</span>
                </div>
              ))}
            </div>
          </>
        )}

        {leftTab === "agents" && (
          <AgentsPanel onSelectAgent={handleSelectAgent} selectedAgentId={selectedAgentId} />
        )}
      </div>

      {/* Chat pane */}
      <div className="chat">
        <div className="chat-stream" ref={streamRef} data-testid="editor-messages">
          {messages.map((m) => (
            <div key={m.id} className={"msg " + m.role} data-testid={`msg-${m.role}`}>
              <div className="msg-role">{m.role}</div>
              <div className="msg-body">{m.content}</div>
            </div>
          ))}
        </div>
        <div className="composer">
          <textarea
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
                e.preventDefault();
                void send();
              }
            }}
            placeholder="Describe what to build… (⌘↵ to send)"
            data-testid="editor-input"
            aria-label="Message the assistant"
          />
          <div className="composer-bar">
            <select className="select-sm" value={model} onChange={(e) => setModel(e.target.value as AgentModel)} aria-label="Model" data-testid="editor-model">
              <option value="claude-opus-4-8">Opus 4.8</option>
              <option value="claude-sonnet-4-6">Sonnet 4.6</option>
            </select>
            <select className="select-sm" value={mode} onChange={(e) => setMode(e.target.value)} aria-label="Mode" data-testid="editor-mode">
              <option value="agent">Agent</option>
              <option value="ask">Ask</option>
            </select>
            <div style={{ flex: 1 }} />
            <button className="btn btn-primary" onClick={() => void send()} disabled={sending} data-testid="editor-send">
              {sending ? "Sending…" : "Send"}
            </button>
          </div>
        </div>
      </div>

      {/* Right pane: file tree + scaffold */}
      <div className="editor-pane right">
        <div className="editor-pane-head">Files · {sessions.find((s) => s.id === activeSession)?.plugin}</div>
        <div style={{ display: "flex", gap: 6, padding: "8px 8px 0" }}>
          <input
            className="field-input"
            style={{ height: 26, fontSize: 12 }}
            placeholder="carrier slug…"
            value={scaffoldSlug}
            onChange={(e) => setScaffoldSlug(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && scaffold()}
            data-testid="editor-scaffold-input"
            aria-label="Carrier slug to scaffold"
          />
          <button className="btn btn-sm" onClick={scaffold} data-testid="editor-scaffold">Scaffold</button>
        </div>
        <div className="editor-pane-body" data-testid="editor-files">
          {files.map((f) => (
            <div key={f} className="file-item" data-testid={`editor-file-${f.replace(/[^a-z]/gi, "")}`}>{f}</div>
          ))}
        </div>
      </div>
    </div>
  );
}
