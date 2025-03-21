"use client"

import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '@karrio/ui/components/ui/breadcrumb'
import { SidebarTrigger } from '@karrio/ui/components/ui/sidebar'
import { Separator } from '@karrio/ui/components/ui/separator'
import { normalizePages } from 'nextra/normalize-pages'
import { usePathname } from 'next/navigation'
import type { PageMapItem } from 'nextra'
import { type FC } from 'react'
import { useTheme } from 'next-themes'
import { useState, useEffect } from 'react'

export interface HeaderProps {
  pageMap: PageMapItem[]
}

export const Header: FC<HeaderProps> = ({ pageMap }) => {
  const pathname = usePathname()
  const { theme } = useTheme()
  const [mounted, setMounted] = useState(false)

  // After mounting, we can check theme
  useEffect(() => {
    setMounted(true)
  }, [])

  // Use normalizePages to extract structured data from pageMap based on current path
  const { activePath } = normalizePages({
    list: pageMap,
    route: pathname
  })

  // Build breadcrumb items based on active path
  const breadcrumbItems = activePath
    .filter(segment => !!segment.name) // Filter out segments with empty names
    .filter(segment => segment.name !== 'docs') // Skip the "docs" segment
    .map((segment, index, segments) => {
      const isLast = index === segments.length - 1

      // Only render link if it's not the last item
      return isLast ? (
        <BreadcrumbItem key={segment.route}>
          <BreadcrumbPage className={`text-xs font-medium text-gray-700 ${mounted && theme === 'dark' ? '!text-gray-300' : ''}`}>
            {segment.title}
          </BreadcrumbPage>
        </BreadcrumbItem>
      ) : (
        <BreadcrumbItem key={segment.route} className="hidden sm:inline-flex">
          <BreadcrumbLink
            href={segment.route}
            className={`text-xs font-medium text-gray-600 hover:text-gray-900 ${mounted && theme === 'dark' ? '!text-gray-400 hover:!text-gray-200' : ''}`}
          >
            {segment.title}
          </BreadcrumbLink>
          <BreadcrumbSeparator className={`mx-1 text-gray-400 ${mounted && theme === 'dark' ? '!text-gray-600' : ''}`} />
        </BreadcrumbItem>
      )
    })

  return (
    <header className={`flex h-12 w-full shrink-0 items-center gap-1 transition-[width,height] ease-linear border-b border-gray-200 bg-white ${mounted && theme === 'dark' ? '!bg-neutral-950 !border-neutral-800' : ''}`}>
      <div className="flex items-center gap-1 px-1.5 w-full">
        <SidebarTrigger className={`-ml-0.5 md:hidden ${mounted && theme === 'dark' ? '!text-gray-300' : 'text-gray-600'}`} />
        <Separator orientation="vertical" className={`mx-1 h-3.5 text-gray-300 md:hidden ${mounted && theme === 'dark' ? '!text-gray-700' : ''}`} />
        <Breadcrumb>
          <BreadcrumbList className="flex-wrap">
            {breadcrumbItems.length > 0 ? (
              breadcrumbItems
            ) : (
              <BreadcrumbItem>
                <BreadcrumbPage className={`text-xs font-medium text-gray-700 ${mounted && theme === 'dark' ? '!text-gray-300' : ''}`}>
                  Documentation
                </BreadcrumbPage>
              </BreadcrumbItem>
            )}
          </BreadcrumbList>
        </Breadcrumb>
      </div>
    </header>
  )
}
