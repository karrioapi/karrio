"use client";

import { AddressCombobox } from "@karrio/ui/components/address-combobox";
import { AddressType } from "@karrio/types";
import { forwardRef } from "react";

interface NameInputProps {
  name?: string;
  value?: string;
  onValueChange?: (value: Partial<AddressType>, refresh?: boolean) => void;
  placeholder?: string;
  label?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  disableSuggestion?: boolean;
  wrapperClass?: string;
  fieldClass?: string;
}

export const NameInput = forwardRef<
  HTMLInputElement,
  NameInputProps
>(({
  name = "person_name",
  value,
  onValueChange,
  placeholder,
  label,
  required = false,
  disabled = false,
  className,
  disableSuggestion = false,
  wrapperClass,
  fieldClass,
  ...props
}, ref) => {
  return (
    <AddressCombobox
      ref={ref}
      name={name}
      value={value}
      onValueChange={onValueChange}
      placeholder={placeholder}
      label={label}
      required={required}
      disabled={disabled}
      className={className}
      disableSuggestion={disableSuggestion}
      wrapperClass={wrapperClass}
      fieldClass={fieldClass}
      {...props}
    />
  );
});
