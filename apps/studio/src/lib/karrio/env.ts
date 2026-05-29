// env.ts — base URL resolution with NO Next.js coupling.
// Server reads process.env.KARRIO_API; the browser reads Vite's
// import.meta.env.VITE_KARRIO_API (only VITE_-prefixed vars are exposed).

function fromVite(): string | undefined {
  try {
    return (import.meta as unknown as { env?: Record<string, string> }).env
      ?.VITE_KARRIO_API;
  } catch {
    return undefined;
  }
}

export function karrioBaseUrl(): string {
  const fromProcess =
    typeof process !== "undefined" ? process.env?.KARRIO_API : undefined;
  return fromProcess || fromVite() || "http://localhost:5002";
}

// Normalize a base + path into a single URL (replaces @karrio/lib `url$`).
export function joinUrl(base: string, path = ""): string {
  return `${base.replace(/\/+$/, "")}/${path.replace(/^\/+/, "")}`;
}
