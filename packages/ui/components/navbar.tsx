"use client";

import { ShortcutDropdown } from "@karrio/ui/components/shortcut-dropdown";
import { TestModeToggle } from "@karrio/ui/components/test-mode-toggle";
import { SidebarTrigger } from "@karrio/ui/components/ui/sidebar";
import { SearchModal } from "@karrio/ui/components/search-modal";
import { Separator } from "@karrio/ui/components/ui/separator";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { SearchBar } from "@karrio/ui/components/search-bar";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Button } from "@karrio/ui/components/ui/button";
import { Search, Blocks, Settings } from "lucide-react";
import { useAppMode } from "@karrio/hooks/app-mode";
import React, { Suspense, useState } from "react";

// Lazy load the AppLauncher component
const AppLauncher = React.lazy(() =>
  import("@karrio/app-store").then(module => ({ default: module.AppLauncher }))
);

// Main Navbar Component
export function Navbar() {
  const { metadata } = useAPIMetadata();
  const { testMode } = useAppMode();
  const [showMobileSearchModal, setShowMobileSearchModal] = useState(false);

  return (
    <>
      {/* Main Navbar */}
      <header className={`sticky z-40 flex h-14 shrink-0 items-center gap-2 bg-white transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12 ${testMode ? 'top-[4px]' : 'top-0'}`}>
        <div className="flex items-center gap-2 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 2xl:px-0">
          {/* Mobile Sidebar Trigger */}
          <SidebarTrigger className="-ml-1 md:hidden" />
          <Separator
            orientation="vertical"
            className="mr-2 h-4 md:hidden"
          />

          {/* Left Section - Search */}
          <div className="flex items-center gap-4 flex-1">
            {/* Desktop Search - Hidden on mobile */}
            <div className="hidden md:block w-full">
              <SearchBar />
            </div>
          </div>

          {/* Right Section - Action Buttons */}
          <div className="flex items-center gap-2">
            {/* Mobile Search Toggle */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setShowMobileSearchModal(true)}
            >
              <Search className="h-4 w-4" />
            </Button>

            {/* Test Mode Toggle */}
            <TestModeToggle />

            {/* App Launcher */}
            {metadata?.APPS_MANAGEMENT && (
              <Suspense fallback={<></>}>
                <AppLauncher />
              </Suspense>
            )}

            {/* Settings */}
            <AppLink href="/settings">
              <Button variant="outline" size="icon" className="rounded-full !rounded-full border-radius-50">
                <Settings className="h-4 w-4" />
              </Button>
            </AppLink>

            {/* Shortcut Dropdown */}
            <ShortcutDropdown />
          </div>
        </div>

        {/* Mobile Search Modal */}
        <SearchModal
          open={showMobileSearchModal}
          onOpenChange={setShowMobileSearchModal}
        />
      </header>
    </>
  );
}
