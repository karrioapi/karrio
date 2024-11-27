"use client";

import { getSession, signOut, useSession } from "next-auth/react";
import { ServerError, ServerErrorCode } from "@karrio/lib";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { SessionType } from "@karrio/types";
import type { Session } from "next-auth";
import { useKarrio } from "./karrio";
import React from "react";

export function useSyncedSession() {
  // Queries
  const query = useQuery(
    ["session"],
    () =>
      getSession().then((_) => {
        console.log("fetch session", new Date());
        return _;
      }),
    { refetchInterval: 120000 },
  );

  return {
    query,
  } as any & { query: { data: SessionType } };
}

export const NextSession = React.createContext<Session | null | undefined>(
  undefined,
);

const NextSessionProvider = ({
  children,
}: {
  children?: React.ReactNode;
}): JSX.Element => {
  const { data: session } = useSession();
  const [sessionState, setSessionState] = React.useState<Session | null>(
    session as Session,
  );

  React.useEffect(() => {
    // set session state if session is not null, has no error and has a new access token
    if (
      (session as any)?.error !== (sessionState as any)?.error ||
      (session as any)?.accessToken !== (sessionState as any)?.accessToken ||
      session === null
    ) {
      setSessionState(session);
    }
  }, [session, sessionState]);

  return (
    <NextSession.Provider value={sessionState}>
      {sessionState !== undefined ? children : <></>}
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
  const { data: session } = useSession();

  React.useEffect(() => {
    if (
      session === null ||
      (session as any)?.error === "RefreshAccessTokenError"
    ) {
      router.push(
        "/signin?next=" + window.location.pathname + window.location.search,
      );
    }
    if (error?.code === ServerErrorCode.API_AUTH_ERROR) {
      signOut({
        callbackUrl:
          "/signin?next=" + window.location.pathname + window.location.search,
      });
    }
  }, [session, error]);

  console.log("session", session, karrio);
  return <>{session && karrio?.isAuthenticated && children}</>;
};

export default NextSessionProvider;
