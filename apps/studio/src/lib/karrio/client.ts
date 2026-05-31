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

// The SessionProvider registers a refresh handler (client-side only). On a 401
// it obtains a fresh access token via the refreshSession server function, so the
// failed request can be retried once transparently. Stays null on the server and
// while unauthenticated.
type RefreshHandler = () => Promise<string | null>;
let refreshHandler: RefreshHandler | null = null;
let inFlightRefresh: Promise<string | null> | null = null;

export function setRefreshHandler(handler: RefreshHandler | null): void {
  refreshHandler = handler;
}

// Fetch with the ctx's auth headers; on 401, refresh the access token once
// (de-duping concurrent refreshes) and retry with the new token.
async function authedFetch(ctx: KarrioCtx, url: string, init: RequestInit = {}): Promise<Response> {
  const withAuth = (token?: string): RequestInit => ({
    ...init,
    headers: { ...authHeaders({ ...ctx, token }), ...(init.headers as Record<string, string> | undefined) },
  });

  let res = await fetch(url, withAuth(ctx.token));
  if (res.status === 401 && refreshHandler) {
    inFlightRefresh ??= refreshHandler().finally(() => {
      inFlightRefresh = null;
    });
    const token = await inFlightRefresh;
    if (token) res = await fetch(url, withAuth(token));
  }
  return res;
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
  const res = await authedFetch(ctx, url.toString());
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
  const res = await authedFetch(ctx, joinUrl(ctx.baseUrl, path), {
    method,
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
  const res = await authedFetch(ctx, joinUrl(ctx.baseUrl, "/graphql"), {
    method: "POST",
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
