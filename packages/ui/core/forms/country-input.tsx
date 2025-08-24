"use client";

import { CountrySelect } from "@karrio/ui/components/country-select";
import { forwardRef } from "react";

interface CountryInputProps {
  name?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  placeholder?: string;
  label?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
}

export const CountryInput = forwardRef<
  HTMLInputElement,
  CountryInputProps
>(({
  name = "country",
  value,
  onValueChange,
  placeholder,
  label,
  required = false,
  disabled = false,
  className,
  ...props
}, ref) => {
  return (
    <CountrySelect
      ref={ref}
      name={name}
      value={value}
      onValueChange={onValueChange}
      placeholder={placeholder}
      label={label}
      required={required}
      disabled={disabled}
      className={className}
      {...props}
    />
  );
});
