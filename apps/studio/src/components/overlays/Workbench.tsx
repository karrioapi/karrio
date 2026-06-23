// Workbench.tsx — Stripe-style developer overlay (⌘`). Always dark.
import { useEffect, useState } from "react";
import { Icon } from "~/components/ui/icons";

const NAV = ["Logs", "Events", "Webhooks", "GraphiQL", "Health", "Workers", "Tracing"] as const;

const LOGS = [
  { id: "l1", method: "POST", status: 201, path: "/v1/shipments", ms: 612 },
  { id: "l2", method: "GET", status: 200, path: "/v1/trackers", ms: 84 },
  { id: "l3", method: "POST", status: 422, path: "/v1/shipments", ms: 38 },
  { id: "l4", method: "GET", status: 200, path: "/v1/connections", ms: 51 },
];

export function Workbench({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [tab, setTab] = useState<(typeof NAV)[number]>("Logs");
  const [full, setFull] = useState(false);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  return (
    <div className={"wb" + (open ? " open" : "") + (full ? " full" : "")} data-theme="dark" data-testid="workbench" aria-hidden={!open}>
      <div className="wb-nav">
        {NAV.map((n) => (
          <div key={n} className={"wb-nav-item" + (tab === n ? " active" : "")} onClick={() => setTab(n)} data-testid={`wb-nav-${n.toLowerCase()}`}>
            {n}
          </div>
        ))}
      </div>
      <div className="wb-main">
        <div className="wb-head">
          <span style={{ fontWeight: 600, fontSize: 12.5 }}>Workbench · {tab}</span>
          <div style={{ marginLeft: "auto", display: "flex", gap: 6 }}>
            <button className="icon-btn" aria-label="Toggle fullscreen" onClick={() => setFull((f) => !f)}><Icon.Workspace size={13} /></button>
            <button className="icon-btn" aria-label="Close workbench" onClick={onClose} data-testid="wb-close"><Icon.X size={13} /></button>
          </div>
        </div>
        <div className="wb-body" data-testid="wb-body">
          {tab === "Logs" ? (
            <div data-testid="wb-logs">
              {LOGS.map((l) => (
                <div key={l.id} className="wb-row" data-testid={`wb-log-${l.id}`}>
                  <span className="wb-method">{l.method}</span>
                  <span className={"wb-status-" + String(l.status)[0]}>{l.status}</span>
                  <span>{l.path}</span>
                  <span style={{ color: "#8b8b93" }}>{l.ms}ms</span>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ color: "#8b8b93" }}>{tab} view — live data wires to the Karrio admin API.</div>
          )}
        </div>
      </div>
    </div>
  );
}
