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
      <body className="font-sans antialiased">
        <RootProvider defaultTheme="light">
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
