import { useEffect, useState } from 'react'
import { Check, ChevronsUpDown, Building2 } from 'lucide-react'
import { authManager, type AuthResponse } from '@/lib/auth'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'

export function OrgSwitcher() {
  const [currentOrg, setCurrentOrg] = useState<AuthResponse['org'] | null>(null)
  const [organizations, setOrganizations] = useState<AuthResponse['org'][]>([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    // Load current organization
    const auth = authManager.getStoredAuth()
    if (auth?.org) {
      setCurrentOrg(auth.org)
    }

    // Fetch all organizations
    const loadOrganizations = async () => {
      try {
        setIsLoading(true)
        const orgs = await authManager.fetchOrganizations()
        setOrganizations(orgs)
      } catch (error) {
        console.error('Failed to load organizations:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadOrganizations()
  }, [])

  const handleOrgSwitch = (org: AuthResponse['org']) => {
    authManager.setCurrentOrg(org)
    setCurrentOrg(org)
    // Reload the page to apply the new organization context
    window.location.reload()
  }

  if (!currentOrg && organizations.length === 0) {
    return null
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          size="sm"
          className="h-8 gap-2 text-sm"
          disabled={isLoading}
        >
          <Building2 className="h-4 w-4" />
          <span className="hidden sm:inline">
            {currentOrg?.name || 'Select Organization'}
          </span>
          <ChevronsUpDown className="h-4 w-4 opacity-50" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel>Organizations</DropdownMenuLabel>
        <DropdownMenuSeparator />
        {organizations.map((org) => (
          <DropdownMenuItem
            key={org.id}
            onClick={() => handleOrgSwitch(org)}
            className="gap-2"
          >
            <Check
              className={`h-4 w-4 ${
                currentOrg?.id === org.id ? 'opacity-100' : 'opacity-0'
              }`}
            />
            <div className="flex flex-col gap-1">
              <span className="font-medium">{org.name}</span>
              {org.slug && (
                <span className="text-xs text-muted-foreground">{org.slug}</span>
              )}
            </div>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
