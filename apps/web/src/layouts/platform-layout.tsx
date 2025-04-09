import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import { PlatformSubnav } from "@/components/platform-subnav";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import RootProvider from "@/hooks/root-provider";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Karrio Platform",
  description: "Karrio Platform",
  icons: {
    icon: "/favicon-dark.ico",
    shortcut: "/favicon-dark-16x16.png",
    apple: "/apple-touch-dark-icon.png",
  },
};

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en"
      suppressHydrationWarning
      className={`${inter.variable} ${jetbrains.variable} ${noto.variable} ${ubuntu.variable} ${oxygen.variable}`}>
      <body className="font-sans antialiased">
        <RootProvider
          defaultTheme="dark"
          forcedTheme="dark"
          disableTransitionOnChange
          sectionKey="platform"
        >
          <div className="flex flex-col min-h-screen bg-background dark:text-white">
            {/* Header */}
            <SiteHeader />

            {/* Platform Subnav */}
            <PlatformSubnav />

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
