import { InputField, InputFieldComponent } from './input-field';
import { useAddressTemplates } from '@karrio/hooks/address';
import { formatAddress, isNone } from '@karrio/lib';
import { AddressType } from '@karrio/types';
import React, { ChangeEvent } from 'react';

interface NameInputComponent extends InputFieldComponent {
  onValueChange: (value: Partial<AddressType>, refresh?: boolean) => void;
  defaultValue?: string;
  disableSuggestion?: boolean;
}

export const NameInput: React.FC<NameInputComponent> = ({ disableSuggestion, onValueChange, ...props }) => {
  const { query } = useAddressTemplates();

  const onInput = (e: ChangeEvent<any>) => {
    e.preventDefault();
    const template = (query.data?.address_templates?.edges || [])
      .find(t => t.node.address?.person_name === e.target.value)
      ?.node;
    let value = template?.address || { person_name: e.target.value };
    onValueChange(value as Partial<AddressType>, !isNone(template));
  };

  return (
    <InputField onInput={onInput} list="address_templates" {...props}>
      {!disableSuggestion && <datalist id="address_templates">
        {(query.data?.address_templates?.edges || [])
          .map(({ node: template }) => (
            <option key={template.id} value={template.address?.person_name as string}>
              {template.label} - {formatAddress(template?.address as any)}
            </option>
          ))
        }
      </datalist>}
    </InputField>
  )
};
