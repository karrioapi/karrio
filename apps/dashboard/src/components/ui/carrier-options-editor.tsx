import * as React from 'react'
import { Trash2, Plus } from 'lucide-react'
import { Button } from './button'
import { Input } from './input'
import { Switch } from './switch'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './select'

interface CarrierOption {
  code: string
  name?: string
  type: string
  description?: string
  required?: boolean
  default?: any
  enum?: string[]
}

interface CarrierOptionsEditorProps {
  value: Record<string, any>
  onChange: (options: Record<string, any>) => void
  availableOptions: CarrierOption[]
  carrierName?: string
}

export function CarrierOptionsEditor({
  value,
  onChange,
  availableOptions,
  carrierName,
}: CarrierOptionsEditorProps) {
  const [selectedOption, setSelectedOption] = React.useState<string>('')
  const [customKey, setCustomKey] = React.useState('')
  const [customValue, setCustomValue] = React.useState('')
  const [showCustom, setShowCustom] = React.useState(false)
  const [showAddOption, setShowAddOption] = React.useState(false)

  // Generic options supported by all carriers
  const genericOptions: CarrierOption[] = [
    { code: 'insurance', name: 'Insurance', type: 'float', description: 'Insurance value for the shipment' },
    { code: 'cash_on_delivery', name: 'Cash on Delivery', type: 'float', description: 'Cash on delivery amount' },
    { code: 'dangerous_good', name: 'Dangerous Goods', type: 'boolean', description: 'Shipment contains dangerous goods' },
    { code: 'declared_value', name: 'Declared Value', type: 'float', description: 'Declared customs value' },
    { code: 'hold_at_location', name: 'Hold at Location', type: 'boolean', description: 'Hold package at carrier location for pickup' },
    { code: 'paperless_trade', name: 'Paperless Trade', type: 'boolean', description: 'Use paperless trade documents' },
    { code: 'signature_confirmation', name: 'Signature Confirmation', type: 'boolean', description: 'Require signature on delivery' },
    { code: 'saturday_delivery', name: 'Saturday Delivery', type: 'boolean', description: 'Enable Saturday delivery' },
  ]

  // Combine all available options (generic + carrier-specific)
  const allAvailableOptions = [...genericOptions, ...availableOptions]

  // Get options that are currently set
  const setOptions = Object.keys(value || {})

  // Get options that can still be added (not yet set)
  const unsetOptions = allAvailableOptions.filter(
    (opt) => !setOptions.includes(opt.code)
  )

  const updateOption = (code: string, newValue: any) => {
    const updated = { ...(value || {}) }
    if (newValue === undefined || newValue === null || newValue === '') {
      delete updated[code]
    } else {
      updated[code] = newValue
    }
    onChange(updated)
  }

  const removeOption = (code: string) => {
    const updated = { ...(value || {}) }
    delete updated[code]
    onChange(updated)
  }

  const addOption = (optionCode: string) => {
    const option = allAvailableOptions.find((opt) => opt.code === optionCode)
    if (!option) return

    const updated = { ...(value || {}) }

    // Set default value based on type
    if (option.type === 'boolean') {
      updated[optionCode] = false
    } else if (option.default !== undefined) {
      updated[optionCode] = option.default
    } else {
      updated[optionCode] = ''
    }

    onChange(updated)
    setSelectedOption('')
    setShowAddOption(false)
  }

  const addCustomOption = () => {
    if (!customKey.trim()) return

    const updated = { ...(value || {}) }
    try {
      // Try to parse as JSON first
      updated[customKey] = JSON.parse(customValue)
    } catch {
      // If parsing fails, use as string
      updated[customKey] = customValue
    }
    onChange(updated)
    setCustomKey('')
    setCustomValue('')
    setShowCustom(false)
  }

  const findOptionDefinition = (code: string): CarrierOption | null => {
    return allAvailableOptions.find((opt) => opt.code === code) || null
  }

  const renderOptionInput = (code: string) => {
    const option = findOptionDefinition(code)
    const currentValue = value?.[code]

    if (!option) {
      // Custom option
      return (
        <Input
          value={typeof currentValue === 'string' ? currentValue : JSON.stringify(currentValue)}
          onChange={(e) => {
            try {
              updateOption(code, JSON.parse(e.target.value))
            } catch {
              updateOption(code, e.target.value)
            }
          }}
        />
      )
    }

    // Render based on type
    if (option.type === 'boolean') {
      return (
        <div className="flex items-center gap-2">
          <Switch
            checked={currentValue === true}
            onCheckedChange={(checked) => updateOption(option.code, checked)}
          />
          <span className="text-sm text-muted-foreground">
            {currentValue === true ? 'Enabled' : 'Disabled'}
          </span>
        </div>
      )
    }

    if (option.enum) {
      return (
        <Select
          value={currentValue?.toString() || undefined}
          onValueChange={(val) => updateOption(option.code, val || undefined)}
        >
          <SelectTrigger>
            <SelectValue placeholder={`Select ${option.name || option.code}`} />
          </SelectTrigger>
          <SelectContent>
            {option.enum.map((enumValue: string) => (
              <SelectItem key={enumValue} value={enumValue}>
                {enumValue}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      )
    }

    return (
      <Input
        type={option.type === 'float' || option.type === 'number' ? 'number' : 'text'}
        step={option.type === 'float' ? '0.01' : undefined}
        placeholder={
          option.default
            ? `Default: ${option.default}`
            : `Enter ${(option.name || option.code).toLowerCase()}`
        }
        value={currentValue?.toString() || ''}
        onChange={(e) => {
          let val: any = e.target.value
          if (option.type === 'float' || option.type === 'number') {
            val = val ? parseFloat(val) : undefined
          }
          updateOption(option.code, val)
        }}
      />
    )
  }

  return (
    <div className="space-y-3">
      {/* Currently Set Options */}
      {setOptions.length > 0 && (
        <div className="space-y-2">
          {setOptions.map((code) => {
            const option = findOptionDefinition(code)
            const isCustom = !option

            return (
              <div key={code} className="flex flex-col gap-2 p-3 border rounded-lg bg-muted/30">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <label className="text-sm font-medium text-foreground">
                        {option?.name || code}
                      </label>
                      {isCustom && (
                        <span className="text-xs text-muted-foreground">(Custom)</span>
                      )}
                    </div>
                    {option?.description && (
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {option.description}
                      </p>
                    )}
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="h-6 w-6 p-0"
                    onClick={() => removeOption(code)}
                    title="Remove option"
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
                <div className="mt-1">{renderOptionInput(code)}</div>
              </div>
            )
          })}
        </div>
      )}

      {/* Add Option Dropdown */}
      {!showAddOption && unsetOptions.length > 0 && (
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => setShowAddOption(true)}
          className="w-full"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Option
        </Button>
      )}

      {showAddOption && unsetOptions.length > 0 && (
        <div className="flex gap-2 items-center p-3 border rounded-lg bg-muted/30">
          <Select
            value={selectedOption}
            onValueChange={(value) => {
              if (value) {
                addOption(value)
              }
            }}
          >
            <SelectTrigger className="flex-1">
              <SelectValue placeholder="Select an option to add" />
            </SelectTrigger>
            <SelectContent>
              {unsetOptions.map((option) => (
                <SelectItem key={option.code} value={option.code}>
                  <div className="flex flex-col">
                    <span className="font-medium">{option.name || option.code}</span>
                    <span className="text-xs text-muted-foreground">
                      {option.description || `Type: ${option.type}`}
                    </span>
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => {
              setShowAddOption(false)
              setSelectedOption('')
            }}
          >
            Cancel
          </Button>
        </div>
      )}

      {/* Add Custom Option */}
      {!showCustom && (
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => setShowCustom(true)}
          className="w-full"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Custom Option
        </Button>
      )}

      {showCustom && (
        <div className="space-y-2 border rounded-lg p-4 bg-muted/30">
          <p className="text-xs text-muted-foreground mb-2">
            Add a custom option not listed above
          </p>
          <div className="flex gap-2">
            <Input
              placeholder="Option key"
              value={customKey}
              onChange={(e) => setCustomKey(e.target.value)}
              className="flex-1"
            />
            <Input
              placeholder="Value (JSON or string)"
              value={customValue}
              onChange={(e) => setCustomValue(e.target.value)}
              className="flex-1"
            />
          </div>
          <div className="flex gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => {
                setShowCustom(false)
                setCustomKey('')
                setCustomValue('')
              }}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              type="button"
              size="sm"
              onClick={addCustomOption}
              disabled={!customKey.trim()}
              className="flex-1"
            >
              Add
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
