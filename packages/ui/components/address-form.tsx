import React from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Checkbox } from "./ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "./ui/collapsible";
import { ChevronDown, ChevronUp, MapPin } from "lucide-react";
import { AddressType, DEFAULT_ADDRESS_CONTENT } from "@karrio/types";
import { COUNTRY_WITH_POSTAL_CODE, isEqual } from "@karrio/lib";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

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
    const [address, setAddress] = React.useState<Partial<AddressType>>(value || DEFAULT_ADDRESS_CONTENT);
    const [advancedExpanded, setAdvancedExpanded] = React.useState(false);
    const [isSubmitting, setIsSubmitting] = React.useState(false);

    React.useEffect(() => {
        setAddress(value || DEFAULT_ADDRESS_CONTENT);
    }, [value]);

    const handleChange = (field: string, fieldValue: string | boolean) => {
        const updatedAddress = { ...address, [field]: fieldValue };
        setAddress(updatedAddress);
        onChange?.(updatedAddress);
    };

    const handleSubmit = async (e?: React.FormEvent) => {
        e?.preventDefault();
        if (!onSubmit) return;

        setIsSubmitting(true);
        try {
            await onSubmit(address);
        } finally {
            setIsSubmitting(false);
        }
    };

    React.useImperativeHandle(ref, () => ({
        submit: () => handleSubmit(),
    }));

    const isPostalRequired = COUNTRY_WITH_POSTAL_CODE.includes(address.country_code || "");
    const isStateRequired = Object.keys(references.states || {}).includes(address.country_code || "");
    const hasChanges = !isEqual(value, address);

    // Enhanced postal code validation
    const validatePostalCode = (postal: string, country: string) => {
        if (!postal || !isPostalRequired) return true;

        const patterns: Record<string, RegExp> = {
            US: /^\d{5}(-\d{4})?$/,
            CA: /^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$/,
            GB: /^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$/i,
            DE: /^\d{5}$/,
            FR: /^\d{5}$/,
            AU: /^\d{4}$/,
            JP: /^\d{3}-\d{4}$/,
        };

        return patterns[country]?.test(postal) ?? true;
    };

    // Phone number formatting helper
    const formatPhoneNumber = (phone: string, country: string) => {
        if (!phone) return phone;

        // Remove all non-digits
        const digits = phone.replace(/\D/g, '');

        // Format based on country
        if (country === 'US' || country === 'CA') {
            if (digits.length === 10) {
                return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
            } else if (digits.length === 11 && digits[0] === '1') {
                return `+1 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7)}`;
            }
        }

        return phone; // Return original if no formatting applied
    };

    return (
        <form onSubmit={handleSubmit} className={`space-y-3 ${className}`}>
            {/* Contact Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="space-y-1">
                    <Label htmlFor="person_name" className="text-xs text-slate-700">
                        Contact Person <span className="text-red-500">*</span>
                    </Label>
                    <Input
                        id="person_name"
                        value={address.person_name || ""}
                        onChange={(e) => handleChange("person_name", e.target.value)}
                        placeholder="Full name"
                        required
                        disabled={disabled}
                        className="h-8"
                    />
                </div>
                <div className="space-y-1">
                    <Label htmlFor="company_name" className="text-xs text-slate-700">Company</Label>
                    <Input
                        id="company_name"
                        value={address.company_name || ""}
                        onChange={(e) => handleChange("company_name", e.target.value)}
                        placeholder="Company name"
                        disabled={disabled}
                        className="h-8"
                    />
                </div>
            </div>

            {/* Country */}
            <div className="space-y-1">
                <Label htmlFor="country_code" className="text-xs text-slate-700">
                    Country <span className="text-red-500">*</span>
                </Label>
                <Select
                    value={address.country_code || ""}
                    onValueChange={(value) => handleChange("country_code", value)}
                    disabled={disabled}
                >
                    <SelectTrigger className="h-8">
                        <SelectValue placeholder="Select country" />
                    </SelectTrigger>
                    <SelectContent>
                        {Object.entries(references.countries || {}).map(([code, name]) => (
                            <SelectItem key={code} value={code}>
                                {name}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            {/* Address Lines */}
            <div className="space-y-3">
                <div className="space-y-1">
                    <Label htmlFor="address_line1" className="text-xs text-slate-700">
                        Street Address <span className="text-red-500">*</span>
                    </Label>
                    <div className="relative">
                        <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                        <Input
                            id="address_line1"
                            value={address.address_line1 || ""}
                            onChange={(e) => handleChange("address_line1", e.target.value)}
                            placeholder="Start typing your address..."
                            required
                            disabled={disabled}
                            className="pl-10 h-8"
                        />
                    </div>
                    <p className="text-xs text-muted-foreground">
                        💡 Tip: For best results, include street number and name
                    </p>
                </div>
                <div className="space-y-1">
                    <Label htmlFor="address_line2" className="text-xs text-slate-700">Address Line 2</Label>
                    <Input
                        id="address_line2"
                        value={address.address_line2 || ""}
                        onChange={(e) => handleChange("address_line2", e.target.value)}
                        placeholder="Apartment, suite, etc. (optional)"
                        disabled={disabled}
                        className="h-8"
                    />
                </div>
            </div>

            {/* City, State, Postal */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="space-y-1">
                    <Label htmlFor="city" className="text-xs text-slate-700">
                        City <span className="text-red-500">*</span>
                    </Label>
                    <Input
                        id="city"
                        value={address.city || ""}
                        onChange={(e) => handleChange("city", e.target.value)}
                        placeholder="City"
                        required
                        disabled={disabled}
                        className="h-8"
                    />
                </div>
                <div className="space-y-1">
                    <Label htmlFor="state_code" className="text-xs text-slate-700">
                        State/Province {isStateRequired && <span className="text-red-500">*</span>}
                    </Label>
                    {address.country_code && references.states?.[address.country_code] ? (
                        <Select
                            value={address.state_code || ""}
                            onValueChange={(value) => handleChange("state_code", value)}
                            disabled={disabled}
                        >
                            <SelectTrigger className="h-8">
                                <SelectValue placeholder="Select state" />
                            </SelectTrigger>
                            <SelectContent>
                                {Object.entries(references.states[address.country_code]).map(([code, name]) => (
                                    <SelectItem key={code} value={code}>
                                        {name}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    ) : (
                        <Input
                            id="state_code"
                            value={address.state_code || ""}
                            onChange={(e) => handleChange("state_code", e.target.value)}
                            placeholder="State/Province"
                            required={isStateRequired}
                            disabled={disabled}
                            className="h-8"
                        />
                    )}
                </div>
                <div className="space-y-1">
                    <Label htmlFor="postal_code" className="text-xs text-slate-700">
                        Postal Code {isPostalRequired && <span className="text-red-500">*</span>}
                    </Label>
                    <div className="relative">
                        <Input
                            id="postal_code"
                            value={address.postal_code || ""}
                            onChange={(e) => handleChange("postal_code", e.target.value)}
                            placeholder="Postal code"
                            required={isPostalRequired}
                            disabled={disabled}
                            className={`h-8 ${address.postal_code && !validatePostalCode(address.postal_code, address.country_code || "")
                                ? "border-red-500 focus:border-red-500"
                                : ""
                                }`}
                        />
                        {address.postal_code && !validatePostalCode(address.postal_code, address.country_code || "") && (
                            <p className="text-xs text-red-500 mt-1">
                                Please enter a valid postal code for {references.countries?.[address.country_code || ""] || "this country"}
                            </p>
                        )}
                    </div>
                </div>
            </div>

            {/* Contact Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                        id="email"
                        type="email"
                        value={address.email || ""}
                        onChange={(e) => handleChange("email", e.target.value)}
                        placeholder="contact@company.com"
                        disabled={disabled}
                    />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="phone_number">Phone</Label>
                    <Input
                        id="phone_number"
                        value={address.phone_number || ""}
                        onChange={(e) => {
                            const formatted = formatPhoneNumber(e.target.value, address.country_code || "");
                            handleChange("phone_number", formatted);
                        }}
                        placeholder="+1 (555) 123-4567"
                        disabled={disabled}
                    />
                </div>
            </div>

            {/* Residential Checkbox */}
            <div className="flex items-center space-x-2">
                <Checkbox
                    id="residential"
                    checked={address.residential || false}
                    onCheckedChange={(checked) => handleChange("residential", !!checked)}
                    disabled={disabled}
                />
                <Label htmlFor="residential">Residential address</Label>
            </div>

            {/* Advanced Fields */}
            <Collapsible open={advancedExpanded} onOpenChange={setAdvancedExpanded}>
                <CollapsibleTrigger asChild>
                    <Button
                        type="button"
                        variant="ghost"
                        className="flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-700 p-0 h-auto"
                    >
                        Advanced Options
                        {advancedExpanded ? (
                            <ChevronUp className="h-4 w-4" />
                        ) : (
                            <ChevronDown className="h-4 w-4" />
                        )}
                    </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="space-y-4 mt-4 pl-4 border-l-2 border-gray-200">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="federal_tax_id">Federal Tax ID</Label>
                            <Input
                                id="federal_tax_id"
                                value={address.federal_tax_id || ""}
                                onChange={(e) => handleChange("federal_tax_id", e.target.value)}
                                placeholder="Federal tax ID"
                                maxLength={20}
                                disabled={disabled}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="state_tax_id">State Tax ID</Label>
                            <Input
                                id="state_tax_id"
                                value={address.state_tax_id || ""}
                                onChange={(e) => handleChange("state_tax_id", e.target.value)}
                                placeholder="State tax ID"
                                maxLength={20}
                                disabled={disabled}
                            />
                        </div>
                    </div>
                </CollapsibleContent>
            </Collapsible>

            {/* Submit Button */}
            {showSubmitButton && (
                <div className="flex justify-end pt-4">
                    <Button
                        type="submit"
                        disabled={disabled || isSubmitting || !hasChanges}
                        className="min-w-[120px]"
                    >
                        {isSubmitting ? "Saving..." : submitButtonText}
                    </Button>
                </div>
            )}
        </form>
    );
});

AddressForm.displayName = "AddressForm";
