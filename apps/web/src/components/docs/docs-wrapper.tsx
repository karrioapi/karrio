'use client'

import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList } from '@karrio/ui/components/ui/breadcrumb'
import { PageNavigation } from '@/components/nextra/page-navigation'
import { usePathname } from 'next/navigation'
import { normalizePages } from 'nextra/normalize-pages'
import Link from 'next/link'

export const DocsWrapper = ({ children, pageMap }) => {
  const pathname = usePathname()

  // Use normalizePages to extract structured data from pageMap based on current path
  const { activePath } = normalizePages({
    list: pageMap,
    route: pathname
  })

  // Get the parent breadcrumb (one level up)
  const parentCrumb = activePath
    .filter(segment => !!segment.name)
    .filter(segment => segment.name !== 'docs')
    .slice(-2, -1)[0]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="prose prose-lg dark:prose-invert mx-auto max-w-4xl">
        {parentCrumb && (
          <Breadcrumb className="mb-4">
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink
                  href={parentCrumb.route}
                  className="text-sm font-medium text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  {parentCrumb.title}
                </BreadcrumbLink>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        )}
        {children}

        {/* Add page navigation */}
        <PageNavigation pageMap={pageMap} />
      </div>
    </div>
  )
}
