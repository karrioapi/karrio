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
  options: RadioOption[];
  className?: string;
  disabled?: boolean;
  name?: string;
  orientation?: "horizontal" | "vertical";
}

export const RadioGroupField = React.forwardRef<HTMLDivElement, RadioGroupFieldComponent>(
  ({
    label,
    required,
    value,
    onValueChange,
    options,
    className,
    disabled,
    name,
    orientation = "horizontal",
    ...props
  }, ref) => {

    return (
      <div className={cn("px-1 py-2", className)} {...props}>
        {label !== undefined && (
          <Label 
            className="capitalize text-xs mb-2 block font-bold"
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

        <RadioGroup
          ref={ref}
          value={value}
          onValueChange={onValueChange}
          disabled={disabled}
          className={cn(
            "flex items-center",
            orientation === "horizontal" ? "flex-row gap-4" : "flex-col gap-4"
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
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                style={{ fontSize: ".8em" }}
              >
                {option.label}
              </Label>
            </div>
          ))}
        </RadioGroup>
      </div>
    );
  }
);

RadioGroupField.displayName = "RadioGroupField";