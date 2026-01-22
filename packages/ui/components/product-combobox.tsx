import * as React from "react";
import { Check, X, Package } from "lucide-react";
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
import { useProducts } from "@karrio/hooks/product";
import { ProductTemplateType } from "@karrio/types";

interface ProductComboboxProps {
  value?: string;
  onValueChange?: (value: ProductTemplateType | null) => void;
  placeholder?: string;
  label?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  wrapperClass?: string;
  fieldClass?: string;
}

interface TemplateOption {
  value: string;
  label: string;
  product: ProductTemplateType;
  searchText: string;
}

const formatProductInfo = (product: ProductTemplateType): string => {
  const parts: string[] = [];
  if (product.sku) parts.push(`SKU: ${product.sku}`);
  if (product.hs_code) parts.push(`HS: ${product.hs_code}`);
  if (product.origin_country) parts.push(product.origin_country);
  return parts.join(" • ");
};

export const ProductCombobox = React.forwardRef<
  React.ElementRef<typeof Input>,
  ProductComboboxProps
>(({
  value,
  onValueChange,
  placeholder = "Search product templates...",
  label,
  required = false,
  disabled = false,
  className,
  wrapperClass,
  fieldClass,
  ...props
}, ref) => {
  const [open, setOpen] = React.useState(false);
  const [inputValue, setInputValue] = React.useState(value || "");
  const inputRef = React.useRef<HTMLInputElement>(null);

  const {
    query: { data: { products } = {} },
  } = useProducts();

  const templateOptions = React.useMemo((): TemplateOption[] => {
    const templates = products?.edges?.map(({ node }) => node) || [];
    return templates.map((template: ProductTemplateType) => ({
      value: template.meta?.label || template.title || "",
      label: template.meta?.label || template.title || "",
      product: template,
      searchText: `${template.meta?.label || ""} ${template.title || ""} ${template.sku || ""} ${template.hs_code || ""} ${template.description || ""}`.toLowerCase(),
    }));
  }, [products]);

  // Filter templates based on input
  const filteredTemplates = React.useMemo(() => {
    if (!inputValue) return templateOptions;
    const searchTerm = inputValue.toLowerCase();
    return templateOptions.filter(template =>
      template.searchText.includes(searchTerm)
    );
  }, [templateOptions, inputValue]);

  const handleInputValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setInputValue(newValue);

    // Show dropdown if we have templates
    if (templateOptions.length > 0) {
      setOpen(true);
    }
  };

  const handleTemplateSelect = (template: TemplateOption) => {
    setInputValue(template.label);
    onValueChange?.(template.product);
    setOpen(false);
    // Return focus to input after selection
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  const handleClear = () => {
    setInputValue("");
    onValueChange?.(null);
    setOpen(false);
    // Return focus to input after clearing
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  const handleInputClick = () => {
    // Open dropdown on click/touch - simple and reliable
    if (templateOptions.length > 0) {
      setOpen(true);
    }
  };

  const handleInputKeyDown = (e: React.KeyboardEvent) => {
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

  const handleOptionSelect = (template: TemplateOption) => {
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

  // Don't render if no product templates available
  if (!products?.edges?.length) {
    return null;
  }

  return (
    <div className={cn("", wrapperClass)}>
      {label && (
        <Label
          className={cn("text-sm font-medium mb-1.5 block")}
        >
          {label}
          {required && (
            <span className="ml-1 text-red-500 text-xs">*</span>
          )}
        </Label>
      )}
      <div className={cn("relative", fieldClass)}>
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverAnchor asChild>
            <div className="relative">
              <Package className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                ref={inputRef}
                value={inputValue}
                onChange={handleInputValueChange}
                onBlur={handleInputBlur}
                onClick={handleInputClick}
                onKeyDown={handleInputKeyDown}
                placeholder={placeholder}
                required={required}
                disabled={disabled}
                className={cn("w-full pl-9 pr-8 h-8", className)}
                autoComplete="off"
                data-lpignore="true"
                data-form-type="other"
                {...props}
              />
            </div>
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
                    {inputValue ? `No products matching "${inputValue}"` : "No product templates available"}
                  </CommandEmpty>
                ) : (
                  <CommandGroup heading="Product Templates">
                    {filteredTemplates.map((template, index) => (
                      <CommandItem
                        key={`${template.product.id}-${index}`}
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
                          {template.product.title && template.product.title !== template.label && (
                            <span className="text-sm text-muted-foreground">
                              {template.product.title}
                            </span>
                          )}
                          <span className="text-xs text-muted-foreground">
                            {formatProductInfo(template.product)}
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

ProductCombobox.displayName = "ProductCombobox";
