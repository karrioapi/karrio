import {
  AddressType,
  DEFAULT_ADDRESS_CONTENT,
  NotificationType,
  ShipmentType,
} from "@karrio/types";
import React, {
  FormEvent,
  useContext,
  useEffect,
  useReducer,
  useRef,
  useState,
} from "react";
import { COUNTRY_WITH_POSTAL_CODE, isEqual, isNone } from "@karrio/lib";
import { AddressAutocompleteInput } from "./address-autocomplete-input";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Label } from "@karrio/ui/components/ui/label";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { ButtonField } from "@karrio/ui/components/button-field";
// import { PostalInput } from "../components/postal-input";
import { InputField } from "@karrio/ui/components/input-field";
// import { PhoneInput } from "../components/phone-input";
import parsePhoneNumber, { AsYouType, PhoneNumber } from 'libphonenumber-js';
import { NameInput } from "../components/name-input";
import { Notify } from "../components/notifier";
// import { CountryInput } from "./country-input";
import { Loading } from "../components/loader";
import { SelectField } from "@karrio/ui/components/select-field";
import { CountrySelect } from "@karrio/ui/components/country-select";

interface AddressFormComponent {
  value?: AddressType;
  default_value?: AddressType | null;
  shipment?: ShipmentType;
  name?: "shipper" | "recipient" | "template";
  onSubmit: (address: AddressType) => Promise<any>;
  onTemplateChange?: (isUnchanged: boolean) => boolean;
  children?: React.ReactNode;
}

function reducer(
  state: any,
  { name, value }: { name: string; value: string | boolean | object },
) {
  switch (name) {
    case "full":
      return { ...(value as object) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}

// Postal code formatting functions
function formatPostalCode(postal_code: string, country_code?: string): [string, boolean] {
  if (country_code === 'CA') return [
    postal_code.toLocaleUpperCase(),
    (/^([A-Za-z]\d[A-Za-z][-\s]?\d[A-Za-z]\d)/).test(postal_code)
  ];
  if (country_code === 'US') return [
    postal_code.trim(),
    (/^[0-9]{5}(?:-[0-9]{4})?$/).test(postal_code)
  ];
  return [postal_code, true];
}

// Phone number formatting functions
function formatPhoneNumber(phoneNumber: string): [string, boolean] {
  const phone = parsePhoneNumber(phoneNumber) as PhoneNumber;
  return [new AsYouType().input(phoneNumber), phone?.isValid() || true];
}

export const AddressForm = ({
  value,
  default_value,
  shipment,
  name,
  onSubmit,
  onTemplateChange,
  children,
}: AddressFormComponent): JSX.Element => {
  const { references } = useAPIMetadata();
  const { notify } = useContext(Notify);
  const form = useRef<HTMLFormElement>(null);
  const { loading, setLoading } = useContext(Loading);
  const [key, setKey] = useState<string>(`address-${Date.now()}`);
  const [address, dispatch] = useReducer(
    reducer,
    value || DEFAULT_ADDRESS_CONTENT,
  );
  const [advancedExpanded, setAdvancedExpanded] = useState<boolean>(false);

  const computeDisableState = (state: AddressType): boolean => {
    const isUnchanged = isEqual(value || DEFAULT_ADDRESS_CONTENT, state);

    return onTemplateChange ? onTemplateChange(isUnchanged) : isUnchanged;
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name: string = target.name;

    dispatch({ name, value });
  };
  
  const handlePostalChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target;
    const [formatted, isValid] = formatPostalCode(target.value, address.country_code);
    if (formatted !== target.value) target.value = formatted;
    dispatch({ name: "postal_code", value: formatted });
  };
  
  const handlePhoneChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target;
    const [formatted, isValid] = formatPhoneNumber(target.value);
    if (formatted !== target.value) target.value = formatted;
    dispatch({ name: "phone_number", value: formatted });
  };
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      address.id && setLoading(true);
      await onSubmit(address);
      address.id &&
        notify({
          type: NotificationType.success,
          message: "Address successfully updated!",
        });
    } catch (err: any) {
      notify({ type: NotificationType.error, message: err });
    }
    setLoading(false);
  };

  useEffect(() => {
    if (
      value &&
      isNone(value.id) &&
      isNone(shipment?.id) &&
      !isNone(default_value)
    ) {
      dispatch({ name: "full", value: default_value as object });
      setKey(`address-${Date.now()}`);
    }
  }, [default_value, value]);
  useEffect(() => {
    if (
      shipment &&
      ["shipper", "recipient"].includes(name || "") &&
      !isEqual(shipment[name as "shipper" | "recipient"], address)
    ) {
      dispatch({
        name: "full",
        value: shipment[name as "shipper" | "recipient"],
      });
    }
  }, [shipment]);

  return (
    <form className="px-1 py-2" onSubmit={handleSubmit} key={key} ref={form}>
      {children}

      <div className="w-full mb-0">
        <NameInput
          label="name"
          className="h-9"
          value={address.person_name}
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
          disableSuggestion={isNone(shipment)}
          onValueChange={(value, refresh) => {
            dispatch({ name: "partial", value });
            refresh && setKey(`address-${Date.now()}`);
          }}
          required
        />
      </div>

      <div className="w-full mb-0">
        <InputField
          label="company"
          name="company_name"
          onChange={handleChange}
          value={address.company_name}
          className="h-9"
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
          max={30}
        />
      </div>

      <div className="w-full mb-0">
        <CountrySelect
          label="country"
          onValueChange={(value) =>
            dispatch({ name: "country_code", value: value as string })
          }
          value={address.country_code}
          className="h-9"
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
          align="end"
          required
        />
      </div>

      <div className="w-full mb-0">
        <AddressAutocompleteInput
          label="Street (Line 1)"
          name="address_line1"
          onValueChange={(value) => dispatch({ name: "partial", value })}
          value={address.address_line1}
          country_code={address.country_code}
          className="h-9"
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
          required
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-0 mb-0">
        <InputField
          label="Unit (Line 2)"
          name="address_line2"
          onChange={handleChange}
          value={address.address_line2}
          className="h-9"
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
          max={50}
        />

        <InputField
          label="city"
          name="city"
          onChange={handleChange}
          value={address.city}
          className="h-9"
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
          required
        />

        <SelectField
          label="province or state"
          onValueChange={(value) =>
            dispatch({ name: "state_code", value: value as string })
          }
          value={address.state_code}
          className="h-9"
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
          options={Object.entries(references.states?.[address.country_code] || {}).map(([code, name]) => ({
            value: code,
            label: name
          }))}
          placeholder="Select state/province"
          required={Object.keys(references.states || {}).includes(
            address.country_code,
          )}
        />

        <InputField
          label="postal code"
          name="postal_code"
          onChange={handlePostalChange}
          value={address.postal_code}
          className="h-9"
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
          required={COUNTRY_WITH_POSTAL_CODE.includes(address.country_code)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-0 mb-0">
        <InputField
          label="email"
          name="email"
          onChange={handleChange}
          value={address.email}
          className="h-9"
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
          type="email"
        />

        <InputField
          label="phone"
          name="phone_number"
          onChange={handlePhoneChange}
          onClick={(e: React.MouseEvent<HTMLInputElement>) => e.currentTarget.select()}
          value={address.phone_number}
          type="tel"
          className="h-9"
          wrapperClass="w-full px-1 py-3"
          fieldClass="mb-0 p-0"
        />
      </div>

      <div className="flex items-center space-x-2 mb-0 py-2 px-2">
        <Checkbox
          id="residential"
          name="residential"
          onCheckedChange={(checked) => handleChange({ target: { name: 'residential', type: 'checkbox', checked } } as any)}
          defaultChecked={address.residential}
        />
        <Label htmlFor="residential" className="text-sm font-normal capitalize" style={{ fontSize: ".8em" }}>
          Residential address
        </Label>
      </div>

      {/* Advanced */}
      <div className="w-full mb-0 pt-4 ml-0">
        <div
          className="w-full text-xs font-bold text-blue-600 px-0 my-1 cursor-pointer flex items-center"
          onClick={() => setAdvancedExpanded(!advancedExpanded)}
        >
          Advanced
          <span className="ml-2 text-sm">
            {advancedExpanded ? (
              <i className="fas fa-chevron-down"></i>
            ) : (
              <i className="fas fa-chevron-up"></i>
            )}
          </span>
        </div>

        <div
          className="ml-2 my-1 px-2 py-0 border-l-2 border-gray-300"
          style={{
            display: `${advancedExpanded ? "block" : "none"}`,
          }}
        >
          <div className="mb-0 pl-2">
            <InputField
              label="federal tax id"
              name="federal_tax_id"
              onChange={handleChange}
              value={address.federal_tax_id}
              className="h-9"
              wrapperClass="px-1 py-3"
              fieldClass="mb-0 p-0"
              max={20}
            />
          </div>

          <div className="mb-0 pl-2">
            <InputField
              label="state tax id"
              name="state_tax_id"
              onChange={handleChange}
              value={address.state_tax_id}
              className="h-9"
              wrapperClass="px-1 py-3"
              fieldClass="mb-0 p-0"
              max={20}
            />
          </div>
        </div>
      </div>

      <div className="p-3 my-5"></div>
      <ButtonField
        type="submit"
        className={`bg-blue-600 text-white hover:bg-blue-700 ${loading ? "opacity-50 cursor-not-allowed" : ""} m-0`}
        fieldClass="p-3"
        controlClass="has-text-centered"
        disabled={computeDisableState(address)}
      >
        <span>
          {isNone(shipment?.id) && name !== "template" ? "Next" : "Save"}
        </span>
      </ButtonField>
    </form>
  );
};
