"use client";

import { CreateOrganizationDialogProvider } from "@karrio/ui/components/create-organization-dialog";
import { AcceptInvitationDialogProvider } from "@karrio/ui/components/accept-invitation-dialog";
import { ErrorBoundary } from "@karrio/ui/core/components/error-boudaries";

import { LoadingProvider } from "@karrio/ui/core/components/loader";
import { Notifier } from "@karrio/ui/core/components/notifier";
import { OrganizationProvider } from "./organization";
import { SessionProvider } from "next-auth/react";
import APIMetadataProvider from "./api-metadata";
import { NextPostHogProvider } from "./posthog";
import { ClientProvider } from "./karrio";
import { bundleContexts } from "./utils";
import AppModeProvider from "./app-mode";
import {
  isServer,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";

const AuthenticatedContexts = bundleContexts([
  ClientProvider,
  APIMetadataProvider,
  AppModeProvider,
  CreateOrganizationDialogProvider,
  AcceptInvitationDialogProvider,
  OrganizationProvider,
  LoadingProvider,
  Notifier,
]);

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

  if (!(props as any).session) {
    return (
      <SessionProvider
        session={(props as any).session}
        refetchInterval={5 * 60}
      >
        <NextPostHogProvider>
          <QueryClientProvider client={queryClient}>
            <APIMetadataProvider {...(props as any)}>
              <ErrorBoundary>{children}</ErrorBoundary>
            </APIMetadataProvider>
          </QueryClientProvider>
        </NextPostHogProvider>
      </SessionProvider>
    );
  }

  return (
    <SessionProvider session={(props as any).session} refetchInterval={5 * 60}>
      <NextPostHogProvider>
        <QueryClientProvider client={queryClient}>
          <AuthenticatedContexts {...props}>
            <ErrorBoundary>{children}</ErrorBoundary>
          </AuthenticatedContexts>
        </QueryClientProvider>
      </NextPostHogProvider>
    </SessionProvider>
  );
}
