// Topbar.tsx — search trigger, test-mode, theme, workbench, app launcher, create.
import { useEffect, useRef, useState } from "react";
import { Icon } from "~/components/ui/icons";
import type { Mode } from "~/lib/modes";
import type { Theme } from "~/lib/theme";

export type CreateKind =
  | "shipment"
  | "tracker"
  | "order"
  | "pickup"
  | "plugin"
  | "apikey";

export function Topbar({
  mode,
  route,
  theme,
  testMode,
  onToggleSidebar,
  onPalette,
  onTestMode,
  onTheme,
  onOpenWorkbench,
  onCreate,
}: {
  mode: Mode;
  route: string;
  theme: Theme;
  testMode: boolean;
  onToggleSidebar: () => void;
  onPalette: () => void;
  onTestMode: (on: boolean) => void;
  onTheme: () => void;
  onOpenWorkbench: () => void;
  onCreate: (kind: CreateKind) => void;
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const createRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      if (createRef.current && !createRef.current.contains(e.target as Node)) {
        setCreateOpen(false);
      }
    };
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  const showLauncher = (mode === "ship" || mode === "build") && route !== "apps";

  return (
    <header className="topbar" data-testid="topbar">
      <button className="icon-btn" title="Toggle sidebar (⌘B)" onClick={onToggleSidebar} data-testid="toggle-sidebar">
        <Icon.Sidebar size={14} />
      </button>
      <button className="search" onClick={onPalette} data-testid="palette-trigger">
        <Icon.Search size={13} />
        <span>Search shipments, orders, plugins…</span>
        <kbd>⌘K</kbd>
      </button>
      <div className="topbar-actions">
        <button
          className={"test-toggle" + (testMode ? " on" : "")}
          onClick={() => onTestMode(!testMode)}
          data-testid="test-mode"
        >
          <span className="toggle-switch" />
          <span>Test mode</span>
        </button>
        <button className="icon-btn" title="Toggle theme" onClick={onTheme} data-testid="theme-toggle">
          {theme === "dark" ? <Icon.Sun size={14} /> : <Icon.Moon size={14} />}
        </button>
        <button className="icon-btn" title="Developer tools" onClick={onOpenWorkbench} data-testid="workbench-trigger">
          <Icon.Terminal size={14} />
        </button>
        {showLauncher && (
          <button className="icon-btn" title="Launch app" data-testid="app-launcher">
            <Icon.Grid size={14} />
          </button>
        )}
        <div ref={createRef} style={{ position: "relative" }}>
          <button className="create-btn" onClick={() => setCreateOpen((v) => !v)} data-testid="create-btn">
            <Icon.Plus size={14} />
            <span>Create</span>
          </button>
          {createOpen && (
            <div className="menu" data-testid="create-menu">
              <MenuItem icon={<Icon.Truck size={14} />} label="New shipment" kbd="⌘L" onClick={() => fire("shipment")} />
              <MenuItem icon={<Icon.Pin size={14} />} label="Track a shipment" kbd="⌘T" onClick={() => fire("tracker")} />
              <MenuItem icon={<Icon.Inbox size={14} />} label="New order" onClick={() => fire("order")} />
              <MenuItem icon={<Icon.Box size={14} />} label="Schedule a pickup" onClick={() => fire("pickup")} />
              <div className="menu-sep" />
              <MenuItem icon={<Icon.Plug size={14} />} label="Install a plugin" onClick={() => fire("plugin")} />
              <MenuItem icon={<Icon.Key size={14} />} label="Generate API key" onClick={() => fire("apikey")} />
            </div>
          )}
        </div>
      </div>
    </header>
  );

  function fire(kind: CreateKind) {
    setCreateOpen(false);
    onCreate(kind);
  }
}

function MenuItem({
  icon,
  label,
  kbd,
  onClick,
}: {
  icon: React.ReactNode;
  label: string;
  kbd?: string;
  onClick: () => void;
}) {
  return (
    <div className="menu-item" onClick={onClick}>
      <span className="icon">{icon}</span>
      <span>{label}</span>
      {kbd && <span className="kbd">{kbd}</span>}
    </div>
  );
}
