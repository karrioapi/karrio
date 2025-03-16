"use client"
import { SidebarProvider, SidebarInset } from '@karrio/ui/components/ui/sidebar'
import { Sidebar } from '@/components/nextra/sidebar'
import { Header } from '@/components/nextra/header'
import { Footer } from '@/components/nextra/footer'
import { TOC } from '@/components/nextra/toc'
import { ThemeProvider } from 'next-themes'
import type { FC, ReactNode } from 'react'
import type { PageMapItem } from 'nextra'

export const NextraTheme: FC<{
  children: ReactNode
  pageMap: PageMapItem[]
}> = ({ children, pageMap }) => {
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
      <div className="flex min-h-screen w-full docs-container dark:bg-neutral-950 dark:text-white">
        <SidebarProvider>
          <Sidebar pageMap={pageMap} />

          <SidebarInset className="flex-1 overflow-hidden">
            <Header pageMap={pageMap} />

            <div className="flex flex-col gap-4 p-4 pt-0 docs-content dark:bg-neutral-950 w-full overflow-auto">
              <div className="w-full max-w-full py-8 px-4 md:px-6 lg:px-8">
                <div className="flex flex-col xl:flex-row xl:gap-10">
                  <div className="flex-1 mx-auto min-w-0 max-w-full prose prose-h1:text-2xl prose-h1:font-semibold prose-h1:mb-6 prose-h2:text-xl prose-h2:font-semibold prose-h2:mt-10 prose-h2:mb-4 prose-h3:text-lg prose-h3:font-medium prose-h3:mt-8 prose-h3:mb-3 prose-p:text-sm prose-p:leading-6 prose-li:text-sm prose-li:leading-6 dark:prose-invert prose-headings:tracking-tight prose-a:text-purple-600 dark:prose-a:text-purple-400 prose-a:no-underline hover:prose-a:text-purple-700 dark:hover:prose-a:text-purple-300 prose-img:rounded-lg prose-code:text-gray-800 dark:prose-code:text-gray-200 prose-pre:bg-gray-50 dark:prose-pre:bg-neutral-900 prose-pre:border prose-pre:border-gray-200 dark:prose-pre:border-neutral-800 prose-pre:rounded-lg docs-prose">
                    {children}
                  </div>

                  <div className="hidden xl:block xl:w-72 xl:flex-none">
                    <TOC toc={[]} />
                  </div>
                </div>
              </div>

              <Footer />
            </div>
          </SidebarInset>
        </SidebarProvider>
      </div>
    </ThemeProvider>
  )
}
