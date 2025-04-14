"use client"

import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"

import { cn } from "@karrio/ui/lib/utils"
import { Button } from "./button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "./command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "./popover"

interface ComboboxProps {
  children?: React.ReactNode
  open?: boolean
  onOpenChange?: (open: boolean) => void
  value?: string | undefined
  onChange?: (value: string) => void
}

// Main Combobox component
const Combobox = ({
  children,
  open,
  onOpenChange,
  ...props
}: ComboboxProps) => {
  return (
    <Popover open={open} onOpenChange={onOpenChange}>
      {children}
    </Popover>
  )
}

// Input component for the Combobox
const ComboboxInput = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ className, ...props }, ref) => (
  <input
    ref={ref}
    className={cn("flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50", className)}
    {...props}
  />
))
ComboboxInput.displayName = "ComboboxInput"

// Trigger component for the Combobox
const ComboboxTrigger = PopoverTrigger

// Content component for the Combobox
const ComboboxPopover = React.forwardRef<
  React.ElementRef<typeof PopoverContent>,
  React.ComponentPropsWithoutRef<typeof PopoverContent>
>(({ className, ...props }, ref) => (
  <PopoverContent
    ref={ref}
    className={cn("p-0", className)}
    {...props}
  />
))
ComboboxPopover.displayName = "ComboboxPopover"

// Using Command and its subcomponents for the List
const ComboboxList = CommandList
const ComboboxEmpty = CommandEmpty
const ComboboxGroup = CommandGroup
const ComboboxOption = CommandItem

export {
  Combobox,
  ComboboxInput,
  ComboboxTrigger,
  ComboboxPopover,
  ComboboxList,
  ComboboxEmpty,
  ComboboxGroup,
  ComboboxOption,
}
