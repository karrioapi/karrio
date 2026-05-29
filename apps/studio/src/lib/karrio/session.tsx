// session.tsx — framework-agnostic session context (no NextAuth).
// The token comes from the Studio server session cookie via the getSession
// server function; org + test-mode are client-controlled. Everything data-layer
// reads its KarrioCtx from here.
import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useQuery } from "@tanstack/react-query";
import { getSession } from "~/server/auth";
import { karrioBaseUrl } from "~/lib/karrio/env";
import type { KarrioCtx } from "~/lib/karrio/client";

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

export function SessionProvider({ children }: { children: ReactNode }) {
  const baseUrl = karrioBaseUrl();
  const [testMode, setTestMode] = useState(false);
  const [orgId, setOrgId] = useState<string | undefined>(undefined);

  const sessionQuery = useQuery({
    queryKey: ["studio-session"],
    queryFn: () => getSession(),
    staleTime: 5 * 60_000,
  });

  const value = useMemo<SessionContextValue>(() => {
    const token = sessionQuery.data?.access;
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
