import { Outlet, createFileRoute, redirect, useNavigate, useParams } from "@tanstack/react-router";
import { useCallback, useEffect, useState } from "react";
import { getSession } from "~/server/auth";
import { Sidebar } from "~/components/shell/Sidebar";
import { Topbar, type CreateKind } from "~/components/shell/Topbar";
import { CommandPalette } from "~/components/overlays/CommandPalette";
import { Workbench } from "~/components/overlays/Workbench";
import { TweaksPanel } from "~/components/overlays/TweaksPanel";
import { MODE_DEFAULTS, routeMode, type Mode } from "~/lib/modes";
import { useSession } from "~/lib/karrio/session";
import {
  applyStoredTweaks,
  getSidebarCollapsed,
  getStoredTheme,
  setSidebarCollapsed as persistSidebar,
  setStoredTheme,
  type Theme,
} from "~/lib/theme";

// Pathless layout: app shell (sidebar + topbar) wrapping every screen.
// Auth guard: unauthenticated requests are redirected to /login.
export const Route = createFileRoute("/_app")({
  beforeLoad: async () => {
    const session = await getSession();
    if (!session) throw redirect({ to: "/login" });
  },
  component: AppLayout,
});

function AppLayout() {
  const navigate = useNavigate();
  const params = useParams({ strict: false }) as { screen?: string };
  const route = params.screen ?? "home";
  const mode = routeMode(route);

  // Test mode is owned by SessionProvider (it drives ctx.testMode → x-test-mode
  // and the React Query keys), so the toggle actually affects data across the app.
  const { testMode, setTestMode } = useSession();
  const [theme, setTheme] = useState<Theme>("dark");
  const [collapsed, setCollapsed] = useState(false);
  const [navOpen, setNavOpen] = useState(false); // mobile off-canvas drawer
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [workbenchOpen, setWorkbenchOpen] = useState(false);
  const [tweaksOpen, setTweaksOpen] = useState(false);

  // Hydrate persisted prefs on the client (avoids SSR/localStorage mismatch).
  useEffect(() => {
    setTheme(getStoredTheme());
    setCollapsed(getSidebarCollapsed());
    applyStoredTweaks();
  }, []);

  const go = useCallback(
    (next: string) => {
      navigate({ to: "/$screen", params: { screen: next } });
      setNavOpen(false); // close the mobile drawer on navigation
    },
    [navigate],
  );

  const onMode = useCallback(
    (m: Mode) => go(MODE_DEFAULTS[m]),
    [go],
  );

  const toggleTheme = useCallback(() => {
    setTheme((prev) => {
      const next: Theme = prev === "dark" ? "light" : "dark";
      setStoredTheme(next);
      return next;
    });
  }, []);

  // On mobile the sidebar toggle opens an off-canvas drawer; on desktop it
  // collapses to an icon rail.
  const toggleSidebar = useCallback(() => {
    const isMobile =
      typeof window !== "undefined" && window.matchMedia("(max-width: 768px)").matches;
    if (isMobile) {
      setNavOpen((o) => !o);
      return;
    }
    setCollapsed((prev) => {
      persistSidebar(!prev);
      return !prev;
    });
  }, []);

  // Keyboard shortcuts (⌘K palette · ⌘` workbench · ⌘\\ theme · ⌘B sidebar).
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const mod = e.metaKey || e.ctrlKey;
      if (!mod) return;
      const k = e.key.toLowerCase();
      if (k === "k") {
        e.preventDefault();
        setPaletteOpen((o) => !o);
      } else if (e.key === "`") {
        e.preventDefault();
        setWorkbenchOpen((o) => !o);
      } else if (k === "\\") {
        e.preventDefault();
        toggleTheme();
      } else if (k === "b") {
        e.preventDefault();
        toggleSidebar();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [toggleTheme, toggleSidebar]);

  const onCreate = useCallback(
    (kind: CreateKind) => {
      if (kind === "plugin") return go("plugins");
      if (kind === "apikey") return go("apikeys");
      // shipment/tracker/order/pickup → land on the relevant list (create sheets
      // with mutations land in the forms phase).
      if (kind === "shipment") return go("shipments");
      if (kind === "tracker") return go("trackers");
      if (kind === "order") return go("orders");
      if (kind === "pickup") return go("pickups");
    },
    [go],
  );

  const onPaletteAction = useCallback(
    (id: string) => {
      if (id === "theme") return toggleTheme();
      if (id === "workbench") return setWorkbenchOpen(true);
      if (id === "appearance") return setTweaksOpen(true);
      onCreate(id as CreateKind);
    },
    [toggleTheme, onCreate],
  );

  return (
    <div className={"app" + (collapsed ? " sidebar-collapsed" : "") + (navOpen ? " nav-open" : "")}>
      {navOpen && (
        <div className="nav-backdrop" onClick={() => setNavOpen(false)} data-testid="nav-backdrop" aria-hidden="true" />
      )}
      <Sidebar route={route} mode={mode} collapsed={collapsed} onGo={go} onMode={onMode} onTweaks={() => setTweaksOpen(true)} />
      <div className="main">
        {testMode && (
          <div className="test-mode-banner" data-testid="test-mode-banner" role="status">
            <span className="test-mode-dot" /> Test mode — showing sandbox data. Actions won’t affect live shipments.
          </div>
        )}
        <Topbar
          mode={mode}
          route={route}
          theme={theme}
          testMode={testMode}
          onToggleSidebar={toggleSidebar}
          onPalette={() => setPaletteOpen(true)}
          onTestMode={setTestMode}
          onTheme={toggleTheme}
          onTweaks={() => setTweaksOpen(true)}
          onOpenWorkbench={() => setWorkbenchOpen(true)}
          onCreate={onCreate}
        />
        <Outlet />
      </div>
      <CommandPalette open={paletteOpen} onClose={() => setPaletteOpen(false)} onGo={go} onAction={onPaletteAction} />
      <Workbench open={workbenchOpen} onClose={() => setWorkbenchOpen(false)} />
      <TweaksPanel open={tweaksOpen} onClose={() => setTweaksOpen(false)} theme={theme} onTheme={toggleTheme} />
    </div>
  );
}
