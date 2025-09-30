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
import { Label } from "@karrio/ui/components/ui/label";
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
  align?: "start" | "center" | "end";
  noWrapper?: boolean;
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
  align = "start",
  noWrapper = false,
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

  // Initialize selected country from value prop (EXACT ORIGINAL LOGIC)
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

  // EXACT ORIGINAL handleInputValueChange with form protection
  const handleInputValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Prevent form-level onChange from interfering
    e.stopPropagation();
    
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

  // EXACT ORIGINAL handleInputFocus with Dialog protection
  const handleInputFocus = (e: React.FocusEvent) => {
    // Prevent any parent handlers from interfering
    e.stopPropagation();
    
    // Small delay to ensure Dialog animations/focus management don't interfere
    setTimeout(() => {
      // Show dropdown when focused, either with filtered results or all countries
      if (inputValue && filteredCountries.length > 0) {
        setOpen(true);
      } else if (!inputValue) {
        // If no input, show all countries
        setOpen(true);
      }
    }, 10);
  };

  // EXACT ORIGINAL handleInputBlur
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

  // Support for noWrapper (commodity modal style)
  if (noWrapper) {
    return (
      <div className="relative">
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
            className="w-64 p-0 max-h-[300px] overflow-hidden"
            align={align}
            onOpenAutoFocus={(e) => e.preventDefault()}
            onWheel={(e) => {
              // Don't prevent wheel events from reaching scrollable content
              if (!e.currentTarget.contains(e.target as Node)) {
                e.preventDefault();
              }
            }}
            style={{ width: 'var(--radix-popover-trigger-width)' }}
          >
            <div 
              className="max-h-[280px] overflow-y-auto overflow-x-hidden p-1" 
              style={{scrollbarWidth: 'thin'}}
              tabIndex={0}
              onWheel={(e) => {
                // Ensure wheel events work for scrolling
                const element = e.currentTarget;
                const canScrollUp = element.scrollTop > 0;
                const canScrollDown = element.scrollTop < element.scrollHeight - element.clientHeight;
                
                if ((e.deltaY < 0 && canScrollUp) || (e.deltaY > 0 && canScrollDown)) {
                  e.stopPropagation();
                }
              }}
            >
              {filteredCountries.length === 0 ? (
                <div className="py-6 text-center text-sm text-muted-foreground">
                  {inputValue ? `No countries found for "${inputValue}"` : "Start typing to search countries"}
                </div>
              ) : (
                filteredCountries.map((country) => (
                  <div
                    key={country.value}
                    className="relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none hover:bg-accent hover:text-accent-foreground"
                    onClick={() => handleCountrySelect(country)}
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
                  </div>
                ))
              )}
            </div>
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
    );
  }

  // Default wrapper (address form style) - Adapted from your original
  return (
    <div className={cn("px-1 py-2", wrapperClass)}>
      {label && (
        <Label 
          className={cn("capitalize text-xs mb-1 block font-bold")}
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
            className="w-64 p-0 max-h-[300px] overflow-hidden"
            align={align}
            onOpenAutoFocus={(e) => e.preventDefault()}
            onWheel={(e) => {
              // Don't prevent wheel events from reaching scrollable content
              if (!e.currentTarget.contains(e.target as Node)) {
                e.preventDefault();
              }
            }}
            style={{ width: 'var(--radix-popover-trigger-width)' }}
          >
            <div 
              className="max-h-[280px] overflow-y-auto overflow-x-hidden p-1" 
              style={{scrollbarWidth: 'thin'}}
              tabIndex={0}
              onWheel={(e) => {
                // Ensure wheel events work for scrolling
                const element = e.currentTarget;
                const canScrollUp = element.scrollTop > 0;
                const canScrollDown = element.scrollTop < element.scrollHeight - element.clientHeight;
                
                if ((e.deltaY < 0 && canScrollUp) || (e.deltaY > 0 && canScrollDown)) {
                  e.stopPropagation();
                }
              }}
            >
              {filteredCountries.length === 0 ? (
                <div className="py-6 text-center text-sm text-muted-foreground">
                  {inputValue ? `No countries found for "${inputValue}"` : "Start typing to search countries"}
                </div>
              ) : (
                filteredCountries.map((country) => (
                  <div
                    key={country.value}
                    className="relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none hover:bg-accent hover:text-accent-foreground"
                    onClick={() => handleCountrySelect(country)}
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
                  </div>
                ))
              )}
            </div>
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
  );
});

CountrySelect.displayName = "CountrySelect";