import * as React from 'react'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './select'
import { useAPIMetadata } from '@/hooks/useAPIMetadata'

interface CountrySelectProps {
  value?: string
  onValueChange?: (value: string) => void
  placeholder?: string
  disabled?: boolean
  className?: string
}

export const CountrySelect = React.forwardRef<
  React.ElementRef<typeof SelectTrigger>,
  CountrySelectProps
>(({ value, onValueChange, placeholder = 'Select a country', disabled, className }, ref) => {
  const { references } = useAPIMetadata()

  const countries = React.useMemo(() => {
    const countryData = references?.countries || {}
    return Object.entries(countryData)
      .map(([code, name]) => ({
        code,
        name: name as string,
      }))
      .sort((a, b) => a.name.localeCompare(b.name))
  }, [references?.countries])

  return (
    <Select value={value} onValueChange={onValueChange} disabled={disabled}>
      <SelectTrigger ref={ref} className={className}>
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent>
        {countries.map(({ code, name }) => (
          <SelectItem key={code} value={code}>
            {name} ({code})
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
})

CountrySelect.displayName = 'CountrySelect'
