import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useThemeConfig } from '@docusaurus/theme-common';
import { usePlatformColorMode } from '../hooks/usePlatformColorMode';
import { useLocation } from '@docusaurus/router';

interface HeaderProps {
  isHomepage?: boolean;
}

const Header: React.FC<HeaderProps> = ({ isHomepage = false }) => {
  const { siteConfig } = useDocusaurusContext();
  const { navbar } = useThemeConfig();
  const { isPlatformTheme } = usePlatformColorMode();
  const location = useLocation();

  // Don't render our custom header on doc pages since they have their own header
  const isDocsPage = location.pathname.startsWith('/docs/');
  if (isDocsPage) {
    return null;
  }

  // Use different background for homepage, platform page, and regular pages
  const navbarClasses = isHomepage
    ? 'bg-white dark:bg-platform-background'
    : isPlatformTheme
      ? 'bg-white dark:bg-platform-card shadow-sm'
      : 'bg-white dark:bg-platform-card shadow-sm';

  // Determine text color based on theme
  const textClass = 'text-gray-900 dark:text-white';
  const navLinkClass = 'text-gray-700 hover:text-karrio-purple dark:text-gray-300 dark:hover:text-platform-purple font-medium';
  const activeNavLinkClass = 'text-karrio-purple dark:text-platform-purple font-medium';

  // Use accent color for primary CTA button
  const ctaButtonClass = isPlatformTheme
    ? 'bg-platform-purple hover:bg-platform-purple-dark text-white px-4 py-2 rounded-md transition-colors font-medium'
    : 'bg-karrio-orange hover:bg-accent-dark text-white px-4 py-2 rounded-md transition-colors font-medium';

  return (
    <header className={`fixed w-full top-0 z-50 ${navbarClasses} header-custom`}>
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1">
            <Link to="/" className="flex items-center gap-2">
              <img
                src={navbar.logo?.src}
                alt={navbar.logo?.alt || 'Karrio Logo'}
                className="h-8"
              />
              <span className={`font-bold text-xl ${textClass}`}>{navbar.title}</span>
            </Link>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <Link to="/docs" className={navLinkClass}>
              Docs
            </Link>
            <Link to="/blog" className={navLinkClass}>
              Blog
            </Link>
            <Link to="/platform" className={isPlatformTheme ? activeNavLinkClass : navLinkClass}>
              Platform
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <Link
              to="https://app.karrio.io"
              className={`${navLinkClass} hidden md:block`}
            >
              Dashboard
            </Link>
            <Link
              to="https://github.com/karrioapi/karrio"
              className={`${navLinkClass} hidden md:block`}
            >
              GitHub
            </Link>
            <Link
              to="https://app.karrio.io/signup"
              className={ctaButtonClass}
            >
              Get Started
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
