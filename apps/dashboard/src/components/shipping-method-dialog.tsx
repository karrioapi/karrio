import { useEffect, useState } from 'react'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Plus, Trash2 } from 'lucide-react'
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
import { Badge } from './ui/badge'
import { CarrierOptionsEditor } from './ui/carrier-options-editor'
import type { ShippingMethod } from '@/types/shipping-methods'
import { useCarrierConnections } from '@/hooks/useCarriers'
import { useCarrierServices, useCarrierMetadata } from '@/hooks/useCarrierReferences'

const formSchema = z.object({
  name: z.string().min(1, { message: 'Name is required' }),
  slug: z.string().optional(),
  description: z.string().optional(),
  carrier_code: z.string().min(1, { message: 'Carrier is required' }),
  carrier_service: z.string().min(1, { message: 'Service is required' }),
  carrier_id: z.string().optional(),
  is_active: z.boolean(),
  carrier_options: z.record(z.string(), z.any()).optional(),
  metadata: z.record(z.string(), z.any()).optional(),
})

type FormData = z.infer<typeof formSchema>

interface ShippingMethodDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  selectedMethod: ShippingMethod | null
  onSuccess?: () => void
  onSubmit?: (values: FormData, method: ShippingMethod | null) => Promise<void>
}

export function ShippingMethodDialog({
  open,
  onOpenChange,
  selectedMethod,
  onSuccess,
  onSubmit,
}: ShippingMethodDialogProps) {
  // Fetch available carrier connections and metadata
  const { data: connectionsData } = useCarrierConnections()
  const connections = connectionsData?.connections || []
  const { data: carrierMetadata } = useCarrierMetadata()
  const availableCarriers = (carrierMetadata || []).filter((c) => c.is_enabled)

  const defaultValues: FormData = {
    name: '',
    slug: '',
    description: '',
    carrier_code: '',
    carrier_service: '',
    carrier_id: '',
    is_active: true,
    carrier_options: {},
    metadata: {},
  }

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues,
  })

  const handleSubmit = async (values: FormData) => {
    if (!onSubmit) {
      console.error('No submit handler provided')
      return
    }

    try {
      // Prepare values - ensure carrier_id is not empty string if optional
      const submitValues = {
        ...values,
        carrier_id: values.carrier_id || undefined,
      }

      // Remove slug when updating (it's auto-generated and read-only)
      if (selectedMethod) {
        delete submitValues.slug
      }

      await onSubmit(submitValues, selectedMethod)
      onSuccess?.()
      onOpenChange(false)
      form.reset(defaultValues)
    } catch (error: any) {
      console.error('Failed to save shipping method:', error)
    }
  }

  const { watch, setValue } = form
  const watchCarrierCode = watch('carrier_code')
  const watchCarrierService = watch('carrier_service')

  // Get services and options for the selected carrier
  const { services, options, metadata: selectedCarrierMeta } = useCarrierServices(watchCarrierCode)

  // Filter connections by carrier_code
  const filteredConnections = connections.filter(
    (c) => c.carrier_name === watchCarrierCode
  )

  useEffect(() => {
    if (open) {
      const initial = selectedMethod
        ? {
            name: selectedMethod.name || '',
            slug: selectedMethod.slug || '',
            description: selectedMethod.description || '',
            carrier_code: selectedMethod.carrier_code || '',
            carrier_service: selectedMethod.carrier_service || '',
            carrier_id: selectedMethod.carrier_id || '',
            is_active: selectedMethod.is_active || false,
            carrier_options: selectedMethod.carrier_options || {},
            metadata: selectedMethod.metadata || {},
          }
        : defaultValues

      form.reset(initial)
    }
  }, [open, selectedMethod])

  // Auto-generate name when carrier and service change (only for new methods)
  useEffect(() => {
    if (!selectedMethod && watchCarrierCode && watchCarrierService) {
      const carrier = availableCarriers.find((c) => c.carrier_name === watchCarrierCode)
      const service = services.find((s) => s.code === watchCarrierService)
      if (carrier && service) {
        setValue('name', `${carrier.display_name} - ${service.name}`)
      }
    }
  }, [watchCarrierCode, watchCarrierService, selectedMethod, availableCarriers, services, setValue])

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl h-[90vh] p-0 flex flex-col overflow-hidden">
        <DialogHeader className="px-6 py-4 border-b shrink-0">
          <DialogTitle>
            {selectedMethod ? 'Edit Shipping Method' : 'Create Shipping Method'}
          </DialogTitle>
          <DialogDescription>
            {selectedMethod
              ? `Update ${selectedMethod.name} configuration.`
              : 'Configure a new shipping method for your store.'}
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className="flex flex-col flex-1 overflow-hidden"
          >
            <div className="flex-1 overflow-y-auto px-6 py-4 space-y-6">
              {/* Name */}
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Name <span className="text-red-500">*</span>
                    </FormLabel>
                    <FormControl>
                      <Input {...field} placeholder="DHL Express - Express Worldwide" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Carrier Code Selection (Primary) */}
              <FormField
                control={form.control}
                name="carrier_code"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Carrier <span className="text-red-500">*</span>
                    </FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value || ''}
                      disabled={!!selectedMethod}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a carrier" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {availableCarriers.map((carrier) => (
                          <SelectItem key={carrier.carrier_name} value={carrier.carrier_name}>
                            <div className="flex items-center gap-2">
                              <CarrierImage
                                carrierName={carrier.carrier_name}
                                size="sm"
                                className="rounded"
                              />
                              <div className="flex flex-col">
                                <span className="font-medium">{carrier.display_name}</span>
                                <span className="text-xs text-gray-500">{carrier.carrier_name}</span>
                              </div>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Service Selection (Required, Dynamic) */}
              {watchCarrierCode && (
                <FormField
                  control={form.control}
                  name="carrier_service"
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
                            <SelectItem key={service.code} value={service.code}>
                              {service.code}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )}

              {/* Carrier Connection (Optional, Filtered by carrier_code) */}
              {watchCarrierCode && (
                <FormField
                  control={form.control}
                  name="carrier_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Carrier Connection (Optional)</FormLabel>
                      <div className="flex gap-2">
                        <Select
                          onValueChange={field.onChange}
                          value={field.value || undefined}
                        >
                          <FormControl>
                            <SelectTrigger className="flex-1">
                              <SelectValue placeholder={
                                filteredConnections.length === 0
                                  ? "No connections available"
                                  : "Select a connection (optional)"
                              } />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {filteredConnections.length === 0 ? (
                              <div className="px-2 py-6 text-center text-sm text-muted-foreground">
                                No carrier connections found for {watchCarrierCode}.
                                <br />
                                Create one in the Carriers page first.
                              </div>
                            ) : (
                              filteredConnections.map((connection) => (
                                <SelectItem key={connection.id} value={connection.id}>
                                  <div className="flex items-center gap-2">
                                    <div className="flex flex-col">
                                      <span className="font-medium">{connection.display_name}</span>
                                      <span className="text-xs text-gray-500">
                                        ID: {connection.carrier_id || 'N/A'}
                                      </span>
                                    </div>
                                    {connection.test_mode && (
                                      <Badge variant="secondary" className="ml-2">
                                        Test
                                      </Badge>
                                    )}
                                  </div>
                                </SelectItem>
                              ))
                            )}
                          </SelectContent>
                        </Select>
                        {field.value && (
                          <Button
                            type="button"
                            variant="outline"
                            size="icon"
                            onClick={() => field.onChange('')}
                            title="Clear connection"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                      <div className="text-xs text-muted-foreground mt-1">
                        {filteredConnections.length > 0
                          ? "Link this method to a specific carrier connection"
                          : `No carrier connections configured for ${selectedCarrierMeta?.display_name || watchCarrierCode}. You can add one later from the Carriers page.`
                        }
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )}

              {/* Carrier Options (Dynamic, based on carrier_code) */}
              {watchCarrierCode && options.length > 0 && (
                <div className="space-y-2">
                  <FormLabel>Carrier Options</FormLabel>
                  <p className="text-xs text-muted-foreground">
                    Configure shipping options for this method. Generic options are available for all carriers,
                    while carrier-specific options are unique to {selectedCarrierMeta?.display_name || 'the selected carrier'}.
                  </p>
                  <CarrierOptionsEditor
                    value={form.watch('carrier_options') || {}}
                    onChange={(updated) => form.setValue('carrier_options', updated)}
                    availableOptions={options}
                    carrierName={selectedCarrierMeta?.display_name}
                  />
                </div>
              )}

              {/* Description */}
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

              {/* Active Toggle */}
              <FormField
                control={form.control}
                name="is_active"
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
            </div>

            <DialogFooter className="px-6 py-4 border-t shrink-0">
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
