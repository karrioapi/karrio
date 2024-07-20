import { POSTHOG_HOST, POSTHOG_KEY } from "@karrio/lib";
import { PostHogProvider } from "posthog-js/react";
import { useRouter } from "next/router";
import { useEffect } from "react";
import posthog from "posthog-js";
import React from "react";

// Check that PostHog is client-side (used to handle Next.js SSR)
if (typeof window !== "undefined") {
  posthog.init(POSTHOG_KEY as string, {
    api_host: POSTHOG_HOST || "https://app.posthog.com",
    // Enable debug mode in development
    loaded: (posthog) => {
      if (process.env.NODE_ENV === "development") posthog.debug();
    },
  });
}

export const NextPostHogProvider: React.FC<{ children?: React.ReactNode }> = ({
  children,
}) => {
  const router = useRouter();

  useEffect(() => {
    // Track page views
    const handleRouteChange = () => posthog?.capture("$pageview");
    router.events.on("routeChangeComplete", handleRouteChange);

    return () => {
      router.events.off("routeChangeComplete", handleRouteChange);
    };
  }, []);

  return <PostHogProvider client={posthog}>{children}</PostHogProvider>;
};
