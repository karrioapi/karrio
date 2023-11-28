import { CreateOrganizationModalProvider } from '@karrio/ui/modals/create-organization-modal';
import { AcceptInvitationProvider } from '@karrio/ui/modals/accept-invitation-modal';
import { forceSignOut, ServerError, ServerErrorCode } from '@karrio/lib';
import NextSessionProvider, { NextSession } from '@karrio/hooks/session';
import { ErrorBoundary } from '@karrio/ui/components/error-boudaries';
import { OrganizationProvider } from '@karrio/hooks/organization';
import { SubscriptionProvider } from '@karrio/hooks/subscription';
import { LoadingProvider } from '@karrio/ui/components/loader';
import { Notifier } from '@karrio/ui/components/notifier';
import AppModeProvider from '@karrio/hooks/app-mode';
import React, { useContext, useEffect } from 'react';
import { useRouter } from 'next/dist/client/router';


const CONTEXT_PROVIDERS: React.FC<{ children?: React.ReactNode }>[] = [
  OrganizationProvider,
  SubscriptionProvider,
  AppModeProvider,
  LoadingProvider,
];


const ContextProviders: React.FC<{ children?: React.ReactNode }> = ({ children, ...props }) => {
  const NestedContexts = CONTEXT_PROVIDERS.reduce((_, Ctx) => <Ctx {...props}>{_}</Ctx>, children);

  return (
    <>
      <Notifier>{NestedContexts}</Notifier>
    </>
  );
};

export const AuthenticatedPage = (content: any, pageProps?: any | {}) => {
  const SessionWrapper: React.FC<{ error?: ServerError, children?: React.ReactNode }> = ({ children, error }) => {
    const router = useRouter();
    const session = useContext(NextSession);

    useEffect(() => {
      if (session === null || (session as any)?.error === "RefreshAccessTokenError") {
        router.push('/login?next=' + window.location.pathname + window.location.search);
      }
      if (error?.code === ServerErrorCode.API_AUTH_ERROR) {
        forceSignOut();
      }
    }, [session, error]);

    return (
      <>
        <ContextProviders {...(pageProps || {})}>
          <ErrorBoundary>
            {session && children}
          </ErrorBoundary>
        </ContextProviders>
      </>
    );
  };

  return (
    <NextSessionProvider>
      <SessionWrapper {...(pageProps || {})}>
        <AcceptInvitationProvider>
          <CreateOrganizationModalProvider>

            {content}

          </CreateOrganizationModalProvider>
        </AcceptInvitationProvider>
      </SessionWrapper>
    </NextSessionProvider>
  )
};
