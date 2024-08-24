import { Metadata, SessionType } from "@karrio/types";
import { ServerError, url$ } from "@karrio/lib";
import MainLayout from "@karrio/core/layouts/main-layout";
import React from "react";

type SectionLayoutProps = {
  metadata?: Metadata;
  error?: ServerError;
  session?: SessionType;
  children?: React.ReactNode;
};

export const SectionLayout: React.FC<SectionLayoutProps> = ({
  metadata,
  error,
  children,
}) => {
  return (
    <MainLayout error={error}>
      <section className="hero is-fullheight">
        <div className="container">
          <div className="has-text-centered my-6 pt-5">
            <a
              href={url$`${metadata?.APP_WEBSITE}`}
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
              {metadata?.APP_NAME.includes("Karrio") && (
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
    </MainLayout>
  );
};
