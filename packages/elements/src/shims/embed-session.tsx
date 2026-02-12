/**
 * Embed-compatible replacement for @karrio/hooks/session.
 *
 * Provides useSyncedSession() that returns a fake authenticated session
 * using the token from KarrioEmbedProvider.  This allows hooks like
 * useAPIUsage, useAppStore, and the Playground/GraphiQL modules to
 * read session.accessToken without next-auth.
 */
import { useKarrioEmbed } from "../providers/karrio-embed-provider";
import React from "react";

interface EmbedSession {
  accessToken: string;
  testMode: boolean;
  orgId: string | undefined;
  error: undefined;
}

export function useSyncedSession() {
  const { token } = useKarrioEmbed();

  const session: EmbedSession = React.useMemo(
    () => ({
      accessToken: token,
      testMode: false,
      orgId: undefined,
      error: undefined,
    }),
    [token],
  );

  // Mimic the react-query result shape the original hook returns
  const query = React.useMemo(
    () => ({
      data: session,
      isLoading: false,
      isError: false,
      isSuccess: true,
      error: null,
      status: "success" as const,
      refetch: () => Promise.resolve({ data: session } as any),
    }),
    [session],
  );

  return {
    query,
    isAuthenticated: true,
    isLoading: false,
  };
}

// Context export (some files import NextSession context)
export const NextSession = React.createContext<{
  session: EmbedSession | null | undefined;
  isAuthenticated: boolean;
  isLoading: boolean;
}>({
  session: null,
  isAuthenticated: true,
  isLoading: false,
});

// SessionWrapper – just renders children in embed
export const SessionWrapper = ({
  children,
}: {
  error?: any;
  children?: React.ReactNode;
}) => {
  return <>{children}</>;
};

// Default export matches the original NextSessionProvider
const NextSessionProvider = ({ children }: { children?: React.ReactNode }) => {
  return <>{children}</>;
};

export default NextSessionProvider;
