import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import { NextPostHogProvider } from "@karrio/hooks/posthog";
import { Toaster } from "@karrio/ui/components/ui/toaster";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import RootProvider from "@/hooks/root-provider";
import type { Metadata } from 'next';
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "Karrio Blog",
  description: "Latest news, updates, and articles about Karrio",
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

export default function BlogLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning
      className={`${inter.variable} ${jetbrains.variable} ${noto.variable} ${ubuntu.variable} ${oxygen.variable} h-full scroll-smooth`}>
      <body className="blog-page" style={{ margin: 0 }}>
        <NextPostHogProvider>
          <RootProvider
            defaultTheme="system"
            disableTransitionOnChange
            sectionKey="content"
          >
            <div className="min-h-screen bg-background antialiased">
              <SiteHeader />

              <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
                <main className="flex-1 mx-auto max-w-3xl">{children}</main>
              </div>

              <SiteFooter />
            </div>
            <Toaster />
          </RootProvider>
        </NextPostHogProvider>
        <img referrerPolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=a16a9706-d13e-4fbc-91ef-c313c2fcec3f" />
      </body>
    </html>
  );
}
