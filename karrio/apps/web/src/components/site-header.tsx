"use client";

import { DocSearchWrapper } from "@/components/search/docsearch-component";
import { ThemeToggle } from "@/components/blog/theme-toggle";
import { Button } from "@karrio/ui/components/ui/button";
import { MobileMenu } from "@/components/mobile-menu";
import { Github, Search } from "lucide-react";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useTheme } from "next-themes";
import Image from "next/image";
import Link from "next/link";

export const SiteHeader = () => {
  const pathname = usePathname();
  const isBlogPage = pathname?.startsWith("/blog");
  const isDocsPage = pathname?.startsWith("/docs");
  const isPlatformPage = pathname?.startsWith("/platform");
  const isMarketingPage = pathname === '/' || (!isPlatformPage && !isBlogPage && !isDocsPage);
  const { theme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Determine which logo to show based on the current page and theme
  const getLogoSrc = () => {
    if (isPlatformPage) {
      return "/logo-light.svg"; // Platform always uses light logo
    } else if (isMarketingPage) {
      return "/logo.svg"; // Marketing always uses dark logo
    } else {
      // For blog/docs, respect the current theme
      return (theme === 'dark' || resolvedTheme === 'dark') ? "/logo-light.svg" : "/logo.svg";
    }
  };

  return (
    <header className="sticky top-0 z-50 py-4 border-b border-border/30 bg-background backdrop-blur-sm dark:border-white/10 dark:backdrop-blur-none shadow-sm dark:shadow-none">
      <div className="container mx-auto relative px-4 sm:px-6 lg:px-0 max-w-6xl bg-background dark:bg-inherit">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-0">
            <MobileMenu isBlogPage={isBlogPage} />
            {/* Hidden DocSearch wrapper for blog pages */}
            <div className="hidden">
              <DocSearchWrapper buttonText="Search blog..." />
            </div>

            <Link href="/" className="flex items-center mr-4">
              {mounted ? (
                <Image
                  src={getLogoSrc()}
                  alt="Karrio Logo"
                  width={120}
                  height={30}
                  style={{ height: 'auto' }}
                  priority
                />
              ) : (
                // Placeholder to prevent layout shift while theme is loading
                <div style={{ width: 120, height: 30 }}></div>
              )}
            </Link>
            <div className="hidden md:flex space-x-6 ml-12 pl-4">
              <Link
                href="/docs"
                className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors font-semibold"
              >
                Docs
              </Link>
              <Link
                href="/blog"
                className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors font-semibold"
              >
                Blog
              </Link>
              <Link
                href="/docs/carriers"
                className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors font-semibold"
              >
                Carriers
              </Link>
              <Link
                href="/platform"
                className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors font-semibold"
              >
                Platform
              </Link>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            {isBlogPage && (
              <>
                <ThemeToggle />
                <Button
                  variant="ghost"
                  size="icon"
                  className="rounded-full p-1.5 text-foreground/80 hover:text-foreground hover:bg-muted dark:text-white/80 dark:hover:text-white dark:hover:bg-[#1a103a]"
                  onClick={() => {
                    // Find a DocSearch button in the DOM and trigger a click on it
                    const docSearchButton = document.querySelector('.DocSearch-Button') as HTMLButtonElement;
                    if (docSearchButton) {
                      docSearchButton.click();
                    }
                  }}
                  aria-label="Search blog"
                >
                  <Search className="h-5 w-5" />
                </Button>
              </>
            )}
            <Button className="dark:bg-[#5722cc] dark:hover:bg-[#5722cc]/90">
              <Link href={"/platform"}>Get Started</Link>
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
