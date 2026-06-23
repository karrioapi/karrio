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
//     → User.metadata["studio.customization"] on the Karrio backend.
//       localStorage is the synchronous cache; async sync via update_user
//       GraphQL mutation. See ~/lib/karrio/preferences.ts for full details.
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

// Customization types and defaults are now owned by ~/lib/karrio/preferences.ts
// (single source of truth). Re-exported here for backwards compatibility with
// any imports that reference studio-state.ts directly.
export type {
  Preferences as Customization,
  Theme,
  Density,
  FontStack,
} from "~/lib/karrio/preferences";

export {
  DEFAULT_PREFERENCES as DEFAULT_CUSTOMIZATION,
  loadPrefs,
  savePrefs,
  applyAndSavePrefs,
  syncToBackend,
  loadFromBackend,
} from "~/lib/karrio/preferences";
