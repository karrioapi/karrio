import { PlatformSubnav } from "@karrio/console/components/platform-subnav";
import { MobileMenu } from "@karrio/console/components/mobile-menu";
import { Button } from "@karrio/insiders/components/ui/button";
import { auth } from "@karrio/console/apis/auth";
import { Github } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export async function WebsiteLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  return (
    <div className="min-h-screen bg-[#0f0826] text-white overflow-x-hidden">
      {/* Header */}
      <header className="py-6 border-b border-white/10">
        <div className="container mx-auto px-0 sm:px-4 md:px-6 max-w-[95%] xl:max-w-[1280px]">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-0">
              <MobileMenu />

              <Link href="/" className="flex items-center mr-4">
                <Image
                  src="/logo.svg"
                  alt="Karrio Logo"
                  width={120}
                  height={30}
                  style={{ height: 'auto' }}
                  priority
                />
              </Link>
              <div className="hidden md:flex space-x-6 ml-12 pl-4">
                <Link
                  href="https://docs.karrio.io"
                  className="text-white/80 hover:text-white transition-colors"
                >
                  Docs
                </Link>
                <Link
                  href="https://karrio.io/blog"
                  className="text-white/80 hover:text-white transition-colors"
                >
                  Blog
                </Link>
                <Link
                  href="https://docs.karrio.io/carriers/"
                  className="text-white/80 hover:text-white transition-colors"
                >
                  Carriers
                </Link>
                <Link
                  href="/"
                  className="text-white/80 hover:text-white transition-colors"
                >
                  Platform
                </Link>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="https://github.com/karrioapi"
                className="text-white/80 hover:text-white"
              >
                <Github className="h-6 w-6" />
              </Link>
              <Button className="bg-[#5722cc] hover:bg-[#5722cc]/90">
                <Link href={session ? "/orgs" : "/signin"}>
                  {session ? "Dashboard" : "Sign In"}
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Platform Subnav */}
      <PlatformSubnav />

      {/* Main Content */}
      <main>
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12">
        <div className="container mx-auto px-4 max-w-[95%] xl:max-w-[1280px]">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
            <div className="col-span-2 md:col-span-1">
              <Image
                src="/logo.svg"
                alt="Karrio Logo"
                width={120}
                height={30}
              />
              <p className="mt-4 text-white/60 text-sm">
                The modern shipping infrastructure for global commerce.
              </p>
            </div>
            <div>
              <h3 className="font-medium mb-4">Product</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/pricing"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Pricing
                  </Link>
                </li>
                <li>
                  <Link
                    href="/enterprise"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Enterprise
                  </Link>
                </li>
                <li>
                  <Link
                    href="/partners"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Partners
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium mb-4">Resources</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="https://docs.karrio.io"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Documentation
                  </Link>
                </li>
                <li>
                  <Link
                    href="/blog"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Blog
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://github.com/karrioapi"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    GitHub
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium mb-4">Company</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/about"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    About
                  </Link>
                </li>
                <li>
                  <Link
                    href="/contact"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Contact
                  </Link>
                </li>
                <li>
                  <Link
                    href="/careers"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Careers
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium mb-4">Legal</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/privacy"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Privacy
                  </Link>
                </li>
                <li>
                  <Link
                    href="/terms"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Terms
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center">
            <p className="text-white/60 text-sm">
              © {new Date().getFullYear()} Karrio, Inc. All rights reserved.
            </p>
            <div className="mt-4 md:mt-0 flex space-x-6">
              <Link
                href="https://twitter.com/karrioapi"
                className="text-white/60 hover:text-white"
              >
                Twitter
              </Link>
              <Link
                href="https://linkedin.com/company/karrioapi"
                className="text-white/60 hover:text-white"
              >
                LinkedIn
              </Link>
              <Link
                href="https://github.com/karrioapi"
                className="text-white/60 hover:text-white"
              >
                GitHub
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
