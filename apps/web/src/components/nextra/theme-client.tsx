"use client"
import { SidebarProvider, SidebarInset } from '@karrio/ui/components/ui/sidebar'
import { PageNavigation } from '@/components/nextra/page-navigation'
import { FloatingBanner } from '@/components/nextra/floating-banner'
import { Sidebar } from '@/components/nextra/sidebar'
import { Header } from '@/components/nextra/header'
import { Footer } from '@/components/nextra/footer'
import RootProvider from '@/hooks/root-provider'
import { TOC } from '@/components/nextra/toc'
import { ThemeConfig } from '@/types/theme'
import type { FC, ReactNode } from 'react'
import type { PageMapItem } from 'nextra'

// Client component that handles the UI
export const NextraThemeClient: FC<{
  children: ReactNode
  pageMap: PageMapItem[]
  themeConfig: ThemeConfig
}> = ({
  children,
  pageMap,
  themeConfig
}) => {
    console.log('NextraThemeClient: Received themeConfig:', themeConfig)

    // Apply theme configuration defaults
    const {
      breadcrumb = true,
      footer = true,
      layout = 'default',
      navbar = true,
      pagination = true,
      sidebar = true,
      timestamp = true,
      toc = true,
      typesetting = 'default'
    } = themeConfig

    // Determine what to hide
    const shouldHideSidebar = !sidebar
    const shouldHideTOC = !toc

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
            {/* Only show sidebar if not hidden */}
            {!shouldHideSidebar && (
              <Sidebar pageMap={pageMap} themeConfig={themeConfig} />
            )}

            <SidebarInset className={`flex-1 flex flex-col overflow-hidden`}>
              {/* Fixed header - responsive width - hide if navbar is false */}
              {navbar && (
                <div className={`fixed top-0 z-40 ${shouldHideSidebar ? 'w-full' : 'w-full md:w-[calc(100%-16rem)]'} bg-background`}>
                  <Header pageMap={pageMap} />
                </div>
              )}

              {/* Main content with padding to account for fixed header */}
              <div className={`flex-1 overflow-y-auto ${navbar ? 'pt-20' : 'pt-0'} bg-background w-full`}>
                <div className="flex flex-col gap-4 docs-content w-full">
                  <div className="w-full mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl min-h-[100vh]">
                    <div className="flex flex-col xl:flex-row xl:gap-10">
                      {/* Main content */}
                      <div className="flex-1 min-w-0 w-full prose prose-h1:text-2xl prose-h1:font-semibold prose-h1:mb-6 prose-h2:text-xl prose-h2:font-semibold prose-h2:mt-10 prose-h2:mb-4 prose-h3:text-lg prose-h3:font-medium prose-h3:mt-8 prose-h3:mb-3 prose-p:text-sm prose-p:leading-6 prose-li:text-sm prose-li:leading-6 dark:prose-invert prose-headings:tracking-tight prose-a:text-purple-600 dark:prose-a:text-purple-400 prose-a:no-underline hover:prose-a:text-purple-700 dark:hover:prose-a:text-purple-300 prose-img:rounded-lg prose-img:max-w-full prose-code:text-gray-800 dark:prose-code:text-gray-200 prose-pre:bg-gray-50 dark:prose-pre:bg-[#0f0c24] prose-pre:border prose-pre:border-gray-200 dark:prose-pre:border-neutral-800 prose-pre:rounded-lg prose-pre:overflow-x-auto docs-prose">
                        {children}

                        {/* Add page navigation component before the footer if pagination is enabled */}
                        {pagination && <PageNavigation pageMap={pageMap} />}
                      </div>

                      {/* Fixed TOC - only on xl screens and if not hidden */}
                      {!shouldHideTOC && (
                        <div className="hidden xl:block xl:w-72 relative">
                          <div className="fixed w-72">
                            <div className="pt-6 pb-16">
                              <TOC toc={[]} />
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Footer - show if footer theme option is true */}
                  {footer && <Footer />}
                </div>
              </div>
            </SidebarInset>
          </SidebarProvider>
        </div>
      </RootProvider>
    )
  }
