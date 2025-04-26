'use client'

import { ChevronLeft, ChevronRight } from 'lucide-react'
import { normalizePages } from 'nextra/normalize-pages'
import { usePathname } from 'next/navigation'
import type { PageMapItem } from 'nextra'
import Link from 'next/link'
import type { FC } from 'react'
import { useState, useEffect } from 'react'

interface PageItem {
  type: string
  name?: string
  route?: string
  title?: string
  children?: PageItem[]
  data?: Record<string, any>
  index?: number // Used for preserving original order
}

interface GroupedSection {
  title: string
  pages: PageItem[]
}

export const PageNavigation: FC<{ pageMap: PageMapItem[] }> = ({ pageMap }) => {
  const pathname = usePathname()
  const [prevPage, setPrevPage] = useState<{ route: string; title: string } | null>(null)
  const [nextPage, setNextPage] = useState<{ route: string; title: string } | null>(null)

  useEffect(() => {
    if (!pageMap || !pathname) return

    try {
      // Use normalizePages to get structured data from pageMap
      const { docsDirectories } = normalizePages({
        list: pageMap,
        route: pathname
      })

      // Find docs entry in the page map
      const docsEntry = docsDirectories.find(item => item.name === 'docs')
      if (!docsEntry) return

      // Get the current active section based on the first segment after /docs/
      const activeSegment = pathname.split('/').filter(Boolean)[1] || ''
      const activeSection = docsEntry.children?.find(item => item.name === activeSegment)

      if (!activeSection || !activeSection.children) return

      // Extract all pages with the same ordering logic used in the sidebar
      const orderedPages: PageItem[] = []
      const activeSectionChildren = activeSection.children as PageItem[]

      // Group pages by their section (same as sidebar.tsx)
      const groupedPages: Record<string, GroupedSection> = activeSectionChildren.reduce((acc: Record<string, GroupedSection>, item: PageItem, index: number) => {
        // Add index property to preserve the original order
        item.index = index

        if (item.type === 'separator' && item.name) {
          acc[item.name] = {
            title: item.title || item.name,
            pages: []
          }
        } else if (item.type === 'page') {
          const lastSeparator = [...activeSectionChildren].reverse().find(
            (s: PageItem) => s.type === 'separator' && activeSectionChildren.indexOf(s) < activeSectionChildren.indexOf(item)
          )
          if (lastSeparator && lastSeparator.name) {
            if (!acc[lastSeparator.name]) {
              acc[lastSeparator.name] = {
                title: lastSeparator.title || lastSeparator.name,
                pages: []
              }
            }
            acc[lastSeparator.name].pages.push(item)
          }
        }
        return acc
      }, {})

      // Process pages in order of sections
      Object.entries(groupedPages).forEach(([_, section]: [string, GroupedSection]) => {
        section.pages.forEach((page: PageItem) => {
          // Handle page with nested children (collapsible sections)
          if (page.children && page.children.length > 0) {
            // Add the parent page first
            if (page.route && page.title && !page.route.endsWith('/index') && !page.route.endsWith('/404')) {
              orderedPages.push(page)
            }

            // Process all children pages (same as renderPageLink in sidebar.tsx)
            page.children.forEach(child => {
              if (child.type === 'page' && child.route && !child.route.endsWith('/index') && !child.route.endsWith('/404')) {
                orderedPages.push(child)
              }

              // Handle data pages
              if (child.data) {
                Object.values(child.data).forEach(dataItem => {
                  if (dataItem.type === 'page' && dataItem.route && !dataItem.route.endsWith('/index') && !dataItem.route.endsWith('/404')) {
                    orderedPages.push(dataItem)
                  }
                })
              }
            })
          }
          // Simple page without children
          else if (page.route && page.title && !page.route.endsWith('/index') && !page.route.endsWith('/404')) {
            orderedPages.push(page)
          }
        })
      })

      // Special handling for carrier integrations section
      if (pathname.includes('/docs/carriers')) {
        // This is a simplified version since we don't have the full carrier data
        // It maintains the existing order of pages in the carriers section
      }

      // Remove duplicates while preserving order
      const uniquePages = orderedPages.filter((page, index, self) =>
        page.route && index === self.findIndex(p => p.route === page.route)
      )

      // Find current page index
      const currentPageIndex = uniquePages.findIndex(page => page.route === pathname)

      // Set previous and next pages
      if (currentPageIndex > 0) {
        const prev = uniquePages[currentPageIndex - 1]
        if (prev.route && prev.title) {
          setPrevPage({ route: prev.route, title: prev.title })
        } else {
          setPrevPage(null)
        }
      } else {
        setPrevPage(null)
      }

      if (currentPageIndex < uniquePages.length - 1 && currentPageIndex !== -1) {
        const next = uniquePages[currentPageIndex + 1]
        if (next.route && next.title) {
          setNextPage({ route: next.route, title: next.title })
        } else {
          setNextPage(null)
        }
      } else {
        setNextPage(null)
      }
    } catch (error) {
      console.error('Error in PageNavigation:', error)
    }
  }, [pageMap, pathname])

  // Skip rendering if neither previous nor next page exists
  if (!prevPage && !nextPage) return null

  return (
    <nav className="mt-12 mb-8 flex items-center justify-between pt-6 dark:border-neutral-800">
      {prevPage ? (
        <Link
          href={prevPage.route}
          className="group flex items-center gap-2 text-sm font-medium transition-colors text-muted-foreground hover:text-foreground dark:hover:text-white"
        >
          <ChevronLeft className="h-4 w-4 transition-colors group-hover:text-purple-600 dark:group-hover:text-purple-400" />
          <div className="flex flex-col">
            {/* <span className="text-xs text-muted-foreground">Previous</span> */}
            <span className="group-hover:text-purple-600 dark:group-hover:text-purple-400">{prevPage.title}</span>
          </div>
        </Link>
      ) : (
        // Empty div for spacing when no previous page
        <div></div>
      )}

      {nextPage && (
        <Link
          href={nextPage.route}
          className="group flex items-center gap-2 text-sm font-medium transition-colors text-muted-foreground hover:text-foreground dark:hover:text-white ml-auto"
        >
          <div className="flex flex-col items-end">
            {/* <span className="text-xs text-muted-foreground">Next</span> */}
            <span className="group-hover:text-purple-600 dark:group-hover:text-purple-400">{nextPage.title}</span>
          </div>
          <ChevronRight className="h-4 w-4 transition-colors group-hover:text-purple-600 dark:group-hover:text-purple-400" />
        </Link>
      )}
    </nav>
  )
}

