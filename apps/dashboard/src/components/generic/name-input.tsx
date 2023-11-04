import InputField, { InputFieldComponent } from '@/components/generic/input-field';
import { useAddressTemplates } from '@/context/address';
import { formatAddress, isNone } from '@/lib/helper';
import { Address } from 'karrio/rest/index';
import React, { ChangeEvent } from 'react';

interface NameInputComponent extends InputFieldComponent {
  onValueChange: (value: Partial<Address>, refresh?: boolean) => void;
  defaultValue?: string;
  disableSuggestion?: boolean;
}

const NameInput: React.FC<NameInputComponent> = ({ disableSuggestion, onValueChange, ...props }) => {
  const { query } = useAddressTemplates();

  const onInput = (e: ChangeEvent<any>) => {
    e.preventDefault();
    const template = (query.data?.address_templates?.edges || [])
      .find(t => t.node.address?.person_name === e.target.value)
      ?.node;
    let value = template?.address || { person_name: e.target.value };
    onValueChange(value as Partial<Address>, !isNone(template));
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

export default NameInput;
