"use client";

import { TestModeToggle } from "@karrio/ui/components/test-mode-toggle";
import { AccountDropdown } from "@karrio/ui/components/account-dropdown";
import { SearchBar } from "@karrio/ui/components/search-bar";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Button } from "@karrio/ui/components/ui/button";
import { useAppMode } from "@karrio/hooks/app-mode";
import { DASHBOARD_VERSION, p } from "@karrio/lib";
import { Menu, Search, Shield, X } from "lucide-react";
import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { AdminSidebar } from "./admin-sidebar";
import { usePathname } from "next/navigation";
import React from "react";

export function AdminHeader() {
  const pathname = usePathname();
  const [showMobileSearch, setShowMobileSearch] = useState(false);
  const [showMobileSidebar, setShowMobileSidebar] = useState(false);

  React.useEffect(() => {
    setShowMobileSidebar(false);
    setShowMobileSearch(false);
  }, [pathname]);


  return (
    <>
      {/* Main Admin Header */}
      <header className="fixed top-0 left-0 right-0 z-20 h-14 bg-white border-b border-gray-200">
        <div className="flex items-center gap-4 h-full max-w-none mx-auto px-4 sm:px-6 lg:px-8">

          <div className="flex items-center gap-2">
            {/* Mobile hamburger menu */}
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setShowMobileSidebar(true)}
            >
              <Menu className="h-5 w-5" />
            </Button>

            {/* Logo */}
            <Link href="/" className="flex items-center gap-2">
              <Image
                src={p`/icon.svg`}
                width={18}
                height={18}
                className="m-1"
                alt="logo"
              />
            </Link>
          </div>

          {/* Admin Badge */}
          <div className="hidden sm:flex items-center gap-2">
            <div className="flex items-center gap-1.5 rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 border border-red-200">
              <Shield className="h-3 w-3" />
              Admin Console
            </div>
            <span className="hidden sm:block rounded bg-gray-100 px-2 py-1 text-xs text-gray-600">
              {DASHBOARD_VERSION}
            </span>
          </div>

          {/* Center Section - Search */}
          <div className="flex items-center gap-4 flex-1 justify-center">
            {/* Desktop Search - Hidden on mobile */}
            <div className="hidden md:block w-full max-w-md">
              <SearchBar
                placeholder="Search admin resources..."
                className="bg-gray-50 hover:bg-gray-100 focus-within:bg-white"
              />
            </div>
          </div>

          {/* Right Section - Action Buttons */}
          <div className="flex items-center gap-2">
            {/* Mobile Search Toggle */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setShowMobileSearch(true)}
            >
              <Search className="h-4 w-4" />
            </Button>

            {/* Test Mode Toggle */}
            <TestModeToggle />

            {/* Account Dropdown */}
            <AccountDropdown />
          </div>
        </div>
      </header>

      {/* Mobile Search Overlay */}
      {showMobileSearch && (
        <div className="fixed inset-0 z-50 bg-black/50 md:hidden" onClick={() => setShowMobileSearch(false)}>
          <div className="absolute top-0 left-0 right-0 bg-white p-2 border-b" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <SearchBar
                  placeholder="Search admin resources..."
                  className="bg-gray-50"
                />
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowMobileSearch(false)}
              >
                Cancel
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Mobile Sidebar */}
      {showMobileSidebar && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          onClick={() => setShowMobileSidebar(false)}
        />
      )}
      <aside
        className={`fixed top-0 left-0 h-full z-40 w-[280px] bg-white shadow-lg transition-transform duration-300 lg:hidden ${showMobileSidebar ? 'translate-x-0' : '-translate-x-full'
          }`}
      >
        <div className="flex items-center justify-between h-14 px-4 border-b">
          <div className="flex items-center gap-2">
            <Link href="/" className="flex items-center gap-2">
              <Image
                src={p`/icon.svg`}
                width={18}
                height={18}
                className="m-1"
                alt="logo"
              />
            </Link>
            <span className="font-semibold text-md">Karrio</span>
          </div>
          <Button variant="ghost" size="icon" onClick={() => setShowMobileSidebar(false)}>
            <X className="h-5 w-5" />
          </Button>
        </div>
        <AdminSidebar isDrawer />
      </aside>
    </>
  );
}
