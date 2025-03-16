"use client"

import type { Heading } from 'nextra'
import type { FC } from 'react'
import clsx from 'clsx'
import { usePathname } from 'next/navigation'
import { useEffect, useRef, useState } from 'react'
import { ScrollArea } from '@karrio/ui/components/ui/scroll-area'

interface TOCProps {
  toc: { title: string; url: string; level: number }[]
}

export const TOC: React.FC<TOCProps> = ({ toc: propsToc }) => {
  const [activeId, setActiveId] = useState<string>('')
  const headingElementsRef = useRef<{ id: string; top: number }[]>([])
  const [extractedToc, setExtractedToc] = useState<TOCProps['toc']>([])
  const pathname = usePathname()

  // Extract headings from the document if no TOC data is provided
  useEffect(() => {
    // Use a small delay to ensure DOM is fully loaded
    const extractHeadings = () => {
      if (propsToc && propsToc.length > 0) {
        setExtractedToc(propsToc);
        return;
      }

      // Target all heading elements within the main content area for better specificity
      const contentArea = document.querySelector('.docs-prose');
      const headingElements = contentArea
        ? Array.from(contentArea.querySelectorAll('h2, h3, h4, h5, h6'))
        : Array.from(document.querySelectorAll('h2, h3, h4, h5, h6'));

      const extractedHeadings = headingElements
        .filter(element => element.id || element.textContent)
        .map(element => {
          // If element doesn't have an ID but has text content, create an ID
          if (!element.id && element.textContent) {
            const generatedId = element.textContent
              .toLowerCase()
              .replace(/[^\w\s-]/g, '')
              .replace(/\s+/g, '-');
            element.id = generatedId;
          }

          return {
            title: element.textContent || '',
            url: `#${element.id}`,
            level: parseInt(element.tagName.charAt(1), 10)
          };
        });

      setExtractedToc(extractedHeadings);
    };

    // Small timeout to ensure DOM is fully rendered
    const timer = setTimeout(extractHeadings, 100);
    return () => clearTimeout(timer);
  }, [propsToc, pathname]); // Re-extract when pathname changes

  const toc = extractedToc;

  useEffect(() => {
    if (toc.length === 0) return

    const updateHeadingPositions = () => {
      const headingElements = Array.from(document.querySelectorAll('h2, h3, h4, h5, h6'))
        .filter(element => element.id)
        .map(element => ({
          id: element.id,
          top: element.getBoundingClientRect().top + window.scrollY - 100
        }))

      headingElementsRef.current = headingElements
    }

    updateHeadingPositions()

    const onScroll = () => {
      const scrollPosition = window.scrollY
      const selected = headingElementsRef.current.find((heading, idx) => {
        return (
          heading.top > scrollPosition &&
          (idx === headingElementsRef.current.length - 1 || headingElementsRef.current[idx + 1].top > scrollPosition)
        )
      })
      if (selected) {
        setActiveId(selected.id)
      }
    }

    onScroll()
    window.addEventListener('scroll', onScroll)
    window.addEventListener('resize', updateHeadingPositions)

    return () => {
      window.removeEventListener('scroll', onScroll)
      window.removeEventListener('resize', updateHeadingPositions)
    }
  }, [toc])

  if (toc.length === 0) {
    return (
      <div className="sticky top-16 max-h-[calc(100vh-4rem)] pl-6">
        <div className="mb-4 text-sm font-medium text-gray-900 dark:text-white toc-heading">On This Page</div>
        <div className="text-sm text-gray-500 dark:text-gray-400">No headings found</div>
      </div>
    )
  }

  return (
    <div className="sticky top-16 max-h-[calc(100vh-4rem)] w-full pl-6">
      <div className="mb-4 text-sm font-medium text-gray-900 dark:text-white toc-heading">On This Page</div>
      <ScrollArea className="h-[calc(100vh-8rem)]">
        <ul className="space-y-2">
          {toc.map(heading => {
            const paddingLeft = heading.level === 2 ? 0 : (heading.level - 2) * 16
            const fontSize = heading.level === 2 ? 'text-sm' :
              heading.level === 3 ? 'text-sm' : 'text-xs'

            return (
              <li
                key={heading.url || `heading-${heading.title}`}
                style={{ paddingLeft: `${paddingLeft}px` }}
                className="transition-colors relative"
              >
                {heading.level > 2 && (
                  <span
                    className="absolute left-0 top-1/2 w-2 h-0 border-t border-gray-300 dark:border-gray-600"
                    style={{ transform: 'translateY(-50%)' }}
                  />
                )}
                <a
                  href={heading.url || '#'}
                  className={clsx(
                    `inline-block py-1 ${fontSize} toc-item`,
                    heading.url && activeId === heading.url.slice(1)
                      ? "active font-medium text-gray-900 dark:text-purple-400"
                      : `text-gray-${heading.level > 3 ? '500' : '600'} hover:text-gray-900 dark:text-gray-${heading.level > 3 ? '500' : '400'} dark:hover:text-gray-200`
                  )}
                  onClick={e => {
                    e.preventDefault()
                    if (heading.url) {
                      const element = document.getElementById(heading.url.slice(1))
                      if (element) {
                        const yOffset = -100  // Adjust scroll position to account for navbar
                        const y = element.getBoundingClientRect().top + window.scrollY + yOffset
                        window.scrollTo({ top: y, behavior: 'smooth' })
                        setActiveId(heading.url.slice(1))
                      }
                    }
                  }}
                >
                  {heading.title}
                </a>
              </li>
            )
          })}
        </ul>
      </ScrollArea>
    </div>
  )
}
