'use client'

import {
  Sidebar as ShadcnSidebar,
  SidebarContent,
  SidebarHeader,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarFooter,
} from '@karrio/ui/components/ui/sidebar'
import {
  Monitor,
  FileText,
  GitFork,
  Database,
  ArrowUpCircle,
  Container,
  BookOpen,
  Zap,
  Home,
  Github,
  ChevronDown,
  ChevronRight,
  Truck,
  Package,
  MapPin,
  ShoppingBag,
  FileImage,
  Users,
  Building2,
  Settings,
  Webhook,
  ScrollText,
  Bolt,
  Activity,
  BarChart3,
  Globe,
  Workflow,
  Shield,
  Terminal,
  PlugZap,
  GitPullRequest,
  Code2,
  Network,
  Cloud,
  Server,
  Hammer,
} from 'lucide-react'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@karrio/ui/components/ui/collapsible'
import { normalizePages } from 'nextra/normalize-pages'
import { usePathname } from 'next/navigation'
import { useState, useEffect, useMemo } from 'react'
import { ThemeConfig, getThemeConfig } from '@/types/theme'
import type { PageMapItem } from 'nextra'
import { useTheme } from 'next-themes'
import type { FC } from 'react'
import Link from 'next/link'
import clsx from 'clsx'

// Define interface for carrier integration
interface CarrierIntegration {
  id: string
  display_name: string
  integration_status: 'production' | 'beta' | 'alpha' | 'deprecated'
  capabilities: string[]
}

interface SidebarProps {
  pageMap: PageMapItem[]
  themeConfig?: ThemeConfig
}

export const Sidebar: FC<SidebarProps> = ({ pageMap, themeConfig }) => {
  const pathname = usePathname()
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  // State for user-toggled sections (this won't cause infinite loops)
  const [userToggled, setUserToggled] = useState<Record<string, boolean>>({})

  // Get theme config from pageMap if not provided as prop
  const currentThemeConfig = themeConfig || getThemeConfig(pageMap, pathname)

  console.log(currentThemeConfig)

  // Check if sidebar should be hidden
  if (currentThemeConfig.sidebar === false) {
    return <></>
  }

  // After mounting, initialize component
  useEffect(() => {
    setMounted(true)
  }, []);

  const { docsDirectories } = normalizePages({
    list: pageMap,
    route: pathname
  })

  // Find docs entry in the page map
  const docsEntry = docsDirectories.find(item => item.name === 'docs')
  const docsChildren = docsEntry?.children || []

  // Get the current active section based on the first segment after /docs/
  const activeSegment = pathname.split('/').filter(Boolean)[1] || ''
  const activeSection = docsChildren.find(item => item.name === activeSegment)
  const activeSectionChildren = activeSection?.children || []

  // Helper function to check if a page has children
  const hasChildren = (page: any): boolean => {
    return page.children && page.children.length > 0;
  };

  // Compute expanded sections based on the current path - this is calculated only when dependencies change
  const pathBasedExpanded = useMemo(() => {
    const result: Record<string, boolean> = {};

    if (!pathname) return result;

    const pathParts = pathname.split('/').filter(Boolean);

    // Create path segments from the current URL
    for (let i = 1; i < pathParts.length; i++) {
      const path = '/' + pathParts.slice(0, i + 1).join('/');
      result[path] = true;
    }

    return result;
  }, [pathname]);

  // Helper to toggle a section
  const toggleSection = (sectionPath: string) => {
    setUserToggled(prev => ({
      ...prev,
      [sectionPath]: !prev[sectionPath] && !pathBasedExpanded[sectionPath]
        ? true
        : !prev[sectionPath]
    }));
  };

  // Combine automatic path-based expansion with user toggles
  const isExpanded = (path: string) => {
    // If user explicitly toggled this section, use that value
    if (userToggled[path] !== undefined) {
      return userToggled[path];
    }
    // Otherwise use path-based expansion
    return pathBasedExpanded[path] || false;
  };

  // Check if a product is an Insiders feature
  const isInsidersProduct = (name: string): boolean => {
    const normalizedName = name.toLowerCase().replace(/\s+/g, '-')
    const insidersProducts = [
      'batch-processing',
      'workflows',
      'shipping-rules',
      'multi-organizations',
      'multi-orgs',
      'admin-console'
    ]
    return insidersProducts.includes(normalizedName)
  }

  // Get icon for a specific page
  const getIcon = (name: string) => {
    const normalizedName = name.toLowerCase().replace(/\s+/g, '-')

    switch (normalizedName) {
      // Product Guide specific icons
      case 'carrier-connections':
        return <Truck className="h-4 w-4" />
      case 'shipments':
        return <Package className="h-4 w-4" />
      case 'tracking':
        return <MapPin className="h-4 w-4" />
      case 'orders':
        return <ShoppingBag className="h-4 w-4" />
      case 'document-generation':
        return <FileImage className="h-4 w-4" />
      case 'user-management':
        return <Users className="h-4 w-4" />
      case 'multi-organizations':
      case 'multi-orgs':
        return <Building2 className="h-4 w-4" />
      case 'shipping-rules':
        return <Settings className="h-4 w-4" />
      case 'workflows':
        return <Workflow className="h-4 w-4" />
      case 'batch-processing':
        return <BarChart3 className="h-4 w-4" />
      case 'admin-console':
        return <Shield className="h-4 w-4" />
      case 'webhooks':
        return <Webhook className="h-4 w-4" />
      case 'api-logs':
        return <ScrollText className="h-4 w-4" />
      case 'events':
        return <Activity className="h-4 w-4" />

      // Development/Setup specific icons
      case 'introduction':
        return <BookOpen className="h-4 w-4" />
      case 'local-development':
        return <Monitor className="h-4 w-4" />
      case 'oss-contribution':
        return <GitFork className="h-4 w-4" />
      case 'pull-requests':
        return <GitPullRequest className="h-4 w-4" />
      case 'contributors-guide':
        return <Users className="h-4 w-4" />
      case 'embeddable-elements':
        return <Code2 className="h-4 w-4" />
      case 'api-development':
        return <Code2 className="h-4 w-4" />
      case 'carrier-integration':
        return <Network className="h-4 w-4" />
      case 'cli-guide':
        return <Terminal className="h-4 w-4" />
      case 'plugin-development':
        return <PlugZap className="h-4 w-4" />
      case 'installation':
        return <Container className="h-4 w-4" />
      case 'database-migrations':
        return <Database className="h-4 w-4" />
      case 'upgrade':
        return <ArrowUpCircle className="h-4 w-4" />
      case 'docker':
        return <Container className="h-4 w-4" />
      case 'aws':
        return <Cloud className="h-4 w-4" />
      case 'gcp':
        return <Cloud className="h-4 w-4" />
      case 'digital-ocean':
        return <Cloud className="h-4 w-4" />
      case 'environment':
        return <Server className="h-4 w-4" />
      case 'custom-builds':
        return <Hammer className="h-4 w-4" />
      case 'guides':
        return <BookOpen className="h-4 w-4" />
      case 'quickstart':
        return <Zap className="h-4 w-4" />

      // Default cases
      default:
        return <FileText className="h-4 w-4" />
    }
  }

  // Group pages by their section
  const groupedPages = activeSectionChildren.reduce((acc: any, item: any) => {
    if (item.type === 'separator') {
      acc[item.name] = {
        title: item.title,
        pages: []
      }
    } else if (item.type === 'page') {
      const lastSeparator = [...activeSectionChildren].reverse().find(
        (s: any) => s.type === 'separator' && activeSectionChildren.indexOf(s) < activeSectionChildren.indexOf(item)
      )
      if (lastSeparator) {
        if (!acc[lastSeparator.name]) {
          acc[lastSeparator.name] = {
            title: lastSeparator.title,
            pages: []
          }
        }
        acc[lastSeparator.name].pages.push(item)
      }
    }
    return acc
  }, {})

  // Fetch carrier items if we're on a carrier page
  const fetchCarrierItems = async () => {
    try {
      const response = await fetch('/carrier-integrations.json');
      const data = await response.json();
      // Transform data to match the interface
      return data.map((item: any) => ({
        id: item.id,
        display_name: item.display_name,
        integration_status: item.integration_status,
        capabilities: item.capabilities || []
      }));
    } catch (error) {
      console.error('Error fetching carrier data:', error);
      return [];
    }
  };

  // State for carrier integrations
  const [carrierIntegrations, setCarrierIntegrations] = useState<CarrierIntegration[]>([]);

  // Load carrier data when on carrier pages
  useEffect(() => {
    if (pathname.includes('/docs/carriers')) {
      fetchCarrierItems().then(data => setCarrierIntegrations(data));
    }
  }, [pathname]);

  // Render a page link with collapsible support for nested children
  const renderPageLink = (page: any) => {
    const isActive = pathname === page.route;
    const hasNestedChildren = hasChildren(page);
    const expanded = isExpanded(page.route);
    const isInPath = pathname.startsWith(page.route + '/');

    if (hasNestedChildren) {
      return (
        <div key={page.route} className="w-full">
          <Collapsible
            open={expanded}
            onOpenChange={() => toggleSection(page.route)}
          >
            <div className="flex items-center w-full">
              <CollapsibleTrigger className="flex items-center w-full gap-2 px-2 py-1.5 text-sm transition-colors relative rounded-md hover:bg-gray-100 dark:hover:bg-muted">
                <div className={clsx(
                  "flex items-center gap-2 w-full",
                  isActive || isInPath
                    ? "text-purple-600 dark:text-purple-400 font-medium"
                    : "text-gray-600 dark:text-gray-300"
                )}>
                  {getIcon(page.title)}
                  <span>{page.title}</span>
                  {isInsidersProduct(page.title) && (
                    <div className="h-1.5 w-1.5 rounded-full bg-purple-500 dark:bg-purple-400 ml-1" />
                  )}
                  <span className="ml-auto">
                    {expanded ?
                      <ChevronDown className="h-3.5 w-3.5" /> :
                      <ChevronRight className="h-3.5 w-3.5" />
                    }
                  </span>
                </div>
              </CollapsibleTrigger>
            </div>
            <CollapsibleContent>
              <div className="pl-2 mt-1 space-y-1 border-l border-gray-200 dark:border-neutral-800 ml-2">
                {page.children && page.children.map((child: any) => {
                  if (child.type === 'page' || (child.data && Object.values(child.data).some((item: any) => item.type === 'page'))) {
                    const childPages = child.data
                      ? Object.entries(child.data).filter(([_, item]: [string, any]) => item.type === 'page')
                      : [[child.name, child]];

                    return childPages.map(([key, childPage]: [string, any]) => (
                      <Link
                        key={childPage.route || `${page.route}/${key}`}
                        href={childPage.route || `${page.route}/${key}`}
                        className={clsx(
                          "flex items-center gap-2 px-2 py-1 text-xs transition-colors relative",
                          pathname === (childPage.route || `${page.route}/${key}`)
                            ? "text-purple-600 dark:text-purple-400 before:absolute before:left-[-9px] before:top-1 before:bottom-1 before:w-0.5 before:bg-purple-600 dark:before:bg-purple-400 before:rounded-full font-medium"
                            : "text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-gray-100"
                        )}
                      >
                        <span>{childPage.title}</span>
                      </Link>
                    ));
                  }
                  return null;
                })}
              </div>
            </CollapsibleContent>
          </Collapsible>
        </div>
      );
    }

    return (
      <Link
        key={page.route}
        href={page.route}
        className={clsx(
          "flex items-center gap-2 px-2 py-1.5 text-sm transition-colors relative",
          pathname === page.route
            ? "text-purple-600 dark:text-purple-400 before:absolute before:left-0 before:top-1 before:bottom-1 before:w-0.5 before:bg-purple-600 dark:before:bg-purple-400 before:rounded-full font-medium"
            : "text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-gray-100"
        )}
      >
        {getIcon(page.title)}
        <span>{page.title}</span>
        {isInsidersProduct(page.title) && (
          <div className="h-1.5 w-1.5 rounded-full bg-purple-500 dark:bg-purple-400 ml-1" />
        )}
      </Link>
    );
  };

  return (
    <ShadcnSidebar className="sidebar border-r border-gray-200 dark:border-neutral-800 bg-background shrink-0">
      <SidebarHeader className="px-5 py-4">
        {/* Desktop Header */}
        <div className="hidden md:block">
          <SidebarMenu>
            <SidebarMenuItem>
              <div className="flex items-center justify-between w-full">
                <Link href="/docs" className="flex items-center">
                  {mounted && (theme === 'dark' ? (
                    <img src="/karrio-docs-light.svg" alt="Karrio Docs" className="h-5 w-auto" />
                  ) : (
                    <img src="/karrio-docs.svg" alt="Karrio Docs" className="h-5 w-auto" />
                  ))}
                </Link>
              </div>
            </SidebarMenuItem>
          </SidebarMenu>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden">
          <div className="space-y-1">
            {docsChildren.map((section) => (
              section.type === 'separator' && (
                <Link
                  key={section.name}
                  href={`/docs/${section.name}`}
                  className={clsx(
                    "flex items-center gap-2 py-1.5 text-sm font-semibold transition-colors",
                    pathname.startsWith(`/docs/${section.name}`)
                      ? "text-purple-600 dark:text-purple-400"
                      : "text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-gray-100"
                  )}
                >
                  <BookOpen className="h-3.5 w-3.5" />
                  <span>{section.title}</span>
                </Link>
              )
            ))}
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent className="px-4 py-6">
        {Object.entries(groupedPages).map(([key, section]: [string, any]) => (
          <div key={key} className="mt-4 first:mt-0">
            <h4 className="px-2 mb-2 text-sm font-semibold text-gray-900 dark:text-gray-100">
              {section.title}
            </h4>
            <div className="space-y-1 pl-2">
              {section.pages.map((page: any) => renderPageLink(page))}

              {/* Show carrier integrations list if on carriers page and this is the carrier section */}
              {pathname.includes('/docs/carriers') && (
                <>
                  {carrierIntegrations.map((integration: CarrierIntegration) => (
                    <Link
                      key={integration.id}
                      href={`/docs/carriers/${integration.id}`}
                      className={clsx(
                        "flex items-center gap-2 px-2 py-1 text-xs transition-colors relative",
                        pathname === `/docs/carriers/${integration.id}`
                          ? "text-purple-600 dark:text-purple-400 before:absolute before:left-0 before:top-1 before:bottom-1 before:w-0.5 before:bg-purple-600 dark:before:bg-purple-400 before:rounded-full font-medium"
                          : "text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-gray-100"
                      )}
                    >
                      <span>{integration.display_name}</span>
                    </Link>
                  ))}
                </>
              )}
            </div>
          </div>
        ))}
      </SidebarContent>

      <SidebarFooter className="border-t py-3 px-2 border-gray-200 dark:border-neutral-800">
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <Link
                  href="/"
                  className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-muted sidebar-item relative"
                >
                  <Home className="h-3.5 w-3.5" />
                  <span>Website</span>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link
                  href="/blog"
                  className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-muted sidebar-item relative"
                >
                  <FileText className="h-3.5 w-3.5" />
                  <span>Blog</span>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <a
                  href="https://github.com/karrioapi/karrio"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-muted sidebar-item relative"
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
