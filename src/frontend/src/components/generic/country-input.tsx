import { Reference } from '@/library/context';
import { Collection } from '@/library/types';
import React, { ChangeEvent, useContext } from 'react';
import InputField, { InputFieldComponent } from '@/components/generic/input-field';

interface CountryInputComponent extends InputFieldComponent {
    onValueChange: (value: string | null) => void;
}

const CountryInput: React.FC<CountryInputComponent> = ({ defaultValue, onValueChange, ...props }) => {
    const Ref = useContext(Reference);
    const onChange = (e: ChangeEvent<any>) => {
        e.preventDefault();
        if (Ref?.countries !== undefined) {
            let value = Object
                .keys(Ref?.countries)
                .find(key => Ref.countries[key] === e.target.value);

            onValueChange(value || null);
        }
    };

    return (
        <InputField onChange={onChange} defaultValue={Ref?.countries[defaultValue as string]} list="countries" {...props}>
            <datalist id="countries">
                {Object
                    .entries((Ref?.countries || {}) as Collection)
                    .map(([code, name]) => (
                        <option key={code} value={name} />
                    ))
                }
            </datalist>
        </InputField>
    )
};

export default CountryInput;