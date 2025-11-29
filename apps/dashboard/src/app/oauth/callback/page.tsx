"use client";

import { storeEncryptedOAuthResult } from "@karrio/lib";
import { Suspense, useEffect } from "react";
import { useSearchParams } from "next/navigation";

/**
 * OAuth Callback Content Component
 *
 * This component handles the OAuth result processing using useSearchParams.
 * It must be wrapped in a Suspense boundary per Next.js 15 requirements.
 *
 * Security considerations:
 * - Uses localStorage (not sessionStorage) because popup windows have separate
 *   sessionStorage contexts from their opener window
 * - Data is encrypted using AES-GCM before storage
 * - The opener window immediately clears the data after reading
 * - Short-lived storage minimizes exposure window
 */
function OAuthCallbackContent() {
  const searchParams = useSearchParams();

  useEffect(() => {
    const oauthResult = searchParams.get("oauth_result");
    const closeWindow = (delay: number) => setTimeout(() => window.close(), delay);

    if (!oauthResult) {
      closeWindow(2000);
      return;
    }

    (async () => {
      try {
        const decodedResult = JSON.parse(atob(oauthResult));
        await storeEncryptedOAuthResult(decodedResult);
        closeWindow(500);
      } catch (e) {
        console.error("Failed to process OAuth result:", e);
        closeWindow(2000);
      }
    })();
  }, [searchParams]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="text-center p-8 bg-white rounded-lg shadow-md max-w-md">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-purple-600 mx-auto mb-4"></div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">
          Completing Authorization
        </h2>
        <p className="text-sm text-gray-600">
          Please wait while we complete your connection...
        </p>
        <p className="text-xs text-gray-400 mt-4">
          This window will close automatically.
        </p>
      </div>
    </div>
  );
}

/**
 * OAuth Callback Page
 *
 * Wraps the callback content in a Suspense boundary as required by Next.js 15
 * when using useSearchParams().
 */
export default function OAuthCallbackPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center bg-gray-50">
          <div className="text-center p-8 bg-white rounded-lg shadow-md max-w-md">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-purple-600 mx-auto mb-4"></div>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">
              Loading...
            </h2>
          </div>
        </div>
      }
    >
      <OAuthCallbackContent />
    </Suspense>
  );
}
