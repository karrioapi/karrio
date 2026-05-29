// ErrorBoundary.tsx — catches render errors, reports via the monitoring seam,
// and shows a friendly recoverable fallback (UX resilience).
import { Component, type ErrorInfo, type ReactNode } from "react";
import { captureError } from "~/lib/monitoring";

type Props = { children: ReactNode };
type State = { error: Error | null };

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    captureError(error, { componentStack: info.componentStack });
  }

  render() {
    if (this.state.error) {
      return (
        <div className="page" data-testid="error-boundary">
          <div className="placeholder">
            <h2>Something went wrong</h2>
            <p>An unexpected error occurred. The team has been notified.</p>
            <button className="btn btn-primary" onClick={() => this.setState({ error: null })}>
              Try again
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
