import React, { useState, useEffect } from 'react';
import Link from '@docusaurus/Link';
import { useLocation } from '@docusaurus/router';
import { usePlatformColorMode } from '../hooks/usePlatformColorMode';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useThemeConfig } from '@docusaurus/theme-common';

interface KarrioLayoutProps {
  children: React.ReactNode;
}

export default function KarrioLayout({ children }: KarrioLayoutProps): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  const { navbar } = useThemeConfig();
  const { isPlatformTheme } = usePlatformColorMode();
  const location = useLocation();
  const [isDarkTheme, setIsDarkTheme] = useState(false);

  // Check for dark theme on client side only
  useEffect(() => {
    const isDark = document.querySelector('html')?.getAttribute('data-theme') === 'dark';
    setIsDarkTheme(isDark);
  }, []);

  // Use different background for different pages
  const isPlatformPage = location.pathname.startsWith('/platform');

  // Header styling
  const headerBgClass = isPlatformTheme
    ? 'bg-white dark:bg-[#0f0826]'
    : 'bg-white dark:bg-platform-background';

  // Navigation link styling
  const navLinkClass = 'text-gray-700 hover:text-karrio-purple dark:text-gray-300 dark:hover:text-white transition-colors';
  const activeNavLinkClass = 'text-karrio-purple dark:text-white font-medium';

  // Primary button styling
  const ctaButtonClass = 'bg-karrio-purple hover:bg-karrio-purple/90 text-white px-4 py-2 rounded-md transition-colors font-medium';

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className={`py-6 border-b ${isDarkTheme ? 'border-white/10' : 'border-gray-200'} ${headerBgClass}`}>
        <div className="container mx-auto px-4 max-w-[95%] xl:max-w-[1280px]">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-0">
              <Link href="/" className="flex items-center mr-8">
                <img
                  src={navbar.logo?.src}
                  alt={navbar.logo?.alt || 'Karrio Logo'}
                  className="h-8"
                />
                <span className="font-bold text-xl ml-2 text-gray-900 dark:text-white">{navbar.title}</span>
              </Link>
              <div className="hidden md:flex space-x-8">
                <Link
                  to="/docs"
                  className={location.pathname.startsWith('/docs') ? activeNavLinkClass : navLinkClass}
                >
                  Docs
                </Link>
                <Link
                  to="/blog"
                  className={location.pathname.startsWith('/blog') ? activeNavLinkClass : navLinkClass}
                >
                  Blog
                </Link>
                <Link
                  to="/carriers"
                  className={location.pathname.startsWith('/carriers') ? activeNavLinkClass : navLinkClass}
                >
                  Carriers
                </Link>
                <Link
                  to="/platform"
                  className={location.pathname.startsWith('/platform') ? activeNavLinkClass : navLinkClass}
                >
                  Platform
                </Link>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              <Link
                href="https://app.karrio.io"
                className={`${navLinkClass} hidden md:block`}
              >
                Dashboard
              </Link>
              <Link
                href="https://github.com/karrioapi/karrio"
                className={`${navLinkClass} hidden md:block`}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="h-6 w-6"
                >
                  <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path>
                  <path d="M9 18c-4.51 2-5-2-7-2"></path>
                </svg>
              </Link>
              <Link
                href="https://app.karrio.io/signup"
                className={ctaButtonClass}
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className={`border-t ${isDarkTheme ? 'border-white/10 bg-[#0f0826]' : 'border-gray-200 bg-gray-50'} py-12`}>
        <div className="container mx-auto px-4 max-w-[95%] xl:max-w-[1280px]">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-medium mb-4 text-gray-900 dark:text-white">Resources</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/docs"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    Docs
                  </Link>
                </li>
                <li>
                  <Link
                    href="/carriers"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    Carriers
                  </Link>
                </li>
                <li>
                  <Link
                    href="/docs/product"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    Product
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium mb-4 text-gray-900 dark:text-white">Community</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="https://github.com/orgs/karrioapi/discussions"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    Discussions
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://discord.com/invite/gS88uE7sEx"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    Discord
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium mb-4 text-gray-900 dark:text-white">Company</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/blog"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    Blog
                  </Link>
                </li>
                <li>
                  <Link
                    href="https://github.com/karrioapi/"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    GitHub
                  </Link>
                </li>
                <li>
                  <Link
                    href="/docs/api/overview"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    API Reference
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium mb-4 text-gray-900 dark:text-white">Get Started</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/platform"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    Platform
                  </Link>
                </li>
                <li>
                  <Link
                    href="/docs/self-hosting/introduction"
                    className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white text-sm"
                  >
                    Self Hosting
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t border-gray-200 dark:border-white/10 flex flex-col md:flex-row justify-between items-center">
            <div className="flex flex-col items-start">
              <Link href="/" className="flex items-center">
                <img
                  src={navbar.logo?.src}
                  alt={navbar.logo?.alt || 'Karrio Logo'}
                  className="h-8"
                />
                <span className="font-bold text-xl ml-2 text-gray-900 dark:text-white">{navbar.title}</span>
              </Link>
              <p className="text-gray-600 dark:text-white/60 text-sm mt-2">
                The modern shipping infrastructure for global commerce
              </p>
              <p className="text-gray-600 dark:text-white/60 text-sm mt-4">
                Copyright © {new Date().getFullYear()} Karrio, Inc.
              </p>
            </div>
            <div className="mt-4 md:mt-0 flex space-x-6">
              <Link
                href="https://linkedin.com/company/karrioapi"
                className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="h-5 w-5"
                >
                  <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                  <rect width="4" height="12" x="2" y="9"></rect>
                  <circle cx="4" cy="4" r="2"></circle>
                </svg>
              </Link>
              <Link
                href="https://github.com/karrioapi"
                className="text-gray-600 dark:text-white/60 hover:text-karrio-purple dark:hover:text-white"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="h-5 w-5"
                >
                  <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path>
                  <path d="M9 18c-4.51 2-5-2-7-2"></path>
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
