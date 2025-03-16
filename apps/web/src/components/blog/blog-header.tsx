"use client";

import { BlogMobileMenu } from "@/components/blog/blog-mobile-menu";
import { Github, Search } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useState, useEffect } from "react";
import { ThemeToggle } from "./theme-toggle";

export function BlogHeader() {
  const [isMounted, setIsMounted] = useState(false);
  const [isDesktop, setIsDesktop] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    const checkIfDesktop = () => {
      setIsDesktop(window.innerWidth >= 768);
    };

    // Initial check
    checkIfDesktop();

    // Add event listener
    window.addEventListener('resize', checkIfDesktop);

    // Cleanup
    return () => window.removeEventListener('resize', checkIfDesktop);
  }, []);

  return (
    <header className="py-6 border-b dark:border-white/10 border-border/30 dark:bg-[#0f0826] bg-background/95 backdrop-blur-sm dark:backdrop-blur-none shadow-sm dark:shadow-none">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-0">
            {/* Mobile menu for navigation items */}
            <BlogMobileMenu />

            <Link href="/" className="flex items-center mr-4">
              <div className="block dark:hidden">
                <Image
                  src="/logo-light.svg"
                  alt="Karrio Logo"
                  width={120}
                  height={30}
                  style={{ height: 'auto' }}
                  priority
                />
              </div>
              <div className="hidden dark:block">
                <Image
                  src="/logo.svg"
                  alt="Karrio Logo"
                  width={120}
                  height={30}
                  style={{ height: 'auto' }}
                  priority
                />
              </div>
            </Link>

            {/* Desktop navigation menu */}
            {isMounted && isDesktop && (
              <div className="hidden md:flex space-x-6 ml-12 pl-4">
                <Link
                  href="/docs"
                  className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors font-medium"
                >
                  Docs
                </Link>
                <Link
                  href="/blog"
                  className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors font-medium"
                >
                  Blog
                </Link>
                <Link
                  href="/carriers"
                  className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors font-medium"
                >
                  Carriers
                </Link>
                <Link
                  href="/platform"
                  className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors font-medium"
                >
                  Platform
                </Link>
              </div>
            )}
          </div>

          <div className="flex items-center space-x-4">
            {isMounted && isDesktop && (
              <button aria-label="Search" className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground">
                <Search className="h-5 w-5" />
              </button>
            )}

            {/* Show GitHub icon on all screen sizes */}
            <Link
              href="https://github.com/karrioapi"
              className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground"
            >
              <Github className="h-5 w-5" />
            </Link>

            {/* Theme toggle button */}
            <ThemeToggle />
          </div>
        </div>
      </div>
    </header>
  );
}
