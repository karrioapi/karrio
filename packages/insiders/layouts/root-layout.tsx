import { geistSans, geistMono } from "@karrio/insiders/fonts/font";
import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Karrio Insiders",
  description: "Karrio Insiders",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
