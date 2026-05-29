// studio-state.ts — Studio-native state contract.
//
// DECISION (passthrough): Studio does NOT own a database. Every piece of state
// — shipping data AND Studio-native state (customization, agents, MCP config) —
// is persisted on the Karrio backend and read/written through the Karrio
// GraphQL/REST API (via @karrio/hooks). This keeps a single source of truth and
// lets Studio stay a thin client.
//
// Mapping of Studio-native state onto existing Karrio surfaces:
//
//   Customization (theme/accent/density/font/layout)
//     → Karrio workspace config / user metadata (metafields)
//       hooks: @karrio/hooks/workspace-config, @karrio/hooks/metadata
//
//   Agent sessions / runs / messages
//     → Karrio metafields namespaced under `studio.agents.*`
//       (graduates to dedicated Karrio endpoints if/when added backend-side)
//
//   MCP servers / clients / invocations
//     → Karrio MCP server (packages/mcp + Django) + metafields
//       `studio.mcp.*`; live status/invocations come from the MCP server.
//
// These namespaces keep Studio state isolated within Karrio metadata so no
// backend migrations are required to ship Studio.

export const STUDIO_NS = {
  customization: "studio.customization",
  agents: "studio.agents",
  mcp: "studio.mcp",
} as const;

export type Customization = {
  theme: "dark" | "light";
  accent: string;
  density: "compact" | "regular" | "comfy";
  font_stack: "Inter" | "IBM Plex" | "System";
  layout?: Record<string, unknown>;
};

export const DEFAULT_CUSTOMIZATION: Customization = {
  theme: "dark",
  accent: "#8B5CF6",
  density: "regular",
  font_stack: "Inter",
};
