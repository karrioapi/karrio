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
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
};

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en"
      data-theme="dark"
      suppressHydrationWarning
      className={`${inter.variable} ${jetbrains.variable} ${noto.variable} ${ubuntu.variable} ${oxygen.variable}`}>
      <body className="min-h-screen font-sans antialiased">
        <RootProvider>
          <div className="min-h-screen bg-[#0f0826] text-white overflow-x-hidden">
            {/* Header */}
            <SiteHeader />

            {/* Platform Subnav */}
            <PlatformSubnav />

            {/* Main Content */}
            <main>
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
