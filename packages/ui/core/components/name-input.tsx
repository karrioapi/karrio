import { useAddressTemplates } from "@karrio/hooks/address";
import React, { ChangeEvent, RefObject } from "react";
import { formatAddress, isNone } from "@karrio/lib";
import { InputFieldComponent } from "./input-field";
import {
  Combobox,
  ComboboxInput,
  ComboboxPopover,
  ComboboxList,
  ComboboxOption
} from "@karrio/ui/components/ui/combobox";
import { AddressType } from "@karrio/types";

interface NameInputComponent extends InputFieldComponent {
  onValueChange: (value: Partial<AddressType>, refresh?: boolean) => void;
  defaultValue?: string;
  disableSuggestion?: boolean;
  label?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  addonRight?: JSX.Element;
  addonLeft?: JSX.Element;
  ref?: RefObject<HTMLInputElement>;
}

export const NameInput = ({
  disableSuggestion,
  value,
  onValueChange,
  label,
  required,
  className,
  fieldClass,
  controlClass,
  wrapperClass,
  children,
  ref,
  addonLeft,
  addonRight,
  ...props
}: NameInputComponent): JSX.Element => {
  const {
    query: { data: { address_templates } = {} },
    filter,
    setFilter,
  } = useAddressTemplates();
  const [query, setQuery] = React.useState<string>((value as string) || "");
  const [open, setOpen] = React.useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    setQuery(e.target.value);
    setFilter({ ...filter, keyword: e.target.value });
    onValueChange(
      { person_name: e.target.value } as Partial<AddressType>,
      false,
    );
    setOpen(true);
  };

  const handleSelect = (address: AddressType) => {
    setQuery(address.address_line1 as string);
    onValueChange(address, true);
    setOpen(false);
  };

  return (
    <>
      <div className={wrapperClass || ""}>
        {label !== undefined && (
          <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
            {label}
            {required && (
              <span className="icon is-small has-text-danger small-icon">
                <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
              </span>
            )}
          </label>
        )}

        <div className={`field ${fieldClass}`}>
          {addonLeft && addonLeft}

          <div className={`control ${controlClass}`}>
            <Combobox open={open && !disableSuggestion && (address_templates?.edges || []).length > 0} onOpenChange={setOpen}>
              <div className={`dropdown is-flex ${open && !disableSuggestion && (address_templates?.edges || []).length > 0 ? "is-active" : ""}`}>
                <ComboboxInput
                  {...props}
                  value={query}
                  className={`dropdown-trigger input ${className || ""}`}
                  {...(isNone(ref) ? { ref } : {})}
                  autoComplete="off"
                  data-lpignore="true"
                  type="search"
                  onChange={handleChange}
                />

                {!disableSuggestion && (
                  <ComboboxPopover className="dropdown-menu">
                    <ComboboxList className="dropdown-content">
                      {(address_templates?.edges || []).map(
                        ({ node: template }) => (
                          <ComboboxOption
                            key={template.id}
                            value={template.id}
                            className="dropdown-item is-clickable"
                            onClick={() => handleSelect(template.address as AddressType)}
                          >
                            <span className="is-size-7 has-text-dark-grey has-text-weight-bold">
                              {template.label} -{" "}
                              {formatAddress(template?.address as any)}
                            </span>
                          </ComboboxOption>
                        ),
                      )}
                    </ComboboxList>
                  </ComboboxPopover>
                )}
              </div>
            </Combobox>
          </div>

          {addonRight ? addonRight : <></>}
        </div>

        {children}
      </div>
    </>
  );
};
