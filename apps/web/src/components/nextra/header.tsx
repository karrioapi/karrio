"use client"

import { SidebarTrigger } from '@karrio/ui/components/ui/sidebar'
import { Button } from '@karrio/ui/components/ui/button'
import { normalizePages } from 'nextra/normalize-pages'
import { Menu, Moon, Search, Sun } from 'lucide-react'
import { usePathname } from 'next/navigation'
import { useState, useEffect } from 'react'
import type { PageMapItem } from 'nextra'
import { useTheme } from 'next-themes'
import { type FC } from 'react'
import Link from 'next/link'
import clsx from 'clsx'
import { DocSearchWrapper } from '@/components/search/docsearch-component'
import { ThemeToggle } from '../blog/theme-toggle'

export interface HeaderProps {
  pageMap: PageMapItem[]
}

export const Header: FC<HeaderProps> = ({ pageMap }) => {
  const pathname = usePathname()
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  // After mounting, we can check theme
  useEffect(() => {
    setMounted(true)
  }, [])

  // Get top-level sections from pageMap
  const { docsDirectories } = normalizePages({
    list: pageMap,
    route: pathname
  })

  // Find docs entry in the page map
  const docsEntry = docsDirectories.find(item => item.name === 'docs')
  const topLevelSections = docsEntry?.children || []

  return (
    <header className={`flex h-14 w-full md:px-8 px-2 shrink-0 items-center border-b border-gray-200 bg-background ${mounted && theme === 'dark' ? '!border-neutral-800' : ''}`}>
      <div className="mx-auto h-full w-full max-w-[95%] xl:max-w-[1280px]">
        {/* Hidden DocSearch wrapper for blog pages */}
        <div className="hidden">
          <DocSearchWrapper buttonText="Search blog..." />
        </div>

        {/* Mobile Header */}
        <div className="flex h-full items-center justify-between md:hidden">
          <Link href="/docs" className="flex items-center">
            {mounted && (theme === 'dark' ? (
              <img src="/karrio-docs-light.svg" alt="Karrio Docs" className="h-5 w-auto" />
            ) : (
              <img src="/karrio-docs.svg" alt="Karrio Docs" className="h-5 w-auto" />
            ))}
          </Link>

          <div className="flex items-center gap-2">
            <ThemeToggle />
            <Button
              variant="ghost"
              size="icon"
              className="rounded-full p-1.5 text-foreground/80 hover:text-foreground hover:bg-muted dark:text-white/80 dark:hover:text-white dark:hover:bg-[#1a103a]"
              onClick={() => {
                // Find a DocSearch button in the DOM and trigger a click on it
                const docSearchButton = document.querySelector('.DocSearch-Button') as HTMLButtonElement;
                if (docSearchButton) {
                  docSearchButton.click();
                }
              }}
              aria-label="Search blog"
            >
              <Search className="h-5 w-5" />
            </Button>

            <SidebarTrigger className={mounted && theme === 'dark' ? '!text-gray-300' : 'text-gray-600'}>
              <Menu className="h-5 w-5" />
            </SidebarTrigger>
          </div>
        </div>

        {/* Desktop Header */}
        <div className="hidden md:flex h-full items-center gap-1">
          <nav className="flex h-full items-center gap-6">
            {topLevelSections.map((section) => (
              section.type === 'separator' && (
                <Link
                  key={section.name}
                  href={`/docs/${section.name}`}
                  className={clsx(
                    "relative flex h-full items-center px-1 text-sm font-medium transition-colors text-gray-700 hover:text-gray-900 dark:text-gray-200 dark:hover:text-white",
                    pathname.startsWith(`/docs/${section.name}`) && "after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-purple-600 dark:after:bg-purple-400"
                  )}
                >
                  {section.title}
                </Link>
              )
            ))}
          </nav>

          <div className="flex-1" />

          <ThemeToggle />
          <Button
            variant="ghost"
            size="icon"
            className="rounded-full p-1.5 text-foreground/80 hover:text-foreground hover:bg-muted dark:text-white/80 dark:hover:text-white dark:hover:bg-[#1a103a]"
            onClick={() => {
              // Find a DocSearch button in the DOM and trigger a click on it
              const docSearchButton = document.querySelector('.DocSearch-Button') as HTMLButtonElement;
              if (docSearchButton) {
                docSearchButton.click();
              }
            }}
            aria-label="Search blog"
          >
            <Search className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  )
}
