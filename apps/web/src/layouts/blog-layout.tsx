import {
  inter,
  jetbrains,
  noto,
  ubuntu,
  oxygen,
} from "@karrio/ui/fonts/font";
import RootProvider from "@/hooks/root-provider";
import { Metadata } from "next";
import React from 'react'

export const metadata: Metadata = {
  title: "Karrio Blog",
  description: "Karrio Blog",
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
};

export default function BlogLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning
      className={`${inter.variable} ${jetbrains.variable} ${noto.variable} ${ubuntu.variable} ${oxygen.variable} h-full scroll-smooth`}>
      <body className="min-h-screen font-sans antialiased">
        <RootProvider>
          {children}
        </RootProvider>
      </body>
    </html>
  )
}
