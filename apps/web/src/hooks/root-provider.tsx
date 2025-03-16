'use client'

import { Analytics } from "@vercel/analytics/react";
import { ThemeProvider } from "next-themes";

export default function RootProvider({
  children,
  defaultTheme = "system"
}: {
  children: React.ReactNode;
  defaultTheme?: "light" | "dark" | "system";
}) {
  return (
    <>
      <ThemeProvider
        attribute="class"
        defaultTheme={defaultTheme}
        enableSystem={defaultTheme === "system"}
        forcedTheme={defaultTheme === "light" ? "light" : undefined}
      >
        {children}
        <Analytics />
      </ThemeProvider>
    </>
  );
}
