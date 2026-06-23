// WorkspaceMenu.tsx — sidebar workspace/org switcher. OSS Karrio is single-tenant
// (no `organizations` in the GraphQL schema), so this presents the connected
// workspace honestly + settings, and notes that multi-org is an Enterprise
// feature rather than faking an org switch.
import { useEffect, useRef, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { useSession } from "~/lib/karrio/session";

export function WorkspaceMenu({ onGo }: { onGo: (route: string) => void }) {
  const { email, ctx } = useSession();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onDoc = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, [open]);

  // Honest workspace identity: the connected Karrio deployment host.
  let host = "workspace";
  try {
    host = new URL(ctx.baseUrl).host;
  } catch {
    /* keep fallback */
  }

  return (
    <div ref={ref} style={{ position: "relative" }}>
      <button
        type="button"
        className="workspace"
        data-testid="workspace-switcher"
        onClick={() => setOpen((o) => !o)}
        aria-haspopup="menu"
        aria-expanded={open}
        style={{ width: "100%", background: "none", border: "none", cursor: "pointer", textAlign: "left", font: "inherit", color: "inherit" }}
      >
        <div className="workspace-logo">K</div>
        <div className="workspace-body" style={{ minWidth: 0, flex: 1 }}>
          <div className="workspace-name">Karrio Studio</div>
          <div className="workspace-mode">{host}</div>
        </div>
        <Icon.ChevronD size={12} className="workspace-chev" style={{ color: "var(--fg-subtle)" }} />
      </button>

      {open && (
        <div className="menu" data-testid="workspace-menu" role="menu" style={{ position: "absolute", top: "calc(100% + 8px)", left: 0, right: 0, zIndex: 50 }}>
          <div style={{ padding: "8px 12px", borderBottom: "1px solid var(--border)" }}>
            <div className="workspace-name" style={{ fontSize: 12.5 }}>Karrio Studio</div>
            <div className="muted" style={{ fontSize: 11 }}>{email ?? host}</div>
          </div>
          <div className="menu-item" role="menuitem" data-testid="workspace-menu-settings" onClick={() => { setOpen(false); onGo("settings"); }}>
            <span className="icon"><Icon.Settings size={14} /></span><span>Workspace settings</span>
          </div>
          <div className="menu-item" role="menuitem" data-testid="workspace-menu-connections" onClick={() => { setOpen(false); onGo("connections"); }}>
            <span className="icon"><Icon.Plug size={14} /></span><span>Carrier connections</span>
          </div>
          <div className="menu-sep" />
          <div className="menu-item" role="menuitem" aria-disabled="true" style={{ opacity: 0.7, cursor: "default" }} data-testid="workspace-menu-orgs">
            <span className="icon"><Icon.Shield size={14} /></span>
            <span>Multiple organizations<span className="muted" style={{ fontSize: 10, marginLeft: 6 }}>Enterprise</span></span>
          </div>
        </div>
      )}
    </div>
  );
}
