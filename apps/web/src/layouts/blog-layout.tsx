import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import { Toaster } from "@karrio/ui/components/ui/toaster";
import { SiteHeader } from "@/components/site-header";
import { Footer } from "@/components/nextra/footer";
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

            <div className="container mx-auto max-w-7xl px-4 py-10">
              <main className="flex-1 mx-auto max-w-3xl">{children}</main>
            </div>

            <Footer />
          </div>
          <Toaster />
        </RootProvider>
      </body>
    </html>
  );
}
