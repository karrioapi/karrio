import { Metadata, SessionType } from '@karrio/types';
import MainLayout from '@/layouts/main-layout';
import { ServerError, p } from '@karrio/lib';
import Link from 'next/link';
import React from 'react';

type SectionLayoutProps = {
  metadata?: Metadata,
  error?: ServerError,
  session?: SessionType,
  children?: React.ReactNode,
};

export const SectionLayout: React.FC<SectionLayoutProps> = ({ metadata, error, children }) => {
  return (
    <MainLayout error={error}>
      <section className="hero is-fullheight">

        <div className="container">
          <div className="has-text-centered my-6 pt-5">
            <a href={p`/`} className="is-size-4 has-text-primary has-text-weight-bold">
              {metadata?.APP_NAME}
            </a>
          </div>

          {children}

        </div>

        <div className="hero-footer">
          <div className="content has-text-centered">
            <p>
              <Link legacyBehavior href="/">
                <span className="button is-white">&copy; {metadata?.APP_NAME}</span>
              </Link>
              <a href="https://docs.karrio.io" className="button is-white">Documentation</a>
            </p>
          </div>
        </div>

      </section>
    </MainLayout>
  );
};
