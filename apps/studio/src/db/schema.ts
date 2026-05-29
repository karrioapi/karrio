// schema.ts — Studio-native state ONLY. All shipping data (shipments, trackers,
// orders, carriers, etc.) lives in the Karrio backend and is read/written via
// @karrio/hooks. This DB holds app customization, agents, and MCP config.
import { sql } from "drizzle-orm";
import {
  integer,
  jsonb,
  pgTable,
  text,
  timestamp,
  uuid,
  varchar,
} from "drizzle-orm/pg-core";

const id = () => uuid("id").primaryKey().defaultRandom();
const timestamps = {
  created_at: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
  updated_at: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull(),
};

// Self-editable app: per-user/org theme, accent, density, font, layout tweaks.
export const appConfig = pgTable("app_config", {
  id: id(),
  org_id: varchar("org_id", { length: 64 }).notNull(),
  user_id: varchar("user_id", { length: 64 }),
  theme: varchar("theme", { length: 16 }).default("dark").notNull(),
  accent: varchar("accent", { length: 16 }).default("#8B5CF6").notNull(),
  density: varchar("density", { length: 16 }).default("regular").notNull(),
  font_stack: varchar("font_stack", { length: 32 }).default("Inter").notNull(),
  layout: jsonb("layout"),
  ...timestamps,
});

// AI Assistant / agent sessions (Editor + ⌘K actions).
export const agentSessions = pgTable("agent_sessions", {
  id: id(),
  org_id: varchar("org_id", { length: 64 }).notNull(),
  user_id: varchar("user_id", { length: 64 }).notNull(),
  title: text("title").notNull(),
  plugin: varchar("plugin", { length: 128 }),
  status: varchar("status", { length: 24 }).default("idle").notNull(),
  ...timestamps,
});

export const agentRuns = pgTable("agent_runs", {
  id: id(),
  session_id: uuid("session_id")
    .notNull()
    .references(() => agentSessions.id, { onDelete: "cascade" }),
  model: varchar("model", { length: 64 }).notNull(),
  mode: varchar("mode", { length: 24 }).default("assistant").notNull(),
  status: varchar("status", { length: 24 }).default("running").notNull(),
  ...timestamps,
});

export const agentMessages = pgTable("agent_messages", {
  id: id(),
  session_id: uuid("session_id")
    .notNull()
    .references(() => agentSessions.id, { onDelete: "cascade" }),
  run_id: uuid("run_id").references(() => agentRuns.id, { onDelete: "set null" }),
  role: varchar("role", { length: 16 }).notNull(), // user | assistant | tool
  content: text("content").notNull(),
  context: jsonb("context"), // @-context chips, file refs, diffs
  created_at: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});

// MCP server management (backed by packages/mcp + Django MCP server).
export const mcpServers = pgTable("mcp_servers", {
  id: id(),
  org_id: varchar("org_id", { length: 64 }).notNull(),
  name: varchar("name", { length: 128 }).notNull(),
  url: text("url"),
  status: varchar("status", { length: 24 }).default("stopped").notNull(),
  config: jsonb("config"),
  ...timestamps,
});

export const mcpClients = pgTable("mcp_clients", {
  id: id(),
  server_id: uuid("server_id")
    .notNull()
    .references(() => mcpServers.id, { onDelete: "cascade" }),
  name: varchar("name", { length: 128 }).notNull(),
  kind: varchar("kind", { length: 32 }), // claude-desktop | cursor | sse
  last_seen: timestamp("last_seen", { withTimezone: true }),
  created_at: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});

export const mcpInvocations = pgTable("mcp_invocations", {
  id: id(),
  server_id: uuid("server_id")
    .notNull()
    .references(() => mcpServers.id, { onDelete: "cascade" }),
  tool: varchar("tool", { length: 128 }).notNull(),
  client_id: uuid("client_id").references(() => mcpClients.id, { onDelete: "set null" }),
  duration_ms: integer("duration_ms"),
  status: varchar("status", { length: 24 }).default("ok").notNull(),
  payload: jsonb("payload"),
  created_at: timestamp("created_at", { withTimezone: true })
    .default(sql`now()`)
    .notNull(),
});

export type AppConfig = typeof appConfig.$inferSelect;
export type AgentSession = typeof agentSessions.$inferSelect;
export type McpServer = typeof mcpServers.$inferSelect;
