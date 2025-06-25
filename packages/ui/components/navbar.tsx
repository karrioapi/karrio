"use client";

import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useAppMode } from "@karrio/hooks/app-mode";
import { Button } from "@karrio/ui/components/ui/button";
import { ShortcutDropdown } from "./shortcut-dropdown";
import { AccountDropdown } from "./account-dropdown";
import { Search, Loader2 } from "lucide-react";
import { TestModeToggle } from "./test-mode-toggle";
import { SidebarTrigger } from "@karrio/ui/components/ui/sidebar";
import { Separator } from "@karrio/ui/components/ui/separator";
import React, { Suspense, useState } from "react";
import { SearchBar } from "./search-bar";
import { SearchModal } from "./search-modal";

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
        <div className="flex items-center gap-2 w-full max-w-7xl mx-auto px-4 2xl:px-0">
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
              <Suspense fallback={
                <Button variant="outline" size="icon" disabled className="rounded-full">
                  <Loader2 className="h-4 w-4 animate-spin" />
                </Button>
              }>
                <AppLauncher />
              </Suspense>
            )}

            {/* Shortcut Dropdown */}
            <ShortcutDropdown />

            {/* Account Dropdown */}
            <AccountDropdown />
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
