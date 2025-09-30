import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
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
import type { CarrierConnection } from '@/hooks/useCarriers'

// Simplified schema for mock data
const formSchema = z.object({
  carrier_name: z.string().min(1, { message: 'Carrier is required' }),
  carrier_id: z.string().min(1, { message: 'Carrier ID is required' }),
  display_name: z.string().min(1, { message: 'Display name is required' }),
  active: z.boolean(),
  test_mode: z.boolean(),
  // Mock credentials fields
  username: z.string().optional(),
  password: z.string().optional(),
  account_number: z.string().optional(),
})

type FormData = z.infer<typeof formSchema>

interface CarrierConnectionDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  selectedConnection: CarrierConnection | null
  onSuccess?: () => void
  onSubmit?: (
    values: FormData,
    connection: CarrierConnection | null,
  ) => Promise<void>
}

// Mock carrier data
const mockCarriers = [
  { value: 'fedex', label: 'FedEx', capabilities: ['shipping', 'tracking'] },
  {
    value: 'ups',
    label: 'UPS',
    capabilities: ['shipping', 'tracking', 'pickup'],
  },
  {
    value: 'dhl_express',
    label: 'DHL Express',
    capabilities: ['shipping', 'tracking'],
  },
  {
    value: 'canada_post',
    label: 'Canada Post',
    capabilities: ['shipping', 'tracking'],
  },
  {
    value: 'purolator',
    label: 'Purolator',
    capabilities: ['shipping', 'tracking', 'pickup'],
  },
  { value: 'usps', label: 'USPS', capabilities: ['shipping', 'tracking'] },
]

export function CarrierConnectionDialog({
  open,
  onOpenChange,
  selectedConnection,
  onSuccess,
  onSubmit,
}: CarrierConnectionDialogProps) {
  const [initialValues, setInitialValues] = useState<FormData | null>(null)

  const defaultValues: FormData = {
    carrier_name: '',
    carrier_id: '',
    display_name: '',
    active: true,
    test_mode: true,
    username: '',
    password: '',
    account_number: '',
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
      await onSubmit(values, selectedConnection)
      onSuccess?.()
      onOpenChange(false)
      form.reset(defaultValues)
    } catch (error: any) {
      console.error('Failed to save carrier connection:', error)
    }
  }

  const { watch, setValue } = form
  const selectedCarrierName = watch('carrier_name')

  useEffect(() => {
    if (open) {
      const initial = selectedConnection
        ? {
            carrier_name: selectedConnection.carrier_name || '',
            carrier_id: selectedConnection.carrier_id || '',
            display_name: selectedConnection.display_name || '',
            active: selectedConnection.active || false,
            test_mode: selectedConnection.test_mode || true,
            username: '',
            password: '',
            account_number: '',
          }
        : defaultValues

      form.reset(initial)
      setInitialValues(initial)
    }
  }, [open, selectedConnection?.id])

  // Auto-generate display name when carrier changes
  useEffect(() => {
    const subscription = watch((value, { name, type }) => {
      if (name === 'carrier_name' && type === 'change' && value.carrier_name) {
        const carrier = mockCarriers.find((c) => c.value === value.carrier_name)
        if (carrier && !selectedConnection) {
          setValue('display_name', carrier.label)
        }
      }
    })
    return () => subscription.unsubscribe()
  }, [watch, setValue, selectedConnection])

  const handleModalClose = () => {
    onOpenChange(false)
  }

  const renderCredentialFields = () => {
    if (!selectedCarrierName) return null

    return (
      <div className="space-y-4">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input
                  {...field}
                  value={field.value || ''}
                  autoComplete="off"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input
                  {...field}
                  type="password"
                  value={field.value || ''}
                  autoComplete="off"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="account_number"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Account Number</FormLabel>
              <FormControl>
                <Input
                  {...field}
                  value={field.value || ''}
                  autoComplete="off"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </div>
    )
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] p-0 flex flex-col">
        <DialogHeader className="px-6 py-4 border-b">
          <DialogTitle>
            {selectedConnection ? 'Edit Connection' : 'Add Connection'}
          </DialogTitle>
          <DialogDescription>
            {selectedConnection
              ? `Update ${selectedConnection.carrier_name} connection details.`
              : 'Register a new carrier account.'}
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className="flex flex-col flex-1 min-h-0"
          >
            <div className="flex-1 overflow-y-auto px-6 py-4">
              <div className="space-y-6">
                <div className="space-y-4">
                  <FormField
                    control={form.control}
                    name="carrier_name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>
                          Carrier <span className="text-red-500">*</span>
                        </FormLabel>
                        <Select
                          onValueChange={field.onChange}
                          value={field.value || ''}
                          disabled={!!selectedConnection}
                        >
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select a carrier" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {mockCarriers.map((carrier) => (
                              <SelectItem
                                key={carrier.value}
                                value={carrier.value}
                              >
                                <div className="flex items-center gap-2">
                                  <CarrierImage
                                    carrierName={carrier.label}
                                    size="sm"
                                    className="rounded"
                                  />
                                  <span>{carrier.label}</span>
                                </div>
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  {watch('carrier_name') && (
                    <>
                      <FormField
                        control={form.control}
                        name="carrier_id"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>
                              Carrier ID <span className="text-red-500">*</span>
                            </FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                autoComplete="off"
                                placeholder="e.g., fedex-us-prod"
                              />
                            </FormControl>
                            <div className="text-xs text-muted-foreground">
                              Friendly tag. e.g:{' '}
                              <strong>fedex-us-prod, ups-ca-test...</strong>
                            </div>
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
                              Display Name{' '}
                              <span className="text-red-500">*</span>
                            </FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                autoComplete="off"
                                placeholder="FedEx US Production"
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
                    </>
                  )}
                </div>

                {watch('carrier_name') && (
                  <div>
                    <h3 className="text-lg font-medium mb-4">Credentials</h3>
                    {renderCredentialFields()}
                  </div>
                )}
              </div>
            </div>

            <DialogFooter className="px-6 py-4 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={handleModalClose}
              >
                Cancel
              </Button>
              <Button type="submit">
                {selectedConnection ? 'Update' : 'Create'} Connection
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}
