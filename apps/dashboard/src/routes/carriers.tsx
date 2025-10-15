import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import {
  Copy,
  Edit,
  MoreVertical,
  Package,
  Plus,
  Search,
  Trash2,
  User,
  Users,
} from 'lucide-react'
import { toast } from 'sonner'
import type { CarrierConnection } from '@/hooks/useCarriers'
import {
  useCarrierConnections,
  useCreateCarrierConnection,
  useDeleteCarrierConnection,
  useSystemConnections,
  useUpdateCarrierConnection,
  useUpdateSystemConnection,
} from '@/hooks/useCarriers'
import { Shell } from '@/components/layouts/shell'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { CarrierImage } from '@/components/ui/carrier-image'
import { CarrierConnectionDialog } from '@/components/carrier-connection-dialog'
import { StatusBadge } from '@/components/ui/status-badge'
import { ConfirmationDialog } from '@/components/ui/confirmation-dialog'
import { Switch } from '@/components/ui/switch'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export const Route = createFileRoute('/carriers')({
  component: CarriersPage,
  head: () => ({
    meta: [{ title: 'Carrier Connections - JTL Shipping' }],
  }),
})

type FilterType = 'all' | 'active' | 'inactive'

function CarriersPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filter, setFilter] = useState<FilterType>('all')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [selectedConnection, setSelectedConnection] =
    useState<CarrierConnection | null>(null)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [connectionToDelete, setConnectionToDelete] = useState<string | null>(null)

  const {
    data: userConnections,
    isLoading: isLoadingUser,
    error: userError,
    refetch: refetchUserConnections,
  } = useCarrierConnections()
  const {
    data: systemConnections,
    isLoading: isLoadingSystem,
    error: systemError,
  } = useSystemConnections()
  const deleteConnection = useDeleteCarrierConnection()
  const updateConnection = useUpdateCarrierConnection()
  const updateSystemConnection = useUpdateSystemConnection()
  const createConnection = useCreateCarrierConnection()

  const handleToggleConnection = async (
    connection: CarrierConnection,
    isSystemCarrier: boolean = false,
  ) => {
    try {
      if (isSystemCarrier) {
        await updateSystemConnection.mutateAsync({
          id: connection.id,
          active: !connection.active,
        })
      } else {
        await updateConnection.mutateAsync({
          id: connection.id,
          active: !connection.active,
        })
      }
      toast.success(
        `Carrier ${connection.active ? 'deactivated' : 'activated'} successfully`
      )
    } catch (error: any) {
      toast.error(error?.message || 'Failed to toggle connection')
    }
  }

  const handleDeleteConnection = async (id: string) => {
    try {
      await deleteConnection.mutateAsync(id)
      toast.success('Carrier connection deleted successfully')
      setDeleteDialogOpen(false)
      setConnectionToDelete(null)
    } catch (error: any) {
      toast.error(error?.message || 'Failed to delete connection')
    }
  }

  const handleCopyId = (carrierId: string) => {
    navigator.clipboard.writeText(carrierId)
    toast.success('Carrier ID copied to clipboard')
  }

  const handleAddConnection = () => {
    setSelectedConnection(null)
    setDialogOpen(true)
  }

  const handleEditConnection = (connection: CarrierConnection) => {
    setSelectedConnection(connection)
    setDialogOpen(true)
  }

  const handleDialogSubmit = async (
    values: any,
    connection: CarrierConnection | null,
  ) => {
    try {
      if (connection) {
        // Remove carrier_name from update payload as it's not accepted by UpdateCarrierConnectionMutationInput
        const { carrier_name, ...updateData } = values
        await updateConnection.mutateAsync({
          id: connection.id,
          ...updateData,
        })
      } else {
        await createConnection.mutateAsync(values)
      }
      await refetchUserConnections()
    } catch (error) {
      throw error
    }
  }

  const handleDialogSuccess = () => {
    setDialogOpen(false)
    setSelectedConnection(null)
  }

  const filterConnections = (connections: Array<CarrierConnection>) => {
    let filtered = connections

    // Apply status filter
    if (filter === 'active') {
      filtered = filtered.filter((c) => c.active)
    } else if (filter === 'inactive') {
      filtered = filtered.filter((c) => !c.active)
    }

    // Apply search filter (search by name and carrier_id)
    if (searchTerm) {
      filtered = filtered.filter(
        (connection) =>
          connection.display_name
            .toLowerCase()
            .includes(searchTerm.toLowerCase()) ||
          connection.carrier_name
            .toLowerCase()
            .includes(searchTerm.toLowerCase()) ||
          connection.carrier_id?.toLowerCase().includes(searchTerm.toLowerCase()),
      )
    }

    return filtered
  }

  const renderCarrierCard = (
    connection: CarrierConnection,
    isSystemCarrier: boolean = false,
  ) => {
    const capabilities = connection.capabilities || []
    const visibleCapabilities = capabilities.slice(0, 2)
    const remainingCount = capabilities.length - 2

    return (
      <Card
        key={connection.id}
        className={`relative group hover:shadow-lg transition-shadow duration-200 border-l-4 min-w-[320px] ${
          connection.active
            ? 'border-l-green-500'
            : 'border-l-gray-300 dark:border-l-gray-700'
        } ${isSystemCarrier ? 'border-orange-200 dark:border-orange-800 bg-orange-50/30 dark:bg-orange-950/30' : ''}`}
      >
        <CardContent className="p-6">
          {/* Header with carrier info and status */}
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-start gap-4 flex-1">
              <div className="relative">
                <CarrierImage
                  carrierName={connection.carrier_name}
                  size="lg"
                  fallbackBackground={isSystemCarrier ? '#ea580c' : '#2563eb'}
                  className="rounded-xl shadow-sm"
                />
                {/* Status indicator */}
                <div
                  className={`absolute -top-1 -right-1 w-4 h-4 rounded-full border-2 border-background ${connection.active ? 'bg-green-500 dark:bg-green-400' : 'bg-muted'}`}
                />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-lg text-foreground truncate">
                    {connection.display_name}
                  </h3>
                  {isSystemCarrier && (
                    <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-orange-100 dark:bg-orange-950 text-orange-800 dark:text-orange-200 ml-2 shrink-0">
                      <Users className="w-3 h-3 mr-1" />
                      System
                    </span>
                  )}
                </div>
                <p className="text-sm text-muted-foreground mb-2 font-medium">
                  {connection.carrier_name}
                </p>
                <div className="flex items-center gap-2 text-sm flex-wrap">
                  <StatusBadge
                    status={connection.active ? 'active' : 'inactive'}
                  />
                  <StatusBadge
                    status={connection.test_mode ? 'test' : 'live'}
                  />
                </div>
              </div>
            </div>

            {/* Actions dropdown */}
            {!isSystemCarrier && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem onClick={() => handleEditConnection(connection)}>
                    <Edit className="h-4 w-4 mr-2" />
                    Edit
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    onClick={() => handleCopyId(connection.carrier_id || '')}
                  >
                    <Copy className="h-4 w-4 mr-2" />
                    Copy ID
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    variant="destructive"
                    onClick={() => {
                      setConnectionToDelete(connection.id)
                      setDeleteDialogOpen(true)
                    }}
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
          </div>

          {/* Capabilities and details */}
          <div className="mb-6">
            {capabilities.length > 0 && (
              <div className="mb-4">
                <span className="text-sm font-medium text-muted-foreground mr-2">
                  Capabilities:
                </span>
                <div className="inline-flex gap-2 flex-wrap mt-2">
                  {visibleCapabilities.map((capability) => (
                    <StatusBadge
                      key={capability}
                      status={capability}
                      variant="secondary"
                    />
                  ))}
                  {remainingCount > 0 && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-muted text-muted-foreground">
                      +{remainingCount} more
                    </span>
                  )}
                </div>
              </div>
            )}

            <div className="flex flex-col gap-3">
              <div className="flex items-center justify-between p-3 bg-card rounded-lg border">
                <span className="text-sm font-medium text-muted-foreground">
                  Carrier ID
                </span>
                <span className="font-semibold text-foreground text-xs font-mono truncate ml-2">
                  {connection.carrier_id || 'N/A'}
                </span>
              </div>
              <div className="flex items-center justify-between p-3 bg-card rounded-lg border">
                <span className="text-sm font-medium text-muted-foreground">
                  Status
                </span>
                <Switch
                  checked={connection.active}
                  onCheckedChange={() =>
                    handleToggleConnection(connection, isSystemCarrier)
                  }
                  disabled={updateConnection.isPending || isSystemCarrier}
                />
              </div>
            </div>
          </div>

          {/* System carrier info */}
          {isSystemCarrier && (
            <div className="bg-orange-50 dark:bg-orange-950 border border-orange-200 dark:border-orange-800 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Users className="h-4 w-4 text-orange-600 dark:text-orange-400" />
                <span className="text-sm font-medium text-orange-800 dark:text-orange-200">
                  System Managed Carrier
                </span>
              </div>
              <p className="text-xs text-orange-700 dark:text-orange-300">
                This carrier is managed by the system administrator. Configuration
                and credentials cannot be modified.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    )
  }

  const filteredUserConnections = filterConnections(
    userConnections?.connections || [],
  )
  const filteredSystemConnections = filterConnections(
    systemConnections?.connections || [],
  )

  return (
    <Shell
      currentPage="carriers"
      pageTitle="Carrier Connections"
      pageDescription="Manage your shipping carrier connections and credentials"
    >
      {/* Header Actions */}
      <div className="flex items-center justify-between mb-6">
        <div></div>
        <Button onClick={handleAddConnection}>
          <Plus className="h-4 w-4 mr-2" />
          Add Carrier
        </Button>
      </div>

      {/* Search and Filters */}
      <div className="flex items-center gap-4 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search carriers by name or ID..."
            className="pl-8"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <Select
          value={filter}
          onValueChange={(value: FilterType) => setFilter(value)}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filter by status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Carriers</SelectItem>
            <SelectItem value="active">Active Only</SelectItem>
            <SelectItem value="inactive">Inactive Only</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Error States */}
      {(userError || systemError) && (
        <Alert variant="destructive" className="mb-6">
          <AlertDescription>
            Failed to load carrier connections. Please try again.
          </AlertDescription>
        </Alert>
      )}

      {/* Loading State */}
      {(isLoadingUser || isLoadingSystem) && (
        <div className="text-center py-8">
          <div className="text-lg">Loading carrier connections...</div>
        </div>
      )}

      {/* Carrier Connections Tabs */}
      {!isLoadingUser && !isLoadingSystem && (
        <Tabs defaultValue="user" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="user" className="flex items-center gap-2">
              <User className="h-4 w-4" />
              My Carriers ({filteredUserConnections.length})
            </TabsTrigger>
            <TabsTrigger value="system" className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              System Carriers ({filteredSystemConnections.length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="user" className="mt-6">
            <div className="grid gap-6 grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
              {filteredUserConnections.map((connection) =>
                renderCarrierCard(connection, false),
              )}

              {filteredUserConnections.length === 0 && (
                <div className="col-span-full text-center py-16">
                  <div className="bg-primary/10 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-6">
                    <Package className="h-12 w-12 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3 text-foreground">
                    No user carrier connections found
                  </h3>
                  <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                    {searchTerm || filter !== 'all'
                      ? 'No user carriers match your search or filter criteria. Try adjusting your search terms.'
                      : 'Get started by connecting your first shipping carrier to begin processing shipments.'}
                  </p>
                  <Button className="px-6 py-2" onClick={handleAddConnection}>
                    <Plus className="h-4 w-4 mr-2" />
                    Add Your First Carrier
                  </Button>
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="system" className="mt-6">
            <div className="grid gap-6 grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
              {filteredSystemConnections.map((connection) =>
                renderCarrierCard(connection, true),
              )}

              {filteredSystemConnections.length === 0 && (
                <div className="col-span-full text-center py-16">
                  <div className="bg-orange-50 dark:bg-orange-950 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-6">
                    <Users className="h-12 w-12 text-orange-600 dark:text-orange-400" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3 text-foreground">
                    No system carrier connections found
                  </h3>
                  <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                    {searchTerm || filter !== 'all'
                      ? 'No system carriers match your search or filter criteria. Try adjusting your search terms.'
                      : 'No system carriers are currently configured by the administrator.'}
                  </p>
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      )}

      {/* Carrier Connection Dialog */}
      <CarrierConnectionDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        selectedConnection={selectedConnection}
        onSubmit={handleDialogSubmit}
        onSuccess={handleDialogSuccess}
      />

      {/* Delete Confirmation Dialog */}
      <ConfirmationDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        title="Delete Carrier Connection"
        description="Are you sure you want to delete this carrier connection? This action cannot be undone."
        confirmLabel="Delete"
        cancelLabel="Cancel"
        onConfirm={() => connectionToDelete && handleDeleteConnection(connectionToDelete)}
        isLoading={deleteConnection.isPending}
      />
    </Shell>
  )
}
