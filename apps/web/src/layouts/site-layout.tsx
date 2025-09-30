import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import { NextPostHogProvider } from "@karrio/hooks/posthog";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { PublicEnvScript } from "next-runtime-env";
import RootProvider from "@/hooks/root-provider";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Karrio",
  description: "Karrio",
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
        <PublicEnvScript />
        <link
          rel="preconnect"
          href={`https://${process.env.NEXT_PUBLIC_ALGOLIA_APP_ID || ''}-dsn.algolia.net`}
          crossOrigin=""
        />
      </head>
      <body className="font-sans antialiased">
        <NextPostHogProvider>
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
        </NextPostHogProvider>
        <img referrerPolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=a16a9706-d13e-4fbc-91ef-c313c2fcec3f" />
      </body>
    </html>
  );
}
