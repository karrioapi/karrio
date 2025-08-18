import React from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Label } from "@karrio/ui/components/ui/label";
import { cn } from "@karrio/ui/lib/utils";

export interface SelectFieldComponent {
  label?: string;
  required?: boolean;
  placeholder?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  onChange?: (event: React.ChangeEvent<HTMLSelectElement>) => void;
  options: Array<string | { value: string; label: string }>;
  className?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  disabled?: boolean;
  labelBold?: boolean;
  name?: string;
  // Props for inline styling (for dropdowns attached to inputs)
  attachedToInput?: boolean;
  attachmentSide?: "left" | "right";
  width?: string;
}

export const SelectField = React.forwardRef<HTMLButtonElement, SelectFieldComponent>(
  ({
    label,
    required,
    placeholder = "Select option",
    value,
    onValueChange,
    onChange,
    options,
    className,
    fieldClass,
    controlClass,
    wrapperClass,
    disabled,
    labelBold = false,
    name,
    attachedToInput = false,
    attachmentSide = "right",
    width = "auto",
    ...props
  }, ref) => {
    
    const handleValueChange = (newValue: string) => {
      // Call ShadCN onValueChange if provided
      if (onValueChange) {
        onValueChange(newValue);
      }
      
      // Call traditional onChange if provided (for compatibility)
      if (onChange) {
        const syntheticEvent = {
          target: { name, value: newValue },
          preventDefault: () => {},
        } as React.ChangeEvent<HTMLSelectElement>;
        onChange(syntheticEvent);
      }
    };

    const normalizedOptions = options.map(option => 
      typeof option === 'string' 
        ? { value: option, label: option }
        : option
    );

    // For attached dropdowns (like weight/currency units)
    if (attachedToInput) {
      const attachedClasses = cn(
        "h-9 border border-input bg-transparent px-3 py-1 pr-8 text-sm shadow-sm transition-colors",
        "focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring",
        "disabled:cursor-not-allowed disabled:opacity-50",
        attachmentSide === "right" && "border-l-0 rounded-l-none rounded-r-md",
        attachmentSide === "left" && "border-r-0 rounded-r-none rounded-l-md",
        width === "auto" ? "w-24" : width,
        className
      );

      return (
        <Select value={value} onValueChange={handleValueChange} disabled={disabled} {...props}>
          <SelectTrigger ref={ref} className={attachedClasses}>
            <SelectValue placeholder={placeholder} />
          </SelectTrigger>
          <SelectContent>
            {normalizedOptions.map((option) => (
              <SelectItem 
                key={option.value} 
                value={option.value}
                className="text-sm"
              >
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      );
    }

    // For standalone dropdowns (normal form fields)
    return (
      <div className={cn("px-1 py-2", wrapperClass)} {...props}>
        {label !== undefined && (
          <Label 
            className={cn("capitalize text-xs mb-1 block", labelBold ? "font-bold" : "font-normal")}
            style={{ fontSize: ".8em" }}
          >
            {label}
            {required && (
              <span className="ml-1 text-red-500 text-xs">
                <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
              </span>
            )}
          </Label>
        )}

        <div className={cn("relative", fieldClass)}>
          <div className={cn("relative", controlClass)}>
            <Select value={value} onValueChange={handleValueChange} disabled={disabled}>
              <SelectTrigger 
                ref={ref}
                className={cn("h-9", className)} // Match small input height
              >
                <SelectValue placeholder={placeholder} />
              </SelectTrigger>
              <SelectContent>
                {normalizedOptions.map((option) => (
                  <SelectItem 
                    key={option.value} 
                    value={option.value}
                    className="text-sm"
                  >
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>
    );
  }
);

SelectField.displayName = "SelectField";