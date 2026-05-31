// agents.ts — Typed store for agent definitions (F2) and MCP server configs (F3).
//
// Persistence: localStorage (single source of truth for OSS).
//
// Backend-adapter seam: the `BackendAdapter` interface below is the integration
// point for a future Karrio API endpoint (e.g. /v1/studio/agents).
// A `localStorageAdapter` is the default — it is the only real implementation
// today because no OSS backend endpoint exists for agent or MCP server configs.
// Replace `defaultAdapter` with a REST adapter once the backend ships.
//
// MCP execution seam: connecting to / invoking an external MCP server requires
// a backend proxy that does not exist in OSS Karrio. The `McpServerConfig`
// records stored here are *configuration only*. The `connectionStatus` field
// is set to "config-only" to make this explicit.
import { getStudioCtx, readMeta, writeMeta } from "~/lib/karrio/metastore";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/** Transport variants for MCP server connections. */
export type McpTransport = "stdio" | "sse" | "http";

/**
 * A user-managed MCP server configuration entry.
 * Storing this config does NOT establish a live connection; actual MCP
 * execution requires a backend proxy (not available in OSS Karrio today).
 */
export type McpServerConfig = {
  /** Unique identifier (UUID v4, client-generated). */
  id: string;
  /** Human-readable label for the server. */
  name: string;
  /** Transport type: stdio (local process) | sse / http (remote). */
  transport: McpTransport;
  /**
   * For stdio: the command to run (e.g. "npx @my/mcp-server").
   * For sse/http: the URL (e.g. "https://mcp.example.com/events").
   */
  endpoint: string;
  /** Environment variables to pass to the server process (stdio only). */
  env: Record<string, string>;
  /** ISO timestamp when the record was created. */
  createdAt: string;
  /** ISO timestamp of last edit. */
  updatedAt: string;
  /**
   * Always "config-only" in OSS — this library stores configuration only.
   * A backend proxy would be required to actually connect and return "ok" or
   * "error". Never display a fabricated "connected" status.
   *
   * TODO(F3-exec): replace with a real status once a backend proxy exists.
   */
  connectionStatus: "config-only";
};

/** Available LLM models for agent definitions. */
export type AgentModel =
  | "claude-opus-4-8"
  | "claude-sonnet-4-6"
  | "claude-haiku-3-5"
  | string;

/** A persisted agent definition (F2). */
export type AgentDef = {
  /** Unique identifier (UUID v4, client-generated). */
  id: string;
  /** Human-readable display name. */
  name: string;
  /** Short description shown in the agents list. */
  description: string;
  /** The system prompt sent before user messages. */
  systemPrompt: string;
  /** Model identifier to use for this agent. */
  model: AgentModel;
  /** Whether this agent is active / surfaced in selectors. */
  enabled: boolean;
  /** Tool IDs this agent is allowed to call. */
  enabledTools: string[];
  /** ISO timestamp when the record was created. */
  createdAt: string;
  /** ISO timestamp of last edit. */
  updatedAt: string;
};

// ---------------------------------------------------------------------------
// Backend-adapter seam (TODO: swap to a REST implementation when backend ships)
// ---------------------------------------------------------------------------

/**
 * Adapter interface for agent + MCP config persistence.
 *
 * TODO(F2/F3-backend): implement a `restAdapter` using
 * `restGet` / `restMutate` from ~/lib/karrio/client once the Karrio API
 * exposes endpoints like /v1/studio/agents and /v1/studio/mcp-servers.
 * The adapter should accept a `KarrioCtx` and delegate to those endpoints,
 * falling back to localStorage on network errors so the UI stays usable.
 */
interface BackendAdapter {
  // --- Agent definitions ---
  listAgents(): Promise<AgentDef[]>;
  saveAgent(agent: AgentDef): Promise<AgentDef>;
  deleteAgent(id: string): Promise<void>;

  // --- MCP server configs ---
  listMcpServers(): Promise<McpServerConfig[]>;
  saveMcpServer(server: McpServerConfig): Promise<McpServerConfig>;
  deleteMcpServer(id: string): Promise<void>;
}

// ---------------------------------------------------------------------------
// localStorage implementation
// ---------------------------------------------------------------------------

const LS_AGENTS_KEY = "karrio-studio:agents";
const LS_MCP_KEY = "karrio-studio:mcp-servers";

function readJson<T>(key: string, fallback: T): T {
  try {
    const raw = typeof localStorage !== "undefined" ? localStorage.getItem(key) : null;
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function writeJson<T>(key: string, value: T): void {
  try {
    if (typeof localStorage !== "undefined") {
      localStorage.setItem(key, JSON.stringify(value));
    }
  } catch {
    /* storage may be unavailable in SSR or private-browsing contexts */
  }
}

const localStorageAdapter: BackendAdapter = {
  listAgents: () => Promise.resolve(readJson<AgentDef[]>(LS_AGENTS_KEY, [])),

  saveAgent: (agent) => {
    const existing = readJson<AgentDef[]>(LS_AGENTS_KEY, []);
    const idx = existing.findIndex((a) => a.id === agent.id);
    const next =
      idx >= 0
        ? existing.map((a) => (a.id === agent.id ? agent : a))
        : [...existing, agent];
    writeJson(LS_AGENTS_KEY, next);
    return Promise.resolve(agent);
  },

  deleteAgent: (id) => {
    const next = readJson<AgentDef[]>(LS_AGENTS_KEY, []).filter((a) => a.id !== id);
    writeJson(LS_AGENTS_KEY, next);
    return Promise.resolve();
  },

  listMcpServers: () => Promise.resolve(readJson<McpServerConfig[]>(LS_MCP_KEY, [])),

  saveMcpServer: (server) => {
    const existing = readJson<McpServerConfig[]>(LS_MCP_KEY, []);
    const idx = existing.findIndex((s) => s.id === server.id);
    const next =
      idx >= 0
        ? existing.map((s) => (s.id === server.id ? server : s))
        : [...existing, server];
    writeJson(LS_MCP_KEY, next);
    return Promise.resolve(server);
  },

  deleteMcpServer: (id) => {
    const next = readJson<McpServerConfig[]>(LS_MCP_KEY, []).filter((s) => s.id !== id);
    writeJson(LS_MCP_KEY, next);
    return Promise.resolve();
  },
};

// ---------------------------------------------------------------------------
// Backend (metafield) adapter — real per-user persistence with localStorage cache
// ---------------------------------------------------------------------------
// Agent + MCP configs persist as per-user JSON metafields under the `studio.*`
// namespace (see metastore.ts), with localStorage as an immediate write-through
// cache and offline fallback. The ctx comes from SessionProvider via setStudioCtx.

const META_AGENTS_KEY = "studio.agents";
const META_MCP_KEY = "studio.mcp-servers";

async function loadList<T>(metaKey: string, lsKey: string): Promise<T[]> {
  const ctx = getStudioCtx();
  if (ctx?.token) {
    try {
      const remote = await readMeta<T[]>(ctx, metaKey);
      if (remote) {
        writeJson(lsKey, remote); // refresh the local cache
        return remote;
      }
    } catch {
      /* network/permission error — fall back to cache */
    }
  }
  return readJson<T[]>(lsKey, []);
}

async function persistList<T>(metaKey: string, lsKey: string, next: T[]): Promise<void> {
  writeJson(lsKey, next); // immediate cache
  const ctx = getStudioCtx();
  if (ctx?.token) {
    try {
      await writeMeta(ctx, metaKey, next);
    } catch {
      /* sync failure is non-fatal; cache holds and re-syncs on next write */
    }
  }
}

const backendAdapter: BackendAdapter = {
  listAgents: () => loadList<AgentDef>(META_AGENTS_KEY, LS_AGENTS_KEY),

  saveAgent: async (agent) => {
    const existing = await loadList<AgentDef>(META_AGENTS_KEY, LS_AGENTS_KEY);
    const idx = existing.findIndex((a) => a.id === agent.id);
    const next = idx >= 0 ? existing.map((a) => (a.id === agent.id ? agent : a)) : [...existing, agent];
    await persistList(META_AGENTS_KEY, LS_AGENTS_KEY, next);
    return agent;
  },

  deleteAgent: async (id) => {
    const next = (await loadList<AgentDef>(META_AGENTS_KEY, LS_AGENTS_KEY)).filter((a) => a.id !== id);
    await persistList(META_AGENTS_KEY, LS_AGENTS_KEY, next);
  },

  listMcpServers: () => loadList<McpServerConfig>(META_MCP_KEY, LS_MCP_KEY),

  saveMcpServer: async (server) => {
    const existing = await loadList<McpServerConfig>(META_MCP_KEY, LS_MCP_KEY);
    const idx = existing.findIndex((s) => s.id === server.id);
    const next = idx >= 0 ? existing.map((s) => (s.id === server.id ? server : s)) : [...existing, server];
    await persistList(META_MCP_KEY, LS_MCP_KEY, next);
    return server;
  },

  deleteMcpServer: async (id) => {
    const next = (await loadList<McpServerConfig>(META_MCP_KEY, LS_MCP_KEY)).filter((s) => s.id !== id);
    await persistList(META_MCP_KEY, LS_MCP_KEY, next);
  },
};

// ---------------------------------------------------------------------------
// Active adapter — metafield-backed with localStorage cache/fallback.
// ---------------------------------------------------------------------------

const defaultAdapter: BackendAdapter = backendAdapter;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function uuid(): string {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
}

function now(): string {
  return new Date().toISOString();
}

// ---------------------------------------------------------------------------
// Public API — agent definitions
// ---------------------------------------------------------------------------

export const agents = {
  list: (): Promise<AgentDef[]> => defaultAdapter.listAgents(),

  create: (
    fields: Omit<AgentDef, "id" | "createdAt" | "updatedAt">,
  ): Promise<AgentDef> => {
    const agent: AgentDef = { ...fields, id: uuid(), createdAt: now(), updatedAt: now() };
    return defaultAdapter.saveAgent(agent);
  },

  update: (
    id: string,
    fields: Partial<Omit<AgentDef, "id" | "createdAt">>,
  ): Promise<AgentDef> => {
    const current = readJson<AgentDef[]>(LS_AGENTS_KEY, []).find((a) => a.id === id);
    if (!current) return Promise.reject(new Error(`Agent not found: ${id}`));
    const updated: AgentDef = { ...current, ...fields, id, updatedAt: now() };
    return defaultAdapter.saveAgent(updated);
  },

  remove: (id: string): Promise<void> => defaultAdapter.deleteAgent(id),
};

// ---------------------------------------------------------------------------
// Public API — MCP server configs
// ---------------------------------------------------------------------------

export const mcpServers = {
  list: (): Promise<McpServerConfig[]> => defaultAdapter.listMcpServers(),

  create: (
    fields: Omit<McpServerConfig, "id" | "createdAt" | "updatedAt" | "connectionStatus">,
  ): Promise<McpServerConfig> => {
    const server: McpServerConfig = {
      ...fields,
      id: uuid(),
      createdAt: now(),
      updatedAt: now(),
      connectionStatus: "config-only",
    };
    return defaultAdapter.saveMcpServer(server);
  },

  update: (
    id: string,
    fields: Partial<Omit<McpServerConfig, "id" | "createdAt" | "connectionStatus">>,
  ): Promise<McpServerConfig> => {
    const current = readJson<McpServerConfig[]>(LS_MCP_KEY, []).find((s) => s.id === id);
    if (!current) return Promise.reject(new Error(`MCP server not found: ${id}`));
    const updated: McpServerConfig = {
      ...current,
      ...fields,
      id,
      updatedAt: now(),
      connectionStatus: "config-only",
    };
    return defaultAdapter.saveMcpServer(updated);
  },

  remove: (id: string): Promise<void> => defaultAdapter.deleteMcpServer(id),
};

// ---------------------------------------------------------------------------
// Default agent definitions seeded on first use
// ---------------------------------------------------------------------------

const SEED_AGENTS: Array<Omit<AgentDef, "id" | "createdAt" | "updatedAt">> = [
  {
    name: "Carrier Connector Builder",
    description: "Scaffolds and edits Karrio carrier connector files end-to-end.",
    systemPrompt:
      "You are an expert Karrio contributor. Help the user build carrier connector modules " +
      "(mappers, providers, schemas, tests) following the Karrio SDK extension pattern " +
      "(`bin/cli sdk add-extension`). Always use `import karrio.lib as lib`.",
    model: "claude-opus-4-8",
    enabled: true,
    enabledTools: ["scaffold_connector", "read_file", "write_file", "run_tests"],
  },
  {
    name: "Shipping Assistant",
    description: "Answers shipping questions and calls Karrio APIs on your behalf.",
    systemPrompt:
      "You are a helpful shipping operations assistant. You can look up shipments, " +
      "create trackers, and fetch rates using the Karrio API. Be concise and accurate.",
    model: "claude-sonnet-4-6",
    enabled: true,
    enabledTools: ["list_shipments", "track_shipment", "get_rates"],
  },
];

/** Seed default agents if the store is empty. Call once at app init. */
export async function seedDefaultAgents(): Promise<void> {
  const existing = await agents.list();
  if (existing.length === 0) {
    await Promise.all(SEED_AGENTS.map((a) => agents.create(a)));
  }
}
