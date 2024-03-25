import { useAddressTemplates } from '@karrio/hooks/address';
import React, { ChangeEvent, RefObject } from 'react';
import { formatAddress, isNone } from '@karrio/lib';
import { InputFieldComponent } from './input-field';
import { Combobox } from '@headlessui/react';
import { AddressType } from '@karrio/types';

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

export const NameInput: React.FC<NameInputComponent> = ({ disableSuggestion, value, onValueChange, label, required, className, fieldClass, controlClass, wrapperClass, children, ref, addonLeft, addonRight, ...props }) => {
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
      <div className={wrapperClass || ""}>
        {label !== undefined && <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
          {label}
          {required && <span className="icon is-small has-text-danger small-icon">
            <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
          </span>}
        </label>}

        <div className={`field ${fieldClass}`}>
          {addonLeft && addonLeft}

          <div className={`control ${controlClass}`}>
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
                    <div className="dropdown-menu" id="dropdown-menu" role="menu" style={{ width: "calc(100%)", maxHeight: '40vh' }}>
                      <Combobox.Options className={'dropdown-content'}>
                        {(address_templates?.edges || []).map(({ node: template }) => (
                          <Combobox.Option
                            as='a'
                            href='#'
                            key={template.id}
                            className={'dropdown-item is-clickable'}
                            value={template.address}
                          >
                            <span className="is-size-7 has-text-dark-grey has-text-weight-bold">
                              {template.label} - {formatAddress(template?.address as any)}
                            </span>
                          </Combobox.Option>
                        ))}
                      </Combobox.Options>
                    </div>
                  </>}

                </div>
              )}
            </Combobox>

          </div>

          {addonRight ? addonRight : <></>}
        </div>

        {children}
      </div>

    </>

  )
};
