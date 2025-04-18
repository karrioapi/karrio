import { Github, Linkedin } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export const SiteFooter = () => {
  return (
    <footer className="bg-[#0f0826] text-white border-t border-white/10 py-12">
      <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div>
            <h3 className="font-medium mb-4">Resources</h3>
            <ul className="space-y-2">
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
                  href="/docs"
                  className="text-white/60 hover:text-white text-sm"
                >
                  Docs
                </Link>
              </li>
              <li>
                <Link
                  href="/docs/api-reference"
                  className="text-white/60 hover:text-white text-sm"
                >
                  API Reference
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium mb-4">Community</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/launch-week-x"
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
                  href="/terms-of-service"
                  className="text-white/60 hover:text-white text-sm"
                >
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link
                  href="/privacy-policy"
                  className="text-white/60 hover:text-white text-sm"
                >
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link
                  href="https://github.com/karrioapi/karrio"
                  className="text-white/60 hover:text-white text-sm"
                >
                  GitHub
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium mb-4">Get Started</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/platform"
                  className="text-white/60 hover:text-white text-sm"
                >
                  Platform
                </Link>
              </li>
              <li>
                <Link
                  href="/docs/self-hosting"
                  className="text-white/60 hover:text-white text-sm"
                >
                  Download
                </Link>
              </li>
              <li>
                <Link
                  href="/changelog"
                  className="text-white/60 hover:text-white text-sm"
                >
                  Changelog
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center">
          <div className="flex flex-col items-start">
            <Link href="/" className="flex items-center">
              <Image
                src="/logo-light.svg"
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
  )
}
