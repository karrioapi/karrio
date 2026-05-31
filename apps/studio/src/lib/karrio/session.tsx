// session.tsx — framework-agnostic session context (no NextAuth).
// The token comes from the Studio server session cookie via the getSession
// server function; org + test-mode are client-controlled. Everything data-layer
// reads its KarrioCtx from here.
import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getSession, refreshSession } from "~/server/auth";
import { karrioBaseUrl } from "~/lib/karrio/env";
import { setRefreshHandler, type KarrioCtx } from "~/lib/karrio/client";
import { applyPrefsToDOM, loadFromBackend } from "~/lib/karrio/preferences";
import { setStudioCtx } from "~/lib/karrio/metastore";

type SessionContextValue = {
  ctx: KarrioCtx;
  isAuthenticated: boolean;
  email?: string;
  testMode: boolean;
  setTestMode: (on: boolean) => void;
  orgId?: string;
  setOrgId: (id?: string) => void;
};

const SessionContext = createContext<SessionContextValue | null>(null);

const TEST_MODE_KEY = "karrio-studio:test-mode";
const ORG_KEY = "karrio-studio:org-id";
const lsGet = (k: string): string | null => {
  try {
    return typeof localStorage !== "undefined" ? localStorage.getItem(k) : null;
  } catch {
    return null;
  }
};
const lsSet = (k: string, v: string | null): void => {
  try {
    if (typeof localStorage === "undefined") return;
    if (v === null) localStorage.removeItem(k);
    else localStorage.setItem(k, v);
  } catch {
    /* storage may be unavailable */
  }
};

export function SessionProvider({ children }: { children: ReactNode }) {
  const baseUrl = karrioBaseUrl();
  const queryClient = useQueryClient();
  const [testMode, setTestModeState] = useState(false);
  const [orgId, setOrgIdState] = useState<string | undefined>(undefined);

  // Hydrate test-mode + org from localStorage on the client (avoids SSR mismatch),
  // so the selected mode persists across reloads and navigation.
  useEffect(() => {
    setTestModeState(lsGet(TEST_MODE_KEY) === "1");
    setOrgIdState(lsGet(ORG_KEY) ?? undefined);
  }, []);

  const setTestMode = (on: boolean) => {
    lsSet(TEST_MODE_KEY, on ? "1" : "0");
    setTestModeState(on);
  };
  const setOrgId = (id?: string) => {
    lsSet(ORG_KEY, id ?? null);
    setOrgIdState(id);
  };

  const sessionQuery = useQuery({
    queryKey: ["studio-session"],
    queryFn: () => getSession(),
    staleTime: 5 * 60_000,
  });

  // Register the 401 → refresh handler so expired access tokens are rotated
  // transparently. Updates the cached session so ctx.token reflects the new
  // access token for subsequent requests.
  useEffect(() => {
    setRefreshHandler(async () => {
      const next = await refreshSession();
      queryClient.setQueryData(["studio-session"], next ?? null);
      return next?.access ?? null;
    });
    return () => setRefreshHandler(null);
  }, [queryClient]);

  // Hydrate Studio UI preferences from the backend (metafield `studio.customization`)
  // once authenticated, so settings follow the user across devices.
  const token = sessionQuery.data?.access;
  useEffect(() => {
    // Register the current ctx so ctx-less stores (agents/MCP configs) can reach
    // the backend, then hydrate UI preferences from the backend metafield.
    setStudioCtx(token ? { baseUrl, token, orgId, testMode } : null);
    if (!token) return;
    void loadFromBackend({ baseUrl, token, orgId, testMode }).then(applyPrefsToDOM);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token, baseUrl, orgId, testMode]);

  const value = useMemo<SessionContextValue>(() => {
    return {
      ctx: { baseUrl, token, orgId, testMode },
      isAuthenticated: Boolean(token),
      email: sessionQuery.data?.email,
      testMode,
      setTestMode,
      orgId,
      setOrgId,
    };
  }, [baseUrl, orgId, testMode, sessionQuery.data]);

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export function useSession(): SessionContextValue {
  const ctx = useContext(SessionContext);
  if (!ctx) throw new Error("useSession must be used within <SessionProvider>");
  return ctx;
}

export function useKarrioCtx(): KarrioCtx {
  return useSession().ctx;
}
