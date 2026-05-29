// client.ts — self-contained Karrio API client (REST + GraphQL) over fetch.
// No @karrio/* dependency, no Next.js. Auth/org/test-mode are passed per call
// via the request context, which the SessionProvider supplies.
import { joinUrl } from "~/lib/karrio/env";

export type KarrioCtx = {
  baseUrl: string;
  token?: string;
  orgId?: string;
  testMode?: boolean;
};

function authHeaders(ctx: KarrioCtx): Record<string, string> {
  return {
    "content-type": "application/json",
    ...(ctx.token ? { authorization: `Bearer ${ctx.token}` } : {}),
    ...(ctx.orgId ? { "x-org-id": ctx.orgId } : {}),
    ...(ctx.testMode ? { "x-test-mode": "true" } : {}),
  };
}

export class KarrioError extends Error {
  constructor(
    message: string,
    public status: number,
    public body?: unknown,
  ) {
    super(message);
    this.name = "KarrioError";
  }
}

export async function restGet<T>(
  ctx: KarrioCtx,
  path: string,
  params?: Record<string, string | number | boolean | undefined>,
): Promise<T> {
  const url = new URL(joinUrl(ctx.baseUrl, path));
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined) url.searchParams.set(k, String(v));
    }
  }
  const res = await fetch(url.toString(), { headers: authHeaders(ctx) });
  if (!res.ok) {
    throw new KarrioError(`GET ${path} failed (${res.status})`, res.status, await safeJson(res));
  }
  return (await res.json()) as T;
}

export async function restMutate<T>(
  ctx: KarrioCtx,
  method: "POST" | "PATCH" | "PUT" | "DELETE",
  path: string,
  body?: unknown,
): Promise<T> {
  const res = await fetch(joinUrl(ctx.baseUrl, path), {
    method,
    headers: authHeaders(ctx),
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!res.ok) {
    throw new KarrioError(`${method} ${path} failed (${res.status})`, res.status, await safeJson(res));
  }
  return (await res.json()) as T;
}

export async function graphql<T>(
  ctx: KarrioCtx,
  query: string,
  variables?: Record<string, unknown>,
): Promise<T> {
  const res = await fetch(joinUrl(ctx.baseUrl, "/graphql"), {
    method: "POST",
    headers: authHeaders(ctx),
    body: JSON.stringify({ query, variables }),
  });
  const json = await res.json();
  if (json.errors?.length) {
    throw new KarrioError(
      json.errors.map((e: { message: string }) => e.message).join("; "),
      res.status,
      json.errors,
    );
  }
  return json.data as T;
}

async function safeJson(res: Response): Promise<unknown> {
  try {
    return await res.json();
  } catch {
    return undefined;
  }
}
