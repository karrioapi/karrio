import { isNone } from "@karrio/lib";
import React, { RefObject } from "react";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { cn } from "@karrio/ui/lib/utils";

export interface InputFieldComponent
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  addonRight?: JSX.Element;
  addonLeft?: JSX.Element;
  iconRight?: JSX.Element;
  iconLeft?: JSX.Element;
  labelBold?: boolean;
  ref?: RefObject<HTMLInputElement>;
}

export const InputField = React.forwardRef<HTMLInputElement, InputFieldComponent>(
  ({
    label,
    required,
    className,
    fieldClass,
    controlClass,
    wrapperClass,
    children,
    addonLeft,
    addonRight,
    iconLeft,
    iconRight,
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
          {addonLeft && (
            <div className="absolute left-0 top-0 bottom-0 flex items-center pl-3">
              {addonLeft}
            </div>
          )}

          <div className={cn("relative flex items-center", controlClass)}>
            <Input
              ref={ref}
              className={cn(
                "h-9", // Match Bulma small input height
                addonLeft && "pl-10",
                addonRight && "pr-10",
                className
              )}
              {...Props}
            />
            {iconLeft && (
              <div className="absolute left-3 top-1/2 -translate-y-1/2">
                {iconLeft}
              </div>
            )}
            {iconRight && (
              <div className="absolute right-3 top-1/2 -translate-y-1/2">
                {iconRight}
              </div>
            )}
          </div>

          {addonRight && (
            <div className="absolute right-0 top-0 bottom-0 flex items-center pr-3">
              {addonRight}
            </div>
          )}
        </div>

        {children}
      </div>
    );
  }
);

InputField.displayName = "InputField";
