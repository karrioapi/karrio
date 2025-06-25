import * as React from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import { Label } from "@karrio/ui/components/ui/label";
import { cn } from "@karrio/ui/lib/utils";

interface EnhancedSelectProps {
  name?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  placeholder?: string;
  label?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  children?: React.ReactNode;
  options?: Array<{
    value: string;
    label: string;
    group?: string;
  }>;
  groups?: Array<{
    label: string;
    options: Array<{
      value: string;
      label: string;
    }>;
  }>;
  // Use conditional rendering instead of display: none
  show?: boolean;
}

export const EnhancedSelect = React.forwardRef<
  React.ElementRef<typeof SelectTrigger>,
  EnhancedSelectProps
>(({
  name,
  value,
  onValueChange,
  placeholder = "Select an option",
  label,
  required = false,
  disabled = false,
  className,
  children,
  options = [],
  groups = [],
  show = true,
  ...props
}, ref) => {
  // Conditionally render the component instead of hiding it
  // This prevents form validation issues with hidden required fields
  if (!show) {
    return null;
  }

  return (
    <div className="space-y-2">
      {label && (
        <Label htmlFor={name} className="text-sm font-medium">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </Label>
      )}
      <Select
        name={name}
        value={value}
        onValueChange={onValueChange}
        required={required}
        disabled={disabled}
      >
        <SelectTrigger
          ref={ref}
          className={cn("w-full", className)}
          id={name}
        >
          <SelectValue placeholder={placeholder} />
        </SelectTrigger>
        <SelectContent>
          {/* Render children if provided */}
          {children}

          {/* Render flat options if provided */}
          {options.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}

          {/* Render grouped options if provided */}
          {groups.map((group) => (
            <div key={group.label}>
              <div className="px-2 py-1.5 text-sm font-semibold text-muted-foreground">
                {group.label}
              </div>
              {group.options.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </div>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
});

EnhancedSelect.displayName = "EnhancedSelect";
