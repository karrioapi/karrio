"use client";

import React, { createContext, useContext, useState, useCallback } from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useUser } from "@karrio/hooks/user";

export type DeveloperView =
  | "activity"
  | "api-keys"
  | "logs"
  | "events"
  | "tracing-records"
  | "apps"
  | "webhooks"
  | "playground"
  | "graphiql"
  // Admin-only views (visible only when isAdminMode=true)
  | "workers"
  | "system-health";

interface DeveloperToolsContextType {
  isOpen: boolean;
  currentView: DeveloperView;
  isAdminMode: boolean;
  openDeveloperTools: (view?: DeveloperView) => void;
  closeDeveloperTools: () => void;
  setCurrentView: (view: DeveloperView) => void;
  toggleDeveloperTools: () => void;
}

const DeveloperToolsContext = createContext<DeveloperToolsContextType | undefined>(undefined);

export function DeveloperToolsProvider({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const [currentView, setCurrentView] = useState<DeveloperView>("activity");
  const { metadata } = useAPIMetadata();
  const { query: { data: { user } = {} } } = useUser();

  const isAdminMode = !!(metadata?.ADMIN_DASHBOARD && (user as any)?.is_staff);

  const openDeveloperTools = useCallback((view: DeveloperView = "activity") => {
    setCurrentView(view);
    setIsOpen(true);
  }, []);

  const closeDeveloperTools = useCallback(() => {
    setIsOpen(false);
  }, []);

  const toggleDeveloperTools = useCallback(() => {
    setIsOpen(prev => !prev);
  }, []);

  // Listen for custom events from sidebar
  React.useEffect(() => {
    const handleToggleEvent = () => {
      toggleDeveloperTools();
    };

    window.addEventListener('toggle-developer-tools', handleToggleEvent);
    return () => window.removeEventListener('toggle-developer-tools', handleToggleEvent);
  }, [toggleDeveloperTools]);

  const contextValue: DeveloperToolsContextType = {
    isOpen,
    currentView,
    isAdminMode,
    openDeveloperTools,
    closeDeveloperTools,
    setCurrentView,
    toggleDeveloperTools,
  };

  return (
    <DeveloperToolsContext.Provider value={contextValue}>
      {children}
    </DeveloperToolsContext.Provider>
  );
}

export function useDeveloperTools() {
  const context = useContext(DeveloperToolsContext);
  if (context === undefined) {
    throw new Error("useDeveloperTools must be used within a DeveloperToolsProvider");
  }
  return context;
}
