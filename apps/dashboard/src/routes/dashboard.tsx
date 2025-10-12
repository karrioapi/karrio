import { createFileRoute, useRouter } from '@tanstack/react-router'
import { Activity, Package, TrendingUp, Users } from 'lucide-react'
import { useSystemUsage } from '@/hooks/useUsage'
import {
  useCarrierConnections,
  useSystemConnections,
} from '@/hooks/useCarriers'
import { Shell } from '@/components/layouts/shell'
import { Button } from '@/components/ui/button'

export const Route = createFileRoute('/dashboard')({
  component: DashboardPage,
})

function DashboardPage() {
  const router = useRouter()

  // Fetch system usage and carrier data
  const { data: systemUsage, isLoading: isLoadingUsage } = useSystemUsage()
  const { data: userConnections, isLoading: isLoadingUserCarriers } =
    useCarrierConnections()
  const { data: systemConnections, isLoading: isLoadingSystemCarriers } =
    useSystemConnections()

  const allCarrierConnections = [
    ...(userConnections?.connections || []),
    ...(systemConnections?.connections || []),
  ]
  const isLoadingCarriers = isLoadingUserCarriers || isLoadingSystemCarriers

  return (
    <Shell currentPage="dashboard">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome to your JTL Shipping. Here's an overview of your data.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Total Shipments
              </p>
              <p className="text-2xl font-bold">
                {isLoadingUsage
                  ? '...'
                  : systemUsage?.total_shipments.toLocaleString() || '0'}
              </p>
            </div>
            <Package className="h-8 w-8 text-muted-foreground" />
          </div>
        </div>

        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                API Requests
              </p>
              <p className="text-2xl font-bold">
                {isLoadingUsage
                  ? '...'
                  : systemUsage?.total_requests.toLocaleString() || '0'}
              </p>
            </div>
            <Activity className="h-8 w-8 text-muted-foreground" />
          </div>
        </div>

        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Shipping Spend
              </p>
              <p className="text-2xl font-bold">
                {isLoadingUsage
                  ? '...'
                  : `$${systemUsage?.total_shipping_spend.toLocaleString() || '0'}`}
              </p>
            </div>
            <TrendingUp className="h-8 w-8 text-muted-foreground" />
          </div>
        </div>

        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Active Carriers
              </p>
              <p className="text-2xl font-bold">
                {isLoadingCarriers
                  ? '...'
                  : allCarrierConnections.filter((c) => c.active).length || '0'}
              </p>
            </div>
            <Users className="h-8 w-8 text-muted-foreground" />
          </div>
        </div>
      </div>

      {/* Carrier Connections Overview */}
      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium">Carrier Connections</h3>
              <button
                onClick={() => router.navigate({ to: '/carriers' })}
                className="text-sm text-primary hover:underline"
              >
                View all
              </button>
            </div>
            <div className="space-y-3">
              {isLoadingCarriers ? (
                <div className="text-sm text-muted-foreground">
                  Loading carriers...
                </div>
              ) : (
                allCarrierConnections.slice(0, 3).map((connection) => (
                  <div
                    key={connection.id}
                    className="flex items-center justify-between p-3 bg-muted rounded-lg"
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`h-2 w-2 rounded-full ${connection.active ? 'bg-green-500 dark:bg-green-400' : 'bg-muted-foreground'}`}
                      ></div>
                      <div>
                        <p className="font-medium">{connection.display_name}</p>
                        <p className="text-sm text-muted-foreground">
                          {connection.carrier_name}
                        </p>
                      </div>
                    </div>
                    <span
                      className={`text-sm font-medium ${connection.active ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}
                    >
                      {connection.active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                )) || (
                  <div className="text-center py-4">
                    <p className="text-sm text-muted-foreground mb-2">
                      No carriers configured
                    </p>
                    <button
                      onClick={() => router.navigate({ to: '/carriers' })}
                      className="text-sm text-primary hover:underline"
                    >
                      Add your first carrier
                    </button>
                  </div>
                )
              )}
            </div>
          </div>
        </div>

        <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
          <div className="p-6">
            <h3 className="text-lg font-medium mb-4">Usage Overview</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                  Total Errors
                </span>
                <span className="font-medium">
                  {isLoadingUsage
                    ? '...'
                    : systemUsage?.total_errors.toLocaleString() || '0'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                  Order Volume
                </span>
                <span className="font-medium">
                  {isLoadingUsage
                    ? '...'
                    : systemUsage?.order_volume.toLocaleString() || '0'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                  Total Trackers
                </span>
                <span className="font-medium">
                  {isLoadingUsage
                    ? '...'
                    : systemUsage?.total_trackers.toLocaleString() || '0'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Shell>
  )
}
