import { ErrorBoundary } from "@karrio/ui/core/components/error-boudaries";
import { Toaster } from "@karrio/ui/components/ui/toaster";
import { PublicEnvScript } from "next-runtime-env";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <PublicEnvScript />
        <meta charSet="utf-8" />
        <link rel="favicon" sizes="180x180" href={`/favicon.ico`} />
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href={`/apple-touch-icon.png`}
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href={`/favicon-32x32.png`}
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href={`/favicon-16x16.png`}
        />
        <link rel="manifest" href={`/manifest.json`} />
        <link rel="mask-icon" href={`/safari-pinned-tab.svg`} color="#9504af" />
        <meta name="msapplication-TileColor" content="#9504af" />
        <meta name="theme-color" content="#9504af" />
        <meta name="robots" content="NONE,NOARCHIVE" />
        <meta name="theme-color" content="#9504af" />
        <link rel="manifest" href={`/manifest.json`} />
      </head>
      <body suppressHydrationWarning>
        <noscript>You need to enable JavaScript to run this app.</noscript>

        <div id="root" style={{ minHeight: "100vh" }}>
          <ErrorBoundary>
            {children}
            <Toaster />
          </ErrorBoundary>
        </div>
      </body>
    </html>
  );
}
