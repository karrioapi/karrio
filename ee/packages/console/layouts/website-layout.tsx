import { PlatformSubnav } from "@karrio/console/components/platform-subnav";
import { MobileMenu } from "@karrio/console/components/mobile-menu";
import { Button } from "@karrio/ui/components/ui/button";
import { auth } from "@karrio/console/apis/auth";
import { Github, Linkedin } from "lucide-react";
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
                <Link href={session ? "/orgs" : "/#pricing"}>
                  {session ? "Dashboard" : "Get Started"}
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
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-medium mb-4">Resources</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="https://docs.karrio.io"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Docs
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://docs.karrio.io/carriers/"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Carriers
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://docs.karrio.io/product"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Product
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium mb-4">Community</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="https://www.karrio.io/launch-week-x"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Launch week X
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://github.com/orgs/karrioapi/discussions"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Discussions
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://discord.com/invite/gS88uE7sEx"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Discord
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium mb-4">Company</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="https://www.karrio.io/blog"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Blog
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://github.com/karrioapi/"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    GitHub
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://docs.karrio.io/reference/openapi"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    API Reference
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium mb-4">Get Started</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="https://platform.karrio.io"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Platform
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://docs.karrio.io/product/self-hosting"
                    className="text-white/60 hover:text-white text-sm"
                  >
                    Download
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center">
            <div className="flex flex-col items-start">
              <Link href="https://karrio.io" className="flex items-center">
                <Image
                  src="/logo.svg"
                  alt="Karrio Logo"
                  width={100}
                  height={25}
                  style={{ height: 'auto' }}
                  priority
                />
              </Link>
              <p className="text-white/60 text-sm mt-2">
                The modern shipping infrastructure for global commerce
              </p>
              <p className="text-white/60 text-sm mt-4">
                Copyright © {new Date().getFullYear()} karrio Inc.
              </p>
            </div>
            <div className="mt-4 md:mt-0 flex space-x-6">
              <Link
                href="https://linkedin.com/company/karrioapi"
                className="text-white/60 hover:text-white flex items-center gap-1"
              >
                <Linkedin className="h-5 w-5" />
              </Link>
              <Link
                href="https://github.com/karrioapi"
                className="text-white/60 hover:text-white flex items-center gap-1"
              >
                <Github className="h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
