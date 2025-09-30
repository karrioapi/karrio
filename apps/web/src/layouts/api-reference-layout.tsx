import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import { NextPostHogProvider } from "@karrio/hooks/posthog";
import { ApiTheme } from '@/components/nextra/api-theme';
import { PublicEnvScript } from "next-runtime-env";
import { getPageMap } from 'nextra/page-map';
import type { ReactNode } from 'react';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: "Karrio API Reference",
  description: "API Reference for Karrio - the modern shipping infrastructure",
  icons: {
    icon: [
      { url: "/favicon.ico", media: "(prefers-color-scheme: light)" },
      { url: "/favicon-dark.ico", media: "(prefers-color-scheme: dark)" }
    ],
    shortcut: [
      { url: "/favicon-16x16.png", media: "(prefers-color-scheme: light)" },
      { url: "/favicon-dark-16x16.png", media: "(prefers-color-scheme: dark)" }
    ],
    apple: [
      { url: "/apple-touch-icon.png", media: "(prefers-color-scheme: light)" },
      { url: "/apple-touch-dark-icon.png", media: "(prefers-color-scheme: dark)" }
    ],
  },
};

export default async function DocsLayout({ children }: { children: ReactNode }) {
  const pageMap = await getPageMap();

  return (
    <html lang="en" suppressHydrationWarning
      className={`${inter.variable} ${jetbrains.variable} ${noto.variable} ${ubuntu.variable} ${oxygen.variable} h-full scroll-smooth`}>
      <head>
        <PublicEnvScript />
        <script async src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
        <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css" />
      </head>
      <body className="docs-page" style={{ margin: 0 }}>
        <NextPostHogProvider>
          <ApiTheme
            pageMap={pageMap}
            logo="/karrio-docs.svg"
            darkLogo="/karrio-docs-light.svg"
          >
            {children}
          </ApiTheme>
        </NextPostHogProvider>
        <img referrerPolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=a16a9706-d13e-4fbc-91ef-c313c2fcec3f" />
      </body>
    </html>
  )
}
