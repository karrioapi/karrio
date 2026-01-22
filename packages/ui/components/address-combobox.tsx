import * as React from "react";
import { Check, X } from "lucide-react";
import { formatAddress } from "@karrio/lib";
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
import { useAddresses } from "@karrio/hooks/address";
import { AddressType } from "@karrio/types";

interface AddressComboboxProps {
  name?: string;
  value?: string;
  onValueChange?: (value: Partial<AddressType>, isTemplateSelection?: boolean) => void;
  placeholder?: string;
  label?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  disableSuggestion?: boolean;
  wrapperClass?: string;
  fieldClass?: string;
}

interface TemplateOption {
  value: string;
  label: string;
  address: AddressType;
  searchText: string;
}

export const AddressCombobox = React.forwardRef<
  React.ElementRef<typeof Input>,
  AddressComboboxProps
>(({
  name = "name",
  value,
  onValueChange,
  placeholder = "Enter name or search templates",
  label,
  required = false,
  disabled = false,
  className,
  disableSuggestion = false,
  wrapperClass,
  fieldClass,
  ...props
}, ref) => {
  const [open, setOpen] = React.useState(false);
  const [inputValue, setInputValue] = React.useState(value || "");
  const inputRef = React.useRef<HTMLInputElement>(null);

  const {
    query: { data: { addresses } = {} },
  } = useAddresses();

  const templateOptions = React.useMemo((): TemplateOption[] => {
    if (disableSuggestion) return [];

    const templates = addresses?.edges?.map(({ node }) => node) || [];
    return templates.map((template: any) => ({
      value: template.meta?.label || template.person_name || "",
      label: template.meta?.label || template.person_name || "",
      address: template as AddressType,
      searchText: `${template.meta?.label || ""} ${template.person_name || ""} ${formatAddress(template)}`.toLowerCase(),
    }));
  }, [addresses, disableSuggestion]);

  // Filter templates based on input
  const filteredTemplates = React.useMemo(() => {
    if (!inputValue || disableSuggestion) return templateOptions;
    const searchTerm = inputValue.toLowerCase();
    return templateOptions.filter(template =>
      template.searchText.includes(searchTerm)
    );
  }, [templateOptions, inputValue, disableSuggestion]);

  const handleInputValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setInputValue(newValue);
    // Always update with the current input value
    onValueChange?.({ person_name: newValue });

    // Show dropdown if we have templates and not disabled
    if (!disableSuggestion && templateOptions.length > 0) {
      setOpen(true);
    }
  };

  const handleTemplateSelect = (template: TemplateOption) => {
    setInputValue(template.label);
    onValueChange?.(template.address, true);
    setOpen(false);
    // Return focus to input after selection
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  const handleClear = () => {
    setInputValue("");
    onValueChange?.({ person_name: "" });
    setOpen(false);
    // Return focus to input after clearing
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  const handleInputClick = () => {
    // Open dropdown on click/touch - simple and reliable
    if (!disableSuggestion && templateOptions.length > 0) {
      setOpen(true);
    }
  };

  const handleInputKeyDown = (e: React.KeyboardEvent) => {
    if (disableSuggestion) return;

    switch (e.key) {
      case 'Tab':
        // Tab shows dropdown for keyboard navigation
        if (templateOptions.length > 0) {
          setOpen(true);
        }
        break;
      case 'Escape':
        // Escape closes dropdown
        e.preventDefault();
        setOpen(false);
        break;
    }
  };

  const [isSelectingOption, setIsSelectingOption] = React.useState(false);

  const handleInputBlur = (e: React.FocusEvent) => {
    // Don't close if we're selecting an option
    if (!isSelectingOption) {
      setOpen(false);
    }
  };

  const handleOptionMouseDown = (e: React.MouseEvent) => {
    // Prevent blur immediately - works for desktop and mobile
    e.preventDefault();
    setIsSelectingOption(true);
  };

  const handleOptionSelect = (template: any) => {
    setIsSelectingOption(false);
    handleTemplateSelect(template);
  };

  // Update input value when prop changes
  React.useEffect(() => {
    if (value !== undefined && value !== inputValue) {
      setInputValue(value);
    }
  }, [value, inputValue]);

  // Cleanup on unmount
  React.useEffect(() => {
    return () => {
      setIsSelectingOption(false);
    };
  }, []);

  // Combine refs
  React.useImperativeHandle(ref, () => inputRef.current!, []);

  if (disableSuggestion) {
    // Simple input when suggestions are disabled
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
          <Input
            ref={inputRef}
            name={name}
            value={inputValue}
            onChange={handleInputValueChange}
            onBlur={handleInputBlur}
            onClick={handleInputClick}
            onKeyDown={handleInputKeyDown}
            placeholder={placeholder}
            required={required}
            disabled={disabled}
            className={cn("w-full pr-8", className)}
            autoComplete="off"
            data-lpignore="true"
            data-form-type="other"
            {...props}
          />
          {inputValue && !disabled && (
            <button
              type="button"
              onClick={handleClear}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-gray-100 rounded-full transition-colors"
              tabIndex={-1}
            >
              <X className="h-4 w-4 text-gray-400 hover:text-gray-600" />
            </button>
          )}
        </div>
      </div>
    );
  }

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
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverAnchor asChild>
            <Input
              ref={inputRef}
              name={name}
              value={inputValue}
              onChange={handleInputValueChange}
              onBlur={handleInputBlur}
              onClick={handleInputClick}
              onKeyDown={handleInputKeyDown}
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
                {filteredTemplates.length === 0 ? (
                  <CommandEmpty>
                    {inputValue ? `Use "${inputValue}" as new name` : "Start typing to search templates"}
                  </CommandEmpty>
                ) : (
                  <CommandGroup>
                    {filteredTemplates.map((template, index) => (
                      <CommandItem
                        key={`${template.value}-${index}`}
                        value={template.value}
                        onSelect={() => handleOptionSelect(template)}
                        onMouseDown={handleOptionMouseDown}
                        className="cursor-pointer"
                      >
                        <Check
                          className={cn(
                            "mr-2 h-4 w-4",
                            inputValue === template.value ? "opacity-100" : "opacity-0"
                          )}
                        />
                        <div className="flex flex-col">
                          <span className="font-medium">{template.label}</span>
                          <span className="text-xs text-muted-foreground">
                            {formatAddress(template.address)}
                          </span>
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
  );
});

AddressCombobox.displayName = "AddressCombobox";
