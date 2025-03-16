"use client";

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Menu, Search, Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';
import { Button } from '@karrio/ui/components/ui/button';

interface DocsHeaderProps {
  onToggleSidebar?: () => void;
}

export function DocsHeader({ onToggleSidebar }: DocsHeaderProps) {
  const { theme, setTheme } = useTheme();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-gray-200 dark:border-white/10 bg-white/95 dark:bg-[#111]/95 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:supports-[backdrop-filter]:bg-[#111]/60">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={onToggleSidebar}
            aria-label="Toggle menu"
          >
            <Menu className="h-5 w-5" />
          </Button>

          <Link href="/docs" className="flex items-center">
            <Image
              src="/logo.svg"
              alt="Karrio Logo"
              width={120}
              height={30}
              priority
              className="dark:hidden"
            />
            <Image
              src="/logo-light.svg"
              alt="Karrio Logo"
              width={120}
              height={30}
              priority
              className="hidden dark:block"
            />
            <span className="ml-2 font-semibold text-lg hidden sm:inline-block">Docs</span>
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <div className="relative hidden md:flex items-center">
            <Search className="absolute left-3 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search or ask..."
              className="h-9 w-64 rounded-md border border-gray-200 bg-white pl-10 pr-4 text-sm text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary dark:border-white/10 dark:bg-[#1a1a1a] dark:text-white dark:placeholder-gray-400"
            />
            <div className="absolute right-3 flex items-center text-xs text-gray-400">
              <kbd className="hidden sm:inline-block rounded bg-gray-100 px-1.5 py-0.5 dark:bg-gray-800">⌘K</kbd>
            </div>
          </div>

          <Button
            variant="ghost"
            size="icon"
            aria-label="Toggle theme"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            className="focus:ring-0 focus:ring-offset-0"
          >
            <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>

          <Button
            variant="default"
            size="sm"
            className="hidden sm:inline-flex"
            asChild
          >
            <Link href="https://platform.karrio.io">
              Dashboard →
            </Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
