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
}

export const DateInput = React.forwardRef<HTMLInputElement, DateInputComponent>(
  ({
    label,
    required,
    className,
    fieldClass,
    controlClass,
    wrapperClass,
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
            className="capitalize text-xs font-normal mb-1 block"
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
