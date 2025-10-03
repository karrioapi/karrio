"use client";
import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from '@karrio/ui/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@karrio/ui/components/ui/card';

interface AppErrorBoundaryProps {
    children: React.ReactNode;
    fallback?: React.ReactNode;
    onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
    showDetails?: boolean;
    context?: string;
}

interface AppErrorBoundaryState {
    hasError: boolean;
    error: Error | null;
    errorInfo: React.ErrorInfo | null;
}

export class AppErrorBoundary extends React.Component<AppErrorBoundaryProps, AppErrorBoundaryState> {
    constructor(props: AppErrorBoundaryProps) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
            errorInfo: null,
        };
    }

    static getDerivedStateFromError(error: Error): Partial<AppErrorBoundaryState> {
        return {
            hasError: true,
            error,
        };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        this.setState({
            error,
            errorInfo,
        });

        // Log the error
        console.error(`App Error${this.props.context ? ` in ${this.props.context}` : ''}:`, error, errorInfo);

        // Call custom error handler if provided
        if (this.props.onError) {
            this.props.onError(error, errorInfo);
        }
    }

    handleRetry = () => {
        this.setState({
            hasError: false,
            error: null,
            errorInfo: null,
        });
    };

    render() {
        if (this.state.hasError) {
            // Use custom fallback if provided
            if (this.props.fallback) {
                return this.props.fallback;
            }

            // Default error UI
            return (
                <Card className="w-full max-w-2xl mx-auto">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-red-600">
                            <AlertTriangle className="h-5 w-5" />
                            Something went wrong
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="text-sm text-slate-600">
                            {this.props.context ? (
                                <p>An error occurred in the {this.props.context}. Please try refreshing or contact support if the problem persists.</p>
                            ) : (
                                <p>An unexpected error occurred. Please try refreshing or contact support if the problem persists.</p>
                            )}
                        </div>

                        <div className="flex items-center gap-2">
                            <Button
                                onClick={this.handleRetry}
                                size="sm"
                                variant="outline"
                                className="flex items-center gap-1"
                            >
                                <RefreshCw className="h-4 w-4" />
                                Try Again
                            </Button>

                            <Button
                                onClick={() => window.location.reload()}
                                size="sm"
                                variant="outline"
                            >
                                Refresh Page
                            </Button>
                        </div>

                        {this.props.showDetails && this.state.error && (
                            <details className="mt-4">
                                <summary className="cursor-pointer text-sm text-slate-500 hover:text-slate-700">
                                    Show Error Details
                                </summary>
                                <div className="mt-2 p-3 bg-slate-50 rounded-md text-xs font-mono text-slate-700 overflow-auto">
                                    <div className="mb-2">
                                        <strong>Error:</strong> {this.state.error.message}
                                    </div>
                                    {this.state.error.stack && (
                                        <div className="mb-2">
                                            <strong>Stack:</strong>
                                            <pre className="whitespace-pre-wrap mt-1">{this.state.error.stack}</pre>
                                        </div>
                                    )}
                                    {this.state.errorInfo?.componentStack && (
                                        <div>
                                            <strong>Component Stack:</strong>
                                            <pre className="whitespace-pre-wrap mt-1">{this.state.errorInfo.componentStack}</pre>
                                        </div>
                                    )}
                                </div>
                            </details>
                        )}
                    </CardContent>
                </Card>
            );
        }

        return this.props.children;
    }
}

// Higher-order component wrapper
export function withAppErrorBoundary<P extends object>(
    Component: React.ComponentType<P>,
    errorBoundaryProps?: Omit<AppErrorBoundaryProps, 'children'>
) {
    const WrappedComponent = (props: P) => (
        <AppErrorBoundary {...errorBoundaryProps}>
            <Component {...props} />
        </AppErrorBoundary>
    );

    WrappedComponent.displayName = `withAppErrorBoundary(${Component.displayName || Component.name})`;

    return WrappedComponent;
}

// Hook for error boundary context
export function useAppErrorHandler() {
    const throwError = React.useCallback((error: Error) => {
        // This will be caught by the nearest error boundary
        throw error;
    }, []);

    const handleAsyncError = React.useCallback((error: Error) => {
        // For async errors, we need to throw in the next tick
        setTimeout(() => {
            throw error;
        }, 0);
    }, []);

    return {
        throwError,
        handleAsyncError,
    };
}
