import { PostHogProvider } from 'posthog-js/react';
import { useRouter } from 'next/router';
import getConfig from 'next/config';
import { useEffect } from 'react';
import posthog from 'posthog-js';
import React from "react";

const { publicRuntimeConfig } = getConfig();

// Check that PostHog is client-side (used to handle Next.js SSR)
if (typeof window !== 'undefined') {
  posthog.init(publicRuntimeConfig.POSTHOG_KEY, {
    api_host: publicRuntimeConfig.POSTHOG_HOST || 'https://app.posthog.com',
    // Enable debug mode in development
    loaded: (posthog) => {
      if (process.env.NODE_ENV === 'development') posthog.debug()
    }
  })
}


export const NextPostHogProvider: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const router = useRouter()

  useEffect(() => {
    // Track page views
    const handleRouteChange = () => posthog?.capture('$pageview')
    router.events.on('routeChangeComplete', handleRouteChange)

    return () => {
      router.events.off('routeChangeComplete', handleRouteChange)
    }
  }, [])

  return (
    <PostHogProvider client={posthog}>
      {children}
    </PostHogProvider>
  )
};
