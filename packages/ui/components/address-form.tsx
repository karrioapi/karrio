import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Checkbox } from "./ui/checkbox";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "./ui/form";
import { EnhancedSelect } from "./enhanced-select";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "./ui/collapsible";
import { ChevronDown, ChevronUp } from "lucide-react";
import { AddressType, DEFAULT_ADDRESS_CONTENT } from "@karrio/types";
import { COUNTRY_WITH_POSTAL_CODE, isEqual } from "@karrio/lib";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { AddressCombobox } from "@karrio/ui/components/address-combobox";
import { CountrySelect } from "@karrio/ui/components/country-select";

/**
 * AddressForm - React Hook Form Implementation
 *
 * This form uses react-hook-form for performance optimization, avoiding
 * re-renders on every keystroke. Key features:
 *
 * - Zod schema validation with conditional required fields (postal_code, state_code)
 * - Template selection via AddressCombobox that can populate all fields
 * - Country-dependent state/province selector (dropdown vs input)
 * - Postal code format validation per country
 * - Phone number formatting
 * - Advanced options (tax IDs) in collapsible section
 * - Imperative handle for external form submission
 *
 * The form uses uncontrolled inputs where possible to minimize re-renders,
 * with controlled components only where necessary (selects, checkboxes).
 */

// Postal code validation patterns by country
const POSTAL_CODE_PATTERNS: Record<string, RegExp> = {
  US: /^\d{5}(-\d{4})?$/,
  CA: /^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$/,
  GB: /^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$/i,
  DE: /^\d{5}$/,
  FR: /^\d{5}$/,
  AU: /^\d{4}$/,
  JP: /^\d{3}-\d{4}$/,
};

// Zod schema for address validation
// Note: postal_code and state_code requirements are validated dynamically
const addressSchema = z.object({
  person_name: z.string().min(1, "Contact person is required"),
  company_name: z.string().optional(),
  country_code: z.string().min(1, "Country is required"),
  address_line1: z.string().min(1, "Street address is required"),
  address_line2: z.string().optional(),
  city: z.string().min(1, "City is required"),
  state_code: z.string().optional(),
  postal_code: z.string().optional(),
  email: z.string().email("Invalid email format").optional().or(z.literal("")),
  phone_number: z.string().optional(),
  residential: z.boolean().optional(),
  federal_tax_id: z.string().max(20, "Max 20 characters").optional(),
  state_tax_id: z.string().max(20, "Max 20 characters").optional(),
});

type AddressFormValues = z.infer<typeof addressSchema>;

interface AddressFormProps {
  value?: Partial<AddressType>;
  onChange?: (address: Partial<AddressType>) => void;
  onSubmit?: (address: Partial<AddressType>) => Promise<void>;
  showSubmitButton?: boolean;
  submitButtonText?: string;
  disabled?: boolean;
  className?: string;
}

export interface AddressFormRef {
  submit: () => Promise<void>;
}

/**
 * Phone number formatting helper
 * Formats US/CA phone numbers, leaves others unchanged
 */
const formatPhoneNumber = (phone: string, country: string): string => {
  if (!phone) return phone;
  const digits = phone.replace(/\D/g, "");

  if (country === "US" || country === "CA") {
    if (digits.length === 10) {
      return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
    } else if (digits.length === 11 && digits[0] === "1") {
      return `+1 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7)}`;
    }
  }
  return phone;
};

/**
 * Validates postal code format based on country
 */
const validatePostalCode = (postal: string, country: string, isRequired: boolean): boolean => {
  if (!postal) return !isRequired;
  const pattern = POSTAL_CODE_PATTERNS[country];
  return pattern ? pattern.test(postal) : true;
};

export const AddressForm = React.forwardRef<AddressFormRef, AddressFormProps>(({
  value = DEFAULT_ADDRESS_CONTENT,
  onChange,
  onSubmit,
  showSubmitButton = true,
  submitButtonText = "Save Address",
  disabled = false,
  className = "",
}, ref) => {
  const { references } = useAPIMetadata();
  const [advancedExpanded, setAdvancedExpanded] = React.useState(false);
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const { toast } = useToast();

  // Initialize form with react-hook-form
  const form = useForm<AddressFormValues>({
    resolver: zodResolver(addressSchema),
    defaultValues: {
      person_name: value?.person_name || "",
      company_name: value?.company_name || "",
      country_code: value?.country_code || "",
      address_line1: value?.address_line1 || "",
      address_line2: value?.address_line2 || "",
      city: value?.city || "",
      state_code: value?.state_code || "",
      postal_code: value?.postal_code || "",
      email: value?.email || "",
      phone_number: value?.phone_number || "",
      residential: value?.residential || false,
      federal_tax_id: value?.federal_tax_id || "",
      state_tax_id: value?.state_tax_id || "",
    },
    mode: "onBlur", // Validate on blur for better UX
  });

  const countryCode = form.watch("country_code");
  const postalCode = form.watch("postal_code");

  // Derived validation requirements based on country
  const isPostalRequired = COUNTRY_WITH_POSTAL_CODE.includes(countryCode || "");
  const isStateRequired = Object.keys(references.states || {}).includes(countryCode || "");

  // Reset form when value prop changes (e.g., template selection from parent)
  React.useEffect(() => {
    if (value) {
      form.reset({
        person_name: value.person_name || "",
        company_name: value.company_name || "",
        country_code: value.country_code || "",
        address_line1: value.address_line1 || "",
        address_line2: value.address_line2 || "",
        city: value.city || "",
        state_code: value.state_code || "",
        postal_code: value.postal_code || "",
        email: value.email || "",
        phone_number: value.phone_number || "",
        residential: value.residential || false,
        federal_tax_id: value.federal_tax_id || "",
        state_tax_id: value.state_tax_id || "",
      });
    }
  }, [value, form]);

  // Notify parent of changes (debounced via form subscription)
  React.useEffect(() => {
    const subscription = form.watch((data) => {
      onChange?.(data as Partial<AddressType>);
    });
    return () => subscription.unsubscribe();
  }, [form, onChange]);

  // Handle form submission
  const handleSubmit = async (data: AddressFormValues) => {
    if (!onSubmit) return;

    // Additional validation for country-dependent required fields
    if (isPostalRequired && !data.postal_code) {
      form.setError("postal_code", { message: "Postal code is required" });
      return;
    }

    if (isStateRequired && !data.state_code) {
      form.setError("state_code", { message: "State/Province is required" });
      return;
    }

    // Validate postal code format
    if (data.postal_code && !validatePostalCode(data.postal_code, data.country_code, isPostalRequired)) {
      form.setError("postal_code", { message: "Invalid postal code format" });
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(data as Partial<AddressType>);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle template selection from AddressCombobox
  const handleTemplateSelection = (addressData: Partial<AddressType>, isTemplateSelection: boolean) => {
    if (isTemplateSelection) {
      // Full template selection - reset entire form
      form.reset({
        person_name: addressData.person_name || "",
        company_name: addressData.company_name || "",
        country_code: addressData.country_code || "",
        address_line1: addressData.address_line1 || "",
        address_line2: addressData.address_line2 || "",
        city: addressData.city || "",
        state_code: addressData.state_code || "",
        postal_code: addressData.postal_code || "",
        email: addressData.email || "",
        phone_number: addressData.phone_number || "",
        residential: addressData.residential || false,
        federal_tax_id: addressData.federal_tax_id || "",
        state_tax_id: addressData.state_tax_id || "",
      });
    } else {
      // Just person_name change from typing
      if (addressData.person_name !== undefined) {
        form.setValue("person_name", addressData.person_name || "");
      }
    }
  };

  // Expose submit method via ref for external triggering
  React.useImperativeHandle(ref, () => ({
    submit: async () => {
      const isValid = await form.trigger();
      if (isValid) {
        const data = form.getValues();
        await handleSubmit(data);
      }
    },
  }));

  // Check for form validity and changes
  const formValues = form.watch();
  const hasChanges = !isEqual(value, formValues);
  const missingRequired = !formValues.person_name || !formValues.country_code ||
    !formValues.address_line1 || !formValues.city ||
    (isPostalRequired && !formValues.postal_code) ||
    (isStateRequired && !formValues.state_code);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className={`space-y-3 ${className}`}>
        {/* Contact Person - full width with template autocomplete */}
        <div className="space-y-1">
          <AddressCombobox
            name="person_name"
            label="Contact Person"
            value={formValues.person_name || ""}
            onValueChange={handleTemplateSelection}
            placeholder="Full name"
            required
            disabled={disabled}
            className="h-8"
            wrapperClass="p-0"
          />
        </div>

        {/* Company - full width */}
        <FormField
          control={form.control}
          name="company_name"
          render={({ field }) => (
            <FormItem className="space-y-1">
              <FormLabel className="text-xs">Company</FormLabel>
              <FormControl>
                <Input
                  {...field}
                  placeholder="Company name"
                  disabled={disabled}
                  className="h-8"
                />
              </FormControl>
              <FormMessage className="text-xs" />
            </FormItem>
          )}
        />

        {/* Country - full width */}
        <div className="space-y-1">
          <Label htmlFor="country_code" className="text-xs">
            Country <span className="text-red-500">*</span>
          </Label>
          <CountrySelect
            value={formValues.country_code || ""}
            onValueChange={(val) => form.setValue("country_code", val, { shouldValidate: true })}
            disabled={disabled}
            noWrapper={true}
          />
          {form.formState.errors.country_code && (
            <p className="text-xs text-red-500">{form.formState.errors.country_code.message}</p>
          )}
        </div>

        {/* Street Address - full width */}
        <FormField
          control={form.control}
          name="address_line1"
          render={({ field }) => (
            <FormItem className="space-y-1">
              <FormLabel className="text-xs">
                Street Address <span className="text-red-500">*</span>
              </FormLabel>
              <FormControl>
                <Input
                  {...field}
                  placeholder="Street address"
                  disabled={disabled}
                  className="h-8"
                />
              </FormControl>
              <FormMessage className="text-xs" />
            </FormItem>
          )}
        />

        {/* Address Line 2 + City - 2 columns */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <FormField
            control={form.control}
            name="address_line2"
            render={({ field }) => (
              <FormItem className="space-y-1">
                <FormLabel className="text-xs">Address Line 2</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    placeholder="Apt, suite, etc. (optional)"
                    disabled={disabled}
                    className="h-8"
                  />
                </FormControl>
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="city"
            render={({ field }) => (
              <FormItem className="space-y-1">
                <FormLabel className="text-xs">
                  City <span className="text-red-500">*</span>
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    placeholder="City"
                    disabled={disabled}
                    className="h-8"
                  />
                </FormControl>
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
        </div>

        {/* State/Province + Postal Code - 2 columns */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {countryCode && references.states?.[countryCode] ? (
            <EnhancedSelect
              name="state_code"
              label="State/Province"
              value={formValues.state_code || ""}
              onValueChange={(val) => form.setValue("state_code", val, { shouldValidate: true })}
              placeholder="Select state"
              required={isStateRequired}
              disabled={disabled}
              className="h-8"
              labelClassName="text-xs"
              options={Object.entries(references.states[countryCode] || {}).map(([code, name]) => ({
                value: code,
                label: String(name)
              }))}
            />
          ) : (
            <FormField
              control={form.control}
              name="state_code"
              render={({ field }) => (
                <FormItem className="space-y-1">
                  <FormLabel className="text-xs">
                    State/Province {isStateRequired && <span className="text-red-500">*</span>}
                  </FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder="State/Province"
                      disabled={disabled}
                      className="h-8"
                    />
                  </FormControl>
                  <FormMessage className="text-xs" />
                </FormItem>
              )}
            />
          )}
          <FormField
            control={form.control}
            name="postal_code"
            render={({ field }) => (
              <FormItem className="space-y-1">
                <FormLabel className="text-xs">
                  Postal Code {isPostalRequired && <span className="text-red-500">*</span>}
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    placeholder="Postal code"
                    disabled={disabled}
                    className={`h-8 ${
                      postalCode && !validatePostalCode(postalCode, countryCode || "", isPostalRequired)
                        ? "border-red-500 focus:border-red-500"
                        : ""
                    }`}
                  />
                </FormControl>
                {postalCode && !validatePostalCode(postalCode, countryCode || "", isPostalRequired) && (
                  <p className="text-xs text-red-500 mt-1">Invalid postal code format</p>
                )}
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
        </div>

        {/* Email + Phone - 2 columns */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem className="space-y-1">
                <FormLabel className="text-xs">Email</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="email"
                    placeholder="contact@company.com"
                    disabled={disabled}
                    className="h-8"
                  />
                </FormControl>
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="phone_number"
            render={({ field }) => (
              <FormItem className="space-y-1">
                <FormLabel className="text-xs">Phone</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    placeholder="+1 (555) 123-4567"
                    disabled={disabled}
                    className="h-8"
                    onChange={(e) => {
                      const formatted = formatPhoneNumber(e.target.value, countryCode || "");
                      field.onChange(formatted);
                    }}
                  />
                </FormControl>
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
        </div>

        {/* Residential Checkbox */}
        <FormField
          control={form.control}
          name="residential"
          render={({ field }) => (
            <FormItem className="flex items-center space-x-2 pt-2">
              <FormControl>
                <Checkbox
                  id="residential"
                  checked={field.value}
                  onCheckedChange={field.onChange}
                  disabled={disabled}
                />
              </FormControl>
              <Label htmlFor="residential" className="text-xs">Residential address</Label>
            </FormItem>
          )}
        />

        {/* Advanced Fields */}
        <Collapsible open={advancedExpanded} onOpenChange={setAdvancedExpanded}>
          <CollapsibleTrigger asChild>
            <Button
              type="button"
              variant="ghost"
              className="flex items-center gap-2 text-xs font-medium text-blue-600 hover:text-blue-700 p-0 h-auto"
            >
              Advanced Options
              {advancedExpanded ? (
                <ChevronUp className="h-3 w-3" />
              ) : (
                <ChevronDown className="h-3 w-3" />
              )}
            </Button>
          </CollapsibleTrigger>
          <CollapsibleContent className="space-y-3 mt-2 pl-3 border-l-2 border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <FormField
                control={form.control}
                name="federal_tax_id"
                render={({ field }) => (
                  <FormItem className="space-y-1">
                    <FormLabel className="text-xs">Federal Tax ID</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        placeholder="Federal tax ID"
                        maxLength={20}
                        disabled={disabled}
                        className="h-8"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="state_tax_id"
                render={({ field }) => (
                  <FormItem className="space-y-1">
                    <FormLabel className="text-xs">State Tax ID</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        placeholder="State tax ID"
                        maxLength={20}
                        disabled={disabled}
                        className="h-8"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />
            </div>
          </CollapsibleContent>
        </Collapsible>
      </form>
    </Form>
  );
});

AddressForm.displayName = "AddressForm";
