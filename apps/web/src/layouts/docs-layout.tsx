import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import RootProvider from "@/hooks/root-provider";
import Script from "next/script";
import { Metadata } from "next";
import React from 'react';

export const metadata: Metadata = {
  title: "Karrio Docs",
  description: "Documentation for Karrio - the modern shipping infrastructure",
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
};

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning
      className={`${inter.variable} ${jetbrains.variable} ${noto.variable} ${ubuntu.variable} ${oxygen.variable} h-full scroll-smooth`}>
      <head>
        <Script id="mermaid-config" strategy="afterInteractive">
          {`
            // Configure mermaid to work with dark mode
            document.addEventListener('nextra-theme-change', function(e) {
              if (window.mermaid) {
                window.mermaid.initialize({
                  theme: document.documentElement.classList.contains('dark') ? 'dark' : 'default'
                });

                // Re-render any existing diagrams
                document.querySelectorAll('.mermaid-container').forEach(el => {
                  if (el.__mermaidData) {
                    window.mermaid.render('mermaid-' + Date.now(), el.__mermaidData)
                      .then(({ svg }) => { el.innerHTML = svg; });
                  }
                });
              }
            });
          `}
        </Script>
      </head>
      <body className="min-h-screen font-sans antialiased">
        <RootProvider>
          {children}
        </RootProvider>
      </body>
    </html>
  )
}
