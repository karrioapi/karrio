"use client";

import { POSTHOG_HOST, POSTHOG_KEY } from "@karrio/lib";
import { PostHogProvider } from "posthog-js/react";
import posthog from "posthog-js";

if (typeof window !== "undefined") {
  posthog.init(POSTHOG_KEY as string, {
    api_host: POSTHOG_HOST,
    capture_pageview: false,
  });
}

export function NextPostHogProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return <PostHogProvider client={posthog}>{children}</PostHogProvider>;
}
