'use client'

import { usePathname } from 'next/navigation'
import type { PageMapItem } from 'nextra'
import { normalizePages } from 'nextra/normalize-pages'
import type { FC } from 'react'
import Link from 'next/link'
import clsx from 'clsx'
import { useState, useRef, useEffect } from 'react'
import { Input } from '@karrio/ui/components/ui/input'
import { Button } from '@karrio/ui/components/ui/button'
import { useTheme } from 'next-themes'
import {
  Monitor,
  Settings,
  Zap,
  Code,
  Boxes,
  Combine,
  FileText,
  HelpCircle,
  File,
  Sun,
  Moon,
  Search,
  X,
  Home,
  Github,
  LifeBuoy,
  ServerCog,
  ChevronRight
} from 'lucide-react'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@karrio/ui/components/ui/collapsible'

// Import shadcn sidebar components (assumed to be available in the UI library)
import {
  Sidebar as ShadcnSidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@karrio/ui/components/ui/sidebar'

export const Sidebar: FC<{ pageMap: PageMapItem[] }> = ({ pageMap }) => {
  const pathname = usePathname()
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({})
  const [searchQuery, setSearchQuery] = useState('')
  const searchRef = useRef<HTMLDivElement>(null)
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  // After mounting, we can show the theme toggle
  useEffect(() => {
    setMounted(true);
    // No need for emergency style anymore as it's properly handled in global.css
  }, [mounted]);

  const { docsDirectories } = normalizePages({
    list: pageMap,
    route: pathname
  })

  // Find docs entry in the page map
  const docsEntry = docsDirectories.find(item => item.name === 'docs')
  const docsChildren = docsEntry?.children || []

  // Icons for sidebar items using Lucide
  const getIcon = (title: string) => {
    switch (title.toLowerCase()) {
      case 'introduction':
        return <Monitor className="h-4 w-4" />
      case 'setup':
        return <Settings className="h-4 w-4" />
      case 'quickstart':
        return <Zap className="h-4 w-4" />
      case 'api development':
      case 'api reference':
      case 'api':
        return <Code className="h-4 w-4" />
      case 'atoms':
        return <Boxes className="h-4 w-4" />
      case 'hooks':
        return <Combine className="h-4 w-4" />
      case 'guides':
      case 'getting started':
        return <FileText className="h-4 w-4" />
      case 'faq':
        return <HelpCircle className="h-4 w-4" />
      case 'developing':
        return <Code className="h-4 w-4" />
      case 'platform':
        return <ServerCog className="h-4 w-4" />
      case 'self hosting':
        return <ServerCog className="h-4 w-4" />
      case 'open source contribution':
        return <Github className="h-4 w-4" />
      default:
        return <File className="h-4 w-4" />
    }
  }

  const toggleSection = (route: string) => {
    setOpenSections(prev => ({
      ...prev,
      [route]: !prev[route]
    }))
  }

  const renderItem = (item: any, depth = 0) => {
    const route = item.route || ('href' in item ? (item.href as string) : '')
    const isActive = pathname === route
    const isParentActive = pathname.startsWith(route) && route !== '/'
    const { title } = item
    const isOpen = openSections[route] || isParentActive

    // Filter out items that don't match the search query
    if (searchQuery && !title.toLowerCase().includes(searchQuery.toLowerCase())) {
      if (!('children' in item) || !item.children.some((child: any) =>
        child.title.toLowerCase().includes(searchQuery.toLowerCase()))) {
        return null
      }
    }

    // For separator type items (Section headers)
    if (item.type === 'separator') {
      return (
        <SidebarGroup key={title}>
          <SidebarGroupLabel key={title}>{title}</SidebarGroupLabel>
          {item.children && (
            <SidebarMenu>
              {item.children.map((child: any) => renderItem(child, depth + 1))}
            </SidebarMenu>
          )}
        </SidebarGroup>
      )
    }

    if ('children' in item) {
      return (
        <SidebarMenu key={route || title} className="px-2">
          <Collapsible
            open={isOpen}
            onOpenChange={() => toggleSection(route)}
          >
            <CollapsibleTrigger className="w-full">
              <SidebarMenuButton tooltip={title}>
                {depth === 0 && getIcon(title)}
                <span>{title}</span>
                <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
              </SidebarMenuButton>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <SidebarGroup>
                {item.children.map((child: any) => renderItem(child, depth + 1))}
              </SidebarGroup>
            </CollapsibleContent>
          </Collapsible>
        </SidebarMenu>
      )
    }

    return (
      <li key={route} className="px-2">
        <Link
          href={route}
          className={clsx(
            "flex items-center gap-2 rounded-md px-2 py-1.5 text-sm transition-colors sidebar-item relative",
            isActive
              ? "text-purple-600 dark:text-purple-400 before:absolute before:left-0 before:top-1 before:bottom-1 before:w-0.5 before:bg-purple-600 dark:before:bg-purple-400 before:rounded-full font-medium"
              : "text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-neutral-800"
          )}
        >
          {depth === 1 && getIcon(title)}
          <span>{title}</span>
        </Link>
      </li>
    )
  }

  // Function to organize the docs by sections
  const renderDocsContent = () => {
    return docsChildren.map((item: any) => {
      if (item.type === 'separator') {
        return renderItem(item, 0);
      }
      return renderItem(item, 0);
    });
  }

  return (
    <ShadcnSidebar className="sidebar border-r border-gray-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 w-72 shrink-0">
      <SidebarHeader className="px-6 py-3">
        <SidebarMenu>
          <SidebarMenuItem>
            <div className="flex items-center justify-between w-full">
              <Link href="/docs" className="flex items-center">
                {mounted && (theme === 'dark' ? (
                  <img src="/logo-light.svg" alt="Karrio" className="h-6 w-auto" />
                ) : (
                  <img src="/logo.svg" alt="Karrio" className="h-6 w-auto" />
                ))}
              </Link>

              <Button
                variant="ghost"
                size="icon"
                className="rounded-full p-1.5 text-gray-500 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-neutral-800"
                onClick={() => {
                  const newTheme = theme === 'dark' ? 'light' : 'dark';
                  setTheme(newTheme);
                  // Force immediate application of the theme classes to ensure consistent styling
                  if (newTheme === 'dark') {
                    document.documentElement.classList.add('dark');
                    document.body.classList.add('dark');
                    document.documentElement.classList.add('docs-dark');
                    document.body.classList.add('docs-dark');
                  } else {
                    document.documentElement.classList.remove('dark');
                    document.body.classList.remove('dark');
                    document.documentElement.classList.remove('docs-dark');
                    document.body.classList.remove('docs-dark');
                  }
                }}
                aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
              >
                {mounted && (theme === 'dark' ? (
                  <Sun className="h-4 w-4" />
                ) : (
                  <Moon className="h-4 w-4" />
                ))}
                <span className="sr-only">Toggle theme</span>
              </Button>
            </div>
          </SidebarMenuItem>
        </SidebarMenu>

        <div className="mt-2" ref={searchRef}>
          <div className="flex items-center rounded-md border px-2 py-1 search-box border-gray-200 dark:border-neutral-800 bg-white dark:bg-neutral-900">
            <Search className="h-3.5 w-3.5 text-gray-500 dark:text-gray-400" />
            <Input
              type="text"
              placeholder="Search docs..."
              className="h-6 w-full border-0 bg-transparent px-2 py-0.5 text-sm outline-none focus-visible:ring-0"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            {searchQuery && (
              <Button
                variant="ghost"
                size="icon"
                className="h-4 w-4 text-gray-500 dark:text-gray-400"
                onClick={() => setSearchQuery('')}
              >
                <X className="h-3.5 w-3.5" />
                <span className="sr-only">Clear search</span>
              </Button>
            )}
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent className="px-2">
        {renderDocsContent()}
      </SidebarContent>

      <SidebarFooter className="border-t py-3 px-2 border-gray-200 dark:border-neutral-800">
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <Link
                  href="/"
                  className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-neutral-800 sidebar-item relative"
                >
                  <Home className="h-3.5 w-3.5" />
                  <span>Website</span>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link
                  href="/blog"
                  className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-neutral-800 sidebar-item relative"
                >
                  <FileText className="h-3.5 w-3.5" />
                  <span>Blog</span>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link
                  href="/docs/api"
                  className={clsx(
                    "flex items-center gap-2 rounded-md px-2 py-1.5 text-sm sidebar-item relative",
                    pathname === "/docs/api"
                      ? "text-purple-600 dark:text-purple-400 before:absolute before:left-0 before:top-1 before:bottom-1 before:w-0.5 before:bg-purple-600 dark:before:bg-purple-400 before:rounded-full font-medium"
                      : "text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-neutral-800"
                  )}
                >
                  <Code className="h-3.5 w-3.5" />
                  <span>API Reference</span>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <a
                  href="https://github.com/karrioapi/karrio"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-neutral-800 sidebar-item relative"
                >
                  <Github className="h-3.5 w-3.5" />
                  <span>GitHub</span>
                </a>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarFooter>
    </ShadcnSidebar>
  )
}
