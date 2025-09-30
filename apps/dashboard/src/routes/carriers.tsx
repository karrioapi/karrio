import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import {
  Edit,
  Package,
  Plus,
  Power,
  Search,
  Settings,
  Trash2,
  User,
  Users,
} from 'lucide-react'
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

export const Route = createFileRoute('/carriers')({
  component: CarriersPage,
})

function CarriersPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [selectedConnection, setSelectedConnection] =
    useState<CarrierConnection | null>(null)

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
    } catch (error) {
      console.error('Failed to toggle connection:', error)
    }
  }

  const handleDeleteConnection = async (id: string) => {
    if (
      window.confirm('Are you sure you want to delete this carrier connection?')
    ) {
      try {
        await deleteConnection.mutateAsync(id)
      } catch (error) {
        console.error('Failed to delete connection:', error)
      }
    }
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
        await updateConnection.mutateAsync({
          id: connection.id,
          ...values,
        })
      } else {
        await createConnection.mutateAsync(values)
      }
      await refetchUserConnections()
    } catch (error) {
      console.error('Failed to save carrier connection:', error)
      throw error
    }
  }

  const handleDialogSuccess = () => {
    setDialogOpen(false)
    setSelectedConnection(null)
  }

  const filterConnections = (connections: Array<CarrierConnection>) => {
    return connections.filter(
      (connection) =>
        connection.display_name
          .toLowerCase()
          .includes(searchTerm.toLowerCase()) ||
        connection.carrier_name
          .toLowerCase()
          .includes(searchTerm.toLowerCase()),
    )
  }

  const renderCarrierCard = (
    connection: CarrierConnection,
    isSystemCarrier: boolean = false,
  ) => {
    return (
      <Card
        key={connection.id}
        className={`relative group hover:shadow-lg transition-shadow duration-200 ${isSystemCarrier ? 'border-orange-200 bg-orange-50/30' : 'border-blue-200 bg-blue-50/30'}`}
      >
        <CardContent className="p-6">
          {/* Header with carrier info and status */}
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-start gap-4">
              <div className="relative">
                <CarrierImage
                  carrierName={connection.carrier_name}
                  size="lg"
                  fallbackBackground={isSystemCarrier ? '#ea580c' : '#2563eb'}
                  className="rounded-xl shadow-sm"
                />
                {/* Status indicator */}
                <div
                  className={`absolute -top-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${connection.active ? 'bg-green-500' : 'bg-gray-400'}`}
                />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-lg text-gray-900 truncate">
                    {connection.display_name}
                  </h3>
                  {isSystemCarrier && (
                    <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-orange-100 text-orange-800 ml-2">
                      <Users className="w-3 h-3 mr-1" />
                      System
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-600 mb-2 font-medium">
                  {connection.carrier_name}
                </p>
                <div className="flex items-center gap-4 text-sm">
                  <span
                    className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full font-medium ${
                      connection.active
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    <div
                      className={`w-2 h-2 rounded-full ${connection.active ? 'bg-green-500' : 'bg-gray-400'}`}
                    />
                    {connection.active ? 'Active' : 'Inactive'}
                  </span>
                  <span
                    className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${
                      connection.test_mode
                        ? 'bg-yellow-100 text-yellow-700'
                        : 'bg-blue-100 text-blue-700'
                    }`}
                  >
                    {connection.test_mode ? 'Test Mode' : 'Live Mode'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Capabilities and details */}
          <div className="mb-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-100">
                <span className="text-sm font-medium text-gray-600">
                  Capabilities
                </span>
                <span className="font-semibold text-gray-900">
                  {connection.capabilities.length || 0}
                </span>
              </div>
              <div className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-100">
                <span className="text-sm font-medium text-gray-600">
                  Carrier ID
                </span>
                <span className="font-semibold text-gray-900 text-xs font-mono">
                  {connection.carrier_id || 'N/A'}
                </span>
              </div>
            </div>
          </div>

          {/* Actions */}
          {!isSystemCarrier ? (
            <div className="flex items-center gap-2">
              <Button
                variant={connection.active ? 'outline' : 'default'}
                size="sm"
                onClick={() => handleToggleConnection(connection, false)}
                disabled={updateConnection.isPending}
                className="flex-1"
              >
                <Power className="h-4 w-4 mr-2" />
                {connection.active ? 'Deactivate' : 'Activate'}
              </Button>
              <Button
                variant="outline"
                size="sm"
                className="flex-1"
                onClick={() => handleEditConnection(connection)}
              >
                <Edit className="h-4 w-4 mr-2" />
                Edit
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleDeleteConnection(connection.id)}
                disabled={deleteConnection.isPending}
                className="text-red-600 hover:text-red-700 hover:bg-red-50"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ) : (
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Users className="h-4 w-4 text-orange-600" />
                <span className="text-sm font-medium text-orange-800">
                  System Managed Carrier
                </span>
              </div>
              <p className="text-xs text-orange-700">
                This carrier is managed by the system administrator.
                Configuration and credentials cannot be modified.
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
        <Button
          className="bg-blue-600 hover:bg-blue-700"
          onClick={handleAddConnection}
        >
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
            placeholder="Search carriers..."
            className="pl-8"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
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
            <div className="grid gap-6 md:grid-cols-2">
              {filteredUserConnections.map((connection) =>
                renderCarrierCard(connection, false),
              )}

              {filteredUserConnections.length === 0 && (
                <div className="col-span-full text-center py-16">
                  <div className="bg-blue-50 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-6">
                    <Package className="h-12 w-12 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3 text-gray-900">
                    No user carrier connections found
                  </h3>
                  <p className="text-gray-600 mb-6 max-w-md mx-auto">
                    {searchTerm
                      ? 'No user carriers match your search. Try adjusting your search terms.'
                      : 'Get started by connecting your first shipping carrier to begin processing shipments.'}
                  </p>
                  <Button
                    className="bg-blue-600 hover:bg-blue-700 px-6 py-2"
                    onClick={handleAddConnection}
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Add Your First Carrier
                  </Button>
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="system" className="mt-6">
            <div className="grid gap-6 md:grid-cols-2">
              {filteredSystemConnections.map((connection) =>
                renderCarrierCard(connection, true),
              )}

              {filteredSystemConnections.length === 0 && (
                <div className="col-span-full text-center py-16">
                  <div className="bg-orange-50 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-6">
                    <Users className="h-12 w-12 text-orange-600" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3 text-gray-900">
                    No system carrier connections found
                  </h3>
                  <p className="text-gray-600 mb-6 max-w-md mx-auto">
                    {searchTerm
                      ? 'No system carriers match your search. Try adjusting your search terms.'
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
    </Shell>
  )
}
