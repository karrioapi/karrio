import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import { ApiTheme } from '@/components/nextra/api-theme'
import { getPageMap } from 'nextra/page-map'
import type { ReactNode } from 'react'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: "Karrio API Reference",
  description: "API Reference for Karrio - the modern shipping infrastructure",
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
      <head>
        <script async src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
        <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css" />
      </head>
      <body className="docs-page" style={{ margin: 0 }}>
        <ApiTheme
          pageMap={pageMap}
          logo="/karrio-docs.svg"
          darkLogo="/karrio-docs-light.svg"
        >
          {children}
        </ApiTheme>
      </body>
    </html>
  )
}
