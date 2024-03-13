import '@fortawesome/fontawesome-free/css/all.min.css';
import 'highlight.js/styles/stackoverflow-light.css';
import '@/styles/theme.scss';
import '@/styles/dashboard.scss';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import APIMetadataProvider from '@karrio/hooks/api-metadata';
import { NextPostHogProvider } from '@karrio/hooks/posthog';
import { ClientProvider } from '@karrio/hooks/karrio';
import { SessionProvider } from "next-auth/react";
import MainLayout from '@/layouts/main-layout';
import type { AppProps } from 'next/app';

const queryClient = new QueryClient();

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <SessionProvider session={pageProps.session} refetchInterval={5 * 60}>
      <NextPostHogProvider>
        <QueryClientProvider client={queryClient}>
          <APIMetadataProvider metadata={pageProps?.metadata}>
            <ClientProvider {...pageProps}>
              <MainLayout error={pageProps?.error}>
                <Component {...pageProps} />
              </MainLayout>
            </ClientProvider>
          </APIMetadataProvider>
        </QueryClientProvider>
      </NextPostHogProvider>
    </SessionProvider>
  );
}

export default MyApp;
