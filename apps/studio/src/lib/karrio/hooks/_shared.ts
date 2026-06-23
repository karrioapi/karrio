// hooks/_shared.ts — helpers shared by the domain hook modules (ship/build/
// govern/resources). Keep this dependency-light so each domain file can be
// rewritten independently for the GraphQL-first migration (see
// STUDIO_GRAPHQL_REBUILD.md).
import { graphql, type KarrioCtx } from "~/lib/karrio/client";

export const keyExtra = (ctx: KarrioCtx) => ({ org: ctx.orgId, test: ctx.testMode });

// Map a GraphQL connection field (`{ field { edges { node } } }`) to a flat
// array of nodes. `endpoint` selects the tenant (/graphql) or admin
// (/admin/graphql) schema.
export async function graphqlEdges<T>(
  ctx: KarrioCtx,
  query: string,
  field: string,
  variables?: Record<string, unknown>,
  endpoint = "/graphql",
): Promise<T[]> {
  const data = await graphql<Record<string, { edges: Array<{ node: T }> }>>(
    ctx,
    query,
    variables,
    endpoint,
  );
  return (data[field]?.edges ?? []).map((e) => e.node);
}
