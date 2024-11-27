"use client";
import React from "react";

interface ErrorBoundaryProps {
  children?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

export const ErrorBoundary = ({
  children,
}: ErrorBoundaryProps): JSX.Element => {
  const [hasError, setHasError] = React.useState(false);

  React.useEffect(() => {
    const handleError = (error: ErrorEvent) => {
      console.log("Error boundaries caught...");
      console.error(error);
      setHasError(true);
    };

    window.addEventListener("error", handleError);
    return () => window.removeEventListener("error", handleError);
  }, []);

  if (hasError) {
    return (
      <section className="hero is-fullheight">
        <div className="container">
          <div className="has-text-centered mt-4 mb-5">
            <span className="has-text-primary has-text-weight-bold is-size-4">
              Uh Oh!
            </span>
          </div>

          <div className="card isolated-card my-6">
            <div className="card-content has-text-centered ">
              <p>Something went wrong!</p>
            </div>
          </div>
        </div>
      </section>
    );
  }

  return <>{children}</>;
};
