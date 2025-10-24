"use client";

import { POSTHOG_HOST, POSTHOG_KEY } from "@karrio/lib";
import { PostHogProvider } from "posthog-js/react";
import posthog from "posthog-js";
import { useEffect, useState } from "react";

export function NextPostHogProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined" && POSTHOG_KEY && !isInitialized) {
      console.log("Initializing PostHog with key:", POSTHOG_KEY?.substring(0, 10) + "...");
      console.log("PostHog host:", POSTHOG_HOST);

      posthog.init(POSTHOG_KEY as string, {
        api_host: POSTHOG_HOST,
        capture_pageview: false,
      });

      setIsInitialized(true);
    }
  }, [isInitialized]);

  return <PostHogProvider client={posthog}>{children}</PostHogProvider>;
}
