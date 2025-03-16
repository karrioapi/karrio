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

export default function WebsiteLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en"
      data-theme="light"
      suppressHydrationWarning
      className={`${inter.variable} ${jetbrains.variable} ${noto.variable} ${ubuntu.variable} ${oxygen.variable}`}>
      <body className="min-h-screen font-sans antialiased">
        <RootProvider defaultTheme="light">
          <div className="min-h-screen overflow-x-hidden">
            {/* Header */}
            <SiteHeader />

            {/* Main Content */}
            <main>{children}</main>

            {/* Footer */}
            <SiteFooter />
          </div>
        </RootProvider>
      </body>
    </html>
  );
}
