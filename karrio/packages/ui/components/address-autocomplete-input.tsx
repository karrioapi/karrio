import {
  useAddressAutocomplete,
  useAddressPredictionFormat,
  QueryAutocompletePrediction,
  AutocompleteConfig,
} from "@karrio/hooks/address-autocomplete";
import React, {
  ChangeEvent,
  useCallback,
  useEffect,
  useState,
} from "react";
import { ADDRESS_AUTO_COMPLETE_SERVICE, ADDRESS_AUTO_COMPLETE_SERVICE_KEY } from "@karrio/lib";
import { Address } from "@karrio/types/rest/api";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { cn } from "@karrio/ui/lib/utils";

interface AddressAutocompleteInputProps {
  name?: string;
  value?: string;
  onValueChange: (value: Partial<Address>) => void;
  defaultValue?: string;
  disableSuggestion?: boolean;
  country_code?: string;
  dropdownClass?: string;
  wrapperClass?: string;
  className?: string;
  fieldClass?: string;
  controlClass?: string;
  label?: string;
  required?: boolean;
  placeholder?: string;
  disabled?: boolean;
  [key: string]: any;
}

export const AddressAutocompleteInput = ({
  onValueChange,
  country_code,
  label,
  required,
  dropdownClass,
  className,
  fieldClass,
  controlClass,
  wrapperClass,
  name,
  children,
  ...props
}: AddressAutocompleteInputProps): JSX.Element => {
  const Props = {
    required,
    ...props,
    ...(Object.keys(props).includes("value")
      ? { value: props.value || "" }
      : {}),
  };

  const [inputValue, setInputValue] = useState<string>(String(props.value || ""));
  const datalistId = `address-predictions-${React.useId()}`;

  // Autocomplete configuration
  const config: AutocompleteConfig = {
    is_enabled: Boolean(ADDRESS_AUTO_COMPLETE_SERVICE),
    provider: ADDRESS_AUTO_COMPLETE_SERVICE,
    key: ADDRESS_AUTO_COMPLETE_SERVICE_KEY,
  };

  // Use the new autocomplete hooks
  const { data: predictions = [], isLoading } = useAddressAutocomplete(
    inputValue,
    country_code,
    config
  );

  const { formatPrediction } = useAddressPredictionFormat(config);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const newValue: string = e.target.value || "";
    setInputValue(newValue);
    // Immediately update the address with the typed value
    onValueChange({ address_line1: newValue });
  };

  const handleInputSelect = async (e: React.FormEvent<HTMLInputElement>) => {
    const selectedValue = (e.target as HTMLInputElement).value;

    // Check if the selected value matches a prediction
    const selectedPrediction = predictions.find(prediction =>
      prediction.description === selectedValue
    );

    if (selectedPrediction) {
      try {
        const address = await formatPrediction(selectedPrediction);
        onValueChange(address);
        setInputValue(address.address_line1 || selectedValue);
      } catch (error) {
        console.error('Error formatting prediction:', error);
        onValueChange({ address_line1: selectedValue });
        setInputValue(selectedValue);
      }
    }
  };

  // Update input value when prop changes
  useEffect(() => {
    if (props.value !== undefined && props.value !== inputValue) {
      setInputValue(String(props.value));
    }
  }, [props.value]);

  return (
    <div className={cn("px-1 py-2", wrapperClass)}>
      {label !== undefined && (
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
          name={name}
          value={inputValue}
          onChange={handleInputChange}
          onInput={handleInputSelect}
          className={cn("w-full", className)}
          list={config.is_enabled && predictions.length > 0 ? datalistId : undefined}
          autoComplete="street-address"
          {...Props}
        />
        {config.is_enabled && predictions.length > 0 && (
          <datalist id={datalistId}>
            {predictions.map((prediction) => (
              <option
                key={prediction.id}
                value={prediction.description}
              >
                {prediction.description}
              </option>
            ))}
          </datalist>
        )}
      </div>
    </div>
  );
};