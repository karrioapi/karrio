import '@fortawesome/fontawesome-free/css/all.min.css';
import 'highlight.js/styles/stackoverflow-light.css';
import '@/styles/theme.scss';
import '@/styles/dashboard.scss';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import APIMetadataProvider from '@/context/api-metadata';
import { SessionProvider } from "next-auth/react";
import { ClientsProvider } from '@/lib/client';
import MainLayout from '@/layouts/main-layout';
import type { AppProps } from 'next/app';

const queryClient = new QueryClient();

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <SessionProvider session={pageProps.session} refetchInterval={5 * 60}>
      <QueryClientProvider client={queryClient}>
        <APIMetadataProvider metadata={pageProps?.metadata}>
          <ClientsProvider>
            <MainLayout error={pageProps?.error}>
              <Component {...pageProps} />
            </MainLayout>
          </ClientsProvider>
        </APIMetadataProvider>
      </QueryClientProvider>
    </SessionProvider>
  );
}

export default MyApp;
