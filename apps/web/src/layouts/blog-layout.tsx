import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
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
      <body className="blog-page" style={{ margin: 0 }}>
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
      </body>
    </html>
  );
}
