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
import { ThemeProvider } from "next-themes";
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
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="min-h-screen bg-background antialiased">
            <SiteHeader />

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
