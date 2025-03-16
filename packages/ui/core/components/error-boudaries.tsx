"use client";
import React from "react";

interface ErrorBoundaryProps {
  children?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    // Non-fatal errors that should be ignored
    const nonFatalErrors = [
      'ResizeObserver loop completed with undelivered notifications',
      'ResizeObserver loop limit exceeded'
    ];

    // Update state so the next render will show the fallback UI
    return {
      hasError: !nonFatalErrors.some(msg => error.message?.includes(msg)),
      error
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // You can log the error to an error reporting service here
    if (!error.message?.includes('ResizeObserver')) {
      console.log("Error boundaries caught...");
      console.error(error);
      console.error(errorInfo);
    }
  }

  render() {
    if (this.state.hasError) {
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
                {process.env.NODE_ENV === 'development' && (
                  <pre className="error-details mt-4">
                    {this.state.error?.toString()}
                  </pre>
                )}
              </div>
            </div>
          </div>
        </section>
      );
    }

    return this.props.children;
  }
}
