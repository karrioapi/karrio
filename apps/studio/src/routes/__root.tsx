import {
  HeadContent,
  Outlet,
  Scripts,
  createRootRoute,
} from "@tanstack/react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { SessionProvider } from "~/lib/karrio/session";
import { ErrorBoundary } from "~/components/ErrorBoundary";
import { initMonitoring } from "~/lib/monitoring";
import { THEME_INIT_SCRIPT } from "~/lib/theme";
// Tailwind/shadcn theme first, then the bespoke enterprise shell CSS (overrides).
import "~/styles/globals.css";
import "~/styles/tokens.css";

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "Karrio Studio" },
      {
        name: "description",
        content:
          "Karrio Studio — ship, build, and govern multi-carrier logistics from one agent-friendly workspace.",
      },
      { name: "theme-color", content: "#0b0b0e" },
    ],
    links: [
      {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&family=JetBrains+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap",
      },
    ],
  }),
  component: RootComponent,
});

function RootComponent() {
  // One QueryClient per app instance; shipping data hooks (@karrio/hooks) use it.
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: { queries: { staleTime: 30_000, retry: 1 } },
      }),
  );
  useEffect(() => initMonitoring(), []);
  return (
    <RootDocument>
      <QueryClientProvider client={queryClient}>
        <SessionProvider>
          <ErrorBoundary>
            <Outlet />
          </ErrorBoundary>
        </SessionProvider>
      </QueryClientProvider>
    </RootDocument>
  );
}

function RootDocument({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        {/* Apply theme before paint to avoid a flash of the wrong theme. */}
        <script dangerouslySetInnerHTML={{ __html: THEME_INIT_SCRIPT }} />
        <HeadContent />
      </head>
      <body>
        <div id="root">{children}</div>
        <Scripts />
      </body>
    </html>
  );
}
