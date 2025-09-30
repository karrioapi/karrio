import { useRouter } from '@tanstack/react-router'
import { useEffect, useState } from 'react'
import { Bell, Home, Package, Truck } from 'lucide-react'
import type { ReactNode } from 'react';
import { oauth } from '@/lib/oauth'
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
import logo from '@/logo.svg'

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
    <div className="flex items-center gap-2 px-2 py-1.5">
      <img src={logo} alt="JTL App" className="size-6" />
      {state === 'expanded' && (
        <span className="text-sm font-semibold">JTL Shipping</span>
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
    const checkAuth = async () => {
      try {
        const authenticated = await oauth.isAuthenticated()
        if (!authenticated) {
          router.navigate({ to: '/signin' })
          return
        }

        setIsAuthenticated(true)

        const storedUserInfo = localStorage.getItem('karrio_user_info')
        if (storedUserInfo) {
          setUserInfo(JSON.parse(storedUserInfo))
        } else {
          // Fetch fresh user info
          const { accessToken } = oauth.getStoredTokens()
          if (accessToken) {
            try {
              const info = await oauth.getUserInfo(accessToken)
              setUserInfo({ name: info.name, email: info.email })
              localStorage.setItem('karrio_user_info', JSON.stringify(info))
            } catch (error) {
              console.error('Failed to fetch user info:', error)
            }
          }
        }
      } catch (error) {
        console.error('Authentication check failed:', error)
        router.navigate({ to: '/signin' })
      }
    }

    checkAuth()
  }, [router])

  const handleLogout = () => {
    oauth.clearTokens()
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('karrio_user_info')
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
      name: 'Carriers',
      icon: Package,
      to: '/carriers',
      current: currentPage === 'carriers',
    },
    {
      name: 'Shipment Methods',
      icon: Truck,
      to: '/shipment-methods',
      current: currentPage === 'shipment-methods',
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

      <SidebarInset>
        {/* Top Navigation Bar */}
        <div className="flex h-14 items-center gap-4 border-b px-4">
          <SidebarTrigger />

          {/* Page Title */}
          {pageTitle && <div className="font-medium">{pageTitle}</div>}

          {/* Right side actions */}
          <div className="ml-auto flex items-center gap-2">
            <Button variant="ghost" size="sm">
              <Bell className="h-4 w-4" />
            </Button>

            {userInfo && (
              <div className="flex items-center gap-2 px-2 py-1 text-sm">
                <div className="text-right">
                  <div className="font-medium">{userInfo.name || 'User'}</div>
                  <div className="text-xs text-muted-foreground">
                    {userInfo.email}
                  </div>
                </div>
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  {(userInfo.name || userInfo.email)[0].toUpperCase()}
                </div>
              </div>
            )}

            <Button variant="outline" size="sm" onClick={handleLogout}>
              Logout
            </Button>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          <div className="container mx-auto p-6">
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
