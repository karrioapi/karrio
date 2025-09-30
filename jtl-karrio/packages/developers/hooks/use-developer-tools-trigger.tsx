"use client";

import { useCallback } from "react";
import { useDeveloperTools, DeveloperView } from "@karrio/developers/context/developer-tools-context";

export function useDeveloperToolsTrigger() {
  const { openDeveloperTools, toggleDeveloperTools } = useDeveloperTools();

  const openDevTools = useCallback((view?: DeveloperView) => {
    openDeveloperTools(view);
  }, [openDeveloperTools]);

  const toggleDevTools = useCallback(() => {
    toggleDeveloperTools();
  }, [toggleDeveloperTools]);

  // Utility functions for specific views
  const openActivity = useCallback(() => openDevTools("activity"), [openDevTools]);
  const openAPIKeys = useCallback(() => openDevTools("api-keys"), [openDevTools]);
  const openWebhooks = useCallback(() => openDevTools("webhooks"), [openDevTools]);
  const openEvents = useCallback(() => openDevTools("events"), [openDevTools]);
  const openLogs = useCallback(() => openDevTools("logs"), [openDevTools]);
  const openApps = useCallback(() => openDevTools("apps"), [openDevTools]);

  return {
    openDevTools,
    toggleDevTools,
    openActivity,
    openAPIKeys,
    openWebhooks,
    openEvents,
    openLogs,
    openApps,
  };
}
