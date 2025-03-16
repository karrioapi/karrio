import { ErrorBoundary } from "@karrio/ui/core/components/error-boudaries";
import { loadMetadata } from "@karrio/core/context/main";
import { PublicEnvScript } from "next-runtime-env";
import { ServerErrorCode } from "@karrio/lib";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { error } = await loadMetadata();

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
      <body>
        <noscript>You need to enable JavaScript to run this app.</noscript>

        <div id="root" style={{ minHeight: "100vh" }}>
          <ErrorBoundary>
            {error?.code !== ServerErrorCode.API_CONNECTION_ERROR ? (
              children
            ) : (
              <section className="hero is-fullheight">
                <div className="container">
                  <div className="has-text-centered mt-4 mb-5">
                    <span className="has-text-primary has-text-weight-bold is-size-4">
                      Uh Oh!
                    </span>
                  </div>

                  <div className="card isolated-card my-6">
                    <div className="card-content has-text-centered ">
                      <p>{error?.message}</p>
                    </div>
                  </div>
                </div>
              </section>
            )}
          </ErrorBoundary>
        </div>
      </body>
    </html>
  );
}
