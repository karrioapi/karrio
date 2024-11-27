"use client";

import * as Sentry from "@sentry/nextjs";
import { useEffect } from "react";

export default function GlobalError({
  error,
}: {
  error: Error & { digest?: string };
}) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <html>
      <body>
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-xl mx-auto text-center">
            <h1 className="text-4xl font-bold mb-4">Something went wrong!</h1>
            <p className="text-gray-600 mb-8">
              We apologize for the inconvenience. Our team has been notified and
              is working to fix the issue.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700"
            >
              Try Again
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
