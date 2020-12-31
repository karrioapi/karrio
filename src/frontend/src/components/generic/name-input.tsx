import { AddressTemplates } from '@/library/context';
import React, { ChangeEvent, useContext, useEffect } from 'react';
import InputField, { InputFieldComponent } from '@/components/generic/input-field';
import { state } from '@/library/api';
import { formatAddress, isNone } from '@/library/helper';
import { Address } from '@purplship/purplship';

interface NameInputComponent extends InputFieldComponent {
    onValueChange: (value: Partial<Address>, refresh?: boolean) => void;
    defaultValue?: string;
    disableSuggestion?: boolean;
}

const NameInput: React.FC<NameInputComponent> = ({ defaultValue, disableSuggestion, onValueChange, ...props }) => {
    const onClick = (e: React.MouseEvent<HTMLInputElement>) => e.currentTarget.select();
    const addressTemplates = useContext(AddressTemplates);
    const onInput = (e: ChangeEvent<any>) => {
        e.preventDefault();
        const template = addressTemplates.results.find(t => t.address?.person_name === e.target.value);
        let value = template?.address || { person_name: e.target.value };
        onValueChange(value as Partial<Address>, !isNone(template));
    };

    useEffect(() => {
        if (!disableSuggestion && addressTemplates.fetched === false) state.fetchAddresses();
    });

    return (
        <InputField onInput={onInput} onClick={onClick} defaultValue={defaultValue} list="address_templates" {...props}>
            {!disableSuggestion && <datalist id="address_templates">
                {addressTemplates
                    .results
                    .map(template => (
                        <option key={template.id} value={template.address?.person_name}>{template.label} - {formatAddress(template?.address as Address)}</option>
                    ))
                }
            </datalist>}
        </InputField>
    )
};

export default NameInput;