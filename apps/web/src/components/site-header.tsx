import { Button } from "@karrio/ui/components/ui/button";
import { MobileMenu } from "@/components/mobile-menu";
import { Github } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export const SiteHeader = () => {
  return (
    <header className="sticky top-0 z-50 py-6 border-b border-border/30 bg-background/95 dark:border-white/10 dark:bg-[#0f0826] backdrop-blur-sm dark:backdrop-blur-none shadow-sm dark:shadow-none">
      <div className="container mx-auto px-0 sm:px-4 md:px-6 max-w-[95%] xl:max-w-[1280px]">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-0">
            <MobileMenu />

            <Link href="/" className="flex items-center mr-4">
              <div className="block dark:hidden">
                <Image
                  src="/logo.svg"
                  alt="Karrio Logo"
                  width={120}
                  height={30}
                  style={{ height: 'auto' }}
                  priority
                />
              </div>
              <div className="hidden dark:block">
                <Image
                  src="/logo-light.svg"
                  alt="Karrio Logo"
                  width={120}
                  height={30}
                  style={{ height: 'auto' }}
                  priority
                />
              </div>
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
                href="/carriers"
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
            <Link
              href="https://github.com/karrioapi"
              className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground"
            >
              <Github className="h-6 w-6" />
            </Link>
            <Button className="dark:bg-[#5722cc] dark:hover:bg-[#5722cc]/90">
              <Link href={"/#pricing"}>Get Started</Link>
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
