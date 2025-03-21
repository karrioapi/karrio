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
import { Head } from 'nextra/components'
import type { Metadata } from 'next'
import Script from 'next/script'

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
      <Head faviconGlyph="✦" />
      <Script id="theme-script" strategy="beforeInteractive">{`
        (function() {
          try {
            let theme = localStorage.getItem('karrio-docs-theme');
            if (!theme) theme = 'system';

            const isDark =
              theme === 'dark' ||
              (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

            if (isDark) {
              document.documentElement.classList.add('dark');
              document.body.classList.add('dark');
              document.documentElement.classList.add('docs-dark');
              document.body.classList.add('docs-dark');
            }
          } catch (e) {
            // Fall back to light theme if localStorage is not available
          }
        })();
      `}</Script>
      <Script id="theme-observer" strategy="afterInteractive">{`
        (function() {
          function syncDarkClass() {
            const htmlHasDark = document.documentElement.classList.contains('dark');
            const bodyHasDark = document.body.classList.contains('dark');
            const htmlHasDocsDark = document.documentElement.classList.contains('docs-dark');
            const bodyHasDocsDark = document.body.classList.contains('docs-dark');

            if (htmlHasDark && !bodyHasDark) {
              document.body.classList.add('dark');
              if (!bodyHasDocsDark) document.body.classList.add('docs-dark');
            } else if (!htmlHasDark && bodyHasDark) {
              document.body.classList.remove('dark');
              if (bodyHasDocsDark) document.body.classList.remove('docs-dark');
            }

            if (htmlHasDocsDark && !bodyHasDocsDark) {
              document.body.classList.add('docs-dark');
            } else if (!htmlHasDocsDark && bodyHasDocsDark) {
              document.body.classList.remove('docs-dark');
            }
          }

          // Add observer for theme changes
          const observer = new MutationObserver(syncDarkClass);
          observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class']
          });

          // Initial sync on page load
          document.addEventListener('DOMContentLoaded', syncDarkClass);
        })();
      `}</Script>
      <body className="docs-page" style={{ margin: 0 }}>
        <NextraTheme pageMap={pageMap}>
          {children}
        </NextraTheme>
      </body>
    </html>
  )
}
