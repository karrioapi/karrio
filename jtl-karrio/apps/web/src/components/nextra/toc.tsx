"use client"

import clsx from 'clsx'
import { usePathname } from 'next/navigation'
import { useEffect, useRef, useState } from 'react'
import { ScrollArea } from '@karrio/ui/components/ui/scroll-area'
import { ExternalLink } from 'lucide-react'

interface TOCProps {
  toc: { title: string; url: string; level: number }[]
}

export const TOC: React.FC<TOCProps> = ({ toc: propsToc }) => {
  const [activeId, setActiveId] = useState<string>('')
  const headingElementsRef = useRef<{ id: string; top: number }[]>([])
  const [extractedToc, setExtractedToc] = useState<TOCProps['toc']>([])
  const pathname = usePathname()
  const tocRef = useRef<HTMLDivElement>(null)
  const [tocHeight, setTocHeight] = useState<string>('calc(100vh - 14rem)')

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

  // Adjust TOC height to prevent overlap with footer
  useEffect(() => {
    if (!tocRef.current) return;

    const footer = document.querySelector('footer');
    if (!footer) return;

    const handleScroll = () => {
      const footerRect = footer.getBoundingClientRect();
      const tocRect = tocRef.current?.getBoundingClientRect();

      if (!tocRect) return;

      // If footer is entering viewport
      if (footerRect.top < window.innerHeight) {
        // Calculate how much of the footer is visible
        const footerVisibleHeight = window.innerHeight - footerRect.top;
        // Add more padding (100px) to ensure the forum link doesn't overlap the footer
        setTocHeight(`calc(100vh - 14rem - ${footerVisibleHeight + 100}px)`);
      } else {
        // Reset to default height when footer is not visible
        setTocHeight('calc(100vh - 14rem)');
      }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

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
      <div className="sticky top-12 max-h-[calc(100vh-12rem)] pl-6" ref={tocRef}>
        <div className="mb-4 text-sm font-medium text-gray-900 dark:text-white toc-heading">On This Page</div>
        <div className="text-sm text-gray-500 dark:text-gray-400">No headings found</div>

        {/* GitHub Forum Link */}
        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-800">
          <a
            href="https://github.com/karrioapi/karrio/discussions"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-xs text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <span>Questions? Ask in the Forum</span>
            <ExternalLink className="h-3 w-3" />
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="sticky top-16 max-h-[calc(100vh-12rem)] w-full pl-6 flex flex-col" ref={tocRef}>
      <div className="mb-4 text-sm font-medium text-gray-900 dark:text-white toc-heading">On This Page</div>

      {/* Flex-grow ScrollArea to take available space */}
      <ScrollArea className="pr-4 flex-grow overflow-hidden" style={{ height: tocHeight }}>
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

      {/* GitHub Forum Link - Outside ScrollArea to stay fixed at bottom */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-800 bg-background z-10">
        <a
          href="https://github.com/karrioapi/karrio/discussions"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-xs text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200"
        >
          <span>Questions? Ask in the Forum</span>
          <ExternalLink className="h-3 w-3" />
        </a>
      </div>
    </div>
  )
}
