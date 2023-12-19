import { InputField, InputFieldComponent } from './input-field';
import { useAddressTemplates } from '@karrio/hooks/address';
import { formatAddress, isNone } from '@karrio/lib';
import { AddressType } from '@karrio/types';
import React, { ChangeEvent, RefObject } from 'react';
import { Combobox } from '@headlessui/react';

interface NameInputComponent extends InputFieldComponent {
  onValueChange: (value: Partial<AddressType>, refresh?: boolean) => void;
  defaultValue?: string;
  disableSuggestion?: boolean;
  label?: string;
  fieldClass?: string;
  controlClass?: string;
  addonRight?: JSX.Element;
  addonLeft?: JSX.Element;
  ref?: RefObject<HTMLInputElement>;
}

export const NameInput: React.FC<NameInputComponent> = ({ disableSuggestion, value, onValueChange, label, required, className, fieldClass, controlClass, children, ref, addonLeft, addonRight, ...props }) => {
  const { query: { data: { address_templates } = {} }, filter, setFilter } = useAddressTemplates();
  const [query, setQuery] = React.useState<string>(value as string || "");

  const setSeltected = (e: AddressType | ChangeEvent<any>) => {
    if (e.hasOwnProperty('address_line1')) {
      setQuery((e as any).address_line1)
      onValueChange(e as AddressType, true);
    } else {
      (e as any).preventDefault();
      setQuery((e as any).target.value)
      setFilter({ ...filter, keyword: (e as any).target.value })
      onValueChange({ person_name: (e as any).target.value } as Partial<AddressType>, false);
    }
  }

  return (
    <>

      <div className={`field ${fieldClass}`}>
        {label !== undefined && <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
          {label}
          {required && <span className="icon is-small has-text-danger small-icon">
            <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
          </span>}
        </label>}
        <div className={`control ${controlClass}`}>
          {addonLeft && addonLeft}

          <Combobox value={query} onChange={setSeltected as any}>
            {({ open }) => (
              <div className={`dropdown is-flex ${(open && (address_templates?.edges || []).length > 0) ? "is-active" : ""}`}>
                <Combobox.Input
                  onChange={setSeltected}
                  className={`dropdown-trigger input ${className || ''}`}
                  {...(isNone(ref) ? { ref } : {})}
                  {...props}
                  autoComplete="off"
                  data-lpignore="true"
                  type="search"
                  displayValue={_ => (_ as any).person_name || query}
                />

                {!disableSuggestion && <>
                  <div className="dropdown-menu" id="dropdown-menu" role="menu" style={{ width: "calc(100%)" }}>
                    <Combobox.Options className={'dropdown-content'}>
                      {(address_templates?.edges || []).map(({ node: template }) => (
                        <Combobox.Option
                          as='a'
                          href='#'
                          key={template.id}
                          className={'dropdown-item is-clickable'}
                          value={template.address}
                        >
                          {template.label} - {formatAddress(template?.address as any)}
                        </Combobox.Option>
                      ))}
                    </Combobox.Options>
                  </div>
                </>}

              </div>
            )}
          </Combobox>

          {addonRight ? addonRight : <></>}
        </div>
        {children}
      </div>

    </>

  )
};
