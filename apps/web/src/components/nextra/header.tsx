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

export interface HeaderProps {
  pageMap: PageMapItem[]
}

export const Header: FC<HeaderProps> = ({ pageMap }) => {
  const pathname = usePathname()
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  const [showSearch, setShowSearch] = useState(false)

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
    <header className={`flex h-14 w-full md:px-8 px-2 shrink-0 items-center border-b border-gray-200 bg-white ${mounted && theme === 'dark' ? '!bg-neutral-950 !border-neutral-800' : ''}`}>
      <div className="mx-auto h-full w-full max-w-[95%] xl:max-w-[1280px]">
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
            <Button
              variant="ghost"
              size="icon"
              className="rounded-full p-1.5 text-gray-500 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-neutral-800"
              onClick={() => setShowSearch(!showSearch)}
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

          <Button
            variant="ghost"
            size="icon"
            className="rounded-full p-1.5 text-gray-500 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-neutral-800"
            onClick={() => {
              const newTheme = theme === 'dark' ? 'light' : 'dark';
              setTheme(newTheme);
            }}
            aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          >
            {mounted && (theme === 'dark' ? (
              <Sun className="h-4 w-4" />
            ) : (
              <Moon className="h-4 w-4" />
            ))}
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
      </div>
    </header>
  )
}
