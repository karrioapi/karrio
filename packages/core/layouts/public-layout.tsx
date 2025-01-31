import "@fortawesome/fontawesome-free/css/all.min.css";
import "highlight.js/styles/stackoverflow-light.css";
import "@/styles/theme.scss";
import "@/styles/dashboard.scss";
import { loadMetadata } from "@karrio/core/context/main";
import { Providers } from "@karrio/hooks/providers";
import { url$ } from "@karrio/lib";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { metadata } = await loadMetadata();
  const pageProps = { metadata };

  console.log(metadata, "metadata");

  return (
    <>
      <Providers {...pageProps}>
        <section className="hero is-fullheight">
          <div className="container">
            <div className="has-text-centered my-6 pt-5">
              <a
                href={url$`${metadata?.APP_WEBSITE || "/"}`}
                className="is-size-4 has-text-primary has-text-weight-bold"
              >
                {metadata?.APP_NAME}
              </a>
            </div>

            {children}
          </div>

          <div className="hero-footer">
            <div className="content has-text-centered">
              <p>
                {metadata?.APP_NAME?.includes("Karrio") && (
                  <>
                    <a
                      href="https://karrio.io"
                      className="button is-white"
                      target="_blank"
                      rel="noreferrer"
                    >
                      <span>&copy; {metadata?.APP_NAME}</span>
                    </a>
                    <a
                      href="https://docs.karrio.io"
                      className="button is-white"
                      target="_blank"
                      rel="noreferrer"
                    >
                      <span>Documentation</span>
                    </a>
                  </>
                )}
              </p>
            </div>
          </div>
        </section>
      </Providers>
    </>
  );
}
