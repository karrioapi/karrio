'use client'

import { Monitor, FileText, GitFork, Database, ArrowUpCircle, Container, BookOpen, Zap, Home, Github } from 'lucide-react'
import { normalizePages } from 'nextra/normalize-pages'
import { useState, useRef, useEffect } from 'react'
import { usePathname } from 'next/navigation'
import type { PageMapItem } from 'nextra'
import { useTheme } from 'next-themes'
import type { FC } from 'react'
import Link from 'next/link'
import clsx from 'clsx'

// Import shadcn sidebar components
import {
  Sidebar as ShadcnSidebar,
  SidebarContent,
  SidebarHeader,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarFooter,
} from '@karrio/ui/components/ui/sidebar'

export const Sidebar: FC<{ pageMap: PageMapItem[] }> = ({ pageMap }) => {
  const pathname = usePathname()
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  // After mounting, initialize component
  useEffect(() => {
    setMounted(true)
  }, []);

  const { docsDirectories } = normalizePages({
    list: pageMap,
    route: pathname
  })

  // Find docs entry in the page map
  const docsEntry = docsDirectories.find(item => item.name === 'docs')
  const docsChildren = docsEntry?.children || []

  // Get the current active section based on the first segment after /docs/
  const activeSegment = pathname.split('/').filter(Boolean)[1] || ''
  const activeSection = docsChildren.find(item => item.name === activeSegment)
  const activeSectionChildren = activeSection?.children || []

  // Get icon for a specific page
  const getIcon = (name: string) => {
    switch (name.toLowerCase()) {
      case 'introduction':
        return <Monitor className="h-4 w-4" />
      case 'local development':
        return <FileText className="h-4 w-4" />
      case 'oss contribution':
        return <GitFork className="h-4 w-4" />
      case 'installation':
        return <FileText className="h-4 w-4" />
      case 'database migrations':
        return <Database className="h-4 w-4" />
      case 'upgrade':
        return <ArrowUpCircle className="h-4 w-4" />
      case 'docker':
        return <Container className="h-4 w-4" />
      case 'guides':
        return <BookOpen className="h-4 w-4" />
      case 'quickstart':
        return <Zap className="h-4 w-4" />
      default:
        return <FileText className="h-4 w-4" />
    }
  }

  // Group pages by their section
  const groupedPages = activeSectionChildren.reduce((acc: any, item: any) => {
    if (item.type === 'separator') {
      acc[item.name] = {
        title: item.title,
        pages: []
      }
    } else if (item.type === 'page') {
      const lastSeparator = [...activeSectionChildren].reverse().find(
        (s: any) => s.type === 'separator' && activeSectionChildren.indexOf(s) < activeSectionChildren.indexOf(item)
      )
      if (lastSeparator) {
        if (!acc[lastSeparator.name]) {
          acc[lastSeparator.name] = {
            title: lastSeparator.title,
            pages: []
          }
        }
        acc[lastSeparator.name].pages.push(item)
      }
    }
    return acc
  }, {})

  return (
    <ShadcnSidebar className="sidebar border-r border-gray-200 dark:border-neutral-800 bg-background shrink-0">
      <SidebarHeader className="px-5 py-4">
        {/* Desktop Header */}
        <div className="hidden md:block">
          <SidebarMenu>
            <SidebarMenuItem>
              <div className="flex items-center justify-between w-full">
                <Link href="/docs" className="flex items-center">
                  {mounted && (theme === 'dark' ? (
                    <img src="/karrio-docs-light.svg" alt="Karrio Docs" className="h-5 w-auto" />
                  ) : (
                    <img src="/karrio-docs.svg" alt="Karrio Docs" className="h-5 w-auto" />
                  ))}
                </Link>
              </div>
            </SidebarMenuItem>
          </SidebarMenu>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden">
          <div className="space-y-1">
            {docsChildren.map((section) => (
              section.type === 'separator' && (
                <Link
                  key={section.name}
                  href={`/docs/${section.name}`}
                  className={clsx(
                    "flex items-center gap-2 py-1.5 text-sm font-semibold transition-colors",
                    pathname.startsWith(`/docs/${section.name}`)
                      ? "text-purple-600 dark:text-purple-400"
                      : "text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-gray-100"
                  )}
                >
                  <BookOpen className="h-3.5 w-3.5" />
                  <span>{section.title}</span>
                </Link>
              )
            ))}
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent className="px-4 py-6">
        {Object.entries(groupedPages).map(([key, section]: [string, any]) => (
          <div key={key} className="mt-4 first:mt-0">
            <h4 className="px-2 mb-2 text-sm font-semibold text-gray-900 dark:text-gray-100">
              {section.title}
            </h4>
            <div className="space-y-1 pl-2">
              {section.pages.map((page: any) => (
                <Link
                  key={page.route}
                  href={page.route}
                  className={clsx(
                    "flex items-center gap-2 px-2 py-1.5 text-sm transition-colors relative",
                    pathname === page.route
                      ? "text-purple-600 dark:text-purple-400 before:absolute before:left-0 before:top-1 before:bottom-1 before:w-0.5 before:bg-purple-600 dark:before:bg-purple-400 before:rounded-full font-medium"
                      : "text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-gray-100"
                  )}
                >
                  {getIcon(page.title)}
                  <span>{page.title}</span>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </SidebarContent>

      <SidebarFooter className="border-t py-3 px-2 border-gray-200 dark:border-neutral-800">
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <Link
                  href="/"
                  className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-muted sidebar-item relative"
                >
                  <Home className="h-3.5 w-3.5" />
                  <span>Website</span>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link
                  href="/blog"
                  className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-muted sidebar-item relative"
                >
                  <FileText className="h-3.5 w-3.5" />
                  <span>Blog</span>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <a
                  href="https://github.com/karrioapi/karrio"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-muted sidebar-item relative"
                >
                  <Github className="h-3.5 w-3.5" />
                  <span>GitHub</span>
                </a>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarFooter>
    </ShadcnSidebar>
  )
}
