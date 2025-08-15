"use client";

import React from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Terminal, Code2 } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";

export function FloatingDeveloperTools() {
  // Simple mobile detection
  const [isMobile, setIsMobile] = React.useState(false);
  const [mounted, setMounted] = React.useState(false);
  const [isDeveloperToolsOpen, setIsDeveloperToolsOpen] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);

    // Listen for developer tools state changes
    const handleDeveloperToolsChange = (event: CustomEvent) => {
      setIsDeveloperToolsOpen(event.detail.isOpen);
    };

    window.addEventListener('developer-tools-state-change', handleDeveloperToolsChange as EventListener);

    return () => {
      window.removeEventListener('resize', checkMobile);
      window.removeEventListener('developer-tools-state-change', handleDeveloperToolsChange as EventListener);
    };
  }, []);

  // Don't render on server, before mounting, when developer tools is open, or on desktop
  if (!mounted || isDeveloperToolsOpen || !isMobile) {
    return null;
  }

  const handleClick = () => {
    const event = new CustomEvent('toggle-developer-tools');
    window.dispatchEvent(event);
  };

  return (
    <Button
      onClick={handleClick}
      className={cn(
        "fixed bottom-6 right-6 z-30 shadow-lg transition-all duration-200 ease-in-out",
        "bg-gray-900 hover:bg-gray-800 text-white border-gray-700",
        "w-12 h-12 px-0 flex items-center justify-center rounded-full"
      )}
    >
      <Code2 className="h-5 w-5" />
    </Button>
  );
}
