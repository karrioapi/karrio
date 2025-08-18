import React from "react";
import { RadioGroup, RadioGroupItem } from "@karrio/ui/components/ui/radio-group";
import { Label } from "@karrio/ui/components/ui/label";
import { cn } from "@karrio/ui/lib/utils";

export interface RadioOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface RadioGroupFieldComponent {
  label?: string;
  required?: boolean;
  value?: string;
  onValueChange?: (value: string) => void;
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  options: RadioOption[];
  className?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  disabled?: boolean;
  labelBold?: boolean;
  name?: string;
  // Layout options
  orientation?: "horizontal" | "vertical";
  gap?: string;
}

export const RadioGroupField = React.forwardRef<HTMLDivElement, RadioGroupFieldComponent>(
  ({
    label,
    required,
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
    orientation = "horizontal",
    gap = "gap-4",
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
        } as React.ChangeEvent<HTMLInputElement>;
        onChange(syntheticEvent);
      }
    };

    return (
      <div className={cn("px-1 py-2", wrapperClass)} {...props}>
        {label !== undefined && (
          <Label 
            className={cn("capitalize text-xs mb-2 block", labelBold ? "font-bold" : "font-normal")}
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
            <RadioGroup
              ref={ref}
              value={value}
              onValueChange={handleValueChange}
              disabled={disabled}
              className={cn(
                "flex items-center",
                orientation === "horizontal" ? `flex-row ${gap}` : `flex-col ${gap}`,
                className
              )}
              name={name}
            >
              {options.map((option) => (
                <div key={option.value} className="flex items-center space-x-2">
                  <RadioGroupItem 
                    value={option.value} 
                    id={`${name}-${option.value}`}
                    disabled={disabled || option.disabled}
                    className="h-4 w-4"
                  />
                  <Label 
                    htmlFor={`${name}-${option.value}`}
                    className={cn(
                      "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
                      "is-size-7 has-text-weight-bold" // Maintain Bulma styling for consistency
                    )}
                    style={{ fontSize: ".8em" }}
                  >
                    {option.label}
                  </Label>
                </div>
              ))}
            </RadioGroup>
          </div>
        </div>
      </div>
    );
  }
);

RadioGroupField.displayName = "RadioGroupField";