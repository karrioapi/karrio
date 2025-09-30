import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { Clock, Edit, Eye, Package, Plus, Truck, X } from 'lucide-react'
import { Shell } from '@/components/layouts/shell'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { CarrierImage } from '@/components/ui/carrier-image'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ShipmentMethodDialog } from '@/components/shipment-method-dialog'
import type { ShipmentMethod } from '@/types/shipment-methods'

export const Route = createFileRoute('/shipment-methods')({
  component: ShipmentMethodsPage,
})

// Legacy interface for mock data - will be replaced with real ShipmentMethod type
interface MockShipmentMethod {
  id: string
  name: string
  carrierName: string
  description: string
  price: string
  currency: string
  deliveryDays: string
  features: Array<string>
  additionalCharges?: Array<{
    name: string
    price: string
  }>
  enabled?: boolean
}

// Mock data based on the screenshot
const mockAvailableShipmentMethods: Array<MockShipmentMethod> = [
  {
    id: '1',
    name: 'Parcel',
    carrierName: 'GLS',
    description: 'Standard delivery, tracking included',
    price: '4.99',
    currency: '€',
    deliveryDays: '2-4 Days Delivery',
    features: ['Standard delivery', 'tracking included'],
  },
  {
    id: '2',
    name: 'Express',
    carrierName: 'GLS',
    description: 'Next day delivery, premium tracking',
    price: '12.99',
    currency: '€',
    deliveryDays: '1 Day Delivery',
    features: ['Next day delivery', 'premium tracking'],
  },
  {
    id: '3',
    name: 'Parcel + Signature',
    carrierName: 'GLS',
    description: 'Standard delivery with signature required',
    price: '6.99',
    currency: '€',
    deliveryDays: '2-4 Days Delivery',
    features: ['Standard delivery with signature required'],
    additionalCharges: [{ name: 'Signature Required', price: '€0.60' }],
  },
]

const mockMyShipmentMethods: Array<MockShipmentMethod> = [
  {
    id: '4',
    name: 'Parcel + Return + Notification',
    carrierName: 'GLS',
    description: 'Standard delivery with return option and notifications',
    price: '8.99',
    currency: '€',
    deliveryDays: '2-4 Days Delivery',
    features: ['Standard delivery with return option and notifications'],
    additionalCharges: [{ name: 'Shop Return', price: '€1.25' }],
    enabled: true,
  },
]

function ShipmentMethodCard({
  method,
  isMyMethod = false,
  onToggle,
  onView,
  onEdit,
}: {
  method: MockShipmentMethod
  isMyMethod?: boolean
  onToggle?: () => void
  onView?: () => void
  onEdit?: () => void
}) {
  const enabled = method.enabled ?? !isMyMethod

  return (
    <Card
      className={`relative group hover:shadow-lg transition-shadow duration-200 min-w-[300px] ${
        isMyMethod
          ? 'border-green-200 bg-green-50/30'
          : enabled
          ? 'border-blue-200 bg-blue-50/30'
          : 'border-gray-200 bg-gray-50/30'
      }`}
    >
      <CardContent className="p-6">
        {/* Header with carrier info and pricing */}
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-start gap-4">
            <div className="relative">
              <CarrierImage
                carrierName={method.carrierName}
                size="lg"
                fallbackBackground={isMyMethod ? '#16a34a' : '#2563eb'}
                className="rounded-xl shadow-sm"
              />
              {/* Status indicator */}
              <div className={`absolute -top-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${
                enabled ? 'bg-green-500' : 'bg-gray-400'
              }`} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-semibold text-lg text-gray-900 truncate">
                  {method.name}
                </h3>
                {isMyMethod && (
                  <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800 ml-2">
                    <Package className="w-3 h-3 mr-1" />
                    My Method
                  </span>
                )}
              </div>
              <p className="text-sm text-gray-600 mb-2 font-medium">
                {method.carrierName} • {method.currency}{method.price}
              </p>
              <div className="flex items-center gap-4 text-sm">
                <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full font-medium ${
                  enabled
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-100 text-gray-600'
                }`}>
                  <div className={`w-2 h-2 rounded-full ${enabled ? 'bg-green-500' : 'bg-gray-400'}`} />
                  {enabled ? 'Available' : 'Disabled'}
                </span>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700">
                  <Clock className="w-3 h-3" />
                  {method.deliveryDays}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Service details */}
        <div className="mb-6">
          <p className="text-sm text-gray-600 mb-4">{method.description}</p>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-100">
              <span className="text-sm font-medium text-gray-600">Features</span>
              <span className="font-semibold text-gray-900">{method.features.length}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-100">
              <span className="text-sm font-medium text-gray-600">Base Rate</span>
              <span className="font-semibold text-gray-900">{method.currency}{method.price}</span>
            </div>
          </div>

          {/* Features list */}
          {method.features.length > 0 && (
            <div className="mb-4">
              <div className="flex flex-wrap gap-1">
                {method.features.slice(0, 3).map((feature, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700"
                  >
                    {feature}
                  </span>
                ))}
                {method.features.length > 3 && (
                  <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-500">
                    +{method.features.length - 3} more
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Additional charges */}
          {method.additionalCharges && method.additionalCharges.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-gray-700">Additional Charges:</h4>
              {method.additionalCharges.map((charge, index) => (
                <div key={index} className="flex justify-between text-sm p-2 bg-gray-50 rounded">
                  <span className="text-gray-600">{charge.name}</span>
                  <span className="font-medium text-gray-900">{charge.price}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            className="flex-1"
            onClick={onView}
          >
            <Eye className="h-4 w-4 mr-2" />
            View
          </Button>
          {isMyMethod && (
            <Button
              variant="outline"
              size="sm"
              className="flex-1"
              onClick={onEdit}
            >
              <Edit className="h-4 w-4 mr-2" />
              Edit
            </Button>
          )}
          {!isMyMethod ? (
            <Button
              variant={enabled ? "outline" : "default"}
              size="sm"
              className="flex-1"
              onClick={onToggle}
            >
              {enabled ? (
                <>
                  <X className="h-4 w-4 mr-2" />
                  Disable
                </>
              ) : (
                <>
                  <Plus className="h-4 w-4 mr-2" />
                  Enable
                </>
              )}
            </Button>
          ) : (
            <Button
              size="sm"
              className="flex-1 bg-blue-600 hover:bg-blue-700"
              onClick={onToggle}
            >
              <Plus className="h-4 w-4 mr-2" />
              Upgrade
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

function ShipmentMethodsPage() {
  const [selectedCarrier, setSelectedCarrier] = useState<string>('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [selectedMethod, setSelectedMethod] = useState<ShipmentMethod | null>(null)

  const handleAddMethod = () => {
    setSelectedMethod(null)
    setDialogOpen(true)
  }

  const handleEditMethod = (method: MockShipmentMethod) => {
    // Convert mock method to real ShipmentMethod type for editing
    // This is temporary - in real implementation, methods would already be the correct type
    const realMethod: ShipmentMethod = {
      id: method.id,
      name: method.name,
      display_name: method.name,
      description: method.description,
      connection_id: '', // Would come from real data
      connection_name: method.carrierName,
      carrier_id: method.carrierName.toLowerCase(),
      carrier_name: method.carrierName,
      service_code: method.name.toLowerCase().replace(/\s+/g, '_'),
      service_name: method.name,
      active: method.enabled || false,
      currency: method.currency.replace(/[€$£¥]/g, '') || 'EUR',
      base_rate: parseFloat(method.price) || 0,
      pricing_zones: [],
      shipping_options: [],
      estimated_delivery_days: {
        min: 2,
        max: 4,
      },
      features: method.features,
      additional_charges: method.additionalCharges?.map(charge => ({
        name: charge.name,
        amount: parseFloat(charge.price.replace(/[€$£¥]/g, '')) || 0,
        currency: method.currency.replace(/[€$£¥]/g, '') || 'EUR',
      })) || [],
    }
    setSelectedMethod(realMethod)
    setDialogOpen(true)
  }

  const handleDialogSubmit = async (values: any, method: ShipmentMethod | null) => {
    try {
      // TODO: Implement actual API call
      console.log('Saving shipment method:', values, method)
      // In real implementation, this would call the GraphQL mutation
    } catch (error) {
      console.error('Failed to save shipment method:', error)
      throw error
    }
  }

  const handleDialogSuccess = () => {
    setDialogOpen(false)
    setSelectedMethod(null)
    // TODO: Refetch data
  }

  return (
    <Shell
      currentPage="shipment-methods"
      pageTitle="Shipment Methods"
      pageDescription="Manage available and configured shipment methods"
    >
      {/* API Notice */}
      <Alert className="mb-6">
        <AlertDescription>
          <strong>Note:</strong> This page displays mock data as the API is not
          ready yet. The actual implementation will connect to real shipment
          method data.
        </AlertDescription>
      </Alert>

      {/* Shipment Methods Tabs */}
      <Tabs defaultValue="available" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="available" className="flex items-center gap-2">
            Available Shipment Methods ({mockAvailableShipmentMethods.length})
          </TabsTrigger>
          <TabsTrigger value="my-methods" className="flex items-center gap-2">
            My Shipment Methods ({mockMyShipmentMethods.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="available" className="mt-6">
          <div className="space-y-6">
            {/* Carrier Filter */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <Select
                  value={selectedCarrier}
                  onValueChange={setSelectedCarrier}
                >
                  <SelectTrigger className="w-[200px]">
                    <SelectValue placeholder="Select carrier" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Carriers</SelectItem>
                    <SelectItem value="gls">GLS</SelectItem>
                    <SelectItem value="dhl">DHL</SelectItem>
                    <SelectItem value="ups">UPS</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button className="bg-blue-600 hover:bg-blue-700">
                Enable All
              </Button>
            </div>

            {/* Available Methods Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {mockAvailableShipmentMethods.map((method) => (
                <ShipmentMethodCard
                  key={method.id}
                  method={method}
                  onView={() => console.log('View method:', method.id)}
                  onToggle={() => console.log('Toggle method:', method.id)}
                />
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="my-methods" className="mt-6">
          <div className="space-y-6">
            {/* My Methods Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {mockMyShipmentMethods.map((method) => (
                <ShipmentMethodCard
                  key={method.id}
                  method={method}
                  isMyMethod
                  onView={() => console.log('View my method:', method.id)}
                  onEdit={() => handleEditMethod(method)}
                  onToggle={() => console.log('Upgrade method:', method.id)}
                />
              ))}
            </div>

            {mockMyShipmentMethods.length === 0 && (
              <div className="text-center py-12">
                <Truck className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">
                  No shipment methods configured
                </h3>
                <p className="text-muted-foreground mb-4">
                  Configure your first shipment method from the available
                  options.
                </p>
                <Button
                  className="bg-blue-600 hover:bg-blue-700"
                  onClick={handleAddMethod}
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Method
                </Button>
              </div>
            )}
          </div>
        </TabsContent>
      </Tabs>

      {/* Shipment Method Dialog */}
      <ShipmentMethodDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        selectedMethod={selectedMethod}
        onSubmit={handleDialogSubmit}
        onSuccess={handleDialogSuccess}
      />
    </Shell>
  )
}
