// UserMenu.tsx — sidebar-foot account menu: real user identity + sign out.
import { useEffect, useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Icon } from "~/components/ui/icons";
import { useSession } from "~/lib/karrio/session";
import { logout } from "~/server/auth";

export function UserMenu({ onGo, onTweaks }: { onGo: (route: string) => void; onTweaks: () => void }) {
  const { email } = useSession();
  const qc = useQueryClient();
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

  const name = email ?? "Account";
  const initials = (email ?? "U").replace(/@.*/, "").slice(0, 2).toUpperCase();

  const signOut = async () => {
    try {
      await logout();
    } catch {
      /* even if the server call fails, clear the client session */
    }
    qc.setQueryData(["studio-session"], null);
    window.location.assign("/login"); // hard nav clears all in-memory state
  };

  return (
    <div className="user-menu-wrap" ref={ref} style={{ position: "relative" }}>
      <button
        type="button"
        className="sidebar-foot"
        onClick={() => setOpen((o) => !o)}
        data-testid="user-menu-trigger"
        aria-haspopup="menu"
        aria-expanded={open}
        style={{ width: "100%", background: "none", border: "none", cursor: "pointer", textAlign: "left", font: "inherit", color: "inherit" }}
      >
        <div className="avatar">{initials}</div>
        <div className="grow user-meta" style={{ minWidth: 0 }}>
          <div className="user-name">{name}</div>
          <div className="user-role">Signed in</div>
        </div>
        <span className="icon-action user-chev"><Icon.ChevronD size={12} /></span>
      </button>

      {open && (
        <div className="menu" data-testid="user-menu" role="menu" style={{ position: "absolute", bottom: "calc(100% + 8px)", left: 0, right: 0, zIndex: 50 }}>
          <div style={{ padding: "8px 12px", borderBottom: "1px solid var(--border)", fontSize: 12 }}>
            <div className="user-name" style={{ fontSize: 12.5 }}>{name}</div>
            <div className="muted" style={{ fontSize: 11 }}>{email ? "Account" : "Not signed in"}</div>
          </div>
          <div className="menu-item" role="menuitem" data-testid="user-menu-settings" onClick={() => { setOpen(false); onGo("settings"); }}>
            <span className="icon"><Icon.Settings size={14} /></span><span>Account settings</span>
          </div>
          <div className="menu-item" role="menuitem" data-testid="user-menu-appearance" onClick={() => { setOpen(false); onTweaks(); }}>
            <span className="icon"><Icon.Sliders size={14} /></span><span>Appearance</span>
          </div>
          <div className="menu-sep" />
          <div className="menu-item" role="menuitem" data-testid="user-menu-logout" onClick={signOut}>
            <span className="icon"><Icon.Lock size={14} /></span><span>Sign out</span>
          </div>
        </div>
      )}
    </div>
  );
}
