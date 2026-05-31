// preferences.ts — single source of truth for Studio UI preferences.
//
// Architecture:
//   Layer 1 (synchronous): localStorage — offline cache, survives reload,
//     identical to prior behaviour. All reads/writes go through here first.
//   Layer 2 (async): Karrio backend — persisted in User.metadata under the
//     "studio.customization" namespace via the update_user GraphQL mutation.
//
// Backend store: User.metadata JSONField on the Karrio User model.
//   Write: update_user(input: { metadata: { "studio.customization": <prefs> } })
//   Read:  The OSS UserType query does not expose metadata in its GraphQL
//          selection set (only email/full_name/is_staff/permissions are returned).
//          TODO(backend): Add `metadata: JSON` field to UserType so that
//          loadFromBackend() can hydrate prefs on fresh login without localStorage.
//          Until then, loadFromBackend() is a documented no-op on reads; the
//          localStorage cache is the authoritative read source.
//
// Usage from components:
//   import { loadPrefs, savePrefs, syncToBackend } from "~/lib/karrio/preferences";
//   const prefs = loadPrefs();           // synchronous — always safe
//   savePrefs({ accent: "#10B981" });    // synchronous + kicks off async sync
//   await syncToBackend(ctx, prefs);     // explicit flush (e.g. on unload)

import type { KarrioCtx } from "~/lib/karrio/client";
import { readMeta, writeMeta } from "~/lib/karrio/metastore";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type Theme = "dark" | "light";
export type Density = "compact" | "regular" | "comfy";
export type FontStack = "Inter" | "IBM Plex" | "System";

/** All Studio appearance / layout preferences. */
export type Preferences = {
  theme: Theme;
  accent: string;
  density: Density;
  font_stack: FontStack;
  /** Reserved for future panel/layout configuration (sidebar width, pane splits, etc.) */
  layout?: Record<string, unknown>;
};

// ---------------------------------------------------------------------------
// Defaults
// ---------------------------------------------------------------------------

export const DEFAULT_PREFERENCES: Readonly<Preferences> = {
  theme: "dark",
  accent: "#8B5CF6",
  density: "regular",
  font_stack: "Inter",
};

// ---------------------------------------------------------------------------
// localStorage keys (kept stable for backwards compat with prior theme.ts)
// ---------------------------------------------------------------------------

const LS_KEYS = {
  theme:    "karrio-theme",
  accent:   "karrio-accent",
  density:  "karrio-density",
  fontStack: "karrio-font",
} as const;

// Namespace used when writing into User.metadata on the Karrio backend.
export const BACKEND_META_KEY = "studio.customization";

// ---------------------------------------------------------------------------
// localStorage helpers
// ---------------------------------------------------------------------------

function lsGet(key: string): string | null {
  try {
    return typeof localStorage !== "undefined" ? localStorage.getItem(key) : null;
  } catch {
    return null;
  }
}

function lsSet(key: string, value: string): void {
  try {
    if (typeof localStorage !== "undefined") localStorage.setItem(key, value);
  } catch {
    // Silently ignore (e.g. private browsing with storage disabled).
  }
}

// ---------------------------------------------------------------------------
// Public API — synchronous layer (localStorage)
// ---------------------------------------------------------------------------

/** Load preferences from localStorage, falling back to defaults. */
export function loadPrefs(): Preferences {
  return {
    theme:      (lsGet(LS_KEYS.theme) as Theme)         || DEFAULT_PREFERENCES.theme,
    accent:     lsGet(LS_KEYS.accent)                   || DEFAULT_PREFERENCES.accent,
    density:    (lsGet(LS_KEYS.density) as Density)     || DEFAULT_PREFERENCES.density,
    font_stack: (lsGet(LS_KEYS.fontStack) as FontStack) || DEFAULT_PREFERENCES.font_stack,
  };
}

/** Persist a partial preferences update to localStorage. Returns the new full prefs. */
export function savePrefs(patch: Partial<Preferences>): Preferences {
  const current = loadPrefs();
  const next: Preferences = { ...current, ...patch };

  if (patch.theme      !== undefined) lsSet(LS_KEYS.theme, next.theme);
  if (patch.accent     !== undefined) lsSet(LS_KEYS.accent, next.accent);
  if (patch.density    !== undefined) lsSet(LS_KEYS.density, next.density);
  if (patch.font_stack !== undefined) lsSet(LS_KEYS.fontStack, next.font_stack);

  return next;
}

// ---------------------------------------------------------------------------
// DOM appliers — apply prefs live via CSS variables / data attributes
// ---------------------------------------------------------------------------

const FONT_STACKS: Record<FontStack, string> = {
  Inter:      `"Inter", -apple-system, sans-serif`,
  "IBM Plex": `"IBM Plex Sans", "Inter", sans-serif`,
  System:     `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`,
};

export function applyPrefsToDOM(prefs: Preferences): void {
  if (typeof document === "undefined") return;
  const root = document.documentElement;
  root.setAttribute("data-theme", prefs.theme);
  root.style.setProperty("--accent", prefs.accent);
  root.dataset.density = prefs.density;
  root.style.setProperty("--font-sans", FONT_STACKS[prefs.font_stack]);
}

/** Apply a single field immediately (no save). */
export function applyTheme(theme: Theme): void {
  if (typeof document !== "undefined")
    document.documentElement.setAttribute("data-theme", theme);
}

export function applyAccent(accent: string): void {
  if (typeof document !== "undefined")
    document.documentElement.style.setProperty("--accent", accent);
}

export function applyDensity(density: Density): void {
  if (typeof document !== "undefined")
    document.documentElement.dataset.density = density;
}

export function applyFont(font: FontStack): void {
  if (typeof document !== "undefined")
    document.documentElement.style.setProperty("--font-sans", FONT_STACKS[font]);
}

// ---------------------------------------------------------------------------
// Backend adapter — async sync layer (Karrio metafields, key-namespaced)
// ---------------------------------------------------------------------------
// Studio prefs persist as a per-user JSON metafield under BACKEND_META_KEY
// ("studio.customization"). Unlike User.metadata (write-only on the OSS
// GraphQL), metafields round-trip cleanly — so loadFromBackend() actually
// hydrates. See metastore.ts.

/**
 * Flush the given preferences to the Karrio backend (metafield
 * `studio.customization`). No-op + silent when unauthenticated or on error —
 * localStorage remains the applied source of truth in that case.
 */
export async function syncToBackend(
  ctx: KarrioCtx,
  prefs: Preferences,
): Promise<void> {
  try {
    await writeMeta(ctx, BACKEND_META_KEY, prefs);
  } catch {
    // Sync failure is non-fatal; local settings stay applied and re-sync later.
  }
}

/**
 * Load preferences from the Karrio backend (metafield `studio.customization`)
 * into localStorage, and return the merged preferences. Falls back to the
 * localStorage cache when unauthenticated or on any error.
 */
export async function loadFromBackend(
  ctx: KarrioCtx,
): Promise<Preferences> {
  try {
    const remote = await readMeta<Partial<Preferences>>(ctx, BACKEND_META_KEY);
    if (remote) {
      const merged = { ...loadPrefs(), ...remote };
      savePrefs(merged);
      return merged;
    }
  } catch {
    // Ignore — fall through to the localStorage cache.
  }
  return loadPrefs();
}

// ---------------------------------------------------------------------------
// Convenience — save + apply + async sync in one call
// ---------------------------------------------------------------------------

/**
 * Apply a preference patch: persists to localStorage, applies to DOM immediately,
 * and fires-and-forgets an async sync to the backend.
 *
 * Pass `ctx` from `useKarrioCtx()` when called inside a React component.
 */
export function applyAndSavePrefs(
  patch: Partial<Preferences>,
  ctx?: KarrioCtx,
): Preferences {
  const next = savePrefs(patch);
  applyPrefsToDOM(next);
  if (ctx) void syncToBackend(ctx, next);
  return next;
}
