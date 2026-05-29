// EditorScreen.tsx — Build › Editor (D4). Agent-first plugin IDE: sessions ·
// assistant chat · files. The chat is wired to the assistant server fn (F1).
import { useRef, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { sendAssistantMessage } from "~/server/assistant";

type Msg = { id: string; role: "user" | "assistant"; content: string };
type Sess = { id: string; title: string; plugin: string };

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

export function EditorScreen() {
  const [sessions, setSessions] = useState<Sess[]>([{ id: "s1", title: "New carrier: Acme Express", plugin: "acme" }]);
  const [activeSession, setActiveSession] = useState("s1");
  const [messages, setMessages] = useState<Msg[]>([
    { id: "m0", role: "assistant", content: "Hi! Describe the carrier or plugin you want to build and I'll scaffold it." },
  ]);
  const [draft, setDraft] = useState("");
  const [model, setModel] = useState("claude-opus-4-8");
  const [mode, setMode] = useState("agent");
  const [sending, setSending] = useState(false);
  const [files, setFiles] = useState<string[]>(FILES);
  const [scaffoldSlug, setScaffoldSlug] = useState("");
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

  return (
    <div className="editor" data-testid="screen-editor">
      <div className="editor-pane">
        <div className="editor-pane-head">
          <span>Agent sessions</span>
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
      </div>

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
            <select className="select-sm" value={model} onChange={(e) => setModel(e.target.value)} aria-label="Model" data-testid="editor-model">
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
