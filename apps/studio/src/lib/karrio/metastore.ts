// metastore.ts — round-trippable per-user backend KV via Karrio metafields.
// Studio-native app state (UI preferences, agent + MCP configs) is stored as
// JSON metafields under a `studio.*` key namespace, scoped to the authenticated
// user by Karrio's ownership model. This is the real backend behind the
// localStorage caches in preferences.ts / agents.ts (unblocks EBE-99).
//
// Verified live: a free-standing `create_metafield(key, type:json, value)` plus
// `metafields(filter:{ key })` gives a clean per-user create/read/update/delete
// round trip — no backend change required.
import { graphql, type KarrioCtx } from "~/lib/karrio/client";

// The SessionProvider registers the current authenticated ctx here (client-side)
// so ctx-less stores (agents.ts) can reach the backend without threading ctx
// through every call. Null on the server / when unauthenticated.
let studioCtx: KarrioCtx | null = null;
export function setStudioCtx(ctx: KarrioCtx | null): void {
  studioCtx = ctx;
}
export function getStudioCtx(): KarrioCtx | null {
  return studioCtx;
}

const READ = `query($key: String!) {
  metafields(filter: { key: $key }) { edges { node { id value } } }
}`;
const CREATE = `mutation($input: CreateMetafieldInput!) {
  create_metafield(input: $input) { metafield { id } errors { field messages } }
}`;
const UPDATE = `mutation($input: UpdateMetafieldInput!) {
  update_metafield(input: $input) { metafield { id } errors { field messages } }
}`;
const DELETE = `mutation($input: DeleteMutationInput!) {
  delete_metafield(input: $input) { id }
}`;

type ReadResult<T> = { metafields: { edges: Array<{ node: { id: string; value: T } }> } };

async function find<T>(ctx: KarrioCtx, key: string): Promise<{ id: string; value: T } | null> {
  const data = await graphql<Partial<ReadResult<T>>>(ctx, READ, { key });
  return data?.metafields?.edges?.[0]?.node ?? null;
}

/** Read a JSON metafield value by key, or null when absent/unauthenticated. */
export async function readMeta<T>(ctx: KarrioCtx, key: string): Promise<T | null> {
  if (!ctx.token) return null;
  return (await find<T>(ctx, key))?.value ?? null;
}

/** Upsert a JSON metafield by key (create or update). No-op when unauthenticated. */
export async function writeMeta(ctx: KarrioCtx, key: string, value: unknown): Promise<void> {
  if (!ctx.token) return;
  const existing = await find(ctx, key);
  if (existing) {
    await graphql(ctx, UPDATE, { input: { id: existing.id, value } });
  } else {
    await graphql(ctx, CREATE, { input: { key, type: "json", value } });
  }
}

/** Delete the metafield for a key, if present. */
export async function deleteMeta(ctx: KarrioCtx, key: string): Promise<void> {
  if (!ctx.token) return;
  const existing = await find(ctx, key);
  if (existing) await graphql(ctx, DELETE, { input: { id: existing.id } });
}
