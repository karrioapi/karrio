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

// --- Tweaks (accent / density / font) — G1–G3 -------------------------------
export type FontStack = "Inter" | "IBM Plex" | "System";

const ACCENT_KEY = "karrio-accent";
const DENSITY_KEY = "karrio-density";
const FONT_KEY = "karrio-font";

export const ACCENTS = ["#8B5CF6", "#3B82F6", "#10B981", "#F97316", "#E11D48"] as const;

const FONT_STACKS: Record<FontStack, string> = {
  Inter: `"Inter", -apple-system, sans-serif`,
  "IBM Plex": `"IBM Plex Sans", "Inter", sans-serif`,
  System: `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`,
};

function ls(key: string): string | null {
  try {
    return typeof localStorage !== "undefined" ? localStorage.getItem(key) : null;
  } catch {
    return null;
  }
}

export const getAccent = () => ls(ACCENT_KEY) || ACCENTS[0];
export const getDensity = () => (ls(DENSITY_KEY) as Density) || "regular";
export const getFont = () => (ls(FONT_KEY) as FontStack) || "Inter";

export function applyAccent(accent: string) {
  if (typeof document !== "undefined") document.documentElement.style.setProperty("--accent", accent);
  try {
    localStorage.setItem(ACCENT_KEY, accent);
  } catch {}
}

export function applyDensity(density: Density) {
  if (typeof document !== "undefined") document.documentElement.dataset.density = density;
  try {
    localStorage.setItem(DENSITY_KEY, density);
  } catch {}
}

export function applyFont(font: FontStack) {
  if (typeof document !== "undefined") {
    document.documentElement.style.setProperty("--font-sans", FONT_STACKS[font]);
  }
  try {
    localStorage.setItem(FONT_KEY, font);
  } catch {}
}

// Apply all persisted tweaks (call once on mount).
export function applyStoredTweaks() {
  applyAccent(getAccent());
  applyDensity(getDensity());
  applyFont(getFont());
}

// Inline script injected pre-render in __root to avoid a theme/tweak flash.
export const THEME_INIT_SCRIPT = `(function(){try{var d=document.documentElement;d.setAttribute('data-theme',localStorage.getItem('${THEME_KEY}')||'dark');var a=localStorage.getItem('${ACCENT_KEY}');if(a)d.style.setProperty('--accent',a);var de=localStorage.getItem('${DENSITY_KEY}');if(de)d.dataset.density=de;}catch(e){}})();`;
