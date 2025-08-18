import React from "react";
import { CountrySelect } from "@karrio/ui/components/country-select";
import { Label } from "@karrio/ui/components/ui/label";
import { cn } from "@karrio/ui/lib/utils";

export interface CountryInputComponent {
  label?: string;
  required?: boolean;
  value?: string;
  onValueChange?: (value: string) => void;
  placeholder?: string;
  className?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  disabled?: boolean;
  labelBold?: boolean;
}

export const CountryInput = React.forwardRef<HTMLInputElement, CountryInputComponent>(
  ({
    label = "Country",
    required,
    value,
    onValueChange,
    placeholder = "Select country",
    className,
    fieldClass,
    controlClass,
    wrapperClass,
    disabled,
    labelBold = false,
    ...props
  }, ref) => {
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
            <CountrySelect
              ref={ref}
              value={value}
              onValueChange={onValueChange}
              placeholder={placeholder}
              disabled={disabled}
              className={cn("h-9", className)} // Match small input height
            />
          </div>
        </div>
      </div>
    );
  }
);

CountryInput.displayName = "CountryInput";
