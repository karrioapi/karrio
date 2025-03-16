"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@karrio/ui/lib/utils';
import {
  Monitor, Server, Code, GitPullRequest, FileText, Package, Database, Layers
} from 'lucide-react';

interface NavItem {
  title: string;
  href: string;
  icon?: React.ReactNode;
  isActive?: boolean;
  children?: NavItem[];
}

interface DocsSidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export function DocsSidebar({ isOpen = false, onClose }: DocsSidebarProps) {
  const pathname = usePathname();

  const navigation: NavItem[] = [
    {
      title: "Getting Started",
      href: "#",
      isActive: false,
      children: [
        {
          title: "Introduction",
          href: "/docs/introduction",
          icon: <Monitor className="h-4 w-4" />,
          isActive: pathname === '/docs/introduction',
        },
        {
          title: "Local Development",
          href: "/docs/local-development",
          icon: <Code className="h-4 w-4" />,
          isActive: pathname === '/docs/local-development',
        },
      ]
    },
    {
      title: "API Reference",
      href: "#",
      isActive: false,
      children: [
        {
          title: "API v2 Reference",
          href: "/docs/api-v2-reference",
          icon: <Database className="h-4 w-4" />,
          isActive: pathname === '/docs/api-v2-reference',
        },
        {
          title: "API v1 Reference",
          href: "/docs/api-v1-reference",
          icon: <Database className="h-4 w-4" />,
          isActive: pathname === '/docs/api-v1-reference',
        },
      ]
    },
    {
      title: "Self Hosting",
      href: "/docs/self-hosting",
      icon: <Server className="h-4 w-4" />,
      isActive: pathname === '/docs/self-hosting',
    },
    {
      title: "Platform",
      href: "/docs/platform",
      icon: <Layers className="h-4 w-4" />,
      isActive: pathname === '/docs/platform',
    },
    {
      title: "Developing",
      href: "/docs/developing",
      icon: <Code className="h-4 w-4" />,
      isActive: pathname === '/docs/developing',
    },
    {
      title: "Open Source Contribution",
      href: "#",
      isActive: false,
      children: [
        {
          title: "Introduction",
          href: "/docs/open-source-contribution/introduction",
          icon: <FileText className="h-4 w-4" />,
          isActive: pathname === '/docs/open-source-contribution/introduction',
        },
        {
          title: "Code styling",
          href: "/docs/open-source-contribution/code-styling",
          icon: <Code className="h-4 w-4" />,
          isActive: pathname === '/docs/open-source-contribution/code-styling',
        },
        {
          title: "Pull requests",
          href: "/docs/open-source-contribution/pull-requests",
          icon: <GitPullRequest className="h-4 w-4" />,
          isActive: pathname === '/docs/open-source-contribution/pull-requests',
        },
        {
          title: "Contributor's Guide",
          href: "/docs/open-source-contribution/contributors-guide",
          icon: <Package className="h-4 w-4" />,
          isActive: pathname === '/docs/open-source-contribution/contributors-guide',
        }
      ]
    }
  ];

  const renderNavItems = (items: NavItem[]) => {
    return items.map((item, index) => {
      // Handle top-level categories
      if (item.children) {
        return (
          <div key={index} className="mb-6">
            <h3 className="font-medium text-sm text-gray-500 dark:text-gray-400 mb-2">
              {item.title}
            </h3>
            <ul className="space-y-1">
              {item.children.map((child, childIndex) => (
                <li key={childIndex}>
                  <Link
                    href={child.href}
                    className={cn(
                      "flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors",
                      child.isActive
                        ? "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white"
                        : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-white"
                    )}
                  >
                    {child.icon}
                    {child.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        );
      }

      // Handle simple nav items
      return (
        <div key={index} className="mb-6">
          <Link
            href={item.href}
            className={cn(
              "flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors font-medium",
              item.isActive
                ? "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white"
                : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-white"
            )}
          >
            {item.icon}
            {item.title}
          </Link>
        </div>
      );
    });
  };

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-30 w-72 border-r border-gray-200 dark:border-white/10 bg-white dark:bg-[#111] transition-transform duration-300 p-6 overflow-y-auto",
        isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      )}
    >
      <div className="space-y-6 pt-10">
        {renderNavItems(navigation)}
      </div>
    </aside>
  );
}
