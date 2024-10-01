import "@fortawesome/fontawesome-free/css/all.min.css";
import "highlight.js/styles/stackoverflow-light.css";
import "@/styles/theme.scss";
import "@/styles/dashboard.scss";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import APIMetadataProvider from "@karrio/hooks/api-metadata";
import { NextPostHogProvider } from "@karrio/hooks/posthog";
import { ClientProvider } from "@karrio/hooks/karrio";
import { SessionProvider } from "next-auth/react";
import MainLayout from "@/layouts/main-layout";
import type { AppProps } from "next/app";

// Set up query client
const queryClient = new QueryClient();

function MyApp({ Component, pageProps }: AppProps) {
  // Check for error in pageProps and render an error screen
  if (pageProps?.error) {
    return (
      <div>
        <h1>Error</h1>
        <p>{pageProps.error.message}</p>
      </div>
    );
  }

  // Check if the component is a known error page like 404 or 500
  const isErrorPage =
    Component.name?.trim() === "Custom404" ||
    Component.name?.trim() === "Custom500";

  if (isErrorPage) {
    return (
      <div>
        <Component {...pageProps} />
      </div>
    );
  }

  return (
    <SessionProvider session={pageProps.session} refetchInterval={5 * 60}>
      <NextPostHogProvider>
        <QueryClientProvider client={queryClient}>
          <APIMetadataProvider {...pageProps}>
            <ClientProvider {...pageProps}>
              {/* Skip MainLayout for error pages */}
              {isErrorPage ? (
                <Component {...pageProps} />
              ) : (
                <MainLayout error={pageProps?.error}>
                  <Component {...pageProps} />
                </MainLayout>
              )}
            </ClientProvider>
          </APIMetadataProvider>
        </QueryClientProvider>
      </NextPostHogProvider>
    </SessionProvider>
  );
}

export default MyApp;
