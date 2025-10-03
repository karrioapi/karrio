"use client";

import { useState } from "react";
import { ErrorBoundary } from "@karrio/ui/core/components/error-boudaries";
import { trpc } from "@karrio/console/trpc/client";
import { SessionProvider } from "next-auth/react";
import { httpBatchLink } from "@trpc/client";
import {
  isServer,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // With SSR, we usually want to set some default staleTime
        // above 0 to avoid refetching immediately on the client
        staleTime: 60 * 1000,
      },
    },
  });
}

let browserQueryClient: QueryClient | undefined = undefined;

function getQueryClient() {
  if (isServer) {
    // Server: always make a new query client
    return makeQueryClient();
  } else {
    // Browser: make a new query client if we don't already have one
    // This is very important, so we don't re-make a new client if React
    // suspends during the initial render. This may not be needed if we
    // have a suspense boundary BELOW the creation of the query client
    if (!browserQueryClient) browserQueryClient = makeQueryClient();
    return browserQueryClient;
  }
}

export function Providers({
  children,
  ...props
}: {
  children: React.ReactNode;
}) {
  const queryClient = getQueryClient();
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: "/api/trpc",
        }),
      ],
    }),
  );

  if (!(props as any).session) {
    return (
      <SessionProvider
        session={(props as any).session}
        refetchInterval={5 * 60}
      >
        <trpc.Provider client={trpcClient} queryClient={queryClient}>
          <QueryClientProvider client={queryClient}>
            <ErrorBoundary>{children}</ErrorBoundary>
          </QueryClientProvider>
        </trpc.Provider>
      </SessionProvider>
    );
  }

  return (
    <SessionProvider session={(props as any).session} refetchInterval={5 * 60}>
      <trpc.Provider client={trpcClient} queryClient={queryClient}>
        <QueryClientProvider client={queryClient}>
          <ErrorBoundary>{children}</ErrorBoundary>
        </QueryClientProvider>
      </trpc.Provider>
    </SessionProvider>
  );
}
