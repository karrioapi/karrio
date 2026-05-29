// Sidebar.tsx — mode-driven navigation (Ship / Build / Govern).
import { Icon, MODE_LABELS, NAV, type Mode } from "~/lib/modes";

const MODES: Mode[] = ["ship", "build", "govern"];

export function Sidebar({
  route,
  mode,
  collapsed,
  onGo,
  onMode,
}: {
  route: string;
  mode: Mode;
  collapsed: boolean;
  onGo: (route: string) => void;
  onMode: (mode: Mode) => void;
}) {
  return (
    <aside className={"sidebar" + (collapsed ? " collapsed" : "")} data-testid="sidebar">
      <div className="workspace" data-testid="workspace-switcher">
        <div className="workspace-logo">K</div>
        <div className="workspace-body" style={{ minWidth: 0, flex: 1 }}>
          <div className="workspace-name">Karrio Studio</div>
          <div className="workspace-mode">acme-shipping</div>
        </div>
        <Icon.ChevronD size={12} className="workspace-chev" style={{ color: "var(--fg-subtle)" }} />
      </div>

      <div className="modes" role="tablist" aria-label="Mode" data-testid="mode-switch">
        {MODES.map((m) => {
          const meta = MODE_LABELS[m];
          const ModeIcon = Icon[meta.icon];
          return (
            <button
              key={m}
              role="tab"
              aria-selected={mode === m}
              className={"mode" + (mode === m ? " active" : "")}
              onClick={() => onMode(m)}
              title={meta.label}
              data-testid={`mode-${m}`}
            >
              <span className="mode-icon">
                <ModeIcon size={12} />
              </span>
              <span className="mode-text">{meta.label}</span>
            </button>
          );
        })}
      </div>

      <nav className="nav">
        {NAV[mode].map((group, gi) => (
          <div className="nav-group" key={group.label ?? gi}>
            {group.label && <div className="nav-label">{group.label}</div>}
            {group.items.map((item) => {
              const ItemIcon = Icon[item.icon];
              const active = item.route === route;
              return (
                <a
                  key={item.label}
                  className={"nav-item" + (active ? " active" : "")}
                  title={item.label}
                  href={`/${item.route}`}
                  onClick={(e) => {
                    e.preventDefault();
                    onGo(item.route);
                  }}
                  data-testid={`nav-${item.route}`}
                  aria-current={active ? "page" : undefined}
                >
                  <span className="nav-icon">
                    <ItemIcon size={14} />
                  </span>
                  <span className="nav-text">{item.label}</span>
                  {item.badge && <span className="badge">{item.badge}</span>}
                </a>
              );
            })}
          </div>
        ))}
      </nav>

      <div className="sidebar-foot">
        <div className="avatar">DK</div>
        <div className="grow user-meta" style={{ minWidth: 0 }}>
          <div className="user-name">Daniel K.</div>
          <div className="user-role">Owner</div>
        </div>
        <span className="icon-action user-chev">
          <Icon.ChevronD size={12} />
        </span>
      </div>
    </aside>
  );
}
