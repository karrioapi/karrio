// hooks.ts — TanStack Query data hooks over the decoupled Karrio client.
// This is the public barrel; the hooks live in domain modules so the GraphQL-
// first migration can be done file-by-file without conflicts:
//   hooks/ship.ts      (UNIT A) — shipments, trackers, connections, pickups,
//                                  document templates, manifests, batches
//   hooks/build.ts     (UNIT B) — apps, plugins, webhooks, api keys, mcp
//   hooks/govern.ts    (UNIT C) — admin, tenants, team, audit, usage
//   hooks/resources.ts (UNIT E) — orders + templates (GraphQL) + all mutations
// Studio-native state (UNIT D) lives in agents.ts / preferences.ts.
// See STUDIO_GRAPHQL_REBUILD.md for the per-hook source mapping.
export * from "~/lib/karrio/hooks/ship";
export * from "~/lib/karrio/hooks/build";
export * from "~/lib/karrio/hooks/govern";
export * from "~/lib/karrio/hooks/resources";
