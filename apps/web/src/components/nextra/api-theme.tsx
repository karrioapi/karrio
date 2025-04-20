"use client"

import { Button } from '@karrio/ui/components/ui/button'
import { normalizePages } from 'nextra/normalize-pages'
import { usePathname } from 'next/navigation'
import { ThemeProvider } from 'next-themes'
import { useState, useEffect } from 'react'
import type { FC, ReactNode } from 'react'
import type { PageMapItem } from 'nextra'
import { Moon, Sun } from 'lucide-react'
import { useTheme } from 'next-themes'
import Link from 'next/link'
import clsx from 'clsx'

interface ApiHeaderProps {
  logo?: string
  darkLogo?: string
  pageMap: PageMapItem[]
}

const ApiHeader: FC<ApiHeaderProps> = ({ logo = "/karrio-docs.svg", darkLogo = "/karrio-docs-light.svg", pageMap }) => {
  const { theme, setTheme } = useTheme()
  const pathname = usePathname()
  const [mounted, setMounted] = useState(false)

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
    <header className={`flex h-14 w-full shrink-0 items-center border-b border-gray-200 bg-background ${mounted && theme === 'dark' ? '!bg-neutral-950 !border-neutral-800' : ''}`}>
      {/* Mobile Header */}
      <div className="flex h-full items-center justify-between px-4 md:hidden w-full">
        <Link href="/docs" className="flex items-center">
          {mounted && (theme === 'dark' ? (
            <img src={darkLogo} alt="Karrio Docs" className="h-5 w-auto" />
          ) : (
            <img src={logo} alt="Karrio Docs" className="h-5 w-auto" />
          ))}
        </Link>
      </div>

      {/* Desktop Header */}
      <div className="hidden md:flex h-full items-center w-full pr-4">
        {/* Logo section - fixed width matching sidebar */}
        <div className="w-64 pr-4 pl-12 py-4 flex items-center h-full">
          <Link href="/docs" className="flex items-center">
            {mounted && (theme === 'dark' ? (
              <img src={darkLogo} alt="Karrio Docs" className="h-5 w-auto" />
            ) : (
              <img src={logo} alt="Karrio Docs" className="h-5 w-auto" />
            ))}
          </Link>
        </div>

        {/* Navigation section - starts after sidebar width */}
        <nav className="flex h-full items-center gap-6 px-12">
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
    </header>
  )
}

export const ApiTheme: FC<{
  children: ReactNode
  pageMap: PageMapItem[]
  logo?: string
  darkLogo?: string
}> = ({ children, pageMap, logo, darkLogo }) => {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      storageKey="karrio-docs-theme"
      enableColorScheme
      disableTransitionOnChange
      themes={['light', 'dark']}
    >
      <div className="flex min-h-screen w-full docs-container overflow-hidden dark:bg-neutral-950 dark:text-white">
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Fixed header - full width */}
          <div className="fixed top-0 z-40 w-full bg-background dark:bg-neutral-950">
            <ApiHeader logo={logo} darkLogo={darkLogo} pageMap={pageMap} />
          </div>

          {/* Main content with padding to account for fixed header */}
          <div className="flex-1 overflow-y-auto pt-12 w-full">
            <div className="flex flex-col gap-4 docs-content dark:bg-neutral-950 w-full">
              <div className="w-full">
                <div className="flex flex-col">
                  {/* Main content - full width */}
                  <div className="flex-1 w-full prose prose-h1:text-2xl prose-h1:font-semibold prose-h1:mb-6 prose-h2:text-xl prose-h2:font-semibold prose-h2:mt-10 prose-h2:mb-4 prose-h3:text-lg prose-h3:font-medium prose-h3:mt-8 prose-h3:mb-3 prose-p:text-sm prose-p:leading-6 prose-li:text-sm prose-li:leading-6 dark:prose-invert prose-headings:tracking-tight prose-a:text-purple-600 dark:prose-a:text-purple-400 prose-a:no-underline hover:prose-a:text-purple-700 dark:hover:prose-a:text-purple-300 prose-img:rounded-lg prose-img:max-w-full prose-code:text-gray-800 dark:prose-code:text-gray-200 prose-pre:bg-gray-50 dark:prose-pre:bg-neutral-900 prose-pre:border prose-pre:border-gray-200 dark:prose-pre:border-neutral-800 prose-pre:rounded-lg prose-pre:overflow-x-auto docs-prose">
                    {children}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ThemeProvider>
  )
}
