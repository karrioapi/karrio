import { useRouter } from '@tanstack/react-router'
import { useEffect, useState } from 'react'
import { Bell, Home, LogOut, Package, Truck } from 'lucide-react'
import type { ReactNode } from 'react';
import { authManager } from '@/lib/auth'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarRail,
  SidebarTrigger,
  useSidebar,
} from '@/components/ui/sidebar'
import { Button } from '@/components/ui/button'

interface ShellProps {
  children: ReactNode
  currentPage: string
  pageTitle?: string
  pageDescription?: string
}

interface NavigationItem {
  name: string
  icon: React.ComponentType<{ className?: string }>
  to: string
  current: boolean
}

interface UserInfo {
  name: string
  email: string
}

function SidebarHeaderContent() {
  const { state } = useSidebar()

  return (
    <div className="flex items-center justify-center px-2 py-3">
      {state === 'expanded' ? (
        <img src="/logo.svg" alt="JTL Shipping" className="h-8 w-auto" />
      ) : (
        <img src="/icon.svg" alt="JTL" className="h-9 w-auto" />
      )}
    </div>
  )
}

export function Shell({
  children,
  currentPage,
  pageTitle,
  pageDescription,
}: ShellProps) {
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null)

  useEffect(() => {
    const checkAuth = () => {
      try {
        const authenticated = authManager.isAuthenticated()
        if (!authenticated) {
          router.navigate({ to: '/signin' })
          return
        }

        setIsAuthenticated(true)

        // Get user info from stored auth
        const auth = authManager.getStoredAuth()
        if (auth.user) {
          const fullName = auth.user.first_name && auth.user.last_name
            ? `${auth.user.first_name} ${auth.user.last_name}`.trim()
            : auth.user.first_name || auth.user.last_name || auth.user.email

          setUserInfo({
            name: fullName,
            email: auth.user.email,
          })
        }
      } catch (error) {
        console.error('Authentication check failed:', error)
        router.navigate({ to: '/signin' })
      }
    }

    checkAuth()
  }, [router])

  const handleLogout = () => {
    authManager.logout()
    router.navigate({ to: '/signin' })
  }

  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  const navigation: Array<NavigationItem> = [
    {
      name: 'Dashboard',
      icon: Home,
      to: '/dashboard',
      current: currentPage === 'dashboard',
    },
    {
      name: 'Carrier Connections',
      icon: Package,
      to: '/carriers',
      current: currentPage === 'carriers',
    },
    {
      name: 'Shipping Methods',
      icon: Truck,
      to: '/shipping-methods',
      current: currentPage === 'shipping-methods',
    },
  ]

  return (
    <SidebarProvider>
      <Sidebar variant="inset" collapsible="icon">
        <SidebarHeader>
          <SidebarHeaderContent />
        </SidebarHeader>

        <SidebarContent>
          <SidebarGroup>
            <SidebarGroupLabel>Navigation</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {navigation.map((item) => (
                  <SidebarMenuItem key={item.name}>
                    <SidebarMenuButton
                      asChild
                      tooltip={item.name}
                      isActive={item.current}
                    >
                      <a
                        href="#"
                        onClick={(e) => {
                          e.preventDefault()
                          router.navigate({ to: item.to as any })
                        }}
                        className="flex items-center gap-3"
                      >
                        <item.icon className="h-4 w-4" />
                        <span>{item.name}</span>
                      </a>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>

        <SidebarFooter>
          <div className="text-xs text-muted-foreground px-2">v1.0.0</div>
        </SidebarFooter>

        <SidebarRail />
      </Sidebar>

      <SidebarInset className="bg-background">
        {/* Top Navigation Bar */}
        <div className="flex h-14 items-center gap-2 sm:gap-4 border-b px-2 sm:px-4 bg-background">
          <SidebarTrigger />

          {/* Page Title - hidden on small screens */}
          {pageTitle && <div className="font-medium hidden md:block">{pageTitle}</div>}

          {/* Right side actions */}
          <div className="ml-auto flex items-center gap-1 sm:gap-2">
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
              <Bell className="h-4 w-4" />
            </Button>

            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" onClick={handleLogout} title="Logout">
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto bg-background">
          <div className="container mx-auto p-6 bg-background">
            {/* Page Header */}
            {(pageTitle || pageDescription) && (
              <div className="mb-6">
                {pageTitle && (
                  <h1 className="text-2xl font-bold tracking-tight">
                    {pageTitle}
                  </h1>
                )}
                {pageDescription && (
                  <p className="text-muted-foreground">{pageDescription}</p>
                )}
              </div>
            )}

            {/* Page Content */}
            {children}
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}
