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

export const getSession = createServerFn({ method: "GET" }).handler(async () => {
  const raw = getCookie(SESSION_COOKIE);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as Session;
  } catch {
    return null;
  }
});
