import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import RootProvider from "@/hooks/root-provider";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Karrio",
  description: "Karrio",
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
};

export default function WebsiteLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en"
      suppressHydrationWarning
      className={`${inter.variable} ${jetbrains.variable} ${noto.variable} ${ubuntu.variable} ${oxygen.variable}`}>
      <head>
        <link
          rel="preconnect"
          href={`https://${process.env.NEXT_PUBLIC_ALGOLIA_APP_ID || ''}-dsn.algolia.net`}
          crossOrigin=""
        />
      </head>
      <body className="font-sans antialiased">
        <RootProvider
          defaultTheme="light"
          forcedTheme="light"
          disableTransitionOnChange
          sectionKey="marketing"
        >
          <div className="flex flex-col min-h-screen">
            {/* Header */}
            <SiteHeader />

            {/* Main Content */}
            <main className="flex-1">
              {children}
            </main>

            {/* Footer */}
            <SiteFooter />
          </div>
        </RootProvider>
      </body>
    </html>
  );
}
