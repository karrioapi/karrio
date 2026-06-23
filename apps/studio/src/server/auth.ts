// auth.ts — server-side session for Studio. Proxies Karrio's JWT auth and
// stores tokens in an httpOnly cookie so SSR pages can authenticate the
// decoupled Karrio client. Access tokens are short-lived; refreshSession()
// rotates them using the stored refresh token (simplejwt /api/token/refresh).
import { createServerFn } from "@tanstack/react-start";
import { getCookie, setCookie, deleteCookie } from "@tanstack/react-start/server";
import { z } from "zod";

const SESSION_COOKIE = "karrio-studio-session";
const KARRIO_API = process.env.KARRIO_API || "http://localhost:5002";
const SESSION_MAX_AGE = 60 * 60 * 24 * 7;

type Session = {
  access: string;
  refresh: string;
  email: string;
};

// Persist the session in a single httpOnly cookie (shared by login + refresh).
function persistSession(session: Session) {
  setCookie(SESSION_COOKIE, JSON.stringify(session), {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: SESSION_MAX_AGE,
  });
}

const credentials = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

// Karrio auth is REST + simplejwt: POST /api/token → { access, refresh }.
async function tokenAuth(email: string, password: string) {
  const res = await fetch(`${KARRIO_API}/api/token`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) return null;
  return (await res.json().catch(() => null)) as { access?: string; refresh?: string } | null;
}

export const login = createServerFn({ method: "POST" })
  .inputValidator((data: unknown) => credentials.parse(data))
  .handler(async ({ data }) => {
    const result = await tokenAuth(data.email, data.password);
    if (!result?.access) {
      return { ok: false as const, errors: [{ messages: ["Invalid email or password."] }] };
    }
    const session: Session = {
      access: result.access,
      refresh: result.refresh ?? "",
      email: data.email,
    };
    persistSession(session);
    return { ok: true as const };
  });

// Exchange the stored refresh token for a fresh access token. simplejwt rotates
// refresh tokens, so we persist whichever refresh token comes back. Returns the
// updated session, or null (and clears the cookie) when the refresh token is
// invalid/expired — the client then redirects to login.
export const refreshSession = createServerFn({ method: "POST" }).handler(async () => {
  const raw = getCookie(SESSION_COOKIE);
  if (!raw) return null;
  let session: Session;
  try {
    session = JSON.parse(raw) as Session;
  } catch {
    return null;
  }
  if (!session.refresh) return null;

  const res = await fetch(`${KARRIO_API}/api/token/refresh`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ refresh: session.refresh }),
  }).catch(() => null);

  const data =
    res && res.ok
      ? ((await res.json().catch(() => null)) as { access?: string; refresh?: string } | null)
      : null;

  if (!data?.access) {
    deleteCookie(SESSION_COOKIE);
    return null;
  }

  const next: Session = { ...session, access: data.access, refresh: data.refresh ?? session.refresh };
  persistSession(next);
  return next;
});

export const logout = createServerFn({ method: "POST" }).handler(async () => {
  deleteCookie(SESSION_COOKIE);
  return { ok: true as const };
});

const registration = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  full_name: z.string().min(1).optional(),
  organization_name: z.string().optional(),
});

export const register = createServerFn({ method: "POST" })
  .inputValidator((data: unknown) => registration.parse(data))
  .handler(async ({ data }) => {
    const res = await fetch(`${KARRIO_API}/graphql`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        query: `mutation($input: RegisterUserMutationInput!) {
          register_user(input: $input) { user { email } errors { field messages } }
        }`,
        variables: {
          input: {
            email: data.email,
            password1: data.password,
            password2: data.password,
            full_name: data.full_name,
            organization_name: data.organization_name,
            redirect_url: "",
          },
        },
      }),
    }).catch(() => null);
    const result = (await res?.json().catch(() => null))?.data?.register_user;
    if (result?.user) return { ok: true as const };
    return { ok: false as const, errors: result?.errors ?? [{ messages: ["Registration failed"] }] };
  });

const resetReq = z.object({ email: z.string().email() });

export const requestPasswordReset = createServerFn({ method: "POST" })
  .inputValidator((data: unknown) => resetReq.parse(data))
  .handler(async ({ data }) => {
    // Fire-and-forget; always report success to avoid account enumeration.
    await fetch(`${KARRIO_API}/graphql`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        query: `mutation($input: RequestPasswordResetMutationInput!) {
          request_password_reset(input: $input) { errors { messages } }
        }`,
        variables: { input: { email: data.email, redirect_url: "" } },
      }),
    }).catch(() => null);
    return { ok: true as const };
  });

export const getSession = createServerFn({ method: "GET" }).handler(async () => {
  const raw = getCookie(SESSION_COOKIE);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as Session;
  } catch {
    return null;
  }
});
