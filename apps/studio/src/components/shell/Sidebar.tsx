// Sidebar.tsx — mode-driven navigation (Ship / Build / Govern).
import { Icon, MODE_LABELS, NAV, type Mode } from "~/lib/modes";
import { UserMenu } from "~/components/shell/UserMenu";
import { WorkspaceMenu } from "~/components/shell/WorkspaceMenu";
import { useFeatureFlags, type FeatureFlag } from "~/lib/karrio/references";

const MODES: Mode[] = ["ship", "build", "govern"];

export function Sidebar({
  route,
  mode,
  collapsed,
  onGo,
  onMode,
  onTweaks,
}: {
  route: string;
  mode: Mode;
  collapsed: boolean;
  onGo: (route: string) => void;
  onMode: (mode: Mode) => void;
  onTweaks: () => void;
}) {
  const { isEnabled } = useFeatureFlags();
  return (
    <aside className={"sidebar" + (collapsed ? " collapsed" : "")} data-testid="sidebar">
      <WorkspaceMenu onGo={onGo} />

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
        {NAV[mode].map((group, gi) => {
          // Hide items gated by a disabled deployment feature flag; drop empty groups.
          const items = group.items.filter((item) => !item.flag || isEnabled(item.flag as FeatureFlag));
          if (items.length === 0) return null;
          return (
          <div className="nav-group" key={group.label ?? gi}>
            {group.label && <div className="nav-label">{group.label}</div>}
            {items.map((item) => {
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
          );
        })}
      </nav>

      <UserMenu onGo={onGo} onTweaks={onTweaks} />
    </aside>
  );
}
