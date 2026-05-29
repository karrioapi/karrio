import { Outlet, createFileRoute, useNavigate, useParams } from "@tanstack/react-router";
import { useCallback, useEffect, useState } from "react";
import { Sidebar } from "~/components/shell/Sidebar";
import { Topbar, type CreateKind } from "~/components/shell/Topbar";
import { MODE_DEFAULTS, routeMode, type Mode } from "~/lib/modes";
import {
  getSidebarCollapsed,
  getStoredTheme,
  setSidebarCollapsed as persistSidebar,
  setStoredTheme,
  type Theme,
} from "~/lib/theme";

// Pathless layout: app shell (sidebar + topbar) wrapping every screen.
export const Route = createFileRoute("/_app")({
  component: AppLayout,
});

function AppLayout() {
  const navigate = useNavigate();
  const params = useParams({ strict: false }) as { screen?: string };
  const route = params.screen ?? "home";
  const mode = routeMode(route);

  const [theme, setTheme] = useState<Theme>("dark");
  const [collapsed, setCollapsed] = useState(false);
  const [testMode, setTestMode] = useState(false);
  const [navOpen, setNavOpen] = useState(false); // mobile off-canvas drawer

  // Hydrate persisted prefs on the client (avoids SSR/localStorage mismatch).
  useEffect(() => {
    setTheme(getStoredTheme());
    setCollapsed(getSidebarCollapsed());
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

  // Keyboard shortcuts (⌘K ⌘L ⌘T ⌘` ⌘\\ ⌘B).
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const mod = e.metaKey || e.ctrlKey;
      if (!mod) return;
      const k = e.key.toLowerCase();
      if (k === "\\") {
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
      if (kind === "plugin") go("plugins");
      if (kind === "apikey") go("apikeys");
      // shipment/tracker/order/pickup create sheets land in later phases.
    },
    [go],
  );

  return (
    <div className={"app" + (collapsed ? " sidebar-collapsed" : "") + (navOpen ? " nav-open" : "")}>
      {navOpen && (
        <div className="nav-backdrop" onClick={() => setNavOpen(false)} data-testid="nav-backdrop" aria-hidden="true" />
      )}
      <Sidebar route={route} mode={mode} collapsed={collapsed} onGo={go} onMode={onMode} />
      <div className="main">
        <Topbar
          mode={mode}
          route={route}
          theme={theme}
          testMode={testMode}
          onToggleSidebar={toggleSidebar}
          onPalette={() => {
            /* command palette lands in cross-cutting phase */
          }}
          onTestMode={setTestMode}
          onTheme={toggleTheme}
          onOpenWorkbench={() => {
            /* workbench overlay lands in Build phase */
          }}
          onCreate={onCreate}
        />
        <Outlet />
      </div>
    </div>
  );
}
