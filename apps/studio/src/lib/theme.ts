// theme.ts — theme + density preferences (persisted to localStorage; mirrored
// to the Studio DB app_config in a later phase). Dark is the default.
export type Theme = "dark" | "light";
export type Density = "compact" | "regular" | "comfy";

const THEME_KEY = "karrio-theme";
const SIDEBAR_KEY = "karrio-sidebar-collapsed";

export function getStoredTheme(): Theme {
  if (typeof localStorage === "undefined") return "dark";
  return (localStorage.getItem(THEME_KEY) as Theme) || "dark";
}

export function setStoredTheme(theme: Theme): void {
  if (typeof document !== "undefined") {
    document.documentElement.setAttribute("data-theme", theme);
  }
  if (typeof localStorage !== "undefined") {
    localStorage.setItem(THEME_KEY, theme);
  }
}

export function getSidebarCollapsed(): boolean {
  if (typeof localStorage === "undefined") return false;
  return localStorage.getItem(SIDEBAR_KEY) === "1";
}

export function setSidebarCollapsed(collapsed: boolean): void {
  if (typeof localStorage !== "undefined") {
    localStorage.setItem(SIDEBAR_KEY, collapsed ? "1" : "0");
  }
}

// Inline script injected pre-render in __root to avoid a theme flash.
export const THEME_INIT_SCRIPT = `(function(){try{var t=localStorage.getItem('${THEME_KEY}')||'dark';document.documentElement.setAttribute('data-theme',t);}catch(e){}})();`;
