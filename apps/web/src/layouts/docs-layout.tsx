import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import { NextraTheme } from '@/components/nextra/theme'
import { getPageMap } from 'nextra/page-map'
import type { ReactNode } from 'react'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: "Karrio Docs",
  description: "Documentation for Karrio - the modern shipping infrastructure",
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
};

export default async function DocsLayout({ children }: { children: ReactNode }) {
  const pageMap = await getPageMap();

  return (
    <html lang="en" suppressHydrationWarning
      className={`${inter.variable} ${jetbrains.variable} ${noto.variable} ${ubuntu.variable} ${oxygen.variable} h-full scroll-smooth`}>
      <body className="docs-page bg-background" style={{ margin: 0 }}>
        <NextraTheme pageMap={pageMap}>
          {children}
        </NextraTheme>
      </body>
    </html>
  )
}
