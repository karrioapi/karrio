'use client'

import { Analytics } from "@vercel/analytics/react";
import { ThemeProvider } from "next-themes";

export default function RootProvider({
  children,
  defaultTheme = "system",
  forcedTheme,
  disableTransitionOnChange = false,
  sectionKey = "app"
}: {
  children: React.ReactNode;
  defaultTheme?: "light" | "dark" | "system";
  forcedTheme?: "light" | "dark";
  disableTransitionOnChange?: boolean;
  sectionKey?: string;
}) {
  return (
    <>
      <ThemeProvider
        attribute="class"
        defaultTheme={defaultTheme}
        enableSystem={defaultTheme === "system"}
        forcedTheme={forcedTheme}
        disableTransitionOnChange={disableTransitionOnChange}
        storageKey={`theme-${sectionKey}`}
      >
        {children}
        <Analytics />
      </ThemeProvider>
    </>
  );
}
