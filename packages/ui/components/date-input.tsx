import React from "react";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { cn } from "@karrio/ui/lib/utils";

export interface DateInputComponent
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  labelBold?: boolean;
}

export const DateInput = React.forwardRef<HTMLInputElement, DateInputComponent>(
  ({
    label,
    required,
    className,
    fieldClass,
    controlClass,
    wrapperClass,
    labelBold = false,
    children,
    ...props
  }, ref) => {
    const Props = {
      required,
      type: "date" as const,
      ...props,
      ...(Object.keys(props).includes("value")
        ? { value: props.value || "" }
        : {}),
    };

    return (
      <div className={cn("px-1 py-2", wrapperClass)}>
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
          <div className={cn("relative flex items-center", controlClass)}>
            <Input
              ref={ref}
              className={cn(
                "h-9", // Match small input height
                "pr-10 sm:pr-8", // Extra padding for date icon on mobile, normal on larger screens
                "[&::-webkit-calendar-picker-indicator]:opacity-100", // Ensure icon is visible
                "[&::-webkit-calendar-picker-indicator]:cursor-pointer", // Make icon clickable
                "[&::-webkit-calendar-picker-indicator]:w-5", // Set icon width
                "[&::-webkit-calendar-picker-indicator]:h-5", // Set icon height
                "[&::-webkit-calendar-picker-indicator]:absolute", // Position icon absolutely
                "[&::-webkit-calendar-picker-indicator]:right-2", // Position from right
                "[&::-webkit-calendar-picker-indicator]:top-1/2", // Center vertically
                "[&::-webkit-calendar-picker-indicator]:-translate-y-1/2", // Center transform
                className
              )}
              {...Props}
            />
          </div>
        </div>

        {children}
      </div>
    );
  }
);

DateInput.displayName = "DateInput";
