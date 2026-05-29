// monitoring.ts — thin, dependency-free observability seam (H4).
// Real SDKs (Sentry, PostHog) are wired at deploy time behind these functions
// so app code never imports them directly. No-ops (console in dev) until a
// provider is registered via registerMonitor(), keeping the bundle lean.
type Monitor = {
  captureError: (error: unknown, context?: Record<string, unknown>) => void;
  trackEvent: (name: string, props?: Record<string, unknown>) => void;
};

let monitor: Monitor | null = null;

export function registerMonitor(m: Monitor) {
  monitor = m;
}

export function captureError(error: unknown, context?: Record<string, unknown>) {
  if (monitor) return monitor.captureError(error, context);
  if (import.meta.env?.DEV) console.error("[monitor] error", error, context ?? "");
}

export function trackEvent(name: string, props?: Record<string, unknown>) {
  if (monitor) return monitor.trackEvent(name, props);
  if (import.meta.env?.DEV) console.debug("[monitor] event", name, props ?? "");
}

// Wire SDKs here when DSN/keys are configured (deploy-time). Example:
//   if (import.meta.env.VITE_SENTRY_DSN) { const s = await import("@sentry/browser"); s.init(...); registerMonitor({...}); }
export function initMonitoring() {
  // Intentionally empty by default — providers register lazily at deploy time.
}
