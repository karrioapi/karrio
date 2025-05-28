"use client"
import { SidebarProvider, SidebarInset } from '@karrio/ui/components/ui/sidebar'
import { Sidebar } from '@/components/nextra/sidebar'
import { Header } from '@/components/nextra/header'
import { Footer } from '@/components/nextra/footer'
import { PageNavigation } from '@/components/nextra/page-navigation'
import RootProvider from '@/hooks/root-provider'
import { TOC } from '@/components/nextra/toc'
import type { FC, ReactNode } from 'react'
import type { PageMapItem } from 'nextra'
import Link from 'next/link'
import { useState, useEffect } from 'react'

const FloatingBanner = () => {
  const [isVisible, setIsVisible] = useState(true)
  const [lastScrollY, setLastScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY

      // Hide banner when scrolling down, show when scrolling up or at top
      if (currentScrollY > lastScrollY && currentScrollY > 50) {
        setIsVisible(false)
      } else {
        setIsVisible(true)
      }

      setLastScrollY(currentScrollY)
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [lastScrollY])

  return (
    <div
      className={`fixed top-16 left-1/2 transform -translate-x-1/2 z-50 transition-all duration-300 md:ml-32 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'
        }`}
    >
      <div className="bg-blue-50 dark:bg-blue-900/50 border border-blue-200 dark:border-blue-700 rounded-lg shadow-sm backdrop-blur-sm px-4 py-2 mx-4">
        <p className="text-xs text-blue-700 dark:text-blue-300 mb-0 whitespace-nowrap">
          📖 Looking for karrio's legacy docs? Visit our{' '}
          <Link
            href="https://docs.karrio.io"
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium underline hover:no-underline text-blue-700 dark:text-blue-300"
          >
            docs.karrio.io
          </Link>
        </p>
      </div>
    </div>
  )
}

export const NextraTheme: FC<{
  children: ReactNode
  pageMap: PageMapItem[]
  hideSidebar?: boolean
  hideTOC?: boolean
}> = ({ children, pageMap, hideSidebar = false, hideTOC = false }) => {
  return (
    <RootProvider
      defaultTheme="system"
      disableTransitionOnChange
      sectionKey="content"
    >
      <div className="flex min-h-screen w-full docs-container overflow-hidden bg-background dark:text-white">
        {/* Floating banner */}
        <FloatingBanner />

        <SidebarProvider>
          {/* Show sidebar on mobile or when hideSidebar is false */}
          <div className={`${hideSidebar ? 'md:hidden' : ''}`}>
            <Sidebar pageMap={pageMap} />
          </div>

          <SidebarInset className={`flex-1 flex flex-col overflow-hidden ${hideSidebar ? 'md:ml-0' : ''}`}>
            {/* Fixed header - responsive width */}
            <div className="fixed top-0 z-40 w-full md:w-[calc(100%-16rem)] bg-background">
              <Header pageMap={pageMap} />
            </div>

            {/* Main content with padding to account for fixed header */}
            <div className="flex-1 overflow-y-auto pt-20 bg-background w-full">
              <div className="flex flex-col gap-4 docs-content w-full">
                <div className="w-full mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl min-h-[100vh]">
                  <div className="flex flex-col xl:flex-row xl:gap-10">
                    {/* Main content */}
                    <div className="flex-1 min-w-0 w-full prose prose-h1:text-2xl prose-h1:font-semibold prose-h1:mb-6 prose-h2:text-xl prose-h2:font-semibold prose-h2:mt-10 prose-h2:mb-4 prose-h3:text-lg prose-h3:font-medium prose-h3:mt-8 prose-h3:mb-3 prose-p:text-sm prose-p:leading-6 prose-li:text-sm prose-li:leading-6 dark:prose-invert prose-headings:tracking-tight prose-a:text-purple-600 dark:prose-a:text-purple-400 prose-a:no-underline hover:prose-a:text-purple-700 dark:hover:prose-a:text-purple-300 prose-img:rounded-lg prose-img:max-w-full prose-code:text-gray-800 dark:prose-code:text-gray-200 prose-pre:bg-gray-50 dark:prose-pre:bg-[#0f0c24] prose-pre:border prose-pre:border-gray-200 dark:prose-pre:border-neutral-800 prose-pre:rounded-lg prose-pre:overflow-x-auto docs-prose">
                      {children}

                      {/* Add page navigation component before the footer */}
                      <PageNavigation pageMap={pageMap} />
                    </div>

                    {/* Fixed TOC - only on xl screens */}
                    {!hideTOC && (
                      <div className="hidden xl:block xl:w-72 relative">
                        <div className="fixed w-72">
                          <div className="pt-10 pb-18">
                            <TOC toc={[]} />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <Footer />
              </div>
            </div>
          </SidebarInset>
        </SidebarProvider>
      </div>
    </RootProvider>
  )
}
