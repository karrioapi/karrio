"use client";

import { getSession, signOut, useSession } from "next-auth/react";
import { ServerError, ServerErrorCode } from "@karrio/lib";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import type { Session } from "next-auth";
import { useKarrio } from "./karrio";
import React from "react";

interface ExtendedSession extends Session {
  accessToken?: string;
  testMode?: boolean;
  error?: string;
  orgId?: string;
}

export function useSyncedSession() {
  const { status } = useSession();

  // Queries
  const query = useQuery({
    queryKey: ["session"],
    queryFn: async () => {
      const session = await getSession();
      return session as ExtendedSession;
    },
    refetchInterval: 120000,
    enabled: status === "authenticated",
    staleTime: 110000, // Slightly less than refetch interval
    retry: (failureCount, error) => {
      // Don't retry if session is invalid or authentication failed
      if (
        (error as any)?.message?.includes("authentication") ||
        status === "unauthenticated"
      ) {
        return false;
      }
      return failureCount < 1;
    },
  });

  return {
    query,
    isAuthenticated: status === "authenticated" && !!(query.data as ExtendedSession)?.accessToken,
    isLoading: status === "loading" || query.isLoading,
  };
}

export const NextSession = React.createContext<{
  session: ExtendedSession | null | undefined;
  isAuthenticated: boolean;
  isLoading: boolean;
}>({
  session: undefined,
  isAuthenticated: false,
  isLoading: true,
});

const NextSessionProvider = ({
  children,
}: {
  children?: React.ReactNode;
}): JSX.Element => {
  const { data: session, status } = useSession();
  const [sessionState, setSessionState] = React.useState<ExtendedSession | null>(session as ExtendedSession);
  const isAuthenticated = status === "authenticated" && !!(session as ExtendedSession)?.accessToken;
  const isLoading = status === "loading";

  React.useEffect(() => {
    if (
      (session as ExtendedSession)?.error !== (sessionState as ExtendedSession)?.error ||
      (session as ExtendedSession)?.accessToken !== (sessionState as ExtendedSession)?.accessToken ||
      session === null
    ) {
      setSessionState(session as ExtendedSession);
    }
  }, [session, sessionState]);

  const value = React.useMemo(() => ({
    session: sessionState,
    isAuthenticated,
    isLoading,
  }), [sessionState, isAuthenticated, isLoading]);

  return (
    <NextSession.Provider value={value}>
      {!isLoading ? children : null}
    </NextSession.Provider>
  );
};

export const SessionWrapper = ({
  children,
  error,
}: {
  error?: ServerError;
  children?: React.ReactNode;
}): JSX.Element => {
  const karrio = useKarrio();
  const router = useRouter();
  const { data: session, status } = useSession();
  const isAuthenticated = status === "authenticated" && !!(session as ExtendedSession)?.accessToken && karrio?.isAuthenticated;

  React.useEffect(() => {
    if (
      session === null ||
      (session as ExtendedSession)?.error === "RefreshAccessTokenError" ||
      error?.code === ServerErrorCode.API_AUTH_ERROR
    ) {
      const redirectUrl = "/signin?next=" + window.location.pathname + window.location.search;

      if (error?.code === ServerErrorCode.API_AUTH_ERROR) {
        signOut({ callbackUrl: redirectUrl });
      } else {
        router.push(redirectUrl);
      }
    }
  }, [session, error, router]);

  return <>{isAuthenticated ? children : null}</>;
};

export default NextSessionProvider;
