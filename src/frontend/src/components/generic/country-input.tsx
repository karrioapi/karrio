import { Reference } from '@/library/context';
import { Collection } from '@/library/types';
import React, { ChangeEvent, useState } from 'react';
import InputField, { InputFieldComponent } from './input-field';

interface CountryInputComponent extends InputFieldComponent {}

const CountryInput: React.FC<CountryInputComponent> = ({ defaultValue, onChange, ...props }) => {
    const [countries, setCountries] = useState<Collection>({});
    const onValueChange = (e: ChangeEvent<any>) => {
        e.preventDefault();
        let value = Object.keys(countries).find(key => countries[key] === e.target.value);
        onChange && onChange({ target: { value } } as any);
    };

    return (
        <>

            <InputField onChange={onValueChange} defaultValue={countries[defaultValue as string]} list="countries" {...props}>
                <datalist id="countries">
                    {Object
                        .entries(countries as Collection)
                        .map(([code, name]) => (
                            <option key={code} value={name} />
                        ))
                    }
                </datalist>
            </InputField>

            <Reference.Consumer>
                {(ref) => {
                    if ((Object.values(ref || {}).length > 0)) setCountries(ref.countries);
                    return <></>;
                }}
            </Reference.Consumer>

        </>
    )
};

export default CountryInput;