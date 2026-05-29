// auth.ts — server-side session for Studio. Proxies Karrio's JWT auth and
// stores tokens in an httpOnly cookie so SSR pages can authenticate the
// KarrioClient + @karrio/hooks. (Phase B fills in refresh + org switching.)
import { createServerFn } from "@tanstack/react-start";
import { getCookie, setCookie, deleteCookie } from "@tanstack/react-start/server";
import { z } from "zod";

const SESSION_COOKIE = "karrio-studio-session";
const KARRIO_API = process.env.KARRIO_API || "http://localhost:5002";

type Session = {
  access: string;
  refresh: string;
  email: string;
};

const credentials = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

async function tokenAuth(email: string, password: string) {
  const res = await fetch(`${KARRIO_API}/graphql`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      query: `mutation($email: String!, $password: String!) {
        token_auth(input: { email: $email, password: $password }) {
          token refresh_token errors { field messages }
        }
      }`,
      variables: { email, password },
    }),
  });
  return (await res.json())?.data?.token_auth;
}

export const login = createServerFn({ method: "POST" })
  .inputValidator((data: unknown) => credentials.parse(data))
  .handler(async ({ data }) => {
    const result = await tokenAuth(data.email, data.password);
    if (!result?.token) {
      return { ok: false as const, errors: result?.errors ?? [{ messages: ["Invalid credentials"] }] };
    }
    const session: Session = {
      access: result.token,
      refresh: result.refresh_token,
      email: data.email,
    };
    setCookie(SESSION_COOKIE, JSON.stringify(session), {
      httpOnly: true,
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production",
      path: "/",
      maxAge: 60 * 60 * 24 * 7,
    });
    return { ok: true as const };
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
