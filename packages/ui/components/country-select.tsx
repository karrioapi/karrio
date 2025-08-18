import * as React from "react";
import { cn } from "@karrio/ui/lib/utils";
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from "@karrio/ui/components/ui/select";
import { Label } from "@karrio/ui/components/ui/label";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

interface CountryOption {
  value: string;
  label: string;
}

interface CountrySelectProps {
  name?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  placeholder?: string;
  label?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  wrapperClass?: string;
  fieldClass?: string;
}

export const CountrySelect = React.forwardRef<
  React.ElementRef<typeof SelectTrigger>,
  CountrySelectProps
>(({
  name = "country_code",
  value,
  onValueChange,
  placeholder = "Select country",
  label,
  required = false,
  disabled = false,
  className,
  wrapperClass,
  fieldClass,
  ...props
}, ref) => {
  const { references } = useAPIMetadata();

  const countryOptions = React.useMemo((): CountryOption[] => {
    const countryData = references?.countries || {};
    return Object.entries(countryData).map(([code, name]) => ({
      value: code,
      label: name as string,
    }));
  }, [references?.countries]);

  return (
    <div className={cn("px-1 py-2", wrapperClass)}>
      {label && (
        <Label 
          className={cn("capitalize text-xs mb-1 block font-normal")}
          style={{ fontSize: ".8em" }}
        >
          {label}
          {required && (
            <span className="ml-1 text-red-500 text-xs">
              <i className="fas fa-asterisk text-[0.7em]"></i>
            </span>
          )}
        </Label>
      )}
      <div className={cn("relative", fieldClass)}>
        <Select value={value} onValueChange={onValueChange} disabled={disabled} name={name} {...props}>
          <SelectTrigger ref={ref} className={cn("h-9", className)}>
            <SelectValue placeholder={placeholder} />
          </SelectTrigger>
          <SelectContent>
            {countryOptions.map((country) => (
              <SelectItem 
                key={country.value} 
                value={country.value}
                className="text-sm"
              >
                <div className="flex items-center gap-2">
                  <span>{country.label}</span>
                  <span className="text-xs text-muted-foreground">({country.value})</span>
                </div>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
});

CountrySelect.displayName = "CountrySelect";
