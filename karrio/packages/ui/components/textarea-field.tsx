import React from "react";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Label } from "@karrio/ui/components/ui/label";
import { cn } from "@karrio/ui/lib/utils";

export interface TextareaFieldComponent
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  labelBold?: boolean;
}

export const TextareaField = React.forwardRef<HTMLTextAreaElement, TextareaFieldComponent>(
  ({
    label,
    required,
    className,
    fieldClass,
    controlClass,
    wrapperClass,
    children,
    labelBold = false,
    ...props
  }, ref) => {
    const Props = {
      required,
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
          <div className={cn("relative", controlClass)}>
            <Textarea
              ref={ref}
              className={cn("min-h-[80px] text-sm", className)}
              {...Props}
            />
            {children}
          </div>
        </div>
      </div>
    );
  }
);

TextareaField.displayName = "TextareaField";
