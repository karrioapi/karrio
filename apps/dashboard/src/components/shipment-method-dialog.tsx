import { useEffect, useState } from 'react'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from './ui/dialog'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from './ui/form'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './ui/select'
import { CarrierImage } from './ui/carrier-image'
import { Button } from './ui/button'
import { Switch } from './ui/switch'
import { Input } from './ui/input'
import { Textarea } from './ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { Trash2, Plus, Settings } from 'lucide-react'
import type {
  ShipmentMethod,
  ShipmentMethodFormData,
  CarrierInfo,
  ShippingService,
  ShippingOption,
} from '@/types/shipment-methods'
import type { CarrierConnection } from '@/hooks/useCarriers'
import { useCarrierConnections } from '@/hooks/useCarriers'
import { useCarrierServices } from '@/hooks/useCarrierReferences'

const formSchema = z.object({
  name: z.string().min(1, { message: 'Name is required' }),
  display_name: z.string().min(1, { message: 'Display name is required' }),
  description: z.string().optional(),
  connection_id: z.string().min(1, { message: 'Connection is required' }),
  service_code: z.string().min(1, { message: 'Service is required' }),
  active: z.boolean(),
  currency: z.string().min(3, { message: 'Currency is required' }),
  base_rate: z.number().min(0).optional(),
  estimated_delivery_days: z
    .object({
      min: z.number().min(1),
      max: z.number().min(1),
    })
    .optional(),
  max_weight: z.number().min(0).optional(),
  max_length: z.number().min(0).optional(),
  max_width: z.number().min(0).optional(),
  max_height: z.number().min(0).optional(),
  shipping_options: z.array(
    z.object({
      code: z.string(),
      name: z.string(),
      value: z.any(),
      enabled: z.boolean(),
    }),
  ),
  supported_countries: z.array(z.string()).optional(),
  metadata: z.record(z.any()).optional(),
})

type FormData = z.infer<typeof formSchema>

interface ShipmentMethodDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  selectedMethod: ShipmentMethod | null
  onSuccess?: () => void
  onSubmit?: (
    values: FormData,
    method: ShipmentMethod | null,
  ) => Promise<void>
}

// Currency options
const currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY']

export function ShipmentMethodDialog({
  open,
  onOpenChange,
  selectedMethod,
  onSuccess,
  onSubmit,
}: ShipmentMethodDialogProps) {
  const [selectedConnection, setSelectedConnection] = useState<string>('')

  // Fetch available carrier connections
  const { data: connectionsData } = useCarrierConnections()
  const connections = connectionsData?.connections || []

  const defaultValues: FormData = {
    name: '',
    display_name: '',
    description: '',
    connection_id: '',
    service_code: '',
    active: true,
    currency: 'USD',
    base_rate: 0,
    estimated_delivery_days: {
      min: 1,
      max: 3,
    },
    shipping_options: [],
    supported_countries: [],
    metadata: {},
  }

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues,
  })

  // Watch form values for dependencies
  const { watch, setValue } = form
  const watchConnectionId = watch('connection_id')

  // Get services and options for the selected connection
  const selectedConnectionData = connections.find((c) => c.id === watchConnectionId)
  const { services, options } = useCarrierServices(selectedConnectionData?.carrier_name)

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'shipping_options',
  })

  const handleSubmit = async (values: FormData) => {
    if (!onSubmit) {
      console.error('No submit handler provided')
      return
    }

    try {
      await onSubmit(values, selectedMethod)
      onSuccess?.()
      onOpenChange(false)
      form.reset(defaultValues)
    } catch (error: any) {
      console.error('Failed to save shipment method:', error)
    }
  }

  useEffect(() => {
    if (open) {
      const initial = selectedMethod
        ? {
            name: selectedMethod.name || '',
            display_name: selectedMethod.display_name || '',
            description: selectedMethod.description || '',
            connection_id: selectedMethod.connection_id || '',
            service_code: selectedMethod.service_code || '',
            active: selectedMethod.active || false,
            currency: selectedMethod.currency || 'USD',
            base_rate: selectedMethod.base_rate || 0,
            estimated_delivery_days: selectedMethod.estimated_delivery_days || {
              min: 1,
              max: 3,
            },
            shipping_options: selectedMethod.shipping_options || [],
            supported_countries: selectedMethod.supported_countries || [],
            metadata: selectedMethod.metadata || {},
          }
        : defaultValues

      form.reset(initial)
      setSelectedConnection(initial.connection_id)
    }
  }, [open, selectedMethod])

  // Auto-generate display name when service changes
  useEffect(() => {
    const subscription = watch((value, { name, type }) => {
      if (name === 'service_code' && type === 'change' && value.service_code) {
        const connection = connections.find((c) => c.id === value.connection_id)
        const service = services.find((s) => s.code === value.service_code)
        if (connection && service && !selectedMethod) {
          setValue('display_name', `${connection.display_name} - ${service.name}`)
          setValue('name', service.code.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()))
        }
      }
    })
    return () => subscription.unsubscribe()
  }, [watch, setValue, selectedMethod, connections, services])

  // Update shipping options when connection changes
  useEffect(() => {
    if (watchConnectionId && !selectedMethod && options.length > 0) {
      const defaultOptions = options.map((option) => ({
        code: option.code,
        name: option.name,
        value: option.default,
        enabled: false,
      }))
      setValue('shipping_options', defaultOptions)
    }
  }, [watchConnectionId, selectedMethod, setValue, options])

  const handleAddShippingOption = () => {
    append({
      code: '',
      name: '',
      value: '',
      enabled: false,
    })
  }

  // Available services and options come from the hook

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] p-0 flex flex-col">
        <DialogHeader className="px-6 py-4 border-b">
          <DialogTitle>
            {selectedMethod ? 'Edit Shipment Method' : 'Create Shipment Method'}
          </DialogTitle>
          <DialogDescription>
            {selectedMethod
              ? `Update ${selectedMethod.display_name} configuration.`
              : 'Configure a new shipment method for your store.'}
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className="flex flex-col flex-1 min-h-0"
          >
            <div className="flex-1 overflow-y-auto">
              <Tabs defaultValue="basic" className="w-full">
                <TabsList className="grid w-full grid-cols-4 mx-6 mt-4">
                  <TabsTrigger value="basic">Basic Info</TabsTrigger>
                  <TabsTrigger value="service">Service Config</TabsTrigger>
                  <TabsTrigger value="pricing">Pricing</TabsTrigger>
                  <TabsTrigger value="options">Options</TabsTrigger>
                </TabsList>

                <TabsContent value="basic" className="px-6 py-4 space-y-6">
                  <div className="grid grid-cols-2 gap-6">
                    <FormField
                      control={form.control}
                      name="connection_id"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>
                            Carrier Connection <span className="text-red-500">*</span>
                          </FormLabel>
                          <Select
                            onValueChange={(value) => {
                              field.onChange(value)
                              setSelectedConnection(value)
                            }}
                            value={field.value || ''}
                            disabled={!!selectedMethod}
                          >
                            <FormControl>
                              <SelectTrigger>
                                <SelectValue placeholder="Select a connection" />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              {connections.map((connection) => (
                                <SelectItem key={connection.id} value={connection.id}>
                                  <div className="flex items-center gap-2">
                                    <CarrierImage
                                      carrierName={connection.carrier_name}
                                      size="sm"
                                      className="rounded"
                                    />
                                    <div className="flex flex-col">
                                      <span className="font-medium">{connection.display_name}</span>
                                      <span className="text-xs text-gray-500">{connection.carrier_name}</span>
                                    </div>
                                    {connection.test_mode && (
                                      <Badge variant="secondary" className="ml-2">
                                        Test
                                      </Badge>
                                    )}
                                  </div>
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    {watchConnectionId && (
                      <FormField
                        control={form.control}
                        name="service_code"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>
                              Service <span className="text-red-500">*</span>
                            </FormLabel>
                            <Select
                              onValueChange={field.onChange}
                              value={field.value || ''}
                            >
                              <FormControl>
                                <SelectTrigger>
                                  <SelectValue placeholder="Select a service" />
                                </SelectTrigger>
                              </FormControl>
                              <SelectContent>
                                {services.map((service) => (
                                  <SelectItem
                                    key={service.code}
                                    value={service.code}
                                  >
                                    {service.name}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    )}
                  </div>

                  <div className="grid grid-cols-2 gap-6">
                    <FormField
                      control={form.control}
                      name="name"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>
                            Method Name <span className="text-red-500">*</span>
                          </FormLabel>
                          <FormControl>
                            <Input {...field} placeholder="Express Delivery" />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="display_name"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>
                            Display Name <span className="text-red-500">*</span>
                          </FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              placeholder="DHL Express - Express Worldwide"
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>

                  <FormField
                    control={form.control}
                    name="description"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Description</FormLabel>
                        <FormControl>
                          <Textarea
                            {...field}
                            placeholder="Fast international delivery with tracking"
                            rows={3}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <div className="flex items-center gap-6">
                    <FormField
                      control={form.control}
                      name="active"
                      render={({ field }) => (
                        <FormItem className="flex items-center gap-2 space-y-0">
                          <FormControl>
                            <Switch
                              checked={field.value}
                              onCheckedChange={field.onChange}
                            />
                          </FormControl>
                          <FormLabel className="!m-0">Active</FormLabel>
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="test_mode"
                      render={({ field }) => (
                        <FormItem className="flex items-center gap-2 space-y-0">
                          <FormControl>
                            <Switch
                              checked={field.value}
                              onCheckedChange={field.onChange}
                            />
                          </FormControl>
                          <FormLabel className="!m-0">Test Mode</FormLabel>
                        </FormItem>
                      )}
                    />
                  </div>
                </TabsContent>

                <TabsContent value="service" className="px-6 py-4 space-y-6">
                  <div className="grid grid-cols-3 gap-6">
                    <FormField
                      control={form.control}
                      name="currency"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Currency</FormLabel>
                          <Select
                            onValueChange={field.onChange}
                            value={field.value}
                          >
                            <FormControl>
                              <SelectTrigger>
                                <SelectValue />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              {currencies.map((currency) => (
                                <SelectItem key={currency} value={currency}>
                                  {currency}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="estimated_delivery_days.min"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Min Delivery Days</FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              type="number"
                              min="1"
                              onChange={(e) =>
                                field.onChange(parseInt(e.target.value) || 1)
                              }
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="estimated_delivery_days.max"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Max Delivery Days</FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              type="number"
                              min="1"
                              onChange={(e) =>
                                field.onChange(parseInt(e.target.value) || 1)
                              }
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <h3 className="text-lg font-medium">Size Limits</h3>
                      <div className="grid grid-cols-2 gap-4">
                        <FormField
                          control={form.control}
                          name="max_weight"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Max Weight (kg)</FormLabel>
                              <FormControl>
                                <Input
                                  {...field}
                                  type="number"
                                  min="0"
                                  step="0.1"
                                  onChange={(e) =>
                                    field.onChange(
                                      parseFloat(e.target.value) || undefined,
                                    )
                                  }
                                />
                              </FormControl>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="max_length"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Max Length (cm)</FormLabel>
                              <FormControl>
                                <Input
                                  {...field}
                                  type="number"
                                  min="0"
                                  onChange={(e) =>
                                    field.onChange(
                                      parseInt(e.target.value) || undefined,
                                    )
                                  }
                                />
                              </FormControl>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="max_width"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Max Width (cm)</FormLabel>
                              <FormControl>
                                <Input
                                  {...field}
                                  type="number"
                                  min="0"
                                  onChange={(e) =>
                                    field.onChange(
                                      parseInt(e.target.value) || undefined,
                                    )
                                  }
                                />
                              </FormControl>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="max_height"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Max Height (cm)</FormLabel>
                              <FormControl>
                                <Input
                                  {...field}
                                  type="number"
                                  min="0"
                                  onChange={(e) =>
                                    field.onChange(
                                      parseInt(e.target.value) || undefined,
                                    )
                                  }
                                />
                              </FormControl>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="pricing" className="px-6 py-4 space-y-6">
                  <FormField
                    control={form.control}
                    name="base_rate"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Base Rate</FormLabel>
                        <FormControl>
                          <Input
                            {...field}
                            type="number"
                            min="0"
                            step="0.01"
                            onChange={(e) =>
                              field.onChange(
                                parseFloat(e.target.value) || undefined,
                              )
                            }
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <div className="p-4 border rounded-lg bg-gray-50">
                    <p className="text-sm text-gray-600">
                      Advanced pricing with zones, weight-based rates, and
                      country-specific pricing will be available in a future
                      update.
                    </p>
                  </div>
                </TabsContent>

                <TabsContent value="options" className="px-6 py-4 space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium">Shipping Options</h3>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={handleAddShippingOption}
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Add Option
                    </Button>
                  </div>

                  <div className="space-y-4">
                    {fields.map((field, index) => {
                      const option = options.find(
                        (opt) => opt.code === field.code,
                      )
                      return (
                        <Card key={field.id}>
                          <CardHeader className="pb-3">
                            <div className="flex items-center justify-between">
                              <CardTitle className="text-sm">
                                Option {index + 1}
                              </CardTitle>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => remove(index)}
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </CardHeader>
                          <CardContent className="space-y-4">
                            <div className="grid grid-cols-3 gap-4">
                              <FormField
                                control={form.control}
                                name={`shipping_options.${index}.code`}
                                render={({ field }) => (
                                  <FormItem>
                                    <FormLabel>Option Code</FormLabel>
                                    <Select
                                      onValueChange={field.onChange}
                                      value={field.value}
                                    >
                                      <FormControl>
                                        <SelectTrigger>
                                          <SelectValue placeholder="Select option" />
                                        </SelectTrigger>
                                      </FormControl>
                                      <SelectContent>
                                        {options.map((opt) => (
                                          <SelectItem
                                            key={opt.code}
                                            value={opt.code}
                                          >
                                            {opt.name}
                                          </SelectItem>
                                        ))}
                                      </SelectContent>
                                    </Select>
                                    <FormMessage />
                                  </FormItem>
                                )}
                              />

                              <FormField
                                control={form.control}
                                name={`shipping_options.${index}.value`}
                                render={({ field }) => (
                                  <FormItem>
                                    <FormLabel>Value</FormLabel>
                                    <FormControl>
                                      {option?.type === 'boolean' ? (
                                        <Switch
                                          checked={field.value}
                                          onCheckedChange={field.onChange}
                                        />
                                      ) : option?.enum ? (
                                        <Select
                                          onValueChange={field.onChange}
                                          value={field.value}
                                        >
                                          <SelectTrigger>
                                            <SelectValue />
                                          </SelectTrigger>
                                          <SelectContent>
                                            {option.enum.map((enumValue) => (
                                              <SelectItem
                                                key={enumValue}
                                                value={enumValue}
                                              >
                                                {enumValue}
                                              </SelectItem>
                                            ))}
                                          </SelectContent>
                                        </Select>
                                      ) : (
                                        <Input
                                          {...field}
                                          type={
                                            option?.type === 'float'
                                              ? 'number'
                                              : 'text'
                                          }
                                          step={
                                            option?.type === 'float'
                                              ? '0.01'
                                              : undefined
                                          }
                                        />
                                      )}
                                    </FormControl>
                                    <FormMessage />
                                  </FormItem>
                                )}
                              />

                              <FormField
                                control={form.control}
                                name={`shipping_options.${index}.enabled`}
                                render={({ field }) => (
                                  <FormItem className="flex items-center gap-2 space-y-0 pt-8">
                                    <FormControl>
                                      <Switch
                                        checked={field.value}
                                        onCheckedChange={field.onChange}
                                      />
                                    </FormControl>
                                    <FormLabel className="!m-0">Enabled</FormLabel>
                                  </FormItem>
                                )}
                              />
                            </div>

                            {option && (
                              <p className="text-xs text-gray-500">
                                Type: {option.type}
                                {option.required && ' (Required)'}
                              </p>
                            )}
                          </CardContent>
                        </Card>
                      )
                    })}

                    {fields.length === 0 && (
                      <div className="text-center py-8 text-gray-500">
                        <Settings className="h-8 w-8 mx-auto mb-2 opacity-50" />
                        <p>No shipping options configured</p>
                        <p className="text-xs">
                          Add options to customize this shipping method
                        </p>
                      </div>
                    )}
                  </div>
                </TabsContent>
              </Tabs>
            </div>

            <DialogFooter className="px-6 py-4 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={() => onOpenChange(false)}
              >
                Cancel
              </Button>
              <Button type="submit">
                {selectedMethod ? 'Update' : 'Create'} Method
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}