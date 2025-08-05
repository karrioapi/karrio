import * as React from "react";
import { Check, X } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandList,
} from "@karrio/ui/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverAnchor,
} from "@karrio/ui/components/ui/popover";
import { Input } from "@karrio/ui/components/ui/input";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

interface CountryOption {
  value: string;
  label: string;
  searchText: string;
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
  React.ElementRef<typeof Input>,
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
  const [open, setOpen] = React.useState(false);
  const [inputValue, setInputValue] = React.useState("");
  const [selectedCountry, setSelectedCountry] = React.useState<CountryOption | null>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  const { references } = useAPIMetadata();

  const countryOptions = React.useMemo((): CountryOption[] => {
    const countryData = references?.countries || {};
    return Object.entries(countryData).map(([code, name]) => ({
      value: code,
      label: name as string,
      searchText: `${name} ${code}`.toLowerCase(),
    }));
  }, [references?.countries]);

  // Filter countries based on input
  const filteredCountries = React.useMemo(() => {
    if (!inputValue) return countryOptions;
    const searchTerm = inputValue.toLowerCase();
    return countryOptions.filter(country =>
      country.searchText.includes(searchTerm)
    );
  }, [countryOptions, inputValue]);

  // Initialize selected country from value prop
  React.useEffect(() => {
    if (value) {
      const country = countryOptions.find(c => c.value === value);
      if (country) {
        setSelectedCountry(country);
        setInputValue(country.label);
      } else {
        // If value doesn't match any country, show the raw value
        setSelectedCountry(null);
        setInputValue(value);
      }
    } else {
      setSelectedCountry(null);
      setInputValue("");
    }
  }, [value, countryOptions]);

  const handleInputValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setInputValue(newValue);

    // Don't auto-select countries while typing - let user choose from filtered options
    // Only clear selection if input is empty
    if (!newValue) {
      setSelectedCountry(null);
      onValueChange?.("");
      setOpen(false);
    } else {
      // Show dropdown when typing - either with filtered results or show "no results"
      setOpen(true);
    }
  };

  const handleCountrySelect = (country: CountryOption) => {
    setSelectedCountry(country);
    setInputValue(country.label);
    onValueChange?.(country.value);
    setOpen(false);
    // Return focus to input after selection
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  const handleClear = () => {
    setSelectedCountry(null);
    setInputValue("");
    onValueChange?.("");
    setOpen(false);
    // Return focus to input after clearing
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  const handleInputFocus = () => {
    // Show dropdown when focused, either with filtered results or all countries
    if (inputValue && filteredCountries.length > 0) {
      setOpen(true);
    } else if (!inputValue) {
      // If no input, show all countries
      setOpen(true);
    }
  };

  const handleInputBlur = (e: React.FocusEvent) => {
    // Only close if focus is not moving to the popover content
    const relatedTarget = e.relatedTarget as HTMLElement;
    if (!relatedTarget || !relatedTarget.closest('[data-radix-popper-content-wrapper]')) {
      setOpen(false);

      // Only revert if input has text but no valid country is selected AND we're not in the middle of selection
      if (inputValue && !selectedCountry && !open) {
        // If there's a value prop, try to restore it
        if (value) {
          const country = countryOptions.find(c => c.value === value);
          if (country) {
            setInputValue(country.label);
            setSelectedCountry(country);
          } else {
            setInputValue("");
            setSelectedCountry(null);
            onValueChange?.("");
          }
        } else {
          setInputValue("");
          setSelectedCountry(null);
        }
      }
    }
  };

  // Combine refs
  React.useImperativeHandle(ref, () => inputRef.current!, []);

  return (
    <div className={wrapperClass || "space-y-2"}>
      {label && (
        <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
          {label}
          {required && (
            <span className="icon is-small has-text-danger small-icon">
              <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
            </span>
          )}
        </label>
      )}
      <div className={`field ${fieldClass || ""}`}>
        <div className="control relative">
          <Popover open={open} onOpenChange={setOpen}>
            <PopoverAnchor asChild>
              <Input
                ref={inputRef}
                name={name}
                value={inputValue}
                onChange={handleInputValueChange}
                onFocus={handleInputFocus}
                onBlur={handleInputBlur}
                placeholder={placeholder}
                required={required}
                disabled={disabled}
                className={cn("w-full pr-8", className)}
                autoComplete="off"
                data-lpignore="true"
                data-form-type="other"
                {...props}
              />
            </PopoverAnchor>
            <PopoverContent
              className="w-full p-0"
              align="start"
              onOpenAutoFocus={(e) => e.preventDefault()}
              style={{ width: 'var(--radix-popover-trigger-width)' }}
            >
              <Command shouldFilter={false}>
                <CommandList>
                  {filteredCountries.length === 0 ? (
                    <CommandEmpty>
                      {inputValue ? `No countries found for "${inputValue}"` : "Start typing to search countries"}
                    </CommandEmpty>
                  ) : (
                    <CommandGroup>
                      {filteredCountries.map((country) => (
                        <CommandItem
                          key={country.value}
                          value={country.value}
                          onSelect={() => handleCountrySelect(country)}
                          onMouseDown={(e) => e.preventDefault()}
                        >
                          <Check
                            className={cn(
                              "mr-2 h-4 w-4",
                              selectedCountry?.value === country.value ? "opacity-100" : "opacity-0"
                            )}
                          />
                          <div className="flex items-center gap-2">
                            <span>{country.label}</span>
                            <span className="text-xs text-muted-foreground">({country.value})</span>
                          </div>
                        </CommandItem>
                      ))}
                    </CommandGroup>
                  )}
                </CommandList>
              </Command>
            </PopoverContent>
          </Popover>
          {inputValue && !disabled && (
            <button
              type="button"
              onClick={handleClear}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-gray-100 rounded-full transition-colors z-10"
              tabIndex={-1}
            >
              <X className="h-4 w-4 text-gray-400 hover:text-gray-600" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
});

CountrySelect.displayName = "CountrySelect";
