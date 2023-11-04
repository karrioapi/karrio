import { ServerError, ServerErrorCode } from '@/lib/helper';
import ErrorBoundary from '@/components/error-boudaries';
import React from 'react';

const MainLayout: React.FC<{ error?: ServerError }> = ({ children, error }) => {
  return (
    <>
      <noscript>You need to enable JavaScript to run this app.</noscript>

      <div id="root" style={{ minHeight: "100vh" }} >
        <ErrorBoundary>
          {(error?.code !== ServerErrorCode.API_CONNECTION_ERROR)
            ? children
            : <section className="hero is-fullheight">
              <div className="container">
                <div className="has-text-centered mt-4 mb-5">
                  <span className="has-text-primary has-text-weight-bold is-size-4">Uh Oh!</span>
                </div>

                <div className="card isolated-card my-6">
                  <div className="card-content has-text-centered ">
                    <p>{error?.message}</p>
                  </div>
                </div>
              </div>
            </section>}
        </ErrorBoundary>
      </div>
    </>
  )
};

export default MainLayout;
