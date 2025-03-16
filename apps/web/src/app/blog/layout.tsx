import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import { BlogHeader } from "@/components/blog/blog-header";
import { Toaster } from "@karrio/ui/components/ui/toaster";
import { Footer } from "@/components/nextra/footer";
import { ThemeProvider } from "next-themes";
import { Head } from 'nextra/components';
import type { Metadata } from 'next';
import Script from 'next/script';
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "Karrio Blog",
  description: "Latest news, updates, and articles about Karrio",
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
};

export default function BlogLayout({
  children,
}: {
  children: React.ReactNode;
}) {
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
      <body className="docs-page blog-page" style={{ margin: 0 }}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="min-h-screen bg-background dark:bg-[#0f0826] antialiased">
            <BlogHeader />

            <div className="container mx-auto max-w-7xl px-4 py-10">
              <main className="flex-1 mx-auto max-w-3xl">{children}</main>
            </div>

            <Footer />
          </div>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
